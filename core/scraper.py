from bs4 import BeautifulSoup
import pandas as pd


class ManualScraper(object):
    """
    Given a path to the HTML page of eloratings.net/XXXX_result,
    parses and returns a Pandas DataFrame of match data. """
    FIELDS = [
        "home_team",
        "away_team",
        "date",
        "location",
        "match_type",
        "home_advantage",
        "home_team_score",
        "away_team_score",
        "home_team_rating_change",
        "away_team_rating_change",
        "home_team_resulting_rating",
        "away_team_resulting_rating",
        "home_team_rank_change",
        "away_team_rank_change",
        "home_team_resulting_rank",
        "away_team_resulting_rank"
    ]

    MONTH_NAME_TO_NUMBER = {
        'JANUARY': 1,
        'FEBRUARY': 2,
        'MARCH': 3,
        'APRIL': 4,
        'MAY': 5,
        'JUNE': 6,
        'JULY': 7,
        'AUGUST': 8,
        'SEPTEMBER': 9,
        'OCTOBER': 10,
        'NOVEMBER': 11,
        'DECEMBER': 12,

        'JAN': 1,
        'FEB': 2,
        'MAR': 3,
        'APR': 4,
        'JUN': 6,
        'JUL': 7,
        'AUG': 8,
        'SEP': 9,
        'OCT': 10,
        'NOV': 11,
        'DEC': 12
    }

    def __init__(self):
        self.num_fields = len(self.FIELDS)

    def get_raw_matches(self, file_path):
        """
        The function that provides the main service.
        :param file_path: the path to an eloratings.net results page.
        :return: a list of match data.
        """
        html_page = self.get_html_page(file_path)
        html_tree = self.get_html_tree(html_page)
        all_match_divs = self.get_all_match_divs(html_tree)
        matches = self.process_match_divs(all_match_divs)
        return pd.DataFrame(matches, columns=self.FIELDS)

    def get_html_page(self, file_path):
        """
        Reads in a file at the specified path
        and returns its string representation.
        """
        with open(file_path, 'r') as file:
            return file.read()

    def get_html_tree(self, page):
        """
        Given the string representation of an HTML file,
        returns its DOM tree representation using BeaultifulSoup.
        """
        return BeautifulSoup(page, "html.parser")

    def get_all_match_divs(self, html_tree):
        """
        Given an HTML DOM tree, extracts and returns all the div tags
        that correspond to individual match data.
        """
        even_indexed_matches = html_tree.findAll(
            "div", {"class": "ui-widget-content slick-row even"}
        )

        odd_indexed_matches = html_tree.findAll(
            "div", {"class": "ui-widget-content slick-row odd"}
        )

        return even_indexed_matches + odd_indexed_matches

    def process_match_divs(self, matches):
        """
        Processes each Match div and returns the list of
        processed results.
        """
        result = []
        for match in matches:
            try:
                result.append(
                    self.process_single_match_div(match)
                )
            except AttributeError:
                print("ParseError for {0}".format(match))

        return result

    def process_single_match_div(self, match):
        """
        Processes each Match div.
        """
        info_divs = match.findAll("div")

        def extract_info(index, extractor_function):
            """
            A higher-order function that processes each column div.
            (each row = individual match, each column = some data about the match)
            """
            tag_contents = info_divs[index].contents
            return extractor_function(tag_contents)

        # simple extractor functions.
        a_tag_extractor = lambda contents, index: contents[index].text
        a_tag_extractor_first = lambda contents: a_tag_extractor(contents, 0)
        a_tag_extractor_second = lambda contents: a_tag_extractor(contents, 2)
        string_tag_extractor = lambda contents, index: str(contents[index])
        string_tag_extractor_first = lambda contents: string_tag_extractor(contents, 0)
        string_tag_extractor_second = lambda contents: string_tag_extractor(contents, 2)

        def date_extractor(contents):
            """An extractor function for the date div."""
            # e.g. ['January 4', <br/>, '2017']
            month_day = contents[0].split(' ')
            month = str(self.MONTH_NAME_TO_NUMBER[month_day[0].upper()])
            day = month_day[1]
            year = contents[2]
            # e.g. '2017-01-04'
            return '-'.join([year, month, day])

        def match_type_extractor(contents):
            """A match type is sometimes an a tag and sometimes a string."""
            try_as_string = string_tag_extractor_first(contents)
            if len(try_as_string) > 30:
                return a_tag_extractor_first(contents)
            return try_as_string

        def custom_int(negative_integer):
            """A custom function that processes numerical data."""
            if len(negative_integer) == 1:
                return 0

            # 8722 = some weird negative character thta looks like '-'
            if ord(negative_integer[0]) == 8722:
                return -1 * int(negative_integer[1:])
            elif ord(negative_integer[0]) == 43:
                return int(negative_integer[1:])
            return int(negative_integer)

        # process non numerical data
        result = [
            extract_info(1, a_tag_extractor_first),
            extract_info(1, a_tag_extractor_second),
            extract_info(0, date_extractor),
            extract_info(3, a_tag_extractor_second),
            extract_info(3, match_type_extractor),
            False,
            extract_info(2, string_tag_extractor_first),
            extract_info(2, string_tag_extractor_second),
        ]

        # process numerical data
        for idx in range(4, 8):
            result.append(
                custom_int(
                    extract_info(idx, string_tag_extractor_first)
                )
            )

            # The input data uses some weird char for the minus sign.
            result.append(
                custom_int(
                    extract_info(idx, string_tag_extractor_second)
                )
            )

        home_team = result[0]
        location = result[3]

        # Sets the home team advantage field if necessary.
        if home_team in location:
            result[5] = True

        return result


class ManualScraperAdapter(object):
    """An adapter so that the model side does not have to know
    the particular scraper specific details. """
    FILE_PATH_SUFFIX = "./data/{0}_result.htm"

    def __init__(self, year):
        self.scraper = ManualScraper()
        self.year = year

    def get_match_data(self):

        file_path = self.FILE_PATH_SUFFIX.format(self.year)

        return self.scraper.get_raw_matches(file_path)

from bs4 import BeautifulSoup


class ManualScraper(object):

    FIELDS = [
        "HomeTeam",
        "AwayTeam",
        "Date",
        "Location",
        "MatchType",
        "HomeAdvantage",
        "HomeTeamScore",
        "AwayTeamScore",
        "HomeTeamResultingRating",
        "AwayTeamResultingRating",
        "HomeTeamRatingChange",
        "AwayTeamRatingChange",
        "HomeTeamRank",
        "AwayTeamRank",
        "HomeTeamRankChange",
        "AwayTeamRankChange"
    ]

    DIV_CLASS_NAMES = [
        {"class": "slick-cell l1 r1 match-cell "},
        {"class": "slick-cell l1 r1 match-cell "},
        {"class": "slick-cell l0 r0 match-cell "},
        {"class": "slick-cell l3 r3 match-cell "},
        {"class": "slick-cell l3 r3 match-cell "},
        None,
        {"class": "slick-cell l2 r2 score-cell "},
        {"class": "slick-cell l2 r2 score-cell "},
        {"class": "slick-cell l5 r5 score-cell "},
        {"class": "slick-cell l5 r5 score-cell "},
        {"class": "slick-cell l4 r4 change-cell "},
        {"class": "slick-cell l4 r4 change-cell "},
        {"class": "slick-cell l7 r7 score-cell "},
        {"class": "slick-cell l7 r7 score-cell "},
        {"class": "slick-cell l6 r6 change-cell "},
        {"class": "slick-cell l6 r6 change-cell "},
    ]

    def __init__(self):
        self.num_fields = len(self.FIELDS)

    def get_raw_matches(self, year_result_file_path):
        html_page = self.get_html_page(year_result_file_path)
        html_tree = self.get_html_tree(html_page)
        all_match_divs = self.get_all_match_divs(html_tree)
        matches = self.process_match_divs(all_match_divs)
        return matches

    def get_html_page(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def get_html_tree(self, page):
        return BeautifulSoup(page, "html.parser")

    def get_all_match_divs(self, html_tree):
        even_indexed_matches = html_tree.findAll(
            "div", {"class": "ui-widget-content slick-row even"}
        )

        odd_indexed_matches = html_tree.findAll(
            "div", {"class": "ui-widget-content slick-row odd"}
        )

        return even_indexed_matches + odd_indexed_matches

    def process_match_divs(self, matches):
        result = []
        for match in matches:
            result.append(
                self.process_single_match_div(match)
            )
        return result

    def process_single_match_div(self, match):

        def extract_info(class_name, extractor_function):
            info_div =  match.find("div", class_name)
            tag_contents = info_div.contents
            return extractor_function(tag_contents)

        a_tag_extractor = lambda contents, index: contents[index].text
        a_tag_extractor_first = lambda contents: a_tag_extractor(contents, 0)
        a_tag_extractor_second = lambda contents: a_tag_extractor(contents, 2)
        string_tag_extractor = lambda contents, index: contents[index]
        string_tag_extractor_first = lambda contents: string_tag_extractor(contents, 0)
        string_tag_extractor_second = lambda contents: string_tag_extractor(contents, 2)

        def date_extractor(contents):
            # e.g. ['January 4', <br/>, '2017']
            month_day = contents[0]
            year = contents[2]
            # e.g. '2017-01-04'
            return '-'.join([year] + month_day.split(' '))

        def custom_int(negative_integer):
            print(negative_integer, )
            if len(negative_integer) == 0:
                return 0

            # 8722 = some weird negative character thta looks like '-'
            if ord(negative_integer[0]) == 8722:
                return -1 * int(negative_integer[1:])
            elif ord(negative_integer[0]) == 43:
                return int(negative_integer[1:])
            return int(negative_integer)

        # process non numerical data
        result = [
            extract_info(self.DIV_CLASS_NAMES[0], a_tag_extractor_first),
            extract_info(self.DIV_CLASS_NAMES[1], a_tag_extractor_second),
            extract_info(self.DIV_CLASS_NAMES[2], date_extractor),
            extract_info(self.DIV_CLASS_NAMES[3], a_tag_extractor_second),
            extract_info(self.DIV_CLASS_NAMES[4], string_tag_extractor_first),
            False
        ]

        # process numerical data
        for idx in range(6, 16, 2):
            result.append(
                custom_int(
                    extract_info(self.DIV_CLASS_NAMES[idx], string_tag_extractor_first)
                )
            )

            # The input data uses some weird char for the minus sign.
            result.append(
                custom_int(
                    extract_info(self.DIV_CLASS_NAMES[idx + 1], string_tag_extractor_second)
                )
            )

        home_team = result[0]
        location = result[3]

        # Sets the home team advantage field if necessary.
        if home_team in location:
            result[5] = True

        return result

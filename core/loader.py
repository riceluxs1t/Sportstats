from core.models import RawMatch


BATCH_SIZE = 1


def load_raw_match_data(raw_matches_df):
    """
    Given a Pandas data frame of raw match data,
    loads it into the Django RawMatch model (i.e. into the database). """

    # for efficient bulk inserting.
    batch = []

    for match in raw_matches_df.iterrows():

        match_part = match[1]

        batch.append(
            RawMatch(
                **match_part.to_dict()
            )
        )

        if len(batch) >= BATCH_SIZE:
            RawMatch.objects.bulk_create(batch)
            batch = []

    RawMatch.objects.bulk_create(batch)

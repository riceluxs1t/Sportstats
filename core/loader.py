from core.models import RawMatch


BATCH_SIZE = 1


def load_raw_match_data(raw_matches_df):

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

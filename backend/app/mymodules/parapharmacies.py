import pandas as pd

df = pd.read_csv('/app/app/parafarmacie.csv', delimiter=';')


def find_by_region(region: int):
    result = df[(df["CODICEREGIONE"] == int(region))]
    result.sort_values(
        by=["DESCRIZIONECOMUNE", "DENOMINAZIONESITO"],
        inplace=True,
        key=lambda col: col.str.lower()
    )
    return [
        {
            "name": row["DENOMINAZIONESITO"],
            "address": row["INDIRIZZO"],
            "cap": row["CAP"],
            "city": row["DESCRIZIONECOMUNE"],
        }
        for _, row in result.iterrows()
    ]


def is_valid_region(region: int):
    return region in [r["code"] for r in list_regions()]


def list_regions():
    regions = df[["CODICEREGIONE", "DESCRIZIONEREGIONE"]].drop_duplicates()
    regions.sort_values(by="DESCRIZIONEREGIONE", inplace=True)
    return [
        {
            "code": row["CODICEREGIONE"],
            "name": row["DESCRIZIONEREGIONE"],
        }
        for _, row in regions.iterrows()
    ]
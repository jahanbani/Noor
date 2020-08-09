"""
neq = 60
ca
x<10 ==> remove
10 =< x <= 0.9 * neq ==>  ca
0.9 * neq < x < neq - 1 ==> ca*3
x=neq ==> ca*5
"""
import os
import time

import ipdb
import pandas as pd


def highlight_max(df):
    """
    highlight the maximum in a Series yellow.
    """
    return ["background-color: black"] * len(df)


def clean_data(df):
    df = df.replace({"الف": "A", "ب": "B", "ج": "C", "د": "D"})
    phonecol = [col for col in df.columns if col.startswith("شماره تلفن همراه")]
    namecol = [col for col in df.columns if col.startswith("نام")]
    citycol = [col for col in df.columns if col.startswith("شهر")]
    councol = [col for col in df.columns if col.startswith("کشور")]
    df = df.rename(
        columns={
            phonecol[0]: "Phone",
            namecol[0]: "Name",
            citycol[0]: "City",
            councol[0]: "Country",
        }
    )
    anscols = pd.to_numeric(df.columns, errors="coerce")
    df = df[
        ["Timestamp", "Phone", "Name", "City", "Country"]
        + df.columns[anscols.notnull()].tolist()
    ]

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    # if not answered
    df.fillna(value="Z", inplace=True)
    return df


def fix_phone(df):
    df["Phone"] = df["Phone"].astype(str)
    # select the last 10 digits of the phone numbers
    df["Phone"] = df["Phone"].str[-10:]

    return df


def rem_dupl(df):
    df = df.sort_values(by="Timestamp")
    df = df.groupby(["Phone"]).first().reset_index()
    return df


def main():
    ans = pd.read_excel("answers.xlsx")
    resp = os.listdir("resp")

    dfu = {}
    for fn in resp:
        data = pd.read_excel(r"resp/" + fn)
        dfc = clean_data(data)
        dfp = fix_phone(dfc)
        dfu[fn[:-5]] = rem_dupl(dfp).set_index("Phone")

    anss = pd.concat(
        [dfu[k].drop(columns=["Timestamp"]) for k, v in dfu.items()],
        join="outer",
        axis=1,
    )
    anss.to_excel("alldatabeforegrading.xlsx")
    anss = anss.iloc[:, ~anss.columns.duplicated()]
    anssq = anss.drop(columns=["City", "Country", "Name"])
    neq = len(anssq.columns)
    print(f"The number of questions is {neq}")

    # grade them
    total = anssq.eq(ans["A"].to_list()).sum(axis=1)
    print(f"The number of participants are {len(total)}")
    total.name = "nc"
    total.index.name = "Phone"
    corans = total.to_frame().reset_index()
    corans = pd.merge(anss, corans, left_index=True, right_on="Phone", how="left")

    # give them points
    corans.loc[corans["nc"] < 10, "point"] = 0
    corans.loc[(corans["nc"] >= 10) & (corans["nc"] < 0.9 * neq), "point"] = corans[
        "nc"
    ]
    corans.loc[(corans["nc"] >= 0.90 * neq) & (corans["nc"] < neq), "point"] = (
        corans["nc"] * 3
    )
    corans.loc[corans["nc"] == neq, "point"] = corans["nc"] * 5

    # draw

    corans = corans[corans["point"] != 0]
    corans = corans.sort_values(by=["point"]).reset_index(drop=True)
    # -1 is necessary to make it compatible with index format
    # Also, in the draw we can have 0
    corans["cumsum"] = corans["point"].cumsum() - 1

    corans.to_excel("beforepool.xlsx")
    # creating an empty df to merge on
    empdf = pd.DataFrame(data={}, index=range(int(corans["cumsum"].max() + 1)))
    df = pd.merge(
        empdf, corans.set_index("cumsum"), right_index=True, left_index=True, how="left"
    ).fillna(method="bfill")
    df = df[
        ["Phone", "Name", "City", "Country", "nc", "point"]
        + [
            col
            for col in df.columns
            if col not in ["Phone", "Name", "City", "Country", "nc", "point"]
        ]
    ]

    df.to_excel("mainfile_doNOTchange.xlsx", index=False)
    # randomly shuffle them
    df = df.sample(frac=1).reset_index(drop=True)
    df["Phone"] = df["Phone"].astype(str)
    df["Phonest"] = df["Phone"].str[0:3]
    df["Phonemd"] = df["Phone"].str[3:6]
    df["Phoneed"] = df["Phone"].str[6:]
    df[
        [
            "Phonest",
            "Phoneed",
            "Name",
            "City",
            "Country",
            "nc",
            "point",
            "Phone",
            "Phonemd",
        ]
    ].style.apply(highlight_max).to_excel("mainfile.xlsx", index=True)

    print(df.shape)

    df[
        [
            "Phonest",
            "Phoneed",
            "Name",
            "City",
            "Country",
            "nc",
            "point",
            "Phone",
            "Phonemd",
        ]
    ].to_excel("mainfilefirstbackup.xlsx", index=True)
    return df


if __name__ == "__main__":
    t0 = time.time()
    df = main()
    t1 = time.time()
    print(f"run time {t1-t0}")

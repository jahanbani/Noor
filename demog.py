import os

import ipdb
import matplotlib.pyplot as plt
import pandas as pd


def clean_dem(df):
    df.replace(
        {
            "کاندا": "Canada",
            "کانادا": "Canada",
            "مونترال": "Montreal",
            "montréal": "Montreal",
            "vancouver, bc": "Vancouver",
            "اتاوا": "ottowa",
            "واترلو": "waterloo",
            "ونکور": "vancouver",
            "united states": "usa",
            "بوستون": "boston",
            "تورنتو": "toronto",
            "طهران": "tehran",
            "امريكا": "usa",
            "ایران": "iran",
            "ایزان": "iran",
            "isfahan": "اصفهان",
            "esfahan": "اصفهان",
            "rasht": "رشت",
            "mashhad": "مشهد",
            "tehran": "تهران",
            "teheran": "تهران",
            "kordestan": "کردستان",
            "tabriz": "تبریز",
            "kerman": "کرمان",
            "ahwaz": "اهواز",
            "kermanshah": "کرمانشاه",
            "lorestan": "لرستان",
            "ghochan": "قوچان",
        },
        inplace=True,
    )  # Canada

    return df


def fix_phone(df):
    df["Phone"] = df["Phone"].astype(str)
    # select the last 10 digits of the phone numbers
    df["Phone"] = df["Phone"].str[-10:]

    return df


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
    df = df[["Phone", "City", "Country"]]

    # if not answered
    df.fillna(value="Z", inplace=True)
    return df


def rem_dup(df):
    grpobj = df.groupby(["Phone"])
    for k in grpobj.groups.keys():
        gp = grpobj.get_group(k)
        if len(gp) > 1:
            if gp.isnull().values.any():
                gp.fillna(method="ffill", inplace=True)
                gp.fillna(method="bfill", inplace=True)
    df = grpobj.first().reset_index()
    return df


resp = os.listdir("resp")

dff = {}
for fn in resp:
    data = pd.read_excel(r"resp/" + fn)
    dfc = clean_data(data)
    dfp = fix_phone(dfc)
    dfu = rem_dup(dfp).set_index("Phone")
    dfu.columns = [str(col) + "_" + fn[1:2] for col in dfu.columns]
    dff[fn[:-5]] = dfu

anss = pd.concat([dff[k] for k, v in dff.items()], join="outer", axis=1,)
anss.fillna(method="ffill", axis=1, inplace=True)
anss.fillna(method="bfill", axis=1, inplace=True)

anss = (
    anss[["City_1", "Country_1"]]
    .apply(lambda x: x.astype(str).str.strip())
    .apply(lambda x: x.astype(str).str.lower())
)
df = clean_dem(anss).apply(lambda x: x.astype(str).str.lower())
df.to_clipboard()
dfn = df.groupby(['City_1']).count().reset_index()
df
ipdb.set_trace()  # XXX

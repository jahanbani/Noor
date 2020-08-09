# Distributed under terms of the MIT license.
"""
draw
"""
import sys
import time

import pandas as pd


def highlight_max(df):
    """
    highlight the maximum in a Series yellow.
    """
    return ["background-color: black"] * len(df)


t0 = time.time()
df = pd.read_excel("mainfile.xlsx", index_col=0)
print(f"reading the mainfile took {time.time()-t0}")
qq = 1
for i in range(7):
    print(f"Doing the draw for winner number {i+1}")
    fg = True
    while fg:
        winner = input("Please enter the winner number: ")
        if (isinstance(winner, str)) & (not winner == "QQ"):
            fg = False
        elif winner == "QQ":
            qq = 0
            break

    if not qq:
        break
    t0 = time.time()
    # df.to_excel("mainfile" + "_before_winner" + "_" + str(winner) + ".xlsx", index=True)
    print(
        df.loc[
            int(winner),
            ["Phonest", "Phonemd", "Phoneed", "Name", "City", "Country", "nc", "point"],
        ]
        .to_frame()
        .T
    )

    # update df
    print("removing the winner from the list")
    df = df[df["Phone"] != df.loc[int(winner), "Phone"]].reset_index(drop=True)
    print(f"the number of available entries are now: {df.shape[0]}")
    print("shuffling the list again")
    df = df.sample(frac=1).reset_index(drop=True)
    print("writing the list")
    try:
        df.to_excel("mainfile" + "_after_winner_" + str(winner) + ".xlsx", index=True)
        print("wrote the excel file now going to csv")

        df.to_csv(
            "mainfile" + "_after_winner_backup_" + str(winner) + ".csv", index=True
        )
    except:
        pass
    t1 = time.time()
    print(f"run time is {t1-t0}")

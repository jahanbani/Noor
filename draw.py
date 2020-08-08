"""

"""
import sys
import time
import tkinter as tk

import pandas as pd


def main():
    df = pd.read_excel("mainfile.xlsx", index_col=0)

    # winner = input("What is the winning number? ")
    # winner = sys.argv[1]

    # print("the winner is ")
    winner = int(sys.argv[1])
    df.to_excel("mainfile" + "_before_winner" + "_" + str(winner) + ".xlsx", index=True)
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
    print("shuffling the list again")
    df = df.sample(frac=1).reset_index(drop=True)
    print("writing the list")
    try:
        df.to_excel("mainfile.xlsx", index=True)
        df.to_excel("mainfile" + "_after_winner_" + str(winner) + ".xlsx", index=True)
    except:
        pass
    print(df.shape)


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print(f"run time {t1-t0}")

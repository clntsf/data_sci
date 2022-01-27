import pandas as pd
import matplotlib.pyplot as plt

original_fp = "data/2020-data.xlsx"
thisyear = 2022
minnum = 10

# to clean the original sheet
def clean_sheet(fp):
    fpout =  f"{__file__[:-17]}/data/{fp[fp.rfind('/'):-5]}-clean.xlsx"
    df = pd.read_excel(fp)

    yob_unique = [*set(df["Year Of Birth"])]
    outdf = pd.DataFrame({"Year Manufactured": yob_unique})
    badcols = ["Vehicle Make", "Vehicle Model", "Year Of Birth"]
    cols = [*filter(lambda x: "%" not in x and x not in badcols, df.columns)]
    for c in cols:
        outdf[c] = [sum(df.loc[df["Year Of Birth"]==yob, c]) for yob in yob_unique]
    outdf = outdf[outdf["Total"]>=minnum]
    outdf.to_excel(fpout, index=False)

# to make the graph of pass pct vs year made
def yob_passpct(fpclean):
    df = pd.read_excel(fpclean)
    passpct = [round(a/b*100,2) for a,b in zip(df["PASS"], df["Total"])]

    plt.plot(df["Year Manufactured"], passpct, 'ro')
    plt.yticks(range(0,101,10))
    plt.xlabel("Year Manufactured")
    plt.ylabel("Pass %")
    plt.title("Pass % of Cars by Year Manufactured")
    plt.savefig("img/yrman-passpct")

cfp = "data/2020-data-clean.xlsx"
yob_passpct(cfp)
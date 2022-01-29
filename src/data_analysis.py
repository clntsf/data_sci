import pandas as pd
import plotly.express as px
from plotly import io

# Config
thisyear = 2022
minnum = 10
fpstem = __file__[:-17]
cleanfp = f"{fpstem}/data/clean/yrman-passpct.txt"

# to clean the original sheet
def get_yrman_passpct(fp):

    # Read filepath into pd.DataFrame and get index column
    fnindex = fp.rfind("/")
    fileyear = int(fp[fnindex+1:fnindex+5])
    df = pd.read_excel(fp)

    yob_unique = [*set(df["Year Of Birth"])]
    data = []

    # Combine data by summing based on value of index column
    for yob in yob_unique:
        rows = df[df["Year Of Birth"]==yob]
        total = sum(rows["Total"])
        if total >= minnum:
            passnum = sum(rows["PASS"])
            data.append([fileyear-yob, round(passnum/total * 100, 2)])
    
    return zip(*data)

def writedata():
    data_years = range(2017,2021)
    data = []
    
    for yr in data_years:
        fp = f"{fpstem}/data/source/{yr}-data.xlsx"
        age, passpct = get_yrman_passpct(fp)
        data += [*zip([str(yr)]*len(age), age, passpct)]

    for age in set([n[1] for n in data]):
        items = [n for n in data if n[1]==age]
        ages, passpcts = [*zip(*items)][1:]
        data.append(["AVG", sum(ages)/len(ages), sum(passpcts)/len(passpcts)])

    data = [*zip(*data)]
    out = pd.DataFrame({"Data Year": data[0], "Age": data[1], "Pass %": data[2]})
    out.to_csv(cleanfp, index=False)

# New plotly graph
def plotdata():
    df = pd.read_csv(cleanfp)
    df["Data Year"] = [*map(str, df["Data Year"])]

    fig = px.line(df, x="Age", y="Pass %", color="Data Year")
    fig.write_html(f"{fpstem}/graphs/output.html")
    fig.show()

if __name__ == "__main__":
    writedata()
    plotdata()
    
# Old matplotlib graph
# to make the graph of pass pct vs year made
# def yrman_passpct(fpclean):
#     df = pd.read_excel(fpclean)
#     passpct = [round(a/b*100,2) for a,b in zip(df["PASS"], df["Total"])]

#     plt.plot(df["Year Manufactured"], passpct, 'ro')        # Plot the data
#     plt.yticks(range(0,101,10))                             # Formatting
#     plt.xlabel("Year Manufactured")
#     plt.ylabel("Pass %")
#     plt.title("Pass % of Cars by Year Manufactured")
#     plt.savefig("img/yrman-passpct")                        # Save as image
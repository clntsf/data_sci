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
        total = sum(df.loc[df["Year Of Birth"]==yob, "Total"])
        if total >= minnum:
            passnum = sum(df.loc[df["Year Of Birth"]==yob, "PASS"])
            data.append([fileyear-yob, round(passnum/total * 100, 2)])
            
    return zip(*data)

def writedata():
    data_years = range(2017,2021)
    yrs, ages, totals, passpcts = [], [], [], []
    
    for yr in data_years:
        fp = f"{fpstem}/data/source/{yr}-data.xlsx"
        age, passpct = get_yrman_passpct(fp)

        yrs+=[str(yr)]*len(age); ages += age; passpcts += passpct
    
    for age in set(ages):
        agelist = [a2 for a2 in ages if a2==age]
        pctlist = [pct for i,pct in enumerate(passpcts) if ages[i] == age]

        yrs.append("AVG")
        ages.append(sum(agelist)/len(agelist))
        passpcts.append(sum(pctlist)/len(pctlist))

    out = pd.DataFrame({"Data Year": yrs, "Age": ages, "Pass %": passpcts})
    out.to_csv(cleanfp, index=False)

def plotdata():
    df = pd.read_csv(cleanfp)
    df["Data Year"] = [*map(str, df["Data Year"])]
    fig = px.line(df, x="Age", y="Pass %", color="Data Year")
    fig.write_html(f"{fpstem}/graphs/output.html")
    fig.show()

if __name__ == "__main__":
    # writedata()
    plotdata()
    
# gonna try using plotly from now on

# # to make the graph of pass pct vs year made
# def yrman_passpct(fpclean):
#     df = pd.read_excel(fpclean)
#     passpct = [round(a/b*100,2) for a,b in zip(df["PASS"], df["Total"])]

#     plt.plot(df["Year Manufactured"], passpct, 'ro')        # Plot the data
#     plt.yticks(range(0,101,10))                             # Formatting
#     plt.xlabel("Year Manufactured")
#     plt.ylabel("Pass %")
#     plt.title("Pass % of Cars by Year Manufactured")
#     plt.savefig("img/yrman-passpct")                        # Save as image
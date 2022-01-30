import pandas as pd
import plotly.express as px

# Config
thisyear = 2022
minnum = 50
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
        passnum = sum(rows["PASS"])

        data.append([fileyear-yob, round(passnum/total * 100, 2), total])
    
    return zip(*data)

def writedata():
    data_years = range(2013,2021)
    data = []
    
    for yr in data_years:
        fp = f"{fpstem}/data/source/{yr}-data.xlsx"
        age, passpct, total = get_yrman_passpct(fp)
        data += [*zip([str(yr)]*len(age), age, passpct, total)]

    data = pd.DataFrame(data, columns=["Data Year", "Age", "Pass %", "Total"])
    data.to_csv(cleanfp, index=False)

# New plotly graph
def plotdata():
    df = pd.read_csv(cleanfp)
    df = df[df["Total"]>=minnum]
    df["Data Year"] = [*map(str, df["Data Year"])]

    avg = []
    ages = [*set(df["Age"])]
    for age in ages:
        rows = df[df["Age"]==age]
        numtotal = max(rows["Total"])

        if numtotal>= minnum:
            rlen = len(rows.index)
            age_avg, pass_avg = sum(rows["Age"])/rlen, sum(rows["Pass %"])/rlen
            avg += [["AVG", age_avg, pass_avg, numtotal]]

    avg = pd.DataFrame(avg, columns=["Data Year", "Age", "Pass %", "Total"])
    df = pd.concat([df, avg], ignore_index=True)

    fig = px.line(df, x="Age", y="Pass %", color="Data Year", markers=True, symbol="Data Year", hover_data=["Total"])
    fig.write_html(f"{fpstem}/graphs/output.html")
    fig.show()

if __name__ == "__main__":
    # writedata()
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
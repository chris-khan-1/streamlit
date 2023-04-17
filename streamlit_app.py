import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px

st.title('Wow would you look at that...')

def to_dict(df, track):
    df2 = df[["Rider", "Pos.", "Points"]]
    df2["Rider"] = df2["Rider"].str.split(' ').str[1].str.split('(?<=.)(?=[A-Z])').str.join('_')
    # df2 = df2.fillna("na")
    df2.columns = ["rider", f"{track}-position", f"{track}-points"]
    df2 = df2.set_index("rider")
    x = df2.to_dict()
    x.values()
    for k, j in x.items():
        try:
            del j["riders"]
            del j["who"]
        except:
            continue
    
    return x

year = 2023
for i in ["RAC", "SPR"]:
    for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
        url = f"https://www.motogp.com/en/gp-results/{year}/{j}/MotoGP/{i}/Classification"

        data = requests.get(url).text
        print(j, i)
        try:
            df = pd.read_html(data)
            dict_ = to_dict(df[0], j)
            st.write(f'{year}/{i}/{j}-{i}.json')

        except:
            break

races = []

for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
    try:
        y = pd.read_json(f"2023/RAC/{j}-RAC.json")
        races.append(y.T)
    except:
        continue

sprints = []

for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
    try:
        a = pd.read_json(f"2023/SPR/{j}-SPR.json")
        sprints.append(a.T)
    except:
        continue

b = pd.concat(sprints).reset_index()

spr_pos = b[b["index"].str.contains("position")].fillna(25)
spr_points = b[b["index"].str.contains("points")].fillna(0)

st.dataframe(spr_pos)
st.dataframe(spr_points)
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

dicts = []
year = 2023
for i in ["SPR"]:
    for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
        url = f"https://www.motogp.com/en/gp-results/{year}/{j}/MotoGP/{i}/Classification"

        data = requests.get(url).text
        try:
            df = pd.read_html(data)
            dict_ = to_dict(df[0], j)
            dicts.append(dict_)

        except ValueError:
            break


b = pd.concat([pd.DataFrame(x).T for x in dicts]).reset_index()

spr_pos = b[b["index"].str.contains("position")].fillna(25)
spr_points = b[b["index"].str.contains("points")].fillna(0)


st.dataframe(spr_pos)
st.dataframe(spr_points)
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

spr_pos = pd.to_numeric(b[b["index"].str.contains("position")].fillna(25))
spr_points = pd.to_numeric(b[b["index"].str.contains("points")].fillna(0))

st.write(spr_pos.dtypes)
st.write(spr_points.dtypes)

st.dataframe(spr_pos)
st.dataframe(spr_points)

fig1 = px.line(
                spr_pos, 
                x=spr_pos["index"], 
                y=spr_pos.columns[1:], 
                template="plotly_dark",
                labels={
                    "index": "Track",
                    "value": "Position",
                    "variable": "Rider"
                    },
                title="MotoGp Rider Sprint Position 2023",
                markers = True
            )

fig1['layout']['yaxis']['autorange'] = "reversed"


st.plotly_chart(fig1, theme="streamlit")
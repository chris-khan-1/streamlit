import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px

st.title('Wow would you look at that...')


def to_dict(df, track):
    df2 = df[["Rider", "Pos.", "Points"]]
    df2["Rider"] = df2["Rider"].str.split(
        ' ').str[1].str.split('(?<=.)(?=[A-Z])').str.join('_')
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

def color_survived(val):
    color='red'
    if val==rider:
        color = 'green'
    return f'background-color: {color}'



tracks = {"NED": "Assen (Netherlands)",
          "ITA": "Mugello (Italy)",
          "RSM": "Misano (San Marino)",
          "FRA": "Le Mans (France)",
          "GBR": "Silverstone (Britain)",
          "GER": "Sachsenring (Germany)",
          "JPN": "Motegi (Japan)",
          "ANC": "Jerez (Spain)",
          "DOH": "Losail (Qatar)",
          "INA": "Mandalika (Indonesia)",
          "EUR": "Ricardo Tormo (Valencia)",
          "ARA": "Aragon",
          "MAL": "Sepang (Malaysia)",
          "AUS": "Phillip Island (Australia)",
          "AME": "COTA (America)",
          "ALR": "Portimao (Portugal)",
          "SPA": "Jerez (Spain)",
          "CZE": "Brno (Czech Republic)",
          "CAT": "Catalunya (Barcelona)",
          "TER": "Aragon",
          "EMI": "Misano (San Marino)",
          "STY": "Red Bull Ring (Austria)",
          "ARG": "Termas de Rio Hondo (Argentina)",
          "VAL": "Ricardo Tormo (Valencia)",
          "THA": "Buriram (Thailand)",
          "AUT": "Red Bull Ring (Austria)",
          "QAT": "Losail (Qatar)",
          "POR": "Portimao (Portugal)"}

df = pd.read_csv("./data/2019-2022_finishes.csv")
df = df.set_index("position")

track = st.selectbox(" ", set(tracks.values()))
acronyms = [i for i,j in tracks.items() if j == track]

if len(acronyms)==1:
    df_final = df.filter(like=acronyms[0], axis=1)
else:
    dfs = []
    for i in acronyms:
        dfs.append(df.filter(like=i, axis=1))
    df_final = pd.concat(dfs, axis=1)

rider = st.selectbox(" ", ["Marc_Marquez","Alex_Rins","Francesco_Bagnaia","Enea_Bastianini","Franco_Morbidelli"])

st.dataframe(df.style.applymap(color_survived))
# st.write(df_final)

# filter = st.text_input("Race Venue")


# dicts = []
# year = 2023
# for i in ["SPR"]:
#     for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
#         url = f"https://www.motogp.com/en/gp-results/{year}/{j}/MotoGP/{i}/Classification"

#         data = requests.get(url).text
#         try:
#             df = pd.read_html(data)
#             dict_ = to_dict(df[0], j)
#             dicts.append(dict_)

#         except ValueError:
#             break


# b = pd.concat([pd.DataFrame(x).T for x in dicts]).reset_index()

# spr_pos = b[b["index"].str.contains("position")].fillna(25)
# cols1 = spr_pos.columns
# spr_pos[cols1[1:]] = spr_pos[cols1[1:]].apply(pd.to_numeric, errors='coerce')

# spr_points = b[b["index"].str.contains("points")].fillna(0)
# cols2 = spr_points.columns
# spr_points[cols2[1:]] = spr_points[cols2[1:]].apply(pd.to_numeric, errors='coerce')

# st.dataframe(spr_pos)
# st.dataframe(spr_points)

# fig1 = px.line(
#                 spr_pos,
#                 x=spr_pos["index"],
#                 y=spr_pos.columns[1:],
#                 template="plotly_dark",
#                 labels={
#                     "index": "Track",
#                     "value": "Position",
#                     "variable": "Rider"
#                     },
#                 title="MotoGp Rider Sprint Position 2023",
#                 markers = True
#             )

# fig1['layout']['yaxis']['autorange'] = "reversed"


# st.plotly_chart(fig1, theme="streamlit")

import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px

st.set_page_config(layout="wide")

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


def color_rider(val):
    color = 'green' if val == rider else ''
    return f'background-color: {color}'

@st.cache_data
def get_results(race_type):
    dicts = []
    year = 2023
    for i in [race_type]:
        for j in ["POR", "ARG", "AME", "SPA", "FRA", "ITA", "GER", "NED", "KAZ", "GBR", "AUT", "CAT", "RSM", "IND", "JPN", "INA", "AUS", "THA", "MAL", "QAT", "VAL"]:
            url = f"https://www.motogp.com/en/gp-results/{year}/{j}/MotoGP/{i}/Classification"

            data = requests.get(url).text
            try:
                df = pd.read_html(data)
                dict_ = to_dict(df[0], j)
                dicts.append(dict_)

            except ValueError:
                break
    return dicts

@st.cache_data
def to_position_df(dicts_):
    b = pd.concat([pd.DataFrame(x).T for x in dicts_]).reset_index()

    spr_pos = b[b["index"].str.contains("position")].fillna(25)
    cols1 = spr_pos.columns
    spr_pos[cols1[1:]] = spr_pos[cols1[1:]].apply(pd.to_numeric, errors='coerce')
    return spr_pos


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

riders = [
            'Francesco_Bagnaia',
            'Brad_Binder',
            'Jorge_Martin',
            'Jack_Miller',
            'Marco_Bezzecchi',
            'Johann_Zarco',
            'Andrea_Dovizioso',
            'Aleix_Espargaro',
            'Takaaki_Nakagami',
            'Valentino_Rossi',
            'Fabio_Quartararo',
            'Alex_Rins',
            'Darryn_Binder',
            'Miguel_Oliveira',
            'Jorge_Lorenzo',
            'Joan_Mir',
            'Marc_Marquez',
            'Lorenzo_Savadori',
            'Luca_Marini',
            'Fabio_Di',
            'Alex_Marquez',
            'Franco_Morbidelli',
            'Maverick_Viñales',
            'Enea_Bastianini',
            'Dani_Pedrosa',
            'Raul_Fernandez'
            ]

df = pd.read_csv("./data/2019-2022_finishes.csv")
df = df.set_index("position")


# get sprint results
sprint_dicts = get_results("SPR")
spr_pos = to_position_df(sprint_dicts)

# get race results
race_dicts = get_results("RAC")
rac_pos = to_position_df(race_dicts)

# ________________________________________________________________________________________________________________
# START OF PAGE LAYOUT
vert_space = '<div style="padding: 25px 5px;"></div>'

st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: #273346 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("MotoGP Analytics")
st.markdown(vert_space, unsafe_allow_html=True)
st.subheader("MotoGP Previous Results")

c1, c2 = st.columns(2)
with c1:
    track = st.selectbox("Select Track:", set(tracks.values()))
with c2:
    rider = st.multiselect("Select Up To Three Riders:", riders, max_selections=3, default="Francesco_Bagnaia")

# filtering dataframe based on user selection
acronyms = [i for i, j in tracks.items() if j == track]

if len(acronyms) == 1:
    df_final = df.filter(like=acronyms[0], axis=1)
else:
    dfs = []
    for i in acronyms:
        dfs.append(df.filter(like=i, axis=1))
    df_final = pd.concat(dfs, axis=1)


df_final["Pos."] = range(1, len(df_final)+1)
df_final.set_index("Pos.", inplace=True)
df_final.fillna('', inplace=True)
df_final = df_final.reindex(sorted(list(df_final.columns), key= lambda x: float(x.split('-')[-1])), axis=1)


if len(rider) == 1:
    st.dataframe(df_final.style.apply(lambda x: ['background-color: green' if s == rider[0] else '' for s in x]), use_container_width=True)
elif len(rider) == 2:
    st.dataframe(df_final.style.apply(lambda x: ['background-color: green' if s == rider[0] else '' 'background-color: #f77d31' if s == rider[1] else '' for s in x]), use_container_width=True)
elif len(rider) == 3:
    st.dataframe(df_final.style.apply(lambda x: ['background-color: green' if s == rider[0] else '' 'background-color: #f77d31' if s == rider[1] else '' 'background-color: #af62ff' if s == rider[2] else ''for s in x]), use_container_width=True)
# st.dataframe(df_final.reset_index().style.applymap(color_rider))


st.markdown(vert_space, unsafe_allow_html=True)

st.subheader("MotoGP Current Results")

st.caption("Doubleclick a rider on the right hand side legend to highlight them. Multiple riders can be selected for comparisons")


sorted_riders = list(spr_pos.columns)
sorted_riders.remove('index')
sorted_riders = sorted(sorted_riders)#, key= lambda x: sum(int(x)))

# plot of sprint positions
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
    title="MotoGp Rider Sprint Positions 2023",
    markers=True,
    category_orders={"variable": sorted_riders}
)

fig1['layout']['yaxis']['autorange'] = "reversed"
fig1.update_layout(height=600)
# fig1.update_yaxes(range=[1, 25])
st.plotly_chart(fig1, theme="streamlit", use_container_width=True, height=600)

# plot of race positions
fig2 = px.line(
    rac_pos,
    x=rac_pos["index"],
    y=rac_pos.columns[1:],
    template="plotly_dark",
    labels={
        "index": "Track",
        "value": "Position",
        "variable": "Rider"
    },
    title="MotoGp Rider Race Positions 2023",
    markers=True,
    category_orders={"variable": sorted_riders}
)

fig2['layout']['yaxis']['autorange'] = "reversed"
fig2.update_layout(height=600)
# fig2.update_yaxes(range=[1, 25])
st.plotly_chart(fig2, theme="streamlit", use_container_width=True, height=600)

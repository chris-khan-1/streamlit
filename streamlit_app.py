import streamlit
import requests
import pandas as pd
import json
import plotly.express as px

streamlit.title('Wow would you look at that...')

# def to_dict(df, track):
#     df2 = df[["Rider", "Pos.", "Points"]]
#     df2["Rider"] = df2["Rider"].str.split(' ').str[1].str.split('(?<=.)(?=[A-Z])').str.join('_')
#     # df2 = df2.fillna("na")
#     df2.columns = ["rider", f"{track}-position", f"{track}-points"]
#     df2 = df2.set_index("rider")
#     x = df2.to_dict()
#     x.values()
#     for k, j in x.items():
#         try:
#             del j["riders"]
#             del j["who"]
#         except:
#             continue
    
#     return x

# year = 2023
# for i in ["RAC", "SPR"]:
#     for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
#         url = f"https://www.motogp.com/en/gp-results/{year}/{j}/MotoGP/{i}/Classification"

#         data = requests.get(url).text
#         print(j, i)
#         try:
#             df = pd.read_html(data)
#             dict_ = to_dict(df[0], j)
#             with open(f'{year}/{i}/{j}-{i}.json', 'w')

#         except:
#             break

# races = []

# for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
#     try:
#         y = pd.read_json(f"2023/RAC/{j}-RAC.json")
#         races.append(y.T)
#     except:
#         continue

# sprints = []

# for j in ["POR","ARG","AME","SPA","FRA","ITA","GER","NED","KAZ","GBR","AUT","CAT","RSM","IND","JPN","INA","AUS","THA","MAL","QAT","VAL"]:
#     try:
#         a = pd.read_json(f"2023/SPR/{j}-SPR.json")
#         sprints.append(a.T)
#     except:
#         continue

# b = pd.concat(sprints).reset_index()

spr_pos = pd.read_json('{"index":{"0":"POR-position","2":"ARG-position","4":"AME-position"},"Francesco_Bagnaia":{"0":1.0,"2":6.0,"4":1.0},"Jorge_Martin":{"0":2.0,"2":8.0,"4":3.0},"Marc_Marquez":{"0":3.0,"2":25.0,"4":25.0},"Jack_Miller":{"0":4.0,"2":10.0,"4":9.0},"Maverick_Vi\\u00f1ales":{"0":5.0,"2":7.0,"4":10.0},"Aleix_Espargaro":{"0":6.0,"2":25.0,"4":4.0},"Miguel_Oliveira":{"0":7.0,"2":25.0,"4":8.0},"Johann_Zarco":{"0":8.0,"2":13.0,"4":11.0},"Alex_Marquez":{"0":9.0,"2":5.0,"4":25.0},"Fabio_Quartararo":{"0":10.0,"2":9.0,"4":19.0},"Raul_Fernandez":{"0":11.0,"2":14.0,"4":15.0},"Brad_Binder":{"0":12.0,"2":1.0,"4":5.0},"Alex_Rins":{"0":13.0,"2":15.0,"4":2.0},"Franco_Morbidelli":{"0":14.0,"2":4.0,"4":14.0},"Takaaki_Nakagami":{"0":15.0,"2":11.0,"4":13.0},"Fabio_Di":{"0":16.0,"2":12.0,"4":17.0},"Marco_Bezzecchi":{"0":25.0,"2":2.0,"4":6.0},"Luca_Marini":{"0":25.0,"2":3.0,"4":7.0},"Enea_Bastianini":{"0":25.0,"2":25.0,"4":25.0},"Joan_Mir":{"0":25.0,"2":25.0,"4":12.0},"Augusto_Fernandez":{"0":25.0,"2":16.0,"4":16.0},"Stefan_Bradl":{"0":25.0,"2":25.0,"4":18.0},"Jonas_Folger":{"0":25.0,"2":25.0,"4":20.0},"Michele_Pirro":{"0":25.0,"2":25.0,"4":25.0}}')
spr_points = pd.read_csv(',index,Francesco_Bagnaia,Jorge_Martin,Marc_Marquez,Jack_Miller,Maverick_Viñales,Aleix_Espargaro,Miguel_Oliveira,Johann_Zarco,Alex_Marquez,Fabio_Quartararo,Raul_Fernandez,Brad_Binder,Alex_Rins,Franco_Morbidelli,Takaaki_Nakagami,Fabio_Di,Marco_Bezzecchi,Luca_Marini,Enea_Bastianini,Joan_Mir,Augusto_Fernandez,Stefan_Bradl,Jonas_Folger,Michele_Pirro\r\n1,POR-points,12.0,9.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0\r\n3,ARG-points,4.0,2.0,0.0,0.0,3.0,0.0,0.0,0.0,5.0,1.0,0.0,12.0,0.0,6.0,0.0,0.0,9.0,7.0,0.0,0.0,0.0,0.0,0.0,0.0\r\n5,AME-points,12.0,7.0,0.0,1.0,0.0,6.0,2.0,0.0,0.0,0.0,0.0,5.0,9.0,0.0,0.0,0.0,4.0,3.0,0.0,0.0,0.0,0.0,0.0,0.0\r\n')

streamlit.dataframe(spr_pos)
streamlit.dataframe(spr_points)
import streamlit as st
import plotly.express as px

from library import *

st.set_page_config(layout="wide")

tracks = get_tracks()

riders = get_riders()

year = get_year()

# Get all data
all_data = get_all_data()

spr_pos, spr_points, rac_pos, rac_points, combined_points, comb_riders, sorted_riders = get_and_transform_current_results(year)

for i in [spr_pos, spr_points, rac_pos, rac_points, combined_points, comb_riders, sorted_riders]:
    st.write(i)

champ_table = get_championship_table(combined_points)

fantasy_df = get_gsheet_data(f"{year}_fantasy")
fantasy_df = filter_fantasy_df(fantasy_df)

fantasy_teams_df = get_gsheet_data(f"{year}_fantasy_constructors")
fantasy_teams_df = filter_fantasy_teams_df(fantasy_teams_df)
# _________________________________________________________________________________________________________________
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

c1, c2, c3= st.columns(3)
with c1:
    track = st.selectbox("Select Track:", set(tracks.values()))
with c2:
    rider = st.multiselect("Select Up To Three Riders:", riders, max_selections=3, default="Francesco_Bagnaia")
with c3:
    race_type = st.selectbox("Select Race Type:", ["Main Race", "Sprint", "Both"])


display_selection(all_data, rider, tracks, track, race_type)


st.markdown(vert_space, unsafe_allow_html=True)

st.subheader("MotoGP Current Results")

st.caption("Doubleclick a rider on the right hand side legend to highlight them. Multiple riders can be selected for comparisons")

# if st.button('Refresh Results'):
#     spr_pos, spr_points, rac_pos, rac_points, combined_points, comb_riders, sorted_riders = refresh_current_results()

# plot of fantasy results
fantasy_plot = px.line(
                fantasy_df,
                x=[i[0] for i in fantasy_df["index"].str.split('_')], 
                y=fantasy_df.columns[1:], 
                template="plotly_dark",
                labels={
                    "x": "Track",
                    "value": "Fantasy Points",
                    "variable": "Rider"
                    },
                title=f"MotoGp Fantasy Points {year}",
                markers = True,
                category_orders={"variable": comb_riders}

            )


fantasy_plot.update_layout(height=600)
st.plotly_chart(fantasy_plot, theme="streamlit", use_container_width=True, height=600)

# plot of real spr + rac points 
real_results_comb_plot = px.line(
                combined_points, 
                x=[i[0] for i in combined_points["index"].str.split('_')], 
                y=combined_points.columns[1:], 
                template="plotly_dark",
                labels={
                    "x": "Track",
                    "value": "Points Total",
                    "variable": "Rider"
                    },
                title=f"MotoGp Total Points {year}",
                markers = True,
                category_orders={"variable": comb_riders}

            )

real_results_comb_plot.update_layout(height=600)
st.plotly_chart(real_results_comb_plot, theme="streamlit", use_container_width=True, height=600)

# plot of fantasy team results
fantasy_team_plot = px.line(
                fantasy_teams_df,
                x=[i[0] for i in fantasy_teams_df["index"].str.split('_')], 
                y=fantasy_teams_df.columns[1:], 
                template="plotly_dark",
                labels={
                    "x": "Track",
                    "value": "Fantasy Points",
                    "variable": "Rider"
                    },
                title=f"MotoGp Fantasy Team Points {year}",
                markers = True,
                # category_orders={"variable": comb_riders}

            )

fantasy_team_plot.update_layout(height=600)
st.plotly_chart(fantasy_team_plot, theme="streamlit", use_container_width=True, height=600)

# plot of sprint positions
sprint_plot = px.line(
    spr_pos,
    x=[i[0] for i in spr_pos["index"].str.split('_')],
    y=spr_pos.columns[1:],
    template="plotly_dark",
    labels={
        "x": "Track",
        "value": "Position",
        "variable": "Rider"
    },
    title=f"MotoGp Rider Sprint Positions {year}",
    markers=True,
    category_orders={"variable": comb_riders}
)

sprint_plot['layout']['yaxis']['autorange'] = "reversed"
# fantasy_plot['layout']['xaxis']['autorange'] = "reversed"
sprint_plot.update_layout(height=600)
# fantasy_plot.update_yaxes(range=[1, 25])
st.plotly_chart(sprint_plot, theme="streamlit", use_container_width=True, height=600)

# plot of race positions
race_plot = px.line(
    rac_pos,
    x=[i[0] for i in rac_pos["index"].str.split('_')],
    y=rac_pos.columns[1:],
    template="plotly_dark",
    labels={
        "x": "Track",
        "value": "Position",
        "variable": "Rider"
    },
    title=f"MotoGp Rider Race Positions {year}",
    markers=True,
    category_orders={"variable": comb_riders}
)

race_plot['layout']['yaxis']['autorange'] = "reversed"
# real_results_comb_plot['layout']['xaxis']['autorange'] = "reversed"
race_plot.update_layout(height=600)
# real_results_comb_plot.update_yaxes(range=[1, 25])
st.plotly_chart(race_plot, theme="streamlit", use_container_width=True, height=600)


# plot of spr + rac points cummulative
total_plot = px.line(
                combined_points.cumsum(), 
                x=[i[0] for i in combined_points["index"].str.split('_')], 
                y=combined_points.columns[1:], 
                template="plotly_dark",
                labels={
                    "x": "Track",
                    "value": "Points Total",
                    "variable": "Rider"
                    },
                title=f"MotoGp Total Cumulative Points {year}",
                markers = True,
                category_orders={"variable": comb_riders}

            )

total_plot.update_layout(height=600)
st.plotly_chart(total_plot, theme="streamlit", use_container_width=True, height=600)


champ_table.index = range(1, len(champ_table)+1)
st.dataframe(champ_table)


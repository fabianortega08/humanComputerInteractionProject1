# Fabian E. Ortega
# Human Computer Interaction - Project 2
# 6/8/2025

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px

#Store liked games
if "liked_games" not in st.session_state:
    st.session_state.liked_games = []

# Page setup
st.set_page_config(
    page_title="Football ",
    layout="centered"
)
st.title(" Soccer 2019 ")

st.subheader(" Premier League ")

# API
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"
querystring = {"h2h": "33-34"}

headers = {
    "x-rapidapi-key": "d04a57e69dmshd8caa0b0b5c386ep100b66jsn8efd681957e1",
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

# Tabs
overview, standings, players, map = st.tabs(["Overview","Standings","Players", "Map"])

# Video URL
video_urls = [
    "https://www.youtube.com/watch?v=RhAvE_Svssw",
    "https://www.youtube.com/watch?v=JUaf8nskJZw",
    "https://www.youtube.com/watch?v=O8W9etfJXOA"
]

# Overview tab
with overview:
    try:
        response = requests.get(url, headers=headers, params=querystring)
        fixtures = response.json().get("response", [])[:3]
        st.success("Loaded Premier League Games")

        for idx, fixture in enumerate(fixtures):
            match = fixture["fixture"]
            teams = fixture["teams"]
            goals = fixture["goals"]

            #Show game date
            match_date = datetime.fromisoformat(match["date"].replace("Z", "+00:00"))

            col1, col4 = st.columns([1, 1])
            with col1:
                # Determine winner
                home_score = goals['home']
                away_score = goals['away']

                home_win = "W" if home_score > away_score else " "
                away_win = "W" if away_score > home_score else " "


                st.write("")
                st.write("")

                st.markdown(
                    f"<div style='display: flex; align-items: center;'>"
                    f"<img src='{teams['home']['logo']}' width='100' style='margin-right:20px;'>"
                    f"<span style='font-size: 20px; font-weight: bold;'>{teams['home']['name']} "
                    f"<span style='color: gray;'>({home_score})</span> <span style='color: green;'>{home_win}</span></span></div>",
                    unsafe_allow_html=True
                )
                st.write("")
                st.write("")

                st.markdown(
                    f"<div style='display: flex; align-items: center; margin-top: 10px;'>"
                    f"<img src='{teams['away']['logo']}' width='100' style='margin-right:20px;'>"
                    f"<span style='font-size: 20px; font-weight: bold;'>{teams['away']['name']} "
                    f"<span style='color: gray;'>({away_score})</span> <span style='color: green;'>{away_win}</span></span></div>",
                    unsafe_allow_html=True

                            )
                st.write("")
                st.write("")

            with col4:
                st.markdown("<h3 style='text-align: center;'>Final</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray;'>{match_date.strftime('%B %d, %Y')}</p>",
                            unsafe_allow_html=True)
                st.video(video_urls[idx])  # Use corresponding video
                st.markdown("<p style='text-align: center; color: gray;'>GAME HIGHLIGHTS</p>", unsafe_allow_html=True)

            match_title = f"{teams['home']['name']} vs {teams['away']['name']} ({match_date.strftime('%b %d, %Y')})"

            with col1:
                if st.button(":thumbsup:", key=f"like_{idx}"):
                    if match_title not in st.session_state.liked_games:
                        st.session_state.liked_games.append(match_title)
                        st.success("Match Liked!")
                if st.button(":thumbsdown:", key=f"dislike_{idx}"):
                    st.error("Match Disliked!.")

    except Exception as e:
        st.error(" Could access game data.")
        st.exception(e)
    #Feedback Request
    st.markdown("---")
    st.markdown("### Suggestions or Feedback")

    user_feedback = st.text_area("Let us know what you think about the app!")

    if st.button("Submit Feedback"):
        if user_feedback.strip():
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please write something before submitting.")

    with players:
        st.header("Premier League Players ")

        season = 2020
        league_id = 39  # Premier League

        #  All Premier League teams
        try:
            teams_url = "https://api-football-v1.p.rapidapi.com/v3/teams"
            teams_query = {"league": league_id, "season": season}
            teams_response = requests.get(teams_url, headers=headers, params=teams_query)
            teams_data = teams_response.json().get("response", [])


            team_options = {team["team"]["name"]: team["team"]["id"] for team in teams_data}

            # Let user select a team
            selected_team_name = st.selectbox("Select a Premier League team", list(team_options.keys()))
            selected_team_id = team_options[selected_team_name]


            players_url = "https://api-football-v1.p.rapidapi.com/v3/players"
            players_query = {"team": selected_team_id, "season": season}
            players_response = requests.get(players_url, headers=headers, params=players_query)
            player_data = players_response.json().get("response", [])

            if not player_data:
                st.warning("No player data found for this team.")
            else:
                st.subheader(f"{selected_team_name} Club")
                num_cols = 3
                for i in range(0, len(player_data), num_cols):
                    cols = st.columns(num_cols)
                    for j, player_entry in enumerate(player_data[i:i + num_cols]):
                        player = player_entry["player"]
                        with cols[j]:
                            st.image(player["photo"], width=100)
                            st.markdown(f"<div style='font-weight: bold; font-size: 20px;'>{player['name']}</div>",
                                        unsafe_allow_html=True)
                            st.caption(f"Age: {player.get('age', 'N/A')}")
                            st.caption(f"Nationality: {player.get('nationality', 'N/A')}")

        except Exception as e:
            st.error("Error fetching Premier League team or player data.")
            st.exception(e)


        with standings:
            st.header("Premier League Standings")

            # Chart custom
            view_option = st.selectbox("Select the type of chart:", ["Interactive Table", "Bar chart"])
            color = st.color_picker("Choose color", "#CE8FFB")
            top_n = st.slider("Pick a length for the table", 1, 20, 10)

            try:
                standings_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
                standings_query = {"league": "39", "season": "2020"}  # Premier League 2020
                response = requests.get(standings_url, headers=headers, params=standings_query)
                data = response.json()

                if data.get("response"):
                    teams_data = data["response"][0]["league"]["standings"][0]

                    # data
                    df = pd.DataFrame([{
                        "Rank": team["rank"],
                        "Club": team["team"]["name"],
                        "Wins": team["all"]["win"],
                        "Draws": team["all"]["draw"],
                        "Losses": team["all"]["lose"],
                        "Goals": team["all"]["goals"]["for"],
                        "Goals Against": team["all"]["goals"]["against"],
                        "Points": team["points"]
                    } for team in teams_data[:top_n]])

                    if view_option == "Interactive Table":
                        st.dataframe(df, use_container_width=True)
                    else:
                        chart = px.bar(
                            df.head(top_n),
                            x="Club",
                            y="Points",
                            color_discrete_sequence=[color]  # Use the color selected by user
                        )
                        chart.update_layout(title="Top Teams - Premier League 2020", xaxis_title="Team",
                                            yaxis_title="Points")
                        st.plotly_chart(chart, use_container_width=True)
                else:
                    st.warning(" No standings data found.")
            except Exception as e:
                st.error("Failed to fetch standings.")
                st.exception(e)

        with map:
            st.header("Primer League Map")
            df = pd.DataFrame(
                np.random.randn(20, 2) / [2, 2] + [52.3555, -1.1743],
                columns=["lat", "lon"],
            )
            st.map(df, size=50)

    #SideBar
    st.sidebar.title("Liked Games"+":thumbsup:")

    #Checkbox
    show_likes = st.sidebar.checkbox("Show Liked Games")

    # Check if user wants to see liked games
    if show_likes:
        if st.session_state.get("liked_games"):
            for match in st.session_state.liked_games:
                st.sidebar.markdown(f"- {match}")
        else:
            st.sidebar.caption("No games liked yet.")
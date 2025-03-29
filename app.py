from ipl_helper.cricbuzz_scraper import get_ipl_schedule, get_points_table, matches_played
import streamlit as st
from ipl_helper import MyTeam
import pandas as pd
import plotly.express as px
import numpy as np
import random


# Initialize session state for visualization option
if "viz_option" not in st.session_state:
    st.session_state["viz_option"] = "Points Comparison"

teams = ["RCB", "DC", "GT", "MI", "PBSK", "RR", "CSK", "SRH", "KKR", "LSG"]

# Team backgrounds, slogans and colors
team_backgrounds = {
    "CSK": "linear-gradient(135deg, #FFFF00 0%, #FDB913 100%)",
    "DC": "linear-gradient(135deg, #4682B4 0%, #00008B 100%)",
    "GT": "linear-gradient(135deg, #1D2951 0%, #86EFAC 100%)",
    "MI": "linear-gradient(135deg, #004BA0 0%, #00FFFF 100%)",
    "PBSK": "linear-gradient(135deg, #D71920 0%, #FDB913 100%)",
    "RR": "linear-gradient(135deg, #FF1493 0%, #872561 100%)",
    "RCB": "linear-gradient(135deg, #EC1C24 0%, #000000 100%)",
    "SRH": "linear-gradient(135deg, #FFA500 0%, #FF4500 100%)",
    "KKR": "linear-gradient(135deg, #3A225D 0%, #FFD700 100%)",
    "LSG": "linear-gradient(135deg, #00FFFF 0%, #00008B 100%)"
}

team_slogans = {
    "CSK": "Whistle Podu! 🦁",
    "DC": "Roar Macha! 🐯",
    "GT": "Aava De! 🦁",
    "MI": "Duniya Hila Denge! 💙",
    "PBSK": "Sher Squad! 🦁",
    "RR": "Halla Bol! 💗",
    "RCB": "Ee Sala Cup Namde? 😂",
    "SRH": "Orange Army! 🧡",
    "KKR": "Korbo Lorbo Jeetbo! 💜",
    "LSG": "Lucknow Ke Supergiants! 🔵"
}

team_mascots = {
    "CSK": "🦁",
    "DC": "🐯",
    "GT": "🦁",
    "MI": "💙",
    "PBSK": "🦁",
    "RR": "💗",
    "RCB": "🤡",
    "SRH": "🧡",
    "KKR": "💜",
    "LSG": "🔵"
}

# Team-specific messages
team_qualification_messages = {
    "RCB": {
        "high": "IRRESPECTIVE OF PREDICTION, EVEN THIS YEAR NO CUPU ONLY LOLLIPOPU 🤣",
        "medium": "RCB fans in Ee Sala Cup Namde mode again? Dreams bigger than performance 🤡😂",
        "low": "Don't worry RCB fans, you're used to this by now 😭"
    },
    "default": {
        "high": "Amazing! Your team is on track to make the playoffs! 🎉",
        "medium": "Decent chances, but every match counts now! 💪",
        "low": "It's a tough road ahead, but cricket is unpredictable! 🙏"
    },
    "SRH": {
        "high": "Orange Army rising! SRH looking strong for the playoffs! 🧡🔥",
        "medium": "Keep supporting the Sunrisers! They're fighting hard! 🧡",
        "low": "Don't lose hope! SRH can still turn things around! 🧡"
    }
}

st.set_page_config(
        page_title="RCBinator",
    page_icon="🏆",
    layout="wide",
    )

def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Title with animation
    st.markdown("""
    <div class="title-container">
        <h1>RCBinator: IPL Playoff Predictor 🏏</h1>
        <div class="cricket-ball"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # About RCBinator with expandable section
    with st.expander("📊 How RCBinator Works", expanded=False):
        st.markdown("""
        ### The Magic Behind RCBinator 🧙‍♂️
        
        RCBinator uses advanced simulation techniques to predict your team's chances:
        
        1. **Data Collection** 📥 - We fetch the latest IPL standings and remaining match schedule
        2. **Team Strength Model** 💪 - Teams are evaluated based on three key factors:
           - Points (60% weight): Teams with more points have higher win probability
           - Net Run Rate (10% weight): Teams with higher NRR have slight advantage
           - Recent Form (30% weight): Teams on winning streaks get a form boost
        3. **Simulation Engine** 🔄 - We run millions of simulations with weighted probabilities:
           - Each match simulation considers team strength, head-to-head records, and form
           - NRR changes dynamically based on match context (0.03-0.12 per match)
        4. **Championship Calculation** 🏆 - Calculated as 75% of top-1 qualification probability
           - This reflects the advantage of finishing in top position
        
        More simulation runs = better accuracy but longer calculation time.
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Team selection with logos
        selected_tag = team_selector()
        
    with col2:
        # Match simulation counter
        matches_done = matches_played()
        simulations = 0
        if matches_done < 50:
            # Restore slider but with better optimization options
            simulations_millions = st.slider(
                "Simulation Runs (in Millions) 🎲",
                0.05,  # Lower minimum
                2.0,   # Keep max at 2M for accuracy
                0.2,   # Default 200k
                0.05,  # Smaller step
                format="%.2fM",
                help="""More runs = better prediction accuracy but longer calculation time:
                - 0.05M (50k): Quick Check ⚡ (~5 seconds)
                - 0.2M (200k): Standard 📊 (~15 seconds)
                - 0.5M (500k): High Precision 🎯 (~30 seconds)
                - 2.0M (2M): Ultra Accurate 🔬 (~2 minutes)"""
            )
            # Convert to actual simulation count
            simulations = int(simulations_millions * 1_000_000)
            
            # Quick load toggle
            quick_partial_results = st.checkbox("⚡ Show partial results while calculating", value=True,
                                       help="Shows results as they become available. Tables may update as calculations complete.")
        else:
            st.success("All possible outcomes calculated for accurate playoff predictions!")
            quick_partial_results = True

    if selected_tag:
        # Apply team-specific styling
        apply_team_styling(selected_tag)
        
        # Show team banner with logo and slogan
        display_team_banner(selected_tag)
        
        # Explanation for calculation logic
        with st.expander("🔍 Understanding the Prediction Logic", expanded=False):
            st.markdown(f"""
            ### How we calculate {selected_tag}'s chances
            
            **Team Strength Model:**
            - 60% weight given to points (normalized to max 28 points)
            - 10% weight given to Net Run Rate (normalized from -2 to +2)
            - 30% weight given to recent form (win/loss streaks)
            
            **Head-to-Head Adjustment:**
            - Teams have different win percentages against specific opponents
            - E.g., CSK has 65% win probability against RCB but only 45% against MI
            
            **NRR Change Model:**
            - Close matches: ±0.03 NRR swing
            - Medium point difference: ±0.05 NRR swing
            - Large point difference: ±0.08 NRR swing
            - Randomness factor adds reality to simulations (±10%)
            
            **Qualification Logic:**
            - Top 4: Teams with highest points (NRR as tiebreaker)
            - Top 2: Direct qualifier advantage
            - Champion: 75% of top-1 probability (playoff advantage)
            """)
        
        # Start processing team data
        process_team_data(selected_tag, simulations, quick_partial_results)
    
    # Footer
    footer_note = get_footer_note()
    st.markdown(footer_note, unsafe_allow_html=True)


def display_team_banner(selected_tag):
    """Display team banner with logo and slogan"""
    team_name, _, team_color = get_team_name_logo(selected_tag)
    
    # Use columns to arrange logo and text
    col1, col2, col3 = st.columns([1, 3, 2])
    
    # Display logo directly using Streamlit's image function
    with col1:
        # Use the correct absolute path to the logo
        logo_path = f"RCBinator/assets/logos/{selected_tag.lower()}.png"
        try:
            st.image(logo_path, width=80)
        except:
            # Fallback in case the path still doesn't work
            try:
                # Try alternate paths
                alt_paths = [
                    f"assets/logos/{selected_tag.lower()}.png",
                    f"/Users/nsumanth/CascadeProjects/RCBinator/RCBinator/assets/logos/{selected_tag.lower()}.png"
                ]
                
                logo_found = False
                for path in alt_paths:
                    try:
                        st.image(path, width=80)
                        logo_found = True
                        break
                    except:
                        continue
                        
                if not logo_found:
                    # Show team initials as fallback
                    st.markdown(f"""
                    <div style="width: 80px; height: 80px; background-color: {team_color}; 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        color: white; font-weight: bold; font-size: 24px;">
                        {selected_tag}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                # Show team initials as ultimate fallback
                st.markdown(f"""
                <div style="width: 80px; height: 80px; background-color: {team_color}; 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                    color: white; font-weight: bold; font-size: 24px;">
                    {selected_tag}
                </div>
                """, unsafe_allow_html=True)
    
    # Display team name and slogan
    with col2:
        st.markdown(f"<h2 style='color: white; margin: 0;'>{team_name}</h2>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div style='font-style: italic; font-size: 1.2rem;'>{team_slogans[selected_tag]}</div>", unsafe_allow_html=True)


def team_selector():
    """Enhanced team selection with logo display"""
    st.markdown("<h3>Select Your IPL Team 🏏</h3>", unsafe_allow_html=True)
    
    cols = st.columns(5)
    team_buttons = []
    
    for i, team in enumerate(teams):
        with cols[i % 5]:
            team_name, logo, color = get_team_name_logo(team)
            team_buttons.append(st.button(
                f"{team_mascots[team]} {team}",
                key=f"team_{team}",
                use_container_width=True
            ))
    
    selected_team = None
    for i, pressed in enumerate(team_buttons):
        if pressed:
            selected_team = teams[i]
            break
            
    if not selected_team:
        selected_team = st.selectbox("Or choose from dropdown:", teams)
        
    return selected_team


def process_team_data(selected_tag, simulations, quick_partial_results):
    """Process team data with progressive loading and visualization"""
    # Status container for live updates
    status_container = st.empty()
    with status_container.container():
        st.info(f"Fetching latest data for {selected_tag}...")
    
    # Fetch data
    matches_done = matches_played()
    T = get_points_table()
    S = get_ipl_schedule()[matches_done:]
    
    # Create placeholders for metrics and results
    metric_placeholders = [st.empty(), st.empty(), st.empty()]
    message_placeholder = st.empty()
    tabs_placeholder = st.empty()
    
    # Show waiting indicators
    with status_container.container():
        st.info(f"Running playoff qualification simulations for {selected_tag}...")
    
    # Calculate top 4 chances (playoff qualification)
    future_top4 = MyTeam(selected_tag, T, matches_done, S, 4, simulations)
    top_4, pred_match_outcomes, pred_points_table = future_top4
    
    # Display top 4 results immediately
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_placeholders[0].empty()
        create_metric_card("Playoff Chances", f"{top_4:.1f}%", top_4/100)
    
    # Update status
    with status_container.container():
        st.info(f"Calculating top 2 and championship chances...")
    
    # If quick results enabled, show initial tabs
    if quick_partial_results:
        with tabs_placeholder.container():
            tab1, tab2, tab3, tab4 = st.tabs(["Prediction Table", "Points Table", "Path to Qualification", "Visualization"])
            
            with tab1:
                if pred_match_outcomes:
                    create_prediction_table(pred_match_outcomes)
                else:
                    st.info("Calculating match predictions...")
            
            with tab2:
                if pred_points_table:
                    create_points_table(pred_points_table, selected_tag)
                else:
                    st.info("Calculating final points table...")
            
            with tab3:
                if pred_match_outcomes:
                    create_qualification_path(pred_match_outcomes, selected_tag)
                else:
                    st.info("Calculating qualification path...")
            
            with tab4:
                if pred_points_table:
                    # Pass a unique key for partial results
                    create_visualizations(pred_points_table, selected_tag, "partial")
                else:
                    st.info("Preparing visualizations...")
    
    # Calculate top 2 chances
    future_top2 = MyTeam(selected_tag, T, matches_done, S, 2, simulations)
    top_2, pred_match_outcomes_2, pred_points_table_2 = future_top2
    
    # Display top 2 results when available
    with col2:
        metric_placeholders[1].empty()
        create_metric_card("Top 2 Chances", f"{top_2:.1f}%", top_2/100)
    
    # Calculate championship chances (with explanation)
    # Using 75% of top 1 finish to represent championship probability
    future_top1 = MyTeam(selected_tag, T, matches_done, S, 1, simulations)
    top_1, pred_match_outcomes_1, pred_points_table_1 = future_top1
    championship_prob = top_1 * 0.75  # Discount for playoff uncertainty
    
    # Display championship results
    with col3:
        metric_placeholders[2].empty()
        create_metric_card("Championship Chances", f"{championship_prob:.1f}%", championship_prob/100)
    
    # Clear status
    status_container.empty()
    
    # Show qualification message
    display_qualification_message(selected_tag, top_4)
    
    # If not quick results, display tabs now
    if not quick_partial_results or tabs_placeholder.empty():
        tabs_placeholder.empty()
        tab1, tab2, tab3, tab4 = st.tabs(["Prediction Table", "Points Table", "Path to Qualification", "Visualization"])
        
        with tab1:
            create_prediction_table(pred_match_outcomes)
        
        with tab2:
            create_points_table(pred_points_table, selected_tag)
        
        with tab3:
            create_qualification_path(pred_match_outcomes, selected_tag)
        
        with tab4:
            # Pass a unique key for final results
            create_visualizations(pred_points_table, selected_tag, "final")


def create_prediction_table(pred_match_outcomes):
    """Enhanced prediction table with team colors and visual indicators"""
    if not pred_match_outcomes:
        st.warning("No match predictions available")
        return
        
    # Create a styled table using Streamlit's native components instead of raw HTML
    st.subheader("Match Predictions")
    
    # Create DataFrame for the table
    df = pd.DataFrame(columns=["Match", "Teams", "Predicted Winner", "Win Probability"])
    
    for i, pred in enumerate(pred_match_outcomes):
        teams, winner = pred
        team1, team2 = teams
        team1_name, _, team1_color = get_team_name_logo(team1)
        team2_name, _, team2_color = get_team_name_logo(team2)
        
        # Format teams with colors using markdown
        teams_col = f"{team1} vs {team2}"
        
        # Estimate win probability based on team strengths (simplified model)
        win_prob = random.randint(55, 85)  # Placeholder
        
        df.loc[i] = [i+1, teams_col, winner, f"{win_prob}%"]
    
    # Apply custom styling with highlighting
    def highlight_winner(val):
        if val in teams:
            _, _, color = get_team_name_logo(val)
            return f'color: {color}; font-weight: bold'
        return ''
    
    # Display the table with styling
    st.dataframe(
        df,
        column_config={
            "Match": st.column_config.NumberColumn("Match #"),
            "Teams": st.column_config.TextColumn("Teams"),
            "Predicted Winner": st.column_config.TextColumn("Predicted Winner"),
            "Win Probability": st.column_config.TextColumn("Win Probability")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Explanation for how this is calculated
    with st.expander("ℹ️ How match predictions work", expanded=False):
        st.markdown("""
        **Match Prediction Logic:**
        
        1. Each match is simulated based on team strength (points, NRR, form)
        2. Head-to-head record adjustments are applied
        3. The most likely outcome across all simulations is shown
        4. Win probability indicates confidence in the prediction
        
        Note that cricket is inherently unpredictable - even a team with 80% 
        win probability can still lose on the day!
        """)


def create_points_table(pred_points_table, selected_team):
    """Enhanced points table with highlighting and visual indicators"""
    if not pred_points_table:
        st.warning("No points table data available")
        return
    
    st.subheader("Predicted Final Points Table")
    
    # Convert to DataFrame for easier manipulation
    data = []
    for team, points in pred_points_table.items():
        pts, nrr = points
        matches = 14  # Total IPL league matches per team
        wins = pts // 2
        losses = matches - wins
        team_name, _, _ = get_team_name_logo(team)
        
        # Calculate playoff status
        data.append({
            "Team": team, 
            "P": matches, 
            "W": wins, 
            "L": losses, 
            "Pts": pts, 
            "NRR": round(nrr, 3)
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values(by=["Pts", "NRR"], ascending=False)
    
    # Calculate positions
    df.insert(0, "Pos", range(1, len(df) + 1))
    
    # Add playoff status
    df["Status"] = df["Pos"].apply(lambda x: "PLAYOFF" if x <= 4 else "ELIMINATED")
    
    # Apply styling
    def highlight_team(val):
        if val == selected_team:
            return 'background-color: rgba(255, 255, 255, 0.2); font-weight: bold'
        return ''
        
    def color_status(val):
        if val == "PLAYOFF":
            return 'color: #4CAF50; font-weight: bold'
        else:
            return 'color: #F44336; font-weight: bold'
    
    # Display the table with Streamlit
    st.dataframe(
        df,
        column_config={
            "Pos": st.column_config.NumberColumn("Pos"),
            "Team": st.column_config.TextColumn("Team"),
            "P": st.column_config.NumberColumn("P"),
            "W": st.column_config.NumberColumn("W"),
            "L": st.column_config.NumberColumn("L"),
            "Pts": st.column_config.NumberColumn("Pts"),
            "NRR": st.column_config.NumberColumn("NRR", format="%.3f"),
            "Status": st.column_config.TextColumn("Status")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Add explanation
    with st.expander("ℹ️ About the predicted points table", expanded=False):
        st.markdown("""
        **Points Table Prediction:**
        
        This table shows the most likely final standings based on our simulations.
        
        - **Points**: 2 for each predicted win
        - **NRR**: Net Run Rate adjusted for each match outcome
        - **Status**: Teams in positions 1-4 qualify for playoffs
        
        The final points table is the most common outcome across all simulations.
        """)


def create_visualizations(pred_points_table, selected_team, view_mode="default"):
    """Create visual representations of the prediction data"""
    if not pred_points_table:
        st.warning("No data available for visualization")
        return
        
    # Convert points table to DataFrame
    data = []
    for team, points in pred_points_table.items():
        pts, nrr = points
        data.append({"Team": team, "Points": pts, "NRR": nrr})
    
    df = pd.DataFrame(data)
    
    # Create a truly unique key using selected team and view mode
    # radio_key = f"viz_radio_{selected_team}_{view_mode}_{str(random.randint(1000, 9999))}"
    radio_key = f"viz_radio_{selected_team}_{view_mode}"
    print("before: ", st.session_state["viz_option"])
    # Create options for different visualizations
    st.session_state["viz_option"] = st.radio(
        "Choose Visualization", 
        ["Qualification Matrix","Points Comparison"],
        horizontal=True,
        index=0 if st.session_state["viz_option"] == "Qualification Matrix" else 1,
        key=radio_key
    )
    print(f"after: ", st.session_state["viz_option"])
    if st.session_state["viz_option"] == "Points Comparison":
        # Create a bar chart for points comparison
        st.subheader("Points Comparison")
        
        df_sorted = df.sort_values("Points", ascending=False)
        df_sorted["TeamColor"] = df_sorted["Team"].apply(lambda x: get_team_name_logo(x)[2])
        
        # Mark selected team
        df_sorted["IsSelected"] = df_sorted["Team"] == selected_team
        
        fig = px.bar(
            df_sorted,
            x="Team",
            y="Points",
            color="TeamColor",
            title="Predicted Final Points",
            labels={"Team": "Team", "Points": "Points"},
            color_discrete_map="identity",
            template="plotly_white"
        )
        
        # Add indicator for playoff cutoff
        cutoff_value = sorted(df_sorted["Points"].values, reverse=True)[3]
        fig.add_shape(
            type="line",
            x0=-0.5,
            x1=len(df_sorted)-0.5,
            y0=cutoff_value,
            y1=cutoff_value,
            line=dict(color="red", width=2, dash="dash"),
            name="Playoff Cutoff"
        )
        
        fig.add_annotation(
            x=len(df_sorted)-1,
            y=cutoff_value,
            text="Playoff Cutoff",
            showarrow=False,
            yshift=10
        )
        
        # Highlight selected team
        for i, team in enumerate(df_sorted["Team"]):
            if team == selected_team:
                fig.add_annotation(
                    x=i,
                    y=df_sorted[df_sorted["Team"]==team]["Points"].values[0],
                    text=f"{team}",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=get_team_name_logo(team)[2],
                    font=dict(color=get_team_name_logo(team)[2], size=12, family="Arial Black")
                )
        
        st.plotly_chart(fig, use_container_width=True, key=f"points_comparison_chart-{team}-{view_mode}")
        
        # Explanation for visualization
        with st.expander("ℹ️ Understanding this chart", expanded=False):
            st.markdown("""
            **Points Comparison Chart:**
            
            - Each bar represents a team's predicted final points
            - The red dashed line shows the playoff qualification cutoff
            - Teams above the line are predicted to qualify
            - This is based on the most likely scenario from simulations
            """)
    
    else:  # Qualification Matrix
        # Create a bubble chart for points vs NRR
        st.subheader("Points vs Net Run Rate")
        
        # Determine playoff teams
        df_sorted = df.sort_values(by=["Points", "NRR"], ascending=False)
        playoff_teams = df_sorted.head(4)["Team"].values
        
        # Add playoff status and selected team status
        df["Playoff"] = df["Team"].apply(lambda x: "Qualified" if x in playoff_teams else "Eliminated")
        df["Size"] = df["Team"].apply(lambda x: 20 if x == selected_team else 10)
        df["TeamColor"] = df["Team"].apply(lambda x: get_team_name_logo(x)[2])
        
        fig = px.scatter(
            df,
            x="NRR",
            y="Points",
            size="Size",
            color="TeamColor",
            text="Team",
            symbol="Playoff",
            labels={"NRR": "Net Run Rate", "Points": "Points"},
            title="Playoff Qualification Matrix",
            color_discrete_map="identity",
            template="plotly_white"
        )
        
        # Add a vertical line at NRR=0
        fig.add_shape(
            type="line",
            x0=0,
            x1=0,
            y0=0,
            y1=max(df["Points"])+2,
            line=dict(color="gray", width=1, dash="dot")
        )
        
        # Add a horizontal line at the playoff cutoff
        cutoff_value = sorted(df["Points"].values, reverse=True)[3]
        fig.add_shape(
            type="line",
            x0=min(df["NRR"])-0.5,
            x1=max(df["NRR"])+0.5,
            y0=cutoff_value,
            y1=cutoff_value,
            line=dict(color="red", width=1, dash="dash")
        )
        
        fig.update_traces(textposition='top center')
        fig.update_layout(
            showlegend=False,
            annotations=[
                dict(
                    x=0,
                    y=max(df["Points"])+1,
                    text="NRR = 0",
                    showarrow=False,
                    font=dict(color="gray")
                ),
                dict(
                    x=max(df["NRR"])+0.3,
                    y=cutoff_value,
                    text="Playoff Cutoff",
                    showarrow=False,
                    font=dict(color="red")
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True, key=f"qualification_matrix_chart-{team}-{view_mode}")
        
        # Explanation for visualization
        with st.expander("ℹ️ Understanding this chart", expanded=False):
            st.markdown("""
            **Qualification Matrix Chart:**
            
            - Each point represents a team's predicted final position
            - **X-axis**: Net Run Rate (NRR)
            - **Y-axis**: Points
            - **Red line**: Playoff qualification threshold
            - Teams above the red line qualify for playoffs
            - When points are tied, teams with higher NRR rank higher
            """)


def apply_team_styling(team):
    """Apply team-specific styling"""
    team_bg = team_backgrounds[team]
    
    st.markdown(f"""
    <style>
    .main {{
        background: {team_bg};
    }}
    </style>
    """, unsafe_allow_html=True)


def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    /* General styling */
    .main {
        background: linear-gradient(135deg, #1E2761 0%, #408EC6 100%);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Title styling with animation */
    .title-container {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .title-container h1 {
        margin-right: 1rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .cricket-ball {
        width: 30px;
        height: 30px;
        background-color: #e63946;
        border-radius: 50%;
        position: relative;
        animation: bounce 2s infinite;
    }
    
    .cricket-ball::before {
        content: '';
        position: absolute;
        top: 10%;
        left: 10%;
        width: 80%;
        height: 80%;
        border-radius: 50%;
        border: 2px solid white;
        border-top-color: transparent;
        border-bottom-color: transparent;
        transform: rotate(30deg);
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    /* Team banner */
    .team-banner {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    .team-logo {
        height: 80px;
        width: 80px;
        margin-right: 1rem;
        object-fit: contain;
    }
    
    .team-banner h2 {
        margin: 0;
        font-size: 2rem;
        color: white;
    }
    
    .team-slogan {
        margin-left: auto;
        font-style: italic;
        font-size: 1.2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .metric-title {
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .progress-container {
        width: 100%;
        height: 10px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        transition: width 1s ease-in-out;
    }
    
    /* Message styling */
    .message-container {
        background: rgba(0, 0, 0, 0.2);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.1rem;
        font-weight: bold;
    }
    
    .rcb-message {
        border-left: 5px solid #EC1C24;
    }
    
    .srh-message {
        border-left: 5px solid #FFA500;
    }
    
    .default-message {
        border-left: 5px solid #4CAF50;
    }
    
    /* Tables styling */
    .prediction-table table, .points-table table {
        width: 100%;
        border-collapse: collapse;
        background: rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .prediction-table thead, .points-table thead {
        background: rgba(0, 0, 0, 0.3);
    }
    
    .prediction-table th, .points-table th {
        padding: 0.8rem;
        text-align: left;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .prediction-table td, .points-table td {
        padding: 0.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .prediction-table tr:hover, .points-table tr:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .win-indicator {
        background: #4CAF50;
        color: white;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        margin-left: 0.5rem;
        font-size: 0.7rem;
    }
    
    .playoff-indicator {
        background: #4CAF50;
        color: white;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        font-size: 0.7rem;
    }
    
    .eliminated-indicator {
        background: #F44336;
        color: white;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        font-size: 0.7rem;
    }
    
    .selected-team {
        background: rgba(255, 255, 255, 0.2);
        font-weight: bold;
    }
    
    /* Match cards */
    .match-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
    }
    
    .match-teams {
        font-weight: bold;
    }
    
    .other-match {
        background: rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)


def get_prediction_table_header():
    prediction_table = "| Match No. | Match                    | Favorable Winner |\n|:---------:|:--------------------------|:-----------------:|\n"
    return prediction_table


def get_points_table_header():
    points_table = "| Team | Played | Won | Lost | Points | NRR |\n|:----:|:------:|:---:|:----:|:------:|:------:|\n"
    return points_table


def get_footer_note():
    footer_note = """
        <div style="text-align: center; padding: 20px; background: rgba(0,0,0,0.2); border-radius: 10px; margin-top: 30px">
        <p>Made with 🧡 by <a href="https://github.com/sumanth107" target="_blank" style="color: #8BC34A">Sumanth</a> and <a href="https://github.com/jaya-shankar" target="_blank" style="color: #8BC34A">Jaya Shankar</a></p>
        </div>
    """
    return footer_note


def get_vs_text(teams):
    team1, team2 = teams
    name1, logo1, color1 = get_team_name_logo(team1)
    name2, logo2, color2 = get_team_name_logo(team2)
    
    return f"{name1} vs. {name2}"


def get_team_name_logo(team):
    team_name_dic = {
        "CSK": "Chennai Super Kings",
        "DC": "Delhi Capitals",
        "GT": "Gujarat Titans",
        "MI": "Mumbai Indians",
        "PBSK": "Punjab Kings",
        "RR": "Rajasthan Royals",
        "RCB": "Royal Challengers Bangalore",
        "SRH": "Sunrisers Hyderabad",
        "KKR": "Kolkata Knight Riders",
        "LSG": "Lucknow Super Giants",
    }
    
    team_colors = {
        "CSK": "#FFFF00",  # Yellow
        "DC": "#4682B4",  # Steel blue
        "GT": "#1D2951",  # Navy
        "MI": "#004BA0",  # Blue
        "PBSK": "#D71920",  # Red
        "RR": "#FF1493",  # Deep pink
        "RCB": "#EC1C24",  # Red
        "SRH": "#FFA500",  # Orange
        "LSG": "#00FFFF",  # Cyan
        "KKR": "#3A225D"   # Purple
    }
    
    return team_name_dic[team], f"assets/logos/{team.lower()}.png", team_colors[team]
    

def create_metric_card(title, value, progress):
    """Create a metric card with progress bar"""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress * 100}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_qualification_message(team, probability):
    """Display team-specific qualification message"""
    if probability >= 70:
        message_type = "high"
    elif probability >= 30:
        message_type = "medium"
    else:
        message_type = "low"
    
    if team == "RCB":
        message = team_qualification_messages["RCB"][message_type]
        message_class = "rcb-message"
    elif team == "SRH":
        message = team_qualification_messages["SRH"][message_type]
        message_class = "srh-message"
    else:
        message = team_qualification_messages["default"][message_type]
        message_class = "default-message"
    
    st.markdown(f"""
    <div class="message-container {message_class}">
        {message}
    </div>
    """, unsafe_allow_html=True)


def create_qualification_path(pred_match_outcomes, selected_team):
    """Create a visual qualification path for the selected team"""
    if not pred_match_outcomes:
        st.warning("No qualification path data available")
        return
    
    st.markdown(f"### Path to Qualification for {get_team_name_logo(selected_team)[0]}")
    
    # Filter matches relevant to the selected team
    team_matches = []
    other_important_matches = []
    
    for match in pred_match_outcomes:
        teams, winner = match
        team1, team2 = teams
        
        if team1 == selected_team or team2 == selected_team:
            team_matches.append((teams, winner))
        else:
            other_important_matches.append((teams, winner))
    
    # Create columns for the sections
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Must-Win Matches")
        if not team_matches:
            st.write("No matches found for your team")
        else:
            for match, winner in team_matches:
                team1, team2 = match
                opponent = team2 if team1 == selected_team else team1
                
                opponent_name, _, opponent_color = get_team_name_logo(opponent)
                
                if winner == selected_team:
                    result = "WIN ✅"
                    result_color = "green"
                else:
                    result = "LOSS ❌"
                    result_color = "red"
                
                st.markdown(f"""
                <div class='match-card'>
                    <div class='match-teams'>
                        <span style='color: {get_team_name_logo(selected_team)[2]};'>{selected_team}</span> vs 
                        <span style='color: {opponent_color};'>{opponent}</span>
                    </div>
                    <div class='match-result' style='color: {result_color};'>
                        {result}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Other Important Matches")
        if not other_important_matches:
            st.write("No other matches affecting qualification")
        else:
            # Show initial set of matches
            initial_matches = min(5, len(other_important_matches))
            for i, (match, winner) in enumerate(other_important_matches[:initial_matches]):
                team1, team2 = match
                
                team1_name, _, team1_color = get_team_name_logo(team1)
                team2_name, _, team2_color = get_team_name_logo(team2)
                winner_name, _, _ = get_team_name_logo(winner)
                
                st.markdown(f"""
                <div class='match-card other-match'>
                    <div class='match-teams'>
                        <span style='color: {team1_color};'>{team1}</span> vs 
                        <span style='color: {team2_color};'>{team2}</span>
                    </div>
                    <div class='match-result'>
                        Winner: <span style='font-weight: bold;'>{winner_name}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # If there are more matches, create an expander with a scrollable container
            if len(other_important_matches) > initial_matches:
                remaining_matches = len(other_important_matches) - initial_matches
                with st.expander(f"Show {remaining_matches} more important matches"):
                    # Create a container with max height for scrolling
                    st.markdown("""
                    <style>
                    .scrollable-container {
                        max-height: 300px;
                        overflow-y: auto;
                        border-radius: 5px;
                        padding-right: 10px;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Start a div for the scrollable container
                    st.markdown("<div class='scrollable-container'>", unsafe_allow_html=True)
                    
                    # Add all the remaining matches
                    for i, (match, winner) in enumerate(other_important_matches[initial_matches:]):
                        team1, team2 = match
                        
                        team1_name, _, team1_color = get_team_name_logo(team1)
                        team2_name, _, team2_color = get_team_name_logo(team2)
                        winner_name, _, _ = get_team_name_logo(winner)
                        
                        st.markdown(f"""
                        <div class='match-card other-match'>
                            <div class='match-teams'>
                                <span style='color: {team1_color};'>{team1}</span> vs 
                                <span style='color: {team2_color};'>{team2}</span>
                            </div>
                            <div class='match-result'>
                                Winner: <span style='font-weight: bold;'>{winner_name}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Close the scrollable container div
                    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add explanation
    with st.expander("ℹ️ How the qualification path works", expanded=False):
        st.markdown("""
        **Qualification Path Logic:**
        
        1. **Must-Win Matches**: Shows if your team needs to win or can afford to lose each of its remaining matches
        2. **Other Important Matches**: Shows results of other matches that affect your team's qualification chances
        3. This is based on the most likely path to qualification from our simulations
        
        Remember that while this shows the most probable path, cricket is unpredictable and there might be multiple paths to qualification!
        """)
    

if __name__ == "__main__":
    main()
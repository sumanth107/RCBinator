import streamlit as st
from ipl_helper import MyTeam, AllTeams
import concurrent.futures


teams = ["RCB", "DC", "GT", "MI", "PBSK", "RR", "CSK", "SRH", "KKR", "LSG"]


button_state = {label: False for label in teams}


st.set_page_config(
        page_title="RCBinator",
        page_icon="🏆",  # Replace this with your desired icon emoji or path to an icon image
        layout="centered",  # Optional: Set the layout style (wide, center, or fullscreen)
    )

def main():
    st.title("RCBinator: IPL Playoff Chances 🏏")

    selected_tag = None
    selected_tag = st.selectbox("Choose Your Team 🏏", teams)



    # Display the buttons and handle their state
   
    # cols = st.columns(5)
    # for i,label in enumerate(teams):
    # # Check if the current button is selected
    #     is_selected = button_state[label]
        
    #     # Set the button style based on its state
    #     button_style = "selected" if is_selected else ""
        
    #     # Create the button and check if it was clicked
    #     if cols[i%5].button(label, key=label,  on_click=lambda label=label: None):
    #         # Update the state of the buttons
    #         for key in button_state:
    #             button_state[key] = False
    #         button_state[label] = True
            
    #         # Store the selected button
    #         selected_tag = label

    if selected_tag:
        col1 , col2 = st.columns(2)
        with st.spinner("Loading... Please wait while your team's data is being processed."):
            
            positions = [4, 2]
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                
                futures = [executor.submit(MyTeam, selected_tag, pos) for pos in positions]
                top_4, pred_match_outcomes, pred_points_table = futures[0].result()
                top_2, pred_match_outcomes_2, pred_points_table_2 = futures[1].result()
                
            
            
            col1.metric("Top 4 Chances", f"{top_4:.2f}%")
            col2.metric("Top 2 Chances", f"{top_2:.2f}%")
            
            st.markdown("Prediction & Points table are shown for top 4 chances")
            
            tab1, tab2 = st.tabs(["Prediction Table", "Points Table"])
            
            with tab1:
                if not pred_match_outcomes:
                    st.markdown("No data available")
                else:
                    prediction_table = get_prediction_table_header()
                    for i, pred_match_outcome  in enumerate(pred_match_outcomes):
                        
                        winner, logo, color = get_team_name_logo(pred_match_outcome[1])
                        # Adjust the spaces between columns to control the width of the middle column
                        prediction_table += f"| {i+1:<9} | {get_vs_text(pred_match_outcome[0]):<26} | <span style='color: {color};'>{pred_match_outcome[1]:<17} </span> |\n"

                    st.markdown(prediction_table, unsafe_allow_html=True)
            with tab2:
                if not pred_match_outcomes:
                    st.markdown("No data available")
                else:
                    points_table = get_points_table_header()
                    for team, points in pred_points_table.items():
                        team_name, logo, color = get_team_name_logo(team)
                        points_table += f"| <span style='color: {color};'>{team:<5} </span> | {'14':<5} | {points//2:<5} | {14 - points//2:<5}  | {points:<5} |\n"

                    st.markdown(points_table, unsafe_allow_html=True)
                
            

        footer_note = get_footer_note()
        st.markdown(footer_note, unsafe_allow_html=True)
        # for i, pred_match_outcome in enumerate(pred_match_outcomes):
        #     st.markdown(f"Match {i+1}: {pred_match_outcome[0]} vs. {pred_match_outcome[1]}")


def get_prediction_table_header():
    prediction_table = "| Match No. | Match                    | Favorable Winner |\n|:---------:|:--------------------------|:-----------------:|\n"
    return prediction_table

def get_points_table_header():
    points_table = "| Team | Played | Won | Lost | Points |\n|:----:|:------:|:---:|:----:|:------:|\n"

    return points_table

def get_footer_note():
    footer_note = """
        <div style="text-align: left; bottom: 0; width: 100%; marginTop: 50px">
        Made by <a href="https://github.com/sumanth107" target="_blank">Sumanth</a> & <a href="https://github.com/jaya-shankar" target="_blank">Jaya Shankar</a>
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
        "GT": "#008000",  # Green
        "MI": "#0000FF",  # Blue
        "PBSK": "#FFC0CB",  # Pink
        "RR": "#FF1493",  # Deep pink
        "RCB": "#FF0000",  # Red
        "SRH": "#FFA500",  # Orange
        "LSG": "#00CED1",   # Dark turquoise
        "KKR": "#FFD700"  # Gold
    }
    
    return team_name_dic[team], f"assets/logos/{team.lower()}.png", team_colors[team]
    


def style_buttons():
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: transparent;
            border: 1px solid white;
            width: 60px;
            border-radius: 25;
            padding: 10px;
            margin: 10px;
            font-size: 18px;
        }
        .selected {
            background-color: red;
            border: 2px solid red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    

if __name__ == "__main__":
    main()
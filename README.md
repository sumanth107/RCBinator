# RCBinator: IPL Playoff Predictor 🏏

RCBinator is an interactive web application that calculates the playoff chances for teams in the Indian Premier League (IPL). The app uses advanced Monte Carlo simulations to predict qualification probabilities based on current standings, remaining matches, and team performance metrics.

### 🔴 [Live App: RCBinator on Streamlit](https://rcbinator.streamlit.app/)


## ✨ Key Features

- **Team-Specific Experiences** - Custom UI themes and messaging based on team selection
- **Advanced Predictions** - Weighted simulation model using points (60%), NRR (10%), and team form (30%)
- **Multiple Visualizations** - Interactive charts, qualification paths, and prediction tables
- **Real-time Calculations** - Live data scraping from Cricbuzz for up-to-date predictions
- **Championship Probability** - Calculate not just playoff qualification but winning chances
- **Detailed Explanations** - Clear insights about prediction methodology and match outcomes

## Prediction Methodology

RCBinator uses a sophisticated model to predict match outcomes:

1. **Team Strength Calculation**
   - Points Table Position (60% weight)
   - Net Run Rate (10% weight)
   - Recent Team Form (30% weight)
   - Historical head-to-head records

2. **Dynamic NRR Modeling**
   - Different NRR changes (0.03-0.12) based on match context
   - Factors in point difference between competing teams
   - Random variation for realistic outcomes

3. **Monte Carlo Simulations**
   - Runs millions of simulations (configurable from 50k to 2M)
   - More simulations = better accuracy (but longer calculation time)

## Technical Deep Dive

### Team Strength Calculation Algorithm

The app uses a weighted formula to calculate team strength:

```python
def calculate_strength(team_data, team_name):
    points, nrr = team_data
    normalized_points = points / 28  
    normalized_nrr = (nrr + 1.5) / 3  
    
    # Weighted combination (60% points, 10% NRR, 30% form)
    strength = (POINTS_WEIGHT * normalized_points) + 
              (NRR_WEIGHT * normalized_nrr) + 
              (FORM_WEIGHT * team_form[team_name])
    
    return max(0.1, min(1.0, strength))  
```

This strength value ranges from 0.1 to 1.0 and represents a team's overall competitiveness. The formula prioritizes points (60%) as the most important factor, while also considering NRR (10%) and recent form (30%).

### Match Win Probability Model

For each match between two teams, the win probability is calculated using:

```
base_probability = strength_team_A / (strength_team_A + strength_team_B)
```

This creates a proportional probability - if Team A is twice as strong as Team B, it will have a ~67% chance of winning (2/(2+1)).

The base probability is then adjusted with head-to-head historical data:

```python
# Apply head-to-head advantage
h2h_modifier = 0
if team_a in head_to_head_advantage and team_b in head_to_head_advantage[team_a]:
    h2h_modifier = head_to_head_advantage[team_a][team_b] - 0.5

# Final probability (capped between 0.1-0.9)
final_prob = base_prob + h2h_modifier
final_prob = max(0.1, min(0.9, final_prob))
```

This captures historical matchup tendencies (e.g., CSK tends to perform better against RCB than MI). Probabilities are capped between 10% and 90% to reflect cricket's inherent unpredictability.

### NRR Change Calculation

Net Run Rate (NRR) changes after matches are dynamically calculated based on team point differentials:

```python
# Simplified NRR change logic
if points_diff >= 8:  # Big gap in points
    nrr_change = 0.08  # Larger NRR swing
elif points_diff >= 4:  # Medium gap
    nrr_change = 0.05  # Medium NRR swing
else:  # Close match
    nrr_change = 0.03  # Smaller NRR swing

# Add randomness (only 20% of the time)
if random.random() > 0.8:
    nrr_change *= 1.1
```

This creates realistic NRR changes that reflect match contexts - dominant teams gain more NRR than teams that barely win.

### Simulation Approaches

The app uses two different approaches based on the number of remaining matches:

1. **Exhaustive Approach** (< 18 matches):
   - Evaluates every possible tournament outcome (2^n possibilities)
   - Each outcome is weighted by its probability of occurrence
   - Sum of weighted qualifying scenarios = qualification probability

2. **Monte Carlo Sampling** (≥ 18 matches):
   - Runs thousands/millions of randomized tournament simulations
   - For each match, winner is determined using weighted probability
   - Percentage of simulations where team qualifies = qualification probability

```python
# Monte Carlo implementation
outcomes = np.random.binomial(1, match_probs, size=(samples, num_matches))

# Process match outcomes
for m_idx, (a, b) in enumerate(matches):
    a_wins = outcomes[:, m_idx].astype(bool)
    b_wins = ~a_wins
    
    # Update points & NRR for team A wins
    pt[a_wins, a] += 2
    nr[a_wins, a] += nrr_changes
    nr[a_wins, b] -= nrr_changes
    
    # Update for team B wins
    pt[b_wins, b] += 2
    nr[b_wins, b] += nrr_changes
    nr[b_wins, a] -= nrr_changes
```

### Qualification Logic

In the IPL, the top 4 teams qualify for playoffs based on:
1. Points (primary criterion)
2. Net Run Rate (tiebreaker)

The simulation checks if a team's position is ≤ 4 after sorting all teams by points and NRR:

```python
# Calculate rankings with weighted points/NRR
composite = pt * 1000 + nr  
rankings = np.argsort(-composite, axis=1)
positions = np.argmax(rankings == target_i, axis=1)
success_mask = positions < for_position
success_count = np.sum(success_mask)

qualification_probability = success_count / samples * 100
```

### Championship Probability Estimation

For championship probability, we:
1. Calculate top-1 finishing probability (same algorithm as above but for position 1)
2. Apply a discount factor of 0.75 to account for playoff uncertainty:

```python
championship_prob = top_1 * 0.75
```

This reflects the advantage of finishing 1st but acknowledges the uncertainty of knockout matches.

### Team Form Tracking

The app maintains a dynamic form tracker that updates during simulations:

```python
def update_team_form(winner, loser):
    team_form[winner] = min(1.0, team_form[winner] + 0.1)
    team_form[loser] = max(0.1, team_form[loser] - 0.1)
```

This creates realistic "hot streaks" and "slumps" that influence match outcomes in later rounds of the tournament.


## Usage Guide

1. **Select Your Team**: Choose your favorite IPL team
2. **Set Simulation Count**: Higher counts give more accurate results
3. **View Results**: Check playoff chances, top 2 probabilities, and championship odds
4. **Explore Visualizations**: See points comparisons, paths to qualification, and more


## Installation for Development

### Prerequisites

- Python 3.9 or higher
- Streamlit
- Pandas, Plotly, NumPy

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/sumanth107/RCBinator.git
   cd RCBinator
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application locally:
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app pointing to your fork
4. Set the main file path to `app.py`
5. Deploy and enjoy your own instance of RCBinator!

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- IPL data is scraped from [Cricbuzz](https://www.cricbuzz.com/)
- Made with 🧡 by [Sumanth](https://github.com/sumanth107) and [Jaya Shankar](https://github.com/jaya-shankar)


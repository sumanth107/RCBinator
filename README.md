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

## 📊 Prediction Methodology

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

## 💻 Usage Guide

1. **Select Your Team**: Choose your favorite IPL team
2. **Set Simulation Count**: Higher counts give more accurate results
3. **View Results**: Check playoff chances, top 2 probabilities, and championship odds
4. **Explore Visualizations**: See points comparisons, paths to qualification, and more


## 🛠️ Installation for Development

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

## 🚀 Deploying to Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app pointing to your fork
4. Set the main file path to `app.py`
5. Deploy and enjoy your own instance of RCBinator!

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- IPL data is scraped from [Cricbuzz](https://www.cricbuzz.com/)


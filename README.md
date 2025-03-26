# RCBinator: IPL Playoff Chances

RCBinator is a web application that calculates the playoff chances for each team in the Indian Premier League (IPL) based on the current points table and remaining matches. It uses a Monte Carlo simulation to estimate the probabilities of each team making it to the top 4.

LIVE URL: https://rcbinator.streamlit.app/
## Features

- Calculate the probability of a specific team reaching the playoffs
- Calculate the probability of all teams reaching the playoffs
- Display an example outcome of matches and points table for the specific team

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Flask
- Requests
- Beautiful Soup 4

### Installation

1. Clone the repository to your local machine:

2. Install the required packages:

4. Open your web browser and navigate to `http://127.0.0.1:5001`

## Usage

1. To calculate the probability of a specific team reaching the playoffs, enter the team name in the "My Team" section and click "Submit".
2. To calculate the probability of all teams reaching the playoffs, click "Submit" in the "All Teams" section.

## Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b your-feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin your-feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The current IPL data is being scrapped from [cricbuzz](https://www.cricbuzz.com/).


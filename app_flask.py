from flask import Flask, render_template, request
from ipl_helper import MyTeam, AllTeams

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/myteam', methods=['POST'])
def myteam():
    team_name = request.form['team_name']
    myteam_probability, op0, ot0 = MyTeam(team_name)
    return render_template('index.html', myteam_probability=myteam_probability, team_name=team_name, op0=op0, ot0=ot0)


@app.route('/allteams', methods=['POST'])
def allteams():
    probabilities = AllTeams()
    return render_template('index.html', allteams_probabilities=probabilities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)



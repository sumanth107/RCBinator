# @uthor: Sumanth Nethi
# Date: 04-29-2023
# RCBinator

import requests
from bs4 import BeautifulSoup
import random


def get_abbreviations(team_names):
    abbreviations = []
    for name in team_names:
        abbreviation = ''.join([word[0] for word in name.split()])
        if abbreviation == 'SH':
            abbreviation = 'SRH'
        elif abbreviation == 'PK':
            abbreviation = 'PBKS'
        abbreviations.append(abbreviation)
    return abbreviations

def matches_played():
    url = "https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/matches"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = soup.find_all('div', class_='cb-series-matches')
    schedule = [x.get_text() for x in matches]
    return sum([1 for x in schedule if 'won' in x])


def get_ipl_schedule():
    url = "https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/matches"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = soup.find_all('div', class_='cb-series-matches')
    schedule = [x.get_text() for x in matches]
    schedule = [x.split(',')[0].strip() for x in schedule]
    schedule = [list(map(lambda x: x.strip(), x.split('vs'))) for x in schedule]
    schedule = [get_abbreviations(x) for x in schedule][:-4]

    return schedule

get_ipl_schedule()


def get_points_table():
    url = "https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/points-table"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    teams = soup.find('table', class_='table cb-srs-pnts')
    table = [x.get_text() for x in teams.find_all('td', class_='cb-srs-pnts-name')]
    table = [''.join([word[0] for word in x.split()]) for x in table]
    table = [x.replace('SH', 'SRH') for x in table]
    table = [x.replace('PK', 'PBKS') for x in table]
    points = [x.get_text() for x in teams.find_all('td', class_='cb-srs-pnts-td')][5::7]
    points = [int(x) for x in points]

    points_table = dict(zip(table, points))

    return points_table


def IPL(team):
    T = get_points_table()
    matches_done = matches_played()
    S = get_ipl_schedule()[matches_done:]
    op, ot = [], []
    j = 0
    while j < 10 ** 4:
        P = []
        T_temp = T.copy()
        for x in S:
            i = random.randint(0, 1)
            T_temp[x[i]] += 2
            P.append([x, x[i]])
        l_temp = sorted(list(T_temp.values()), reverse=True)

        if T_temp[team] >= l_temp[3]:
            if P not in op:
                op.append(P)
                ot.append(dict(sorted(T_temp.items(), key=lambda item: item[1], reverse=True)))
        j += 1
    return 100 * len(op) / j


def AllTeams():
    matches_done = matches_played()
    probabilities = {}
    for i in get_points_table().keys():
        probabilities[i] = IPL(i)
    return probabilities


def MyTeam(team):
    matches_done = matches_played()
    T = get_points_table()
    S = get_ipl_schedule()[matches_done:]
    op, ot = [], []
    j = 0
    while j < 10 ** 4:
        P = []
        T_temp = T.copy()
        for x in S:
            i = random.randint(0, 1)
            T_temp[x[i]] += 2
            P.append([x, x[i]])
        l_temp = sorted(list(T_temp.values()), reverse=True)

        if T_temp[team] >= l_temp[3]:
            if P not in op:
                op.append(P)
                ot.append(dict(sorted(T_temp.items(), key=lambda item: item[1], reverse=True)))
        j += 1
    # for i in range(2):
    #     print(op[i])
    #     print(ot[i])
    #     print("-----------------------------------------")
    # print("Chance of favorable outcome :", 100 * len(op) / j, "%")
    return 100 * len(op) / j, op[0], ot[0]



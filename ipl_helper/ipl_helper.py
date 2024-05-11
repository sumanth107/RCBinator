# @uthor: Sumanth Nethi
# Date: 04-29-2023
# RCBinator

import requests
from bs4 import BeautifulSoup
import random
import re
import copy

def get_ipl_page_url():
    base_url = "https://www.cricbuzz.com"
    series_url = base_url + "/cricket-series"
    response = requests.get(series_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    ipl_page_url = soup.find('a', title='Indian T20 League 2024')['href']
    if not ipl_page_url:
        return None
    ipl_page_url = base_url + ipl_page_url
    return ipl_page_url

def get_abbreviations(team_names):
    abbreviations = []
    for name in team_names:
        abbreviation = ''.join([word[0] for word in name.split()])
        if abbreviation == 'SH':
            abbreviation = 'SRH'
        elif abbreviation == 'PK':
            abbreviation = 'PBSK'
        abbreviations.append(abbreviation)
    return abbreviations

def matches_played():
    url = get_ipl_page_url()  + '/matches'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = soup.find_all('div', class_='cb-series-matches')
    schedule = [x.get_text() for x in matches]
    return sum([1 for x in schedule if 'won' in x])


def get_ipl_schedule():
    url = get_ipl_page_url()  + '/matches'
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
    url = get_ipl_page_url()  + '/points-table'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    teams = soup.find('table', class_='table cb-srs-pnts')
    table = [x.get_text() for x in teams.find_all('td', class_='cb-srs-pnts-name')]
    table = [''.join([word[0] for word in x.split()]) for x in table]
    table = [x.replace('SH', 'SRH') for x in table]
    table = [x.replace('PK', 'PBSK') for x in table]
    table = [re.sub(r'[^a-zA-Z]', '', text) for text in table]
    points = [x.get_text() for x in teams.find_all('td', class_='cb-srs-pnts-td')][5::7]
    nrr = [x.get_text() for x in teams.find_all('td', class_='cb-srs-pnts-td')][6::7]

    points = [int(x) for x in points]
    nrr = [float(x) for x in nrr]
    points_table = {}
    for team,pts,nrr in zip(table, points, nrr):
        points_table[team] = [pts,nrr]
    
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


def MyTeam(team, for_position = 4):
    matches_done = matches_played()
    T = get_points_table()
    S = get_ipl_schedule()[matches_done:]
    op, ot = [], []
    j = 0
    no_remaining_matches = len(S)

    max_num = int(''.join('1' for _ in range(no_remaining_matches)),base=2) + 1
    outcome = 0
    while outcome < max_num:
        print(outcome)
        poss_outcomes = bin(outcome)[2:]
        poss_outcomes = '0' * (no_remaining_matches - len(poss_outcomes)) + poss_outcomes
        poss_outcomes = [int(o) for o in poss_outcomes]
        P = []
        T_temp = copy.deepcopy(T)
        for x,i in zip(S, poss_outcomes):
            T_temp[x[i]][0] += 2
            T_temp[x[i]][1] += 0.05
            j = (i+1)%2
            T_temp[x[j]][1] -= 0.05
            P.append([x, x[i]])
        l_temp = sorted(list(T_temp.values()), reverse=True)

        if T_temp[team][0] >= l_temp[for_position-1][0] and T_temp[team][1] >= l_temp[for_position-1][1]:
            if P not in op:
                op.append(P)
                ot.append(dict(sorted(T_temp.items(), key=lambda item:  (item[1][0], item[1][1]), reverse=True)))
        outcome += 1
    # for i in range(2):
    #     print(op[i])
    #     print(ot[i])
    #     print("-----------------------------------------")
    # print("Chance of favorable outcome :", 100 * len(op) / j, "%")
    if len(op) == 0 or len(ot) == 0:
        return 100 * len(op) / outcome, None,None
    return 100 * len(op) / outcome, op[0], ot[0]



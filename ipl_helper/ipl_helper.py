# @uthor: Sumanth Nethi
# Date: 04-29-2023
# RCBinator

import random
import numpy as np
import copy

from ipl_helper.cricbuzz_scraper import get_ipl_schedule, get_points_table, matches_played



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



def MyTeam(team,T, matches_done , S, for_position,simulations=100_000):
    def calculate_strength(team_data):
        """Points dominate, NRR as minor tiebreaker"""
        points, nrr = team_data
        return max(points + nrr, 1) # Now points dominate (e.g., 18 + 1.2 = 19.2)

    def get_team_position(table, team_name):
        sorted_teams = sorted(table.values(), key=lambda x: (-x[0], -x[1]))
        for pos, t in enumerate(sorted_teams, 1):
            if (t[0], t[1]) == (table[team_name][0], table[team_name][1]):
                return pos
        return len(sorted_teams)

    
    no_remaining = len(S)

    if no_remaining == 0:
        pos = get_team_position(T, team)
        return (100.0 if pos <= for_position else 0.0, [], [])

    # Precompute match probabilities
    match_probs = []
    for match in S:
        team_a, team_b = match
        strength_a = calculate_strength(T[team_a])
        strength_b = calculate_strength(T[team_b])
        prob_a = strength_a / (strength_a + strength_b)
        match_probs.append(prob_a)

    # Exhaustive search for <22 matches (weighted)
    if no_remaining < 22:
        total_outcomes = 1 << no_remaining
        success = 0.0
        example_out = None
        example_tab = None

        for outcome in range(total_outcomes):
            temp_T = copy.deepcopy(T)
            scenario = []
            scenario_prob = 1.0  # Track probability of this outcome
            
            for match_idx in range(no_remaining):
                team_a, team_b = S[match_idx]
                bit_pos = no_remaining - 1 - match_idx
                result = (outcome >> bit_pos) & 1
                
                # Update probability for this outcome
                if result == 0:
                    scenario_prob *= match_probs[match_idx]
                    winner = team_a
                else:
                    scenario_prob *= (1 - match_probs[match_idx])
                    winner = team_b
                
                # Update table
                temp_T[winner][0] += 2
                temp_T[winner][1] += 0.05
                loser = team_b if result == 0 else team_a
                temp_T[loser][1] -= 0.05
                scenario.append(((team_a, team_b), winner))

            # Check qualification
            sorted_teams = sorted(temp_T.values(), key=lambda x: (-x[0], -x[1]))
            cutoff = sorted_teams[for_position-1] if len(sorted_teams) >= for_position else (0, 0)
            team_entry = temp_T[team]
            
            if (team_entry[0] > cutoff[0]) or (team_entry[0] == cutoff[0] and team_entry[1] >= cutoff[1]):
                success += scenario_prob
                if not example_out:
                    example_out = scenario
                    example_tab = dict(sorted(temp_T.items(), key=lambda x: (-x[1][0], -x[1][1])))

        return (success * 100, example_out, example_tab)

    # Monte Carlo for ≥22 matches
    else:
        teams = list(T.keys())
        team_idx = {t: i for i, t in enumerate(teams)}
        target_i = team_idx[team]
        matches = [(team_idx[m[0]], team_idx[m[1]]) for m in S]
        num_matches = len(matches)

        points = np.array([T[t][0] for t in teams], dtype=np.float32)
        nrr = np.array([T[t][1] for t in teams], dtype=np.float32)
        samples = simulations

        # Generate outcomes using precomputed probabilities
        outcomes = np.random.binomial(1, match_probs, size=(samples, num_matches))

        pt = np.tile(points, (samples, 1))
        pt[pt > 22] = 22  # Cap points
        nr = np.tile(nrr, (samples, 1))

        for m_idx, (a, b) in enumerate(matches):
            a_wins = outcomes[:, m_idx].astype(bool)
            pt[a_wins, a] += 2
            nr[a_wins, a] += 0.05
            nr[a_wins, b] -= 0.05
            pt[~a_wins, b] += 2
            nr[~a_wins, b] += 0.05
            nr[~a_wins, a] -= 0.05

        # Calculate rankings
        composite = pt * 1000 + nr  # Points dominate by 1000:1 ratio
        rankings = np.argsort(-composite, axis=1)
        positions = np.argmax(rankings == target_i, axis=1)
        success_mask = positions < for_position
        success_count = np.sum(success_mask)

        # Example outcome
        example_out, example_tab = None, None
        if success_count > 0:
            idx = np.where(success_mask)[0][0]
            pt_ex = points.copy()
            nr_ex = nrr.copy()
            scenario = []
            
            for m_idx, (a, b) in enumerate(matches):
                result = outcomes[idx, m_idx]
                winner = teams[a] if result else teams[b]
                scenario.append(((teams[a], teams[b]), winner))
                
                if result:
                    pt_ex[a] += 2
                    nr_ex[a] += 0.05
                    nr_ex[b] -= 0.05
                else:
                    pt_ex[b] += 2
                    nr_ex[b] += 0.05
                    nr_ex[a] -= 0.05

            sorted_t = sorted(zip(pt_ex, nr_ex, teams), 
                            key=lambda x: (-x[0], -x[1]))
            example_tab = {t: (float(p), float(n)) for p, n, t in sorted_t}
            example_out = scenario

        return (success_count / samples * 100, example_out, example_tab)
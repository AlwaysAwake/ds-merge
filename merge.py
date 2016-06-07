# -*- coding: utf-8 -*-

from __future__ import print_function
import json

# import codecs
# codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

gamble_data = dict()
lineup_data = dict()
stats_data = dict()
match_vectors_of_year = dict()

blacklist = set()
whitelist = set()

START_YEAR = 2007
END_YEAR = 2016


def read_data():
	# Read gamble data
	for year in range(START_YEAR, END_YEAR + 1):
		with open('./gamble_data/' + str(year) + '.json') as gamble_file:
			print("Loading gamble_data of %d" % (year))
			gamble_data[year] = json.load(gamble_file)

	# Read lineup data
	for year in range(START_YEAR, END_YEAR + 1):
		with open('./lineup_data/' + str(year) + '.json') as lineup_file:
			print("Loading lineup_data of %d" % (year))
			lineup_data[year] = json.load(lineup_file)

	# Read stats data
	for year in range(START_YEAR, END_YEAR + 1):
		with open('./player_stats/fifa' + str(year) + '.json') as stats_file:
			print("Loading stats_data of %d" % (year))
      stats_data[year] = json.load(stats_file)


def fill_empty_attributes():
	for year in range(START_YEAR, END_YEAR + 1):
		for player in stats_data[year]:
			groups = [["Marking", "Tackling", "SlideTackling", "StandTackling"], ["Aggregation", "Anticipation", "Composure", "Ceativity", "Reactions", "AttPosition", "Interceptions", "Vision"], ["Crossing", "Passing", "LongBalls", "ShortPass", "LongPass"], ["Acceleration", "Pace", "Stamina", "Strength", "Balance", "SprintSpeed", "Agility", "Jumping"], ["Heading", "ShotAccuracy", "ShotPower", "LongShots", "Finishing", "FKAcc", "Curve", "Penalties", "YeVolleysar"], ["Reflexes", "Rushing", "Handling", "GKPosition", "GKDiving", "GKHandling", "GKKicking", "GKReflexes"]]
			for group in groups:
				sum = 0
				count = 0
				for attribute in group:
					if player[attribute] != 'XX':
						sum += int(player[attribute])
						count += 1
				for attribute in group:
					if player[attribute] == 'XX':
						player[attribute] = sum / count


def search_player(player_name, year):
	for player in stats_data[year]:
		if player["info"]["Name"].lower() == player_name.lower() or set([player_name, player["info"]["Name"]]) in whitelist:
			return player
	for player in stats_data[year]:
		for word in player_name.replace("-", " ").split(' '):
			if player["info"]["Name"].lower().find(word.lower()) != -1 and set([player_name, player["info"]["Name"]]) not in blacklist:
				print("Name in stat set: %s" % (player["info"]["Name"]))
				print("Original name: %s" % (player_name))
				while True:
					proceed = raw_input("Choice yes if above two is equivalent player(Y/N) ")
					if proceed == 'Y' or proceed == 'y':
						whitelist.add(frozenset({player_name, player["info"]["Name"]}))
						return player
					elif proceed == 'N' or proceed == 'n':
						blacklist.add(frozenset({player_name, player["info"]["Name"]}))
						break
	return False

"""
def get_average():
	attributes = ["Height", "Weight", "Age", "Overall", "Potential", "BallControl", "Dribbling", "Marking", "Tackling", "SlideTackling", "StandTackling", "Aggregation", "Anticipation", "Composure", "Ceativity", "Reactions", "AttPosition", "Interceptions", "Vision", "Crossing", "Passing", "LongBalls", "ShortPass", "LongPass", "Acceleration", "Pace", "Stamina", "Strength", "Balance", "SprintSpeed", "Agility", "Jumping", "Heading", "ShotAccuracy", "ShotPower", "LongShots", "Finishing", "FKAcc", "Curve", "Penalties", "YeVolleysar", "Reflexes", "Rushing", "Handling", "GKPosition", "GKDiving", "GKHandling", "GKKicking", "GKReflexes"]
	for year in range(START_YEAR, END_YEAR + 1):
		average_stats[year] = dict()
		teams = set()
		for player in stats_data[year]:
			teams.add(player["Team"])

		sums = dict()
		counts = dict()
		for team in list(teams):
			sums[team] = dict()
			counts[team] = dict()
			average_stats[year][team] = dict()
			for attribute in attributes:
				sums[team][attribute] = 0
				counts[team][attribute] = 0

		for player in stats_data[year]:
			for attribute in attributes:
				if player[attribute] != 'XX':
					sums[player["Team"]][attribute] += int(player[attribute])
					counts[player["Team"]][attribute] += 1

		for team in teams:
			for attribute in attributes:
				value = sums[team][attribute] / counts[team][attribute]
				average_stats[year][team][attribute] = value
"""

def extract_stats(player):
	vector = [player[attribute] for attribute in ["Height", "Weight", "Age", "Overall", "Potential", "BallControl", "Dribbling", "Marking", "Tackling", "SlideTackling", "StandTackling", "Aggregation", "Anticipation", "Composure", "Ceativity", "Reactions", "AttPosition", "Interceptions", "Vision", "Crossing", "Passing", "LongBalls", "ShortPass", "LongPass", "Acceleration", "Pace", "Stamina", "Strength", "Balance", "SprintSpeed", "Agility", "Jumping", "Heading", "ShotAccuracy", "ShotPower", "LongShots", "Finishing", "FKAcc", "Curve", "Penalties", "YeVolleysar", "Reflexes", "Rushing", "Handling", "GKPosition", "GKDiving", "GKHandling", "GKKicking", "GKReflexes"]]
	return vector


def extract_odds(odds):
	vector = [odds[attribute] for attribute in ["home_win", "draw", "away_win"]]
	return vector


def parse_match_result(score_str):
	score = score_str.split(":")
	home_score = int(score[0])
	away_score = int(score[1])
	return [
		1 if home_score > away_score else 0,
		1 if home_score == away_score else 0,
		1 if home_score < away_score else 0
	]


def merge():
	attributes = ["Height", "Weight", "Age", "Overall", "Potential", "BallControl", "Dribbling", "Marking", "Tackling", "SlideTackling", "StandTackling", "Aggregation", "Anticipation", "Composure", "Ceativity", "Reactions", "AttPosition", "Interceptions", "Vision", "Crossing", "Passing", "LongBalls", "ShortPass", "LongPass", "Acceleration", "Pace", "Stamina", "Strength", "Balance", "SprintSpeed", "Agility", "Jumping", "Heading", "ShotAccuracy", "ShotPower", "LongShots", "Finishing", "FKAcc", "Curve", "Penalties", "YeVolleysar", "Reflexes", "Rushing", "Handling", "GKPosition", "GKDiving", "GKHandling", "GKKicking", "GKReflexes"]
	for year in range(START_YEAR, END_YEAR + 1):
		match_vectors_of_year[year] = list()
		for k, v in lineup_data[year].items():
			team_split = k.split("-")
			home_team = team_split[0].rstrip(" ")
			away_team = team_split[1].lstrip(" ")
			match_vector = list()
			team_average = dict()
			for team in ["home", "away"]:
				team_average[team] = dict()
				teammates = list()
				for player_name in v[team]:
					result = search_player(player_name, year)
					if result != False:
						teammates.append(result)

				for attribute in attributes:
					team_average[team][attribute] = 0
					for teammate in teammates:
						team_average[team][attribute] += int(teammate[attribute])
					team_average[team][attribute] /= len(teammate)

			for team in ["home", "away"]:
				for player_name in v[team]:
					result = search_player(player_name, year)
					if result != False:
						match_vector += extract_stats(result)
					else:
						match_vector += extract_stats(team_average[team])

			match_vector += parse_match_result(gamble_data[year][k]["score"])
			match_vectors_of_year[year].append(match_vector)


def validate_data():
	feature_length = len(match_vectors_of_year[START_YEAR][0])
	print("Feature length: %d" % (feature_length))
	for year in range(START_YEAR, END_YEAR + 1):
		for match in match_vectors_of_year[year]:
			if feature_length != len(match):
				print("Error! training sample length mismatch")
				print("Current match vector length: %d" % (len(match)))


def generate_output_json():
	with open("training_set.json", "w") as training_file:
		json.dump(match_vectors_of_year, training_file)


def generate_output():
	with open("training_set.txt", "w") as training_file:
		for year in range(START_YEAR, END_YEAR):
			for match in match_vectors_of_year[year]:
				print(match, file=training_file)
	with open("test_set.txt", "w") as test_file:
		for match in match_vectors_of_year[END_YEAR]:
			print(match, file=test_file)


if __name__ == "__main__":
	print("Start")
	read_data()
	fill_empty_attributes()
	merge()
	validate_data()
	generate_output_json()
	generate_output()

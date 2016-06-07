import json

START_YEAR = 2007
END_YEAR = 2016

gamble_data = dict()

for year in range(START_YEAR, END_YEAR + 1):
	with open('./gamble_data/' + str(year) + '.json') as gamble_file:
		print("Loading gamble_data of %d" % (year))
		gamble_data[year] = json.load(gamble_file)
	print "Year {0}: {1}".format(year, len(gamble_data[year]))
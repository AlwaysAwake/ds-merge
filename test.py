import json

a = list({frozenset({1, 2}), frozenset({3, 4})})
b = list()
b.append({1, 2, 3})
b.append({3, 4, 5, 6})

c = dict()
c["white"] = a
c["black"] = b

with open("test.json", "w") as outfile:
	json.dump(c, outfile)
import os
import json

LANG="fr"

with open(os.path.join(".", "data", LANG, "articles.json")) as fp:
	data = json.load(fp)

full = ""

for text in data:
	full += "\n" + text["text"]

print("Number of files: ", len(data))
print("Number of tokens: ", len(full.split()))
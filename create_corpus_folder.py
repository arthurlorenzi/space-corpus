import os
import json
from pathlib import Path

LANG="en"

corpus_dir = Path(".", "data", "corpus", LANG)
corpus_dir.mkdir(parents=True, exist_ok=True)

with open(os.path.join(".", "data", LANG, "articles.json")) as fp:
	data = json.load(fp)

meta = {}

for article in data:
	title = article['title']

	meta[title] = {
		'title': article['title'],
		'authors': article['authors'],
		'topics': article['topics']
	}

	file_path = Path(corpus_dir, title.replace('/', '') + '.txt')

	with file_path.open('w') as fp:
		fp.write(article['text'])


meta_path = Path(corpus_dir, '_meta.json')

with meta_path.open('w') as fp:
	json.dump(meta, fp)
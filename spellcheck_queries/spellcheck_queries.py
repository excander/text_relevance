from bs4 import BeautifulSoup
from collections import defaultdict
import time
import random
import requests
import pickle
import sys

queries_dict = defaultdict(list)
i = 1
with open('text-relevance-competition-ir-1-ts-fall-2019/queries.numerate.txt') as queries_file:
	for line in queries_file:
		line_lst = line.rstrip().split()
		query_id, query = line_lst[0], ' '.join(line_lst[1:])
		queries_dict[query_id].append(query)
		response = requests.get('https://www.google.com/search?q='+query)
		resp_html = response.text
		soup = BeautifulSoup(resp_html, 'html.parser')
		checked = soup.find(id="scl")
		# if checked:
		# 	checked = checked.find('i')
		if checked:
			checked = checked.text
			queries_dict[query_id].append(checked)

		print(i, query+ "                         >>->>                     "+ checked if checked else query)
		print(i, query+ "                         >>->>                     "+ checked if checked else query, file=sys.stderr)
		i += 1
		time.sleep(random.randint(1,5)/random.randint(1,10))
		

with open('checked_queries_by_google.pickle', 'wb') as handle:
	pickle.dump(queries_dict, handle)
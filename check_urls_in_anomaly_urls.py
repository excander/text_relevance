import json

anomaly_urls = []
with open('anomaly_detection/anomaly_urls.json', 'r') as handler:
	anomaly_urls = json.load(handler)

anomaly_urls = set(i.rstrip() for i in anomaly_urls)

c=0
all = 0
with open('text-relevance-competition-ir-1-ts-fall-2019/urls.numerate.txt') as textfile:
	for line in textfile:
		line_lst = line.rstrip().split()
		url_id, url = line_lst[0], ' '.join(line_lst[1:])
		if url in anomaly_urls:
			# print(url)
			c+=1
		all +=1

print(c)
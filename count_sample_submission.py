import csv
from collections import defaultdict

data = defaultdict(int)

with open('text-relevance-competition-ir-1-ts-fall-2019/sample.technosphere.ir1.textrelevance.submission.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data[row[0]] += 1

for k in data:
	print(k, ':', data[k])
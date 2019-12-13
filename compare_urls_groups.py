from collections import defaultdict
import pandas as pd
import csv

urls = ['kek']
query_urls = defaultdict(set)

with open('text-relevance-competition-ir-1-ts-fall-2019/urls.numerate.txt') as textfile:
    for line in textfile:
        line_lst = line.rstrip().split()
        url_id, url = line_lst[0], ' '.join(line_lst[1:])
        urls.append(url)


with open('text-relevance-competition-ir-1-ts-fall-2019/sample.technosphere.ir1.textrelevance.submission.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader)
    for row in spamreader:
        # print(row[0], row[1], urls[int(row[1])])
        query_urls[int(row[0])].add(urls[int(row[1])])


# anomaly
doc_id_url = defaultdict(str)
group_id_urls = defaultdict(set)

# with open('anomaly_detection/parsing_output_alldescription,doc_id.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     next(spamreader)
#     for row in spamreader:
#         if row:
#             description,doc_id,keywords,site_name,title,url = row[0], row[1], row[2], row[3], row[4], row[5]
#             print(doc_id, url)

all_descr_df = pd.read_csv('anomaly_detection/parsing_output_alldescription,doc_id.csv')

for index, row in all_descr_df.iterrows():
    doc_id_url[row['doc_id']] = row['url'].rstrip()

train_groups = pd.read_csv('anomaly_detection/train_groups.csv')

for index, row in train_groups.iterrows():
    group_id_urls[row['group_id']].add(doc_id_url[row['doc_id']])



#search
for s in query_urls.values():
    if s in group_id_urls.values():
        print('ура')
        

from urllib.parse import urlparse
from urllib.parse import unquote
from pprint import pprint as pp
from collections import defaultdict
from transliterate import translit, get_available_language_codes
from bs4 import BeautifulSoup
import requests
import random
import pickle
import pandas as pd
import time
import maru
import sys


urls = [
	'travmhelp.ru/stati/pervaya-pomoshch-pri-razryve-svyazok',
	'megapredmet.ru/1-35210.html',
	'facebook.com/pages/%D0%A2%D1%83%D1%80%D0%BC%D0%B0%D0%BB%D0%B8%D0%BD%D0%BE%D0%B2%D0%B0%D1%8F-%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%86%D0%B8%D1%8F/294560463970429',
	'forum.materinstvo.ru/lofiversion/index.php/t55523-1550.html',
	'eva.ru/kids/messages-2043571.htm',
	'cow-leech.ru/docs/index-1426.html?page=5',
]

def splitter(sent, seps = ['.', '-', '_', '&', '+']):
	for sep in seps:
		sent = ' '.join(sent.split(sep))
	sent = sent.lower()
	sent = sent.split(' ') 
	# if type(sent) != list:
	# 	sent = [].append(sent)
	return sent

def transform_url(url_id, url):
	eng_res = []
	result = []
	q = urlparse(url).query
	path = urlparse(url).path
	if urlparse(url).query:
		splitted_query = q.split('=')
		for term in splitted_query:
			perc_freq = term.count("%")/(len(term)+1)
			if perc_freq > (0.1):
				unquoted_q = unquote(term)  #########
				# result += splitter(unquoted_q) !
				# print('unquoted_q:', splitter(unquoted_q))
			elif '-' in term or '_' in term:
				tmp_lst = splitter(term)
				# get_freq_vocab(tmp_lst)
				filtered = [s for s in tmp_lst if s not in bad_words]
				eng_res += filtered
				transited_lst = [translit(s, 'ru') for s in filtered]
				result += transited_lst 
			else:
				pass
				# result += splitter(term) !
				# print('ELSE Q:', splitter(term))
	if path:
		splitted_path = path.split('/')
		# result += [splitted_path[0]] !
		for term in splitted_path[1:]:
			perc_freq = term.count("%")/(len(term)+1)
			if perc_freq > (0.1):
				unquoted_path = unquote(term)
				# result += splitter(unquoted_path) !
				# print('unquoted_path:', splitter(unquoted_path))
			elif '-' in term or '_' in term:
				tmp_lst = splitter(term)
				# get_freq_vocab(tmp_lst)
				filtered = [s for s in tmp_lst if s not in bad_words]
				eng_res += filtered
				transited_lst = [translit(s, 'ru') for s in filtered]
				result += transited_lst 
			else:
				pass
				# result += splitter(term)!
				# print('term:', splitter(term))
	url_for_google = ' '.join(eng_res)
	if not url_for_google:
		checked = "не отправлен в гугл"
	elif len(eng_res) > 10:
		checked = ''
		block_size = 7
		subqueries = [eng_res[i: i + block_size] for i in range(0, len(eng_res), block_size)]
		for subquery in subqueries:
			short_for_google = ' '.join(subquery)
			checked += ' ' + spellcheck_by_google(url_id, short_for_google)
	else:
		checked = spellcheck_by_google(url_id, url_for_google)
		if checked == url_for_google:
			url_for_google_translit = ' '.join(result)
			checked = spellcheck_by_google(url_id, url_for_google_translit)

	return checked, eng_res, result



freq_vocab = defaultdict(int)

def get_freq_vocab(term_list):
	for term in term_list:
		freq_vocab[term] += 1


def spellcheck_by_google(idd, query):
	user_agent = random.choice(user_agent_list)
	headers = {'User-Agent': user_agent}

	print('query for google: ', query)
	# print('headers:', headers)
	response = requests.get('https://www.google.com/search?q='+query, headers=headers)
	resp_html = response.text
	soup = BeautifulSoup(resp_html, 'html.parser')
	checked = soup.find(id="fprsl")
	if not checked:
		checked = soup.find(id="gL9Hy")
	# if checked:
	#   checked = checked.find('i')
	if checked:
	    checked = checked.text
	    print('ADDED', idd, file = sys.stderr)
	    uid_checked_url[idd] = checked
	else:
		print("ГУГЛ НЕ ИСПРАВИЛ")
		uid_NOT_checked_url[idd] = checked
		checked = query

	# print(query+ "                         >>->>                     "+ checked if checked else "ГУГЛ НЕ ИСПРАВИЛ " + )
	# print(query+ "                         >>->>                     "+ checked if checked else query, file=sys.stderr)

	time.sleep(random.randint(2,3)/random.randint(4,5))
	return checked



def start():
	with open('text-relevance-competition-ir-1-ts-fall-2019/urls.numerate.txt') as textfile:
		# for url in urls:
		for iteration,line in enumerate(textfile):
			line_lst = line.rstrip().split()
			url_id, url = line_lst[0], ' '.join(line_lst[1:])

			if (int(url_id) in top10_urls or int(url_id) in top20_urls):
				print ('exists in top10_urls or top20_urls')
			elif (int(url_id) in top40_urls):
				if url_id not in uid_checked_url and url_id not in uid_NOT_checked_url:

					checked, eng_res, result = transform_url(url_id, url)

					print("iteration", iteration, file=sys.stderr)
					print('url_id:', url_id)
					print(url, end = '\n')
					print(checked)
					print(checked, file = sys.stderr)
					print(eng_res)
					print(result, end='\n\n\n\n\n\n\n\n\n')
				else:
					print(url_id, 'exists in uid_checked_url or in uid_NOT_checked_url', file = sys.stderr)


			# get_freq_vocab(result)

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

with open('bad_words.pickle', 'rb') as handle:
	bad_words = pickle.load(handle)

# with open('top-10_urls.pickle', 'rb') as handle:
# 	top10_urls = pickle.load(handle)

# with open('top-20_urls.pickle', 'rb') as handle:
# 	top20_urls = pickle.load(handle)

# with open('top-40_urls.pickle', 'rb') as handle:
# 	top40_urls = pickle.load(handle)

url_data = pd.read_csv('clear_url_rang_mail.csv', encoding='utf-8')
url_data = url_data.drop(['Unnamed: 0'], axis=1)

mail_urls = set(url_data.url_id)

# for i in (top10_urls, top20_urls, top40_urls):
# 	print(len(i))

uid_checked_url = dict()
uid_NOT_checked_url = dict()

try:
	with open('uid_checked_url.pickle', 'rb') as handle:
		uid_checked_url = pickle.load(handle)
	with open('uid_NOT_checked_url.pickle', 'rb') as handle:
		uid_NOT_checked_url = pickle.load(handle)
except:
	print('нет файла')

try:
	start()
except:
	with open('uid_checked_url.pickle', 'wb') as handle:
		pickle.dump(uid_checked_url, handle)
		print("сработал ексепт ексепшн, файл дозаписан", file =sys.stderr)
	with open('uid_NOT_checked_url.pickle', 'wb') as handle:
		pickle.dump(uid_NOT_checked_url, handle)

# # print(len(freq_vocab))
# # sorted_freq_vocab = sorted([(count, word) for word, count in freq_vocab.items() if len(word)==3], reverse=True)
# # pp([i[1] for i in sorted_freq_vocab])
# # for i in sorted_freq_vocab:
# # 	print(i[1])

with open('uid_checked_url.pickle', 'wb') as handle:
		pickle.dump(uid_checked_url, handle)

with open('uid_NOT_checked_url.pickle', 'wb') as handle:
		pickle.dump(uid_NOT_checked_url, handle)

# analyzer = maru.get_analyzer(tagger='crf', lemmatizer='pymorphy')
# [' '.join([morph.lemma for morph in analyzed[i] if morph.tag.pos != 'PUNCT']) for i, m in enumerate(analyzed)]


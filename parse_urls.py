from urllib.parse import urlparse
from urllib.parse import unquote
from pprint import pprint as pp
from collections import defaultdict
from transliterate import translit, get_available_language_codes
import maru


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

def transform_url(url):
	result = []
	q = urlparse(url).query
	path = urlparse(url).path
	if urlparse(url).query:
		splitted_query = q.split('=')
		for term in splitted_query:
			perc_freq = term.count("%")/(len(term)+1)
			if perc_freq > (0.1):
				unquoted_q = unquote(term)  #########
				result += splitter(unquoted_q)
				# print('unquoted_q:', splitter(unquoted_q))
			else:
				result += splitter(term)
				# print('ELSE Q:', splitter(term))
	if path:
		splitted_path = path.split('/')
		for term in splitted_path:
			perc_freq = term.count("%")/(len(term)+1)
			if perc_freq > (0.1):
				unquoted_path = unquote(term)
				result += splitter(unquoted_path)
				# print('unquoted_path:', splitter(unquoted_path))
			else:
				result += splitter(term)
				# print('term:', splitter(term))
	return result

freq_vocab = defaultdict(int)

def get_freq_vocab(term_list):
	for term in term_list:
		freq_vocab[term] += 1

# pp(urls)
# print()


with open('text-relevance-competition-ir-1-ts-fall-2019/urls.numerate.txt') as textfile:
	for url in urls:
	# for line in textfile:
		# line_lst = line.rstrip().split()
		# url_id, url = line_lst[0], ' '.join(line_lst[1:])

		result = transform_url(url)

		print(url, end = '\n\n')
		print(result, end='\n\n\n\n\n\n\n\n\n')

		# get_freq_vocab(result)


# print(len(freq_vocab))
# sorted_freq_vocab = sorted([(count, translit(word, 'ru')) for word, count in freq_vocab.items() if len(word) >= 4], reverse=True)
# pp(sorted_freq_vocab)



analyzer = maru.get_analyzer(tagger='crf', lemmatizer='pymorphy')
# [' '.join([morph.lemma for morph in analyzed[i] if morph.tag.pos != 'PUNCT']) for i, m in enumerate(analyzed)]
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import random
import requests
import pickle
import sys
import re
import pprint as pp
from urllib.parse import urlparse
import time


def make_urls_dict(urls):
    with open('../text-relevance-competition-ir-1-ts-fall-2019/urls.numerate.txt') as textfile:
        for line in textfile:
            line_lst = line.rstrip().split()
            url_id, url = line_lst[0], ' '.join(line_lst[1:])
            path = urlparse(url).path
            path = path if not path.endswith('/') else path[:-1]
            urls[path] = int(url_id)

def spellcheck_by_google():
    with open('text-relevance-competition-ir-1-ts-fall-2019/queries.numerate.txt') as queries_file:
        for line in queries_file:
            line_lst = line.rstrip().split()
            query_id, query = line_lst[0], ' '.join(line_lst[1:])
            queries_dict[query_id].append(query)
            response = requests.get('https://www.google.com/search?q='+query, headers=headers)
            resp_html = response.text
            soup = BeautifulSoup(resp_html, 'html.parser')
            checked = soup.find(id="scl")
            # if checked:
            #   checked = checked.find('i')
            if checked:
                checked = checked.text
                queries_dict[query_id].append(checked)

            print(i, query+ "                         >>->>                     "+ checked if checked else query)
            print(i, query+ "                         >>->>                     "+ checked if checked else query, file=sys.stderr)
            i += 1
            time.sleep(random.randint(2,7)/random.randint(1,5))
            

    with open('checked_queries_by_google.pickle', 'wb') as handle:
        pickle.dump(queries_dict, handle)

def get_mailru_rate():
    try:
        global NNN
        global START
        global DELAY_FROM
        global DELAY_TO
        global proxy
        print('here:', NNN, START)


        with open('../text-relevance-competition-ir-1-ts-fall-2019/queries.numerate.txt') as queries_file:
            for line in queries_file:
                user_agent = random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}

                if NNN >= START:
                    print(line)
                    line_lst = line.rstrip().split()
                    query_id, query = line_lst[0], ' '.join(line_lst[1:])

                    if query_id not in query_id__list_of_uid_url_rate:
                        print(NNN, file = sys.stderr)
                        print(headers, file = sys.stderr)
                        site_url = 'https://go.mail.ru/search?q='
                        site_url = 'http://localhost/'
                        response = requests.get(site_url+query, headers=headers, proxies={"http": proxy, "https": proxy})
                        resp_html = response.text
                        
                        soup = BeautifulSoup(resp_html, 'html.parser')
                        # pattern = re.compile('"go.dataJson = \"(.*?)\";"') 
                        pattern = re.compile('"orig_url":"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?') 
                        results = pattern.findall(soup.text)
                        results = [''.join(i[1:]) for i in results if not (i[-1].endswith('.jpg') or i[-1].endswith('.gif') or i[-1].endswith('.png'))      ]
                        results = [res if not res.startswith('www.') else res[4:] for res in results]
                        results = [res if not res.endswith('/') else res[:-1] for res in results]
                        results = [res if not 'wikibit' in res else res.replace('wikibit.site', 'wikibit.me') for res in results]
                        query_id__list_of_mail_urls[query_id] = results

                        results = [urlparse(res).path for res in results]
                        if not results:
                            print("Подождем пару минут", file=sys.stderr)
                            time.sleep(120)
                        else:
                            good_results = [(our_urls_paths_slash[res],res,rate) for rate,res in enumerate(results) if res in our_urls_paths_slash]

                            query_id__list_of_uid_url_rate[query_id] = good_results

                            print(query)
                            print(query, file = sys.stderr)

                            pp.pprint(results)
                            pp.pprint(results, sys.stderr)

                            print()
                            print(file=sys.stderr)

                            pp.pprint(good_results)
                            pp.pprint(good_results, sys.stderr)

                            print('\n\n\n')
                            print('\n\n\n', file = sys.stderr)

                            time.sleep(random.randint(DELAY_FROM, DELAY_TO))
                    else:
                        print(NNN, 'exists', file = sys.stderr)
                
                else:
                    pass

                NNN += 1


                

        with open('query_id__list_of_uid_url_rate.pickle', 'wb') as handle:
          pickle.dump(query_id__list_of_uid_url_rate, handle)

        with open('query_id__list_of_mail_urls.pickle', 'wb') as handle:
          pickle.dump(query_id__list_of_mail_urls, handle)
    except:
        with open('query_id__list_of_uid_url_rate.pickle', 'wb') as handle:
          pickle.dump(query_id__list_of_uid_url_rate, handle)


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

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

query_id__list_of_uid_url_rate = defaultdict(list)

try:
    with open('query_id__list_of_uid_url_rate.pickle', 'rb') as handle:
        query_id__list_of_uid_url_rate = pickle.load(handle)
        print('query_id__list_of_uid_url_rate.pickle loaded, len = ', len(query_id__list_of_uid_url_rate), file = sys.stderr)
except:
    print('нет файла')



our_urls_paths_slash = dict()
make_urls_dict(our_urls_paths_slash)

queries_dict = defaultdict(list)

proxy = None



NNN = 1
DELAY_FROM = 30
DELAY_TO = 120
START = 1

# query_id__list_of_uid_url_rate.pickle = defaultdict(list)
query_id__list_of_mail_urls = defaultdict(list)

get_mailru_rate()

# pp.pprint(our_urls_paths_slash)
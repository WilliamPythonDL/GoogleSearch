# GoogleSearch
Google Search Program

/GoogleSearch/Demo/google_search.py
中google_search.py为程序调用演示



## 代理使用演示
PROXIES = [{
    'http': 'http://127.0.0.1:10086',
    'https': 'http://127.0.0.1:10086'
}]

# 调用主程序
# 或者 mg = MainGoogle(PROXIES)
mg = MainGoogle()


# Get {'title','url','text'}
for i in mg.search(query='python', num=1, language='en'):
    pprint.pprint(i)

time.sleep(random.randint(1, 5))


# Get 第一页
for url in mg.search_url(query='python'):
    pprint.pprint(url)

time.sleep(random.randint(1, 5))


# Get 第二页
for url in mg.search_url(query='python', start=10):
    pprint.pprint(url)

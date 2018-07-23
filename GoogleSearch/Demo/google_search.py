import os
import sys
import time
import random
import pprint

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from MainGoogle import MainGoogle


## 代理使用演示
PROXIES = [{
    'http': 'http://127.0.0.1:8118',
    'https': 'http://127.0.0.1:8118'
}]


# 或者 mg = MainGoogle(PROXIES)
mg = MainGoogle()


# Get {'title','url','text'}
for i in mg.search(query='python', num=1, language='en'):
    pprint.pprint(i)

time.sleep(random.randint(1, 5))

# Output
# {'text': 'The official home of the Python Programming Language.',
#  'title': 'Welcome to Python.org',
#  'url': 'https://www.python.org/'}
# {'text': '', 'title': ''}

# Get 第一页
for url in mg.search_url(query='python'):
    pprint.pprint(url)

time.sleep(random.randint(1, 5))

# Output
# 'https://www.python.org/'
# 'https://www.python.org/getit/'
# 'https://www.python.org/about/apps/'
# 'https://www.python.org/about/gettingstarted/'
# 'https://docs.python.org/3/tutorial/'
# 'https://www.python.org/psf/'
# 'https://www.python.org/about/'
# 'https://www.w3schools.com/python/'
# 'https://en.wikipedia.org/wiki/Python_(programming_language)'
# 'https://medium.freecodecamp.org/what-can-you-do-with-python-the-3-main-applications-518db9a68a78'
# 'https://www.codecademy.com/learn/learn-python'
# 'https://www.datacamp.com/courses/intro-to-python-for-data-science'

# Get 第二页
for url in mg.search_url(query='python', start=10):
    pprint.pprint(url)

# Output
# 'https://www.tutorialspoint.com/python/'
# 'https://github.com/python'
# 'https://github.com/python/cpython'
# 'https://hackernoon.com/why-is-python-so-slow-e5074b6fe55b'
# 'https://developers.slashdot.org/story/18/07/20/227246/is-python-the-future-of-programming'
# 'https://www.coursera.org/lecture/python/video-welcome-to-python-guido-van-rossum-NhDlc'
# 'http://www.pplex.ch/home'
# 'https://www.udemy.com/complete-python-bootcamp/'
# 'https://www.edx.org/course/introduction-to-python-absolute-beginner-0'
# 'https://www.geeksforgeeks.org/python-programming-language/'

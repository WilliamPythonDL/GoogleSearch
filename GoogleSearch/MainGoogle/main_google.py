import os
import random
import sys
import time

import cchardet
import requests

from pyquery import PyQuery as pq
from MainGoogle.config import USER_AGENT, DOMAIN, BLACK_DOMAIN, URL_SEARCH, URL_NEXT, URL_NUM, LOGGER

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from urllib import quote_plus
    from urlparse import urlparse, parse_qs


class MainGoogle():

    def __init__(self, proxies=None):
        self.proxies = random.choice(proxies) if proxies else None

    def search(self, query, language=None, num=None, start=0, pause=2):
        """
        获取想过要的信息,例如 title,description,url
        """
        content = self.search_page(query, language, num, start, pause)
        pq_content = self.pq_html(content)
        for item in pq_content('div.g').items():
            result = {}
            result['title'] = item('h3.r>a').eq(0).text()
            href = item('h3.r>a').eq(0).attr('href')
            if href:
                url = self.filter_link(href)
                result['url'] = url
            text = item('span.st').text()
            result['text'] = text
            yield result

    def search_page(self, query, language=None, num=None, start=0, pause=2):
        """
        Google search
        """
        time.sleep(pause)
        domain = self.get_random_domain()
        if start > 0:
            url = URL_NEXT
            url = url.format(
                domain=domain, language=language, query=quote_plus(query), num=num, start=start)
        else:
            if num is None:
                url = URL_SEARCH
                url = url.format(
                    domain=domain, language=language, query=quote_plus(query))
            else:
                url = URL_NUM
                url = url.format(
                    domain=domain, language=language, query=quote_plus(query), num=num)
        if language is None:
            url = url.replace('hl=None&', '')
        # 添加 headers
        headers = {'user-agent': self.get_random_user_agent()}
        try:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            r = requests.get(url=url,
                             proxies=self.proxies,
                             headers=headers,
                             allow_redirects=False,
                             verify=False,
                             timeout=30)
            LOGGER.info(url)
            content = r.content
            charset = cchardet.detect(content)
            text = content.decode(charset['encoding'])
            return text
        except Exception as e:
            LOGGER.exception(e)
            return None

    def search_url(self, query, language=None, num=None, start=0, pause=2):
        """
        获取Google search页面的URL
        """
        content = self.search_page(query, language, num, start, pause)
        pq_content = self.pq_html(content)
        for item in pq_content('h3.r').items():
            href = item('a').attr('href')
            if href:
                url = self.filter_link(href)
                if url:
                    yield url

    def filter_link(self, link):
        """
        如果该链接未产生有效结果，则返回None。
        :return：有效的结果
        """
        try:
            # 有效结果是指向Google域的绝对URL
            # like images.google.com 
            o = urlparse(link, 'http')
            if o.netloc:
                return link
            # 解析隐藏的URL.
            if link.startswith('/url?'):
                link = parse_qs(o.query)['q'][0]
                # 有效结果是指向Google域的绝对URL
                # like images.google.com
                o = urlparse(link, 'http')
                if o.netloc:
                    return link
        # 否则或者出错，返回None。
        except Exception as e:
            LOGGER.exception(e)
            return None

    def pq_html(self, content):
        
        return pq(content)

    def get_random_user_agent(self):

        return random.choice(self.get_data('user_agents.txt', USER_AGENT))

    def get_random_domain(self):

        domain = random.choice(self.get_data('all_domain.txt', DOMAIN))
        if domain in BLACK_DOMAIN:
            self.get_random_domain()
        else:
            return domain

    def get_data(self, filename, default=''):

        root_folder = os.path.dirname(__file__)
        user_agents_file = os.path.join(
            os.path.join(root_folder, 'data'), filename)
        try:
            with open(user_agents_file) as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [default]
        return data

import requests
import codecs
from bs4 import BeautifulSoup as bs
from random import randint

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
           'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.3; rv:98.0) Gecko/20100101 Firefox/98.0',
           'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8'}
           ]

__all__ = ('work_ua', 'dou_ua', 'djinni_co')


def work_ua(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title':title.text, 'url': domain+href,
                                 'description': content, 'company':company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})
    
    return jobs, errors


def dou_ua(url, city=None, language=None):
    jobs = []
    errors = []
    # domain = 'https://jobs.dou.ua'
    # url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'
    if url:
        resp = requests.get(url, headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_list:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class', 'title'})
                        href = title.a['href']
                        cont = li.find('div', attrs={'class', 'sh-info'})
                        content = cont.text
                        company = 'No name'
                        a = title.find('a', attrs={'class', 'company'})
                        if a:
                            company = a.text
                        jobs.append({'title': title.text, 'url': href,
                                     'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


def djinni_co(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    if url:
        # url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'
        resp = requests.get(url, headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class', 'list-jobs'})
            if main_ul:
                li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                for li in li_list:
                    title = li.find('div', attrs={'class', 'list-jobs__title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class', 'list-jobs__description'})
                    content = cont.p.text
                    company = 'No name'
                    comp = li.find('div', attrs={'class', 'list-jobs__details__info'})
                    if comp:
                        company = comp.text
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})
    return jobs, errors


if __name__=='__main__':
    url='https://djinni.co/jobs/keyword-python/kyiv/'
    jobs, errors = djinni_co(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()

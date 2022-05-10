import codecs

from scraping.parsers import *

parsers = ((work_ua, 'https://www.work.ua/ru/jobs-kyiv-python'),
           (dou_ua, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'),
           (djinni_co, 'https://djinni.co/jobs/keyword-python/kyiv/')
           )

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e


h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()

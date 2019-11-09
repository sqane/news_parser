from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import datetime
from superparser import models
from django.shortcuts import render, HttpResponse, redirect

def index(request):
    context = {}
    context['news'] = models.News.objects.all()
    return render(request,
                  'index.html',
                  context)

def parse_news(request):
    news = models.News.objects.all()
    for each in news:
        each.delete()
    i = 1
    data = {}
    do_next = True
    while do_next != False :
        site = requests.get('https://pasmi.ru/cat/news/page/'+str(i)+'/')
        html = site.text
        soup = BeautifulSoup(html,features='html.parser')
        otbor = soup.select(".entry-title")
        if otbor.__len__() == 0:
            do_next = False
            break
        for each in otbor:
            site1 = requests.get(each.attrs['href'])
            print(each.attrs['href'])
            soup1 = BeautifulSoup(site1.text,features='html.parser')
            body = soup1.select(".entry-content .content")
            body1 = body[0]
            time = soup1.select(".info .time")
            time1 = time[0].text
            date = datetime.datetime.strptime(time1,'%d.%m.%Y / %H:%M')
            [s.extract() for s in body1('script')]
            n = models.News()
            n.name = each.text
            n.body = body1.text
            n.date_added = date
            n.save()
            # /data[str(i)+str(each.sourceline)] = {'name':each.text,'body':body1.text,'date_added':date}
        i = i+1
    return HttpResponse('ok')


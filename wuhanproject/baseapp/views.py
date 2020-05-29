import feedparser
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.db import transaction, IntegrityError
import uuid

from django.utils.timezone import now, timedelta

# Create your views here.
from baseapp.models import *

from django.urls import reverse
from django.shortcuts import render

from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
import requests
# from isodata import parse_duration
from django.conf import settings

import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import ast
import json
from pyvirtualdisplay import Display
import os

from django.utils.timezone import localdate
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from ipware import get_client_ip
from geoip import geolite2

from datetime import datetime
import dateutil.parser

from forum.models import Post


def home(request):
    if request.method == "GET":
        # client_ip, is_routable = get_client_ip(request)
        client_ip = '81.169.181.179'
        country_code = None
        if client_ip is None:
            pass
        # Unable to get the client's IP address
        else:
            # print(get_client_ip(request))
            match = geolite2.lookup(client_ip)
            if match is not None:
                get_code = match.country
                try:
                    country_code = CountryCode.objects.get(code=get_code)
                except Exception as e:
                    print(e)
                    pass

                # print(match.country)# 'US'
                # print(match.continent)# 'NA'
                # print(match.timezone)# 'America/Los_Angeles'
                # print(match.subdivisions)
                # print(frozenset(['CA']))
            # We got the client's IP address
            # if is_routable:
            #     pass
            # # The client's IP address is publicly routable on the Internet
            # else:
            #     pass
        # The client's IP address is private

        date_flag = DateFlag.objects.last()
        country_item = None
        world_item = None
        all_country_item = CountryItem.objects.filter(date_flag=date_flag).order_by('-confirmed', '-death',
                                                                                    'country_code__english')
        all_country_item_chart = CountryItem.objects.filter(date_flag=date_flag).order_by('-confirmed', '-death',
                                                                                          'country_code__english')

        cnn_item = BBCItem.objects.all().order_by('-created')[:5]
        youtube_item = YoutubeItem.objects.all().order_by('-created')[:5]

        if country_code is not None:
            try:
                country_item = CountryItem.objects.get(country_code=country_code, date_flag=date_flag)
            except Exception as e:
                print(e)

        try:
            world_item = WorldItem.objects.get(date_flag=date_flag)
        except Exception as e:
            print(e)

        posts = Post.objects.filter(featured=True).order_by('-date_published').all()[:1]
        all_usa_item = USAStateItem.objects.filter(date_flag=date_flag).order_by('-confirmed', '-death',
                                                                                 'usa_state_code__english')

        if country_code is not None and country_code.code == "US":
            all_usa_item = USAStateItem.objects.filter(date_flag=date_flag).order_by('-confirmed', '-death',
                                                                                     'usa_state_code__english')

            return render(request, 'baseapp/home_usa.html', {'country_item': country_item,
                                                             'all_usa_item': all_usa_item,
                                                             'all_country_item': all_country_item,
                                                             'all_country_item_chart': all_country_item_chart,
                                                             'world_item': world_item,
                                                             'cnn_item': cnn_item,
                                                             'posts': posts})

        elif country_code is not None and country_code == "DE":
            all_germany_item = GermanyStateItem.objects.filter(date_flag=date_flag).order_by('-confirmed', '-death',
                                                                                 'germany_state_code__german')

            return render(request, 'baseapp/home_germany.html', {'country_item': country_item,
                                                             'all_germany_item': all_germany_item,
                                                             'all_country_item': all_country_item,
                                                             'all_country_item_chart': all_country_item_chart,
                                                             'world_item': world_item,
                                                             'cnn_item': cnn_item,
                                                             'posts': posts})



        # us 일 경우 home 아이콘 배치를 어떻게할까
        # dateflag 고려해서 데이터 받기.
        return render(request, 'baseapp/home.html', {'country_item': country_item,
                                                     'all_country_item': all_country_item,
                                                     'all_country_item_chart': all_country_item_chart,
                                                     'world_item': world_item,
                                                     'cnn_item': cnn_item,
                                                     'youtube_item': youtube_item,
                                                     'posts': posts})
    else:
        return render(request, 'baseapp/home.html')


def news(request):
    if request.method == "GET":

        cnn_item = BBCItem.objects.all().order_by('-created')[:50]

        return render(request, 'baseapp/news.html', {'cnn_item': cnn_item, })
    else:
        return render(request, 'baseapp/news.html')


def chart(request):
    if request.method == "GET":
        client_ip, is_routable = get_client_ip(request)
        country_code = None
        if client_ip is None:
            pass
        # Unable to get the client's IP address
        else:
            # print(get_client_ip(request))
            match = geolite2.lookup(client_ip)
            if match is not None:
                get_code = match.country
                try:
                    country_code = CountryCode.objects.get(code=get_code)
                except Exception as e:
                    print(e)
                    pass

        date_flag = DateFlag.objects.last()
        country_item = None
        world_item = None
        all_country_item = CountryItem.objects.filter(date_flag=date_flag).order_by('-confirmed', '-death',
                                                                                    'country_code__english').all()

        cnn_item = BBCItem.objects.all().order_by('-created')[:5]

        if country_code is not None:
            try:
                country_item = CountryItem.objects.get(country_code=country_code, date_flag=date_flag)
            except Exception as e:
                print(e)

        try:
            world_item = WorldItem.objects.get(date_flag=date_flag)
        except Exception as e:
            print(e)

        posts = Post.objects.filter().order_by('-date_published').all()[:1]

        return render(request, 'baseapp/chart.html', {'country_item': country_item,
                                                      'all_country_item': all_country_item,
                                                      'world_item': world_item,
                                                      'cnn_item': cnn_item,
                                                      'posts': posts})
    else:
        return render(request, 'baseapp/chart.html')


YOUTUBE_DATA_API_KEY = 'AIzaSyDAOuwrMiVMDaRxcKBGATckFTjrYlgHSGA'  # youtube api key. 민구야 발급 받는 게 좋을 듯?


@csrf_exempt
def update_bbc(request):
    if request.method == "POST":

        payload = json.loads(
            request.body.decode('utf-8'))

        token = payload["token"]
        if not token == settings.OXIBUG_TOKEN:
            return JsonResponse({"data": "failed"}, safe=False)

        url = "http://feeds.bbci.co.uk/news/rss.xml"  # Getting URL
        feed = feedparser.parse(url)  # Parsing XML data

        ids = BBCItem.objects.order_by("-pk").values_list("pk", flat=True)[:100]
        BBCItem.objects.exclude(pk__in=list(ids)).delete()

        try:
            with transaction.atomic():

                for item in feed["entries"]:
                    if 'Corona' in str(item["title"]):

                        a = str(item["description"])[:str(item["description"]).find("<img src=")]
                        cnn_item_created, created = BBCItem.objects.get_or_create(url=item['link'])
                        if created:
                            cnn_item_created.title = item["title"]
                            cnn_item_created.published_date = item["published"]
                            cnn_item_created.content = a
                            cnn_item_created.url = item['link']

                            django_date = datetime. \
                                strptime(item["published"], '%a, %d %b %Y %H:%M:%S %Z'). \
                                strftime('%Y-%m-%dT%H:%M:%S.000Z')
                            cnn_item_created.published_date_raw = dateutil.parser.parse(django_date)
                            cnn_item_created.save()

        except Exception as e:
            print(e)
            return JsonResponse({"data": "failed"}, safe=False)

        return JsonResponse({"data": "success"}, safe=False)

    else:
        return render(request, 'baseapp/home.html')


@csrf_exempt
def update_country(request):
    if request.method == "POST":
        # print("data: "+str(request.POST.form))
        # get_data = request.POST.get("oxibug1905", None)
        # print(get_data)

        # type(get_data)
        # print(request.POST.get("haha", None))
        # print(request.POST)
        # print(request.POST.dict())
        # print(str(request.POST.dict()))

        payload = json.loads(
            request.body.decode('utf-8'))
        # print(str(payload) + "gogo")
        token = payload["token"]
        if not token == settings.OXIBUG_TOKEN:
            return JsonResponse({"data": "token failed"}, safe=False)

        import pandas as pd

        data = pd.DataFrame(payload['world'])

        country = data['Country/Region'].to_list()  # 열 이름: Country/Region
        confirmed = data['Confirmed Cases'].to_list()  # 열 이름: Confirmed Cases
        deaths = data['Deaths'].to_list()  # 열 이름: Deaths
        recovered = data['Recovered'].to_list()  # 열 이름: Recovered
        iso = data['ISO'].to_list()  # 열 이름: ISO

        try:
            with transaction.atomic():

                date_flag_create = DateFlag.objects.create()

                confirmed_count = 0
                deaths_count = 0
                recovered_count = 0

                for item in range(len(country)):
                    confirmed_count = confirmed_count + int(confirmed[item])
                    deaths_count = deaths_count + int(deaths[item])
                    recovered_count = recovered_count + int(recovered[item])

                    country_code, created = CountryCode.objects.get_or_create(code=iso[item])
                    country_code.english = country[item]
                    country_code.save()

                    country_item_create = CountryItem.objects.create(date_flag=date_flag_create,
                                                                     country_code=country_code,
                                                                     confirmed=int(confirmed[item]),
                                                                     death=int(deaths[item]),
                                                                     recovered=int(recovered[item]),
                                                                     death_rate=round(
                                                                         deaths[item] / confirmed[item] * 100,
                                                                         2))

                world_item_create = WorldItem.objects.create(date_flag=date_flag_create,
                                                             country_count=int(str(len(country))),
                                                             confirmed=int(str(confirmed_count)),
                                                             death=int(str(deaths_count)),
                                                             recovered=int(str(recovered_count)),
                                                             death_rate=round(deaths_count / confirmed_count * 100, 2))

                data_usa = pd.DataFrame(payload['USA'])
                country_usa = data_usa['USAState'].to_list()  # 열 이름: Country/Region
                confirmed_usa = data_usa['Confirmed Cases'].to_list()  # 열 이름: Confirmed Cases
                deaths_usa = data_usa['Deaths'].to_list()  # 열 이름: Deaths
                recovered_usa = data_usa['Recovered'].to_list()  # 열 이름: Recovered
                iso_usa = data_usa['short'].to_list()  # 열 이름: ISO
                print(country_usa)
                print(iso_usa)
                confirmed_count_usa = 0
                deaths_count_usa = 0
                recovered_count_usa = 0

                etc_index = 0
                for item in range(len(country_usa)):
                    confirmed_count_usa = confirmed_count_usa + int(confirmed_usa[item])
                    deaths_count_usa = deaths_count_usa + int(deaths_usa[item])
                    recovered_count_usa = recovered_count_usa + int(recovered_usa[item])
                    short_usa = iso_usa[item]
                    print(short_usa)

                    if str(iso_usa[item]) == "etc":
                        etc_index += 1
                        short_usa = short_usa + str(etc_index)
                        print("modi: " + short_usa)
                    country_code_usa, created = USAStateCode.objects.get_or_create(code=short_usa)
                    country_code_usa.english = country_usa[item]
                    country_code_usa.save()

                    usa_item_create = USAStateItem.objects.create(date_flag=date_flag_create,
                                                                  usa_state_code=country_code_usa,
                                                                  confirmed=int(confirmed_usa[item]),
                                                                  death=int(deaths_usa[item]),
                                                                  recovered=int(recovered_usa[item]),
                                                                  death_rate=round(
                                                                      deaths_usa[item] / confirmed_usa[item] * 100,
                                                                      2))

                data_germany = pd.DataFrame(payload['Germany'])
                country_germany = data_germany['GermanyState'].to_list()  # 열 이름: Country/Region
                confirmed_germany = data_germany['Confirmed Cases'].to_list()  # 열 이름: Confirmed Cases
                deaths_germany = data_germany['Deaths'].to_list()  # 열 이름: Deaths
                recovered_germany = data_germany['Recovered'].to_list()  # 열 이름: Recovered
                iso_germany = data_germany['short'].to_list()  # 열 이름: ISO
                print(country_germany)
                print(iso_germany)
                confirmed_count_germany = 0
                deaths_count_germany = 0
                recovered_count_germany = 0

                etc_index = 0
                for item in range(len(country_germany)):
                    confirmed_count_germany = confirmed_count_germany + int(confirmed_germany[item])
                    deaths_count_germany = deaths_count_germany + int(deaths_germany[item])
                    recovered_count_germany = recovered_count_germany + int(recovered_germany[item])
                    short_germany = iso_germany[item]
                    print(short_germany)

                    if str(iso_germany[item]) == "etc":
                        etc_index += 1
                        short_germany = short_germany + str(etc_index)
                        print("modi: " + short_germany)
                    country_code_germany, created = GermanyStateCode.objects.get_or_create(code=short_germany)
                    country_code_germany.german = country_germany[item]
                    country_code_germany.save()

                    germany_item_create = GermanyStateItem.objects.create(date_flag=date_flag_create,
                                                                  germany_state_code=country_code_germany,
                                                                  confirmed=int(confirmed_germany[item]),
                                                                  death=int(deaths_germany[item]),
                                                                  recovered=int(recovered_germany[item]),
                                                                  death_rate=round(
                                                                      deaths_germany[item] / confirmed_germany[item] * 100,
                                                                      2))


        except Exception as e:
            print(e)
            return JsonResponse({"data": "failed"}, safe=False)

        return JsonResponse({"data": "success"}, safe=False)
    else:
        return render(request, 'baseapp/home.html')



# @csrf_exempt
# def update_us(request):
#     if request.method == "POST":

#         payload = json.loads(
#             request.body.decode('utf-8'))
#         token = payload["token"]
#         if not token == settings.OXIBUG_TOKEN:
#             return JsonResponse({"data": "token failed"}, safe=False)

#         import pandas as pd
#         data = pd.DataFrame(payload)

#         country = data['USAState'].to_list()  # 열 이름: Country/Region
#         confirmed = data['Confirmed Cases'].to_list()  # 열 이름: Confirmed Cases
#         deaths = data['Deaths'].to_list()  # 열 이름: Deaths
#         recovered = data['Recovered'].to_list()  # 열 이름: Recovered
#         iso = data['ISO'].to_list()  # 열 이름: ISO

#         try:
#             with transaction.atomic():

#                 date_flag_create = USADateFlag.objects.create()

#                 confirmed_count = 0
#                 deaths_count = 0
#                 recovered_count = 0

#                 for item in range(len(country)):
#                     confirmed_count = confirmed_count + int(confirmed[item])
#                     deaths_count = deaths_count + int(deaths[item])
#                     recovered_count = recovered_count + int(recovered[item])

#                     code, created = USAStateCode.objects.get_or_create(code=iso[item])
#                     code.english = country[item]
#                     code.save()

#                     country_item_create = USAStateItem.objects.create(date_flag=date_flag_create,
#                                                                       country_code=code,
#                                                                       confirmed=int(confirmed[item]),
#                                                                       death=int(deaths[item]),
#                                                                       recovered=int(recovered[item]),
#                                                                       death_rate=round(
#                                                                           deaths[item] / confirmed[item] * 100,
#                                                                           2))

#                 world_item_create = WorldItem.objects.create(date_flag=date_flag_create,
#                                                              country_count=int(str(len(country))),
#                                                              confirmed=int(str(confirmed_count)),
#                                                              death=int(str(deaths_count)),
#                                                              recovered=int(str(recovered_count)),
#                                                              death_rate=round(deaths_count / confirmed_count * 100, 2))
#         except Exception as e:
#             print(e)
#             return JsonResponse({"data": "failed"}, safe=False)

#         return JsonResponse({"data": "success"}, safe=False)
#     else:
#         return render(request, 'baseapp/home.html')


@csrf_exempt
def update_youtube(request):
    if request.method == "POST":
        # print("data: "+str(request.POST.form))
        # get_data = request.POST.get("oxibug1905", None)
        # print(get_data)

        # type(get_data)
        # print(request.POST.get("haha", None))
        # print(request.POST)
        # print(request.POST.dict())
        # print(str(request.POST.dict()))

        ids = YoutubeItem.objects.order_by("-pk").values_list("pk", flat=True)[:20]
        YoutubeItem.objects.exclude(pk__in=list(ids)).delete()

        payload = json.loads(
            request.body.decode('utf-8'))
        # print(str(payload) + "gogo")
        token = payload["token"]
        if not token == settings.OXIBUG_TOKEN:
            return JsonResponse({"data": "token failed"}, safe=False)

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': 'corona',  # 검색어: corona
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 5,  # 불러올 비디오 갯수: 5개
            'type': 'video',
            'relevanceLanguage': 'en',
            'location': "51.509865,-0.118092",
            'locationRadius': '1000km',
            'regionCode': 'GB'
        }
        video_ids = []

        r = requests.get(search_url, params=search_params)

        print(r.json())

        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])
        print("video_ids:" + str(video_ids))

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 5,
        }
        print("video_params:" + str(video_params))
        r = requests.get(video_url, params=video_params)

        results = r.json()['items']
        print("results:" + str(results))

        videos = []

        try:
            with transaction.atomic():

                for result in results:
                    print("result" + str(result))
                    youtube_item_created, created = YoutubeItem.objects.get_or_create(video_id=result['id'])
                    if created:
                        # youtube_item_created.update(video_id=result['id'],
                        #                             url=f'https://www.youtube.com/watch?v={ result["id"] }',
                        #                             title=result['snippet']['title'],
                        #                             channel_title=result['snippet'][
                        #                                 'channelTitle'],
                        #                             description=result['snippet']['description'],
                        #                             published_date=result['snippet'][
                        #                                 'publishedAt'],
                        #                             published_date_raw=result['snippet'][
                        #                                 'publishedAt'],
                        #                             thumbnail=
                        #                             result['snippet']['thumbnails']['high'][
                        #                                 'url'])

                        youtube_item_created.url = f'https://www.youtube.com/watch?v={ result["id"] }'
                        youtube_item_created.title = result['snippet']['title']
                        youtube_item_created.channel_title = result['snippet']['channelTitle']
                        youtube_item_created.description = result['snippet']['description']
                        youtube_item_created.published_date = result['snippet']['publishedAt']
                        youtube_item_created.published_date_raw = result['snippet']['publishedAt']
                        youtube_item_created.thumbnail = result['snippet']['thumbnails']['high']['url']
                        youtube_item_created.save()

                return JsonResponse({"data": "success"}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"data": "failed"}, safe=False)

    else:
        return render(request, 'baseapp/home.html')


def add_post(request):
    if request.method == "GET":
        client_ip, is_routable = get_client_ip(request)
        country_code = None
        if client_ip is None:
            pass
        # Unable to get the client's IP address
        else:
            # print(get_client_ip(request))
            match = geolite2.lookup(client_ip)
            if match is not None:
                get_code = match.country
                try:
                    country_code = CountryCode.objects.get(code=get_code)
                except Exception as e:
                    print(e)
                    pass

        return render(request, 'baseapp/home.html', {'country_item': country_item,
                                                     'all_country_item': all_country_item,
                                                     'world_item': world_item,
                                                     'cnn_item': cnn_item,
                                                     'youtube_item': youtube_item})
    else:
        return render(request, 'baseapp/home.html')


def crawl_on_linux(request):
    if request.method == "GET":

        webdriver_path = r'chromedriver_linux64\chromedriver'  # path
        os.environ['webdriver.chrome.driver'] = webdriver_path
        display = Display(visible=0, size=(800, 600))
        display.start()

        with open('language_dict.txt', 'r', encoding='utf-8') as f:  # language_dict.txt에 저장된 {언어: {중국어: 영어}} 불러오기.
            language_dict = json.loads(f.read())

        # while True:
        #    time.sleep(60 * 30)  # 30분 쉰다
        '''
        중국 자료를 크롤링
        '''
        china_url = r'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0'
        # browser = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options,
        #                           service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        browser = webdriver.Chrome(executable_path=webdriver_path)

        browser.get(china_url)
        time.sleep(5)
        soup_china = BeautifulSoup(browser.page_source, 'html.parser')

        ####### 중국을 제외한 나라들의 데이터
        out_china_text = soup_china.find('script', id='getListByCountryTypeService2').text
        json_start = out_china_text.find('[')
        json_end = out_china_text.rfind(']')

        out_china = ast.literal_eval(out_china_text[json_start:json_end + 1])
        out_china = pd.DataFrame(out_china)
        out_china = out_china[['provinceName', 'confirmedCount', 'deadCount', 'curedCount']]
        #######

        ####### 대만, 홍콩, 마카오의 데이터
        in_china_text = soup_china.find('script', id='getListByCountryTypeService1').text
        json_start = in_china_text.find('[')
        json_end = in_china_text.rfind(']')

        in_china = ast.literal_eval(in_china_text[json_start:json_end + 1])
        in_china = pd.DataFrame(in_china)
        in_china = in_china[['provinceName', 'confirmedCount', 'deadCount', 'curedCount']]

        in_but_out_china = ['香港', '台湾', '澳门']  # 홍콩, 대만, 마카오
        in_but_out_china = in_china[in_china['provinceName'].isin(in_but_out_china)]  # 홍콩, 대만, 마카오 데이터만 추출
        #######

        ####### 중국 본토 데이터
        china_text = soup_china.find('script', id='getStatisticsService').text
        json_start = china_text.find('id')
        json_end = china_text.rfind('}catch')

        china = json.loads(china_text[json_start - 2:json_end])
        china = pd.DataFrame([china])
        china = china[['confirmedCount', 'deadCount', 'curedCount']]

        main_china = china - in_but_out_china[['confirmedCount', 'deadCount', 'curedCount']].sum()
        main_china['provinceName'] = '中国'
        main_china = main_china[['provinceName', 'confirmedCount', 'deadCount', 'curedCount']]
        #######

        data = pd.concat([out_china, in_but_out_china, main_china])
        data = data.rename(
            columns={'provinceName': 'Country/Region', 'confirmedCount': 'Confirmed Cases', 'deadCount': 'Deaths',
                     'curedCount': 'Recovered'})  # column name을 존스홉스킨스와 동일하게 변경
        data.sort_values(by='Confirmed Cases', ascending=False, inplace=True)
        data.reset_index(drop=True, inplace=True)

        '''
        영어로 번역. language_dict에 있는지 확인한 후에, 없으면 파파고를 이용하자
        '''
        country = []
        papa_url = r'https://papago.naver.com/?sk=zh-CN&tk=en&st='
        for c in data['Country/Region'].to_list():
            if c in list(language_dict['English'].keys()):
                country.append(language_dict['English'][c])
            else:
                browser.get(papa_url)
                time.sleep(2)
                browser.find_element_by_css_selector('#sourceEditArea textarea').send_keys(c)
                time.sleep(4)
                papa_soup = BeautifulSoup(browser.page_source, 'html.parser')
                country.append(papa_soup.find('div', id='txtTarget').text)

        language_dict['English'] = {}  # language_dict['English']에 새로운 번역 추가
        for c, e in zip(data['Country/Region'].to_list(), country):
            language_dict['English'][c] = e

        language_dict = json.dumps(language_dict, ensure_ascii=False)
        with open('language_dict.txt', 'w', encoding='utf-8') as f:
            print(language_dict, file=f)

        data['Country/Region'] = country

        browser.close()

        #### 서버에서 처리할 데이터 ####
        Country = data['Country/Region'].to_list()  # 열 이름: Country/Region
        Confirmed = data['Confirmed Cases'].to_list()  # 열 이름: Confirmed Cases
        Deaths = data['Deaths'].to_list()  # 열 이름: Deaths
        Recovered = data['Recovered'].to_list()  # 열 이름: Recovered

        return render(request, 'baseapp/home.html')
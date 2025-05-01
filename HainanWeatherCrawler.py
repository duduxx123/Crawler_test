import requests
import pandas
import json
from lxml import etree
import random
import os
import csv

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 ",
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

if __name__ == '__main__':
    url = 'https://www.weather.com.cn/textFC/hainan.shtml'
    headers = {'User-Agent': random.choice(user_agent_list)}
    request = requests.get(url=url,headers=headers)
    request.encoding = 'utf-8'  # 设置网页的编码格式
    text = request.text
    # print(text)
    html = etree.HTML(text)
    data_list = html.xpath('//ul[@class="day_tabs"]/li/text()') # 日期(7天)

    city_res = []
    city_list = html.xpath('//div[@class="lQCity"]/ul/li')
    for city in city_list:
        city_res.append(city.xpath('./a/text()')[0])

    table_list=html.xpath('//div[@class="conMidtab"]')
    final_table_list = list()
    for i in range(len(table_list)):
        final_table_list.append(table_list[i].xpath('./div[@class="conMidtab3"]/table/tr'))

    seven_day_weather = list()
    for table in final_table_list:
        weather_dict_list = list()
        for row in table:
            res = row.xpath('./td/text()')
            fengli = row.xpath('./td/span/text()')

            weather_dict = {
                'city': res[0],
                'day_weather': res[2],
                'eve_weather': res[6],
                'day_temp': res[5],
                'eve_temp': res[-2],
                'day_wind': fengli[0]+fengli[1],
                'eve_wind': fengli[2]+fengli[3],
            }
            weather_dict_list.append(weather_dict)

        print(weather_dict_list)
        seven_day_weather.append(weather_dict_list)

    if os.path.exists('csv_data') == False:
        os.mkdir('csv_data')

    for i in range(len(seven_day_weather)):
        filename = '海南天气'+data_list[i]
        with open(f'csv_data/{filename}.csv', 'w', newline='',encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=seven_day_weather[0][0].keys())
            # 写入表头
            writer.writeheader()
            for row in seven_day_weather[i]:
                writer.writerow(row)











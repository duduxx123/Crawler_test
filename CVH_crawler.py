import requests
import json
from tqdm import tqdm
import random
import csv
import os

'''
2024.7.28 优化了一下代码，新增flag开关
7.31 修复了一下进度条bug，新增图片爬取(有需要手动加上)
2025.4.1 修复了headers不加Referer就无法正确发起请求
'''

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

headers = {
    # 有些网站会检查请求的 Referer 字段，确保请求是从合法的页面跳转而来
    'Referer': 'https://www.cvh.ac.cn/spms/list.php?taxonName=%E7%99%BE%E5%90%88%E7%A7%91',
    'User-Agent': random.choice(user_agent_list),
}


# 你想要查询的关键字保存在name中，也可以创建列表循环运行
# name = 'Amana'
name='百合科'
offset = 30  # 这是页数，第一页0，然后30，60，90。。。每次+30(他一页只显示30条数据)
url = f'https://www.cvh.ac.cn/controller/spms/list.php?&taxonName={name}'
result = []
# res = requests.get(url, headers={'user-agent': random.choice(user_agent_list)}, timeout=10)
res = requests.get(url, headers=headers, timeout=10)
json_data = json.loads(res.text)
print(json_data)
total = json_data['total']
biaoben_list = json_data['rows']
result.append(biaoben_list)
print(f"共找到{total}条数据")
progress_bar = tqdm(total=total,ncols=100)
previous_offset = 0

while total > offset:
    tqdm.write(f"正在爬取第{int(offset / 30) + 1}页数据")
    url = f'https://www.cvh.ac.cn/controller/spms/list.php?&taxonName={name}&offset={offset}'
    res = requests.get(url, headers=headers, timeout=10)
    json_data = json.loads(res.text)
    biaoben_list = json_data['rows']
    result.append(biaoben_list)
    # 计算增量更新
    progress_bar.update(offset - previous_offset)
    previous_offset = offset
    offset += 30
    if offset > total:
        progress_bar.update(total - progress_bar.n)

progress_bar.close()  # 关闭进度条

# 将二维数组转换成一维，合并数据
dic_result_list = sum(result, [])

# print(len(dic_result_list), dic_result_list)

class Biaoben:
    elevation = None

    def __init__(self, collectionID=None, institutionCode=None, chineseName=None
                 , country=None, stateProvince=None, recordedBy=None):
        self.collectionID = collectionID
        self.institutionCode = institutionCode
        if chineseName != '' and chineseName is not None:
            self.chineseName = chineseName
        else:
            self.chineseName = None
        self.url = f'https://www.cvh.ac.cn/spms/detail.php?id={self.collectionID}'
        self.country = country
        self.stateProvince = stateProvince
        self.recordedBy = recordedBy

    def update(self, elevation):
        self.elevation = elevation

    def __str__(self):
        return f'{self.collectionID} | {self.institutionCode} | {self.chineseName} | {self.url}  |  {self.recordedBy}'


def getBiaobenById(id: str):
    url = f'https://www.cvh.ac.cn/controller/spms/detail.php?id={id}'
    res = requests.get(url, headers={'user-agent': random.choice(user_agent_list)}, timeout=10)
    js_data = json.loads(res.text)
    biaoben_info = js_data['rows']
    print(biaoben_info['institution'], biaoben_info['recordedBy']
          , biaoben_info['elevation'], biaoben_info['habitat'],
          biaoben_info['reproductiveCondition'])
    # 如果有详细页才有的参数想封装进去就放进params里面
    params = dict()
    params['elevation'] = biaoben_info['elevation']
    return params


# 获取标本的图片，保存到./csv_data/img目录中
# code参数代表collectionCode，ins参数代表institutionCode，都已经爬下来了可以直接从字典中获取
# 例如：biaoben_info['collectionCode']
def getImg(code : str,ins : str):
    imgUrl=f'https://www.cvh.ac.cn/controller/spms/image.php?institutionCode={ins}&catalogNumber={code}'
    res = requests.get(url=imgUrl,headers={'user-agent' : random.choice(user_agent_list)})
    os.makedirs('csv_data/img',exist_ok=True)
    with open(f'csv_data/img/{ins}{code}.jpg','wb') as file:
        file.write(res.content)


# 封装
flag = False  # 如果想爬取详细页面的信息(比如海拔)就设置为True，开启后速度会比较慢
dic_data_list = list()
for index in dic_result_list:
    bio = Biaoben(index['collectionID'], index['institutionCode']
                  , index['chineseName'], index['country'], index['stateProvince']
                  , index['recordedBy'])
    if flag is True:
        params = getBiaobenById(index['collectionID'])
        bio.update(params['elevation'])
    dic_data_list.append(bio.__dict__)
    print(bio.__dict__)  # 将对象转换为字典


# fieldnames = dic_result_list[0].keys()
fieldnames = dic_data_list[0].keys()
if os.path.exists('csv_data') == False:
    os.mkdir('csv_data')
with open('csv_data/crawler_output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # 写入表头
    writer.writeheader()
    # 写入数据
    for row in dic_data_list:
        writer.writerow(row)


# print("____________________________________________")
# id = 'eb58e795'
# get_biaobenById(id)

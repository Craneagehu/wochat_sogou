import re
import time
import csv
import requests
from lxml import etree


def public_enquiry(keyword):

    params = {
        'type': 1,
        's_from': 'input',
        'query': keyword,
        'ie': 'utf8',
        '_sug_': 'n',
        '_sug_type_': '',
        'page': 1
    }
    #SNUID必须过一段时间进行更换，否则会出现验证码
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'SUV=00F70D23B7433F2A5D52626B4A6A3719; SUID=243E43B71B148B0A5D638CC3000E7CEF; wuid=AAFtzXuDKQAAAAqLFBve1QkAGwY=; CXID=7121293F2655AB558753AA54ED4CDA08; ad=Syllllllll2NYc89lllllVLIvaolllllH1GMJlllll9lllll9klll5@@@@@@@@@@; IPLOC=CN5000; ABTEST=8|1571729912|v1; weixinIndexVisited=1; JSESSIONID=aaa_H3kkY2ZJpgfmIQu1w; PHPSESSID=pemp38nencju4jpc3s91qjs515; SNUID=952A57A31411819AEF2F27B0159541B0; successCount=1|Wed, 23 Oct 2019 02:31:36 GMT; sct=8',
        'Host': 'weixin.sogou.com',
        'Referer': 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=AI%E6%9C%89%E9%81%93&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=8488&sst0=1571797743479&lkt=5%2C1571797736977%2C1571797738121',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }


    while True:
        info = {}
        url = 'https://weixin.sogou.com/weixin'
        res = requests.get(url,headers=headers,params=params)
        res.encoding = 'utf-8'
        e = etree.HTML(res.text)

        pages = len(e.xpath('//*[@id="main"]/div[4]/div[@id="pagebar_container"]/a[contains(@id,"sogou_page_")]'))+1

        tag_p =e.xpath('//ul[@class="news-list2"]//li')
        if tag_p:
            for p in tag_p:
                #公众号名
                title = p.xpath('./div/div[2]/p[1]/a//text()')
                title = ''.join(title)

                #微信号
                wechat_ID = p.xpath('./div/div[2]/p[2]/label/text()')[0]

                #功能介绍
                function_introduction = p.xpath('./dl[1]/dd//text()')
                function_introduction = ''.join(function_introduction) if function_introduction else '没有相关内容'

                #最近文章
                recent_articles = p.xpath('./dl[2]/dd/a/text()')
                recent_articles = recent_articles[0] if recent_articles else '没有相关内容'

                #日期
                time_text = p.xpath('./dl[2]/dd/span//text()')
                if time_text:
                    timestamp = re.findall('\d+',time_text[0])[0]
                    date = time.strftime('%Y-%m-%d',time.localtime(int(timestamp)))

                else:
                    date = ''

                info["title"]=title
                info["wechat_ID"] = wechat_ID
                info["function_introduction"]=function_introduction
                info["recent_articles"] = recent_articles
                info["date"] = date

                rows.append(info)


        else:
            result = '未查到相关公众号'


        if int(params['page']) == pages:
            break

        else:
            params['page'] += 1

    hd = ["title","wechat_ID","function_introduction","recent_articles","date"]
    with open('C:/Users/MSI1/Desktop/weixin-sougou/wechatID.csv','w',newline='') as f:
        f_csv = csv.DictWriter(f, hd)
        f_csv.writeheader()
        f_csv.writerows(rows)



if __name__ =="__main__":
    rows = []
    keyword='AI有道'
    public_enquiry(keyword)


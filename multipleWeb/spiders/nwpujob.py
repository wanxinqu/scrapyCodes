# -*- coding: utf-8 -*-
import scrapy
from multipleWeb.items import nwpujobItem
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

SMTPserver = 'smtp.qq.com'
sender = '1034378945@qq.com'
password = "sxmelvrzgwzebcad"
body_comtent_html = ""

class NwpujobSpider(scrapy.Spider):
    name = 'nwpujob'
    allowed_domains = ['job.nwpu.edu.cn']
    start_urls = [
        'http://job.nwpu.edu.cn/jobInfoList.do?page=1&order=infoPlus.submitTime&sort=desc&filter=%7bstatus%3a1%2cworkType%3a0%7d&ext=0']

    def parse(self, response):
        linklist = response.xpath('//div[@class = "row"]/div')
        print(linklist)
        global body_comtent_html
        # 每页详情信息
        for link in linklist:
            title = link.xpath('h3/a/text()').extract()  # 标题

            # todaydate = time.strftime("%Y-%m-%d")
            todaydate = "2017-07-05"
            item_nwpujob = nwpujobItem()
            if len(title):
                date_link = link.xpath('ul/li/text()').extract()[1].split("：")[1].strip()
                if date_link==todaydate:
                    print("date is same")
                    item_nwpujob['link'] = 'http://job.nwpu.edu.cn' + (link.xpath('h3/a/@href').extract()[0])
                    item_nwpujob['title'] = (link.xpath('h3/a/text()').extract()[0]).strip()
                    item_nwpujob['company'] = (link.xpath('p/strong[1]/text()').extract()[0]).strip()
                    item_nwpujob['company_property'] = (link.xpath('p/strong[3]/text()').extract()[0]).strip()
                    item_nwpujob['industry'] = (link.xpath('p/strong[4]/text()').extract()[0]).strip()
                    item_nwpujob['location'] = link.xpath('p/strong[5]/text()').extract()
                    item_nwpujob['date'] = link.xpath('ul/li/text()').extract()[1].split("：")[1].strip()

                    body_comtent_html =  '<li><a href="' + str(item_nwpujob['link']) + '">' + str(item_nwpujob['title'])+'</a></li>'
                    print("^" * 50)
                    print(body_comtent_html)
                    item_nwpujob['body'] = body_comtent_html

                    yield item_nwpujob



        # 获取翻页链接
        content_link = response.url
        page_num = int(str(content_link).split("page=")[1].split("&")[0])
        print(content_link)
        print(page_num)
        if (page_num < 5):
            new_page_num = page_num + 1
            page_string = "page=" + str(page_num)
            new_page_string = "page=" + str(new_page_num)
            next_page_url = str(content_link).replace(page_string, new_page_string)
            print(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def close(self):
        global body_comtent_html
        subject = u'今日招聘信息一揽子'
        body_html = '<p>小美女：</p><p>早安！</p><p>你感兴趣公司的招聘信息已经整理好！</p>'
        print(body_html)

        msgRoot = MIMEMultipart()
        msgRoot['From'] = Header("大漂亮", 'utf-8')
        msgRoot['To'] = Header('凉皮妹妹', 'utf-8')
        msgRoot['Subject'] = Header(subject, 'utf-8')

        f = open("data_total.txt", "r")
        body_total = f.read()
        body = body_html + body_total

        print(body)
        msgRoot.attach(MIMEText(body, 'html', 'utf-8'))

        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465);
            server.login(sender, password)  # 登录服务器
            server.sendmail(sender, '1034378945@qq.com', msgRoot.as_string())
            server.close()
            print('邮件发送成功')
        except smtplib.SMTPException:
            print('邮件发送失败')
# -*- coding: utf-8 -*-
import scrapy
from multipleWeb.items import yingjieshengItem
import time
import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

SMTPserver = 'smtp.qq.com'
sender = '1034378945@qq.com'
password = "sxmelvrzgwzebcad"
body_comtent_html = ""

class YingjieshengSpider(scrapy.Spider):
    name = 'yingjiesheng'
    allowed_domains = ['bbs.yingjiesheng.com']
    start_urls = ['http://bbs.yingjiesheng.com/forum.php?mod=forumdisplay&fid=542&filter=typeid&typeid=3409']

    def parse(self, response):
        global body_comtent_html
        # todaydate = time.strftime("%Y-%m-%d")

        today_recommandation = response.xpath('//table[@id = "threadlisttableid"]/tbody[2]/tr/th/a/@href').extract()[2]
        recommandation_date = response.xpath('//table[@id = "threadlisttableid"]/tbody[2]/tr/td[2]/em/span/text()').extract()[0].split(' ')[0]


        year = recommandation_date.split("-")[0]
        month = recommandation_date.split("-")[1]
        day = recommandation_date.split("-")[2]
        if len(month)<2:
            month ='0'+month
        if len(day)<2:
            day='0'+day
        test_date=year+'-'+month+'-'+day
        print(test_date)
        test_date="2017-07-20"
        todaydate= "2017-07-20"

        if test_date == todaydate:
            print("same")
            yield scrapy.Request(url=today_recommandation, callback=self.content_page)
        else:
            print("No update in "+ todaydate)

    def content_page(self, response):
        global body_comtent_html

        subject = u'今日招聘信息一揽子'
        body_html = '<p>小美女：</p><p>早安！</p><p>你感兴趣公司的招聘信息已经整理好！</p>'
        print(body_html)

        linklist = response.xpath(
            '//section[@class = "tn-page-ed-type-text ng-scope ng-pristine ng-valid tn-page-editable"]')

        for link in linklist:

            link2 = link.xpath('table/tbody/tr/td')
            for eve_link in link2:
                print("*" * 40)
                print(eve_link.extract())

                item_yingjiesheng = yingjieshengItem()
                location = eve_link.xpath('p/a/span/text()').extract()[0]
                if str(location) == '北京':
                    print('-' * 50)

                    item_yingjiesheng['link'] = eve_link.xpath('p/a/@href').extract()[0]
                    item_yingjiesheng['company'] = eve_link.xpath('p/a/text()').extract()[0]
                    item_yingjiesheng['location'] = eve_link.xpath('p/a/span/text()').extract()[0]

                    body_comtent_html = '<li><a href="' + str(item_yingjiesheng['link']) + '">' + '[北京]' + str(
                        item_yingjiesheng['company']) + '</a></li>'

                    item_yingjiesheng['body'] = body_comtent_html

                    yield item_yingjiesheng



        # msgRoot = MIMEMultipart('related')
        # msgRoot['From'] = Header("大漂亮", 'utf-8')
        # msgRoot['To'] = Header('凉皮妹妹', 'utf-8')
        # msgRoot['Subject'] = Header(subject, 'utf-8')
        #
        # msgAlternative = MIMEMultipart('alternative')
        # msgRoot.attach(msgAlternative)
        # msgText = MIMEText(body, 'html', 'utf-8')
        # msgAlternative.attach(msgText)
        #
        # try:
        #     server = smtplib.SMTP_SSL("smtp.qq.com", 465);
        #     server.login(sender, password)  # 登录服务器
        #     server.sendmail(sender, '1034378945@qq.com', msgRoot.as_string())
        #     server.close()
        #     print('邮件发送成功')
        # except smtplib.SMTPException:
        #     print('邮件发送失败')
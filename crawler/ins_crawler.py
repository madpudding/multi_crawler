__author__ = 'fcj'
# message: ins 头像粉丝数爬虫脚本
# time: 09/11/2019

import csv
import asyncio
from lxml import etree
from pyppeteer import launch

chrome_settings = {
    'view_port': {
        'width': 1920,
        'height': 1080
    },
    'time_out': 0,
    'time_wait': 2000,
    'launch_option': {
        'headless':
            True,
        'args': [
            '--no-sandbox',
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-infobars',
        ],
        'autoClose':
            True,
    },
    'flush_time': 1,
    'click_evaluate': {
        'width': 960.0,
        'height': 540.0,
    },
    'evaluate': 'window.scrollBy(0, document.body.scrollHeight)',
}


def data_select(content, index):
    index += 1
    # pyppeteer 代理设置
    # proxy_pool = ProxyPool()
    # args = chrome_settings['launch_option']['args']
    # chrome_settings['launch_option']['args'] = args.\
    #     append('--proxy-server='+str(proxy_pool.get_proxy()))
    for line in content:
        asyncio.get_event_loop().run_until_complete(
            page_crawler(pro_id=line[0], ins_url=line[1], index=index))


async def page_crawler(pro_id, ins_url, index):
    """start pyppeteer"""
    # {'timeout': 3 * 1000}
    browser = await launch(options=chrome_settings['launch_option'])
    page = await browser.newPage()
    await page.goto(ins_url)
    await asyncio.wait([
        page.waitForNavigation({'timeout': 3 * 1000}),
    ])
    await page.waitFor(chrome_settings['time_wait'])
    content = await page.content()
    await page.close()
    await browser.close()
    page_parser(content, index=index, pid=pro_id)


def page_parser(page_content, index, pid):
    resp = etree.HTML(page_content)
    # xpath 使用requests也可以用，但使用requests会出现莫名错误(得不到正确的网页)
    followers = resp.xpath('//meta[@property="og:description"]/@content')
    head_img = resp.xpath('//meta[@property="og:title"]/@content')
    name = resp.xpathxpath('//meta[@property="og:image"]/@content')

    with open('D:/ins.csv', 'a', encoding="utf-8", newline="") as fw:
        writer = csv.writer(fw)
        if len(followers) > 0 and len(head_img) > 0:
            row = [pid, name[0], head_img[0], followers[0]]
            print(index, row)
            writer.writerow(row)
        else:  # 需要关注才能知道粉丝数
            row = [pid]
            print(index, row)
            writer.writerow(row)


def csv_content():
    with open('D:/ins_url.csv', 'r', encoding="utf-8") as fr:
        reader = csv.reader(fr)
        merchant = []
        for line in reader:
            merchant.append(int(line[0]))
    return merchant


if __name__ == '__main__':
    ind = 0  # 统计次数
    query = csv_content()
    data_select(content=query, index=ind)

import os
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
delay = 1  # 每次请求间隔1秒
requests.packages.urllib3.disable_warnings()  # 忽略警告

# def getChapters(content):
#     url = "https://www.2biqu.com/biqu11646/"
#
#     response = requests.get(url, verify=False)
#     if response.status_code == 200:
#         html_content = response.content
#         soup = BeautifulSoup(html_content, 'lxml')  # 使用 lxml 解析器
#
#         # 将 BeautifulSoup 对象转换为 lxml.etree.Element 对象以便使用 XPath
#         lxml_html = etree.HTML(str(soup))
#
#         # 使用 XPath 选择器获取所有章节链接
#         xpath_expression = '/html/body/div[3]/div[3]/div/div[2]/ul/li/a'
#         chapter_links = lxml_html.xpath(xpath_expression)
#
#         for link in chapter_links:
#             chapter_url =url+link.get('href')
#             chapter_name = link.text
#             print(chapter_url,chapter_name)
#
#
# # //获取正文
# def  getContent(content):
#     url = "https://www.2biqu.com/biqu11646/10945230.html"
#     requests.packages.urllib3.disable_warnings()  # 忽略警告
#     response = requests.get(url, verify=False)
#
#     if response.status_code == 200:
#         # 尝试使用GBK编码解码响应内容
#         html_content = response.content.decode('gbk')
#
#         soup = BeautifulSoup(html_content, 'html.parser')
#
#         # 提取标题
#         title_tag = soup.find('h1', class_='title')  # 假设标题在h1标签中且有特定class
#         novel_title = title_tag.text.strip() if title_tag else None
#
#         # 提取正文内容
#         content_tag = soup.find('div', id='content')  # 假设正文在一个id为'content'的div标签内
#         novel_content = content_tag.get_text().strip() if content_tag else None
#
#         print(novel_title)
#         print(novel_content)

def get_chapters(url_base):
    response = requests.get(url_base, verify=False)
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'lxml')  # 使用 lxml 解析器
        lxml_html = etree.HTML(str(soup))

        xpath_expression = '/html/body/div[3]/div[3]/div/div[2]/ul/li/a'
        xpath_expression2 = '/html/head/title'
        chapter_links = lxml_html.xpath(xpath_expression)
        titlelink= lxml_html.xpath(xpath_expression2)
        chapters = []
        for link in chapter_links:
            chapter_url = url_base + link.get('href')
            chapter_name = link.text
            chapters.append((chapter_url, chapter_name))

        return chapters,titlelink[0].text


def get_content(url):
    time.sleep(delay)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        html_content = response.content.decode('gbk')
        soup = BeautifulSoup(html_content, 'html.parser')

        title_tag = soup.find('h1', class_='title')
        novel_title = title_tag.text.strip() if title_tag else None
        print(novel_title)
        content_tag = soup.find('div', id='content')
        novel_content = content_tag.get_text().strip() if content_tag else None

        return  novel_content


def save_to_txt(directory, novel_title, chapters_content):
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, f'{novel_title}.txt'), 'w', encoding='utf-8') as novel_file:
        novel_file.write(f'目录：\n')
        for chapter_url, chapter_name in chapters_content:
            novel_file.write(f'{chapter_name}\n')

        novel_file.write('\n\n正文：\n')
        for chapter_url, chapter_name in chapters_content:
            chapter_content = get_content(chapter_url)
            novel_file.write(f'【{chapter_url}】\n{chapter_content}\n\n')


def get_robots_txt(url):
    robots_url = f"{url}/robots.txt"
    response = requests.get(robots_url,verify=False)

    if response.status_code == 200:
        # 确保 HTTP 状态码为 200，表示成功获取资源
        print( response.text)
        return response.text
    else:
        return None
if __name__ == '__main__':
    # 使用函数

    url_base = "https://www.2biqu.com/biqu11646/"
    # get_robots_txt('https://www.2biqu.com')
    chapters,title = get_chapters(url_base)

    directory = f'D:\desktop\我的笔记'
    # novel_title, _ = get_content(url_base + chapters[0][0])  # 使用第一章的URL获取小说标题

    chapters_content = [(url, name) for url, name in chapters]

    save_to_txt(directory, title, chapters_content)

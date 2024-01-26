from pathlib import Path

import google.generativeai as genai
import os

from google.api_core.client_options import ClientOptions
import urllib3

# 请替换为您的代理服务器地址和端口
proxy_host = '127.0.0.1'
# proxy_host = '192.168.237.245'
proxy_port = 7890

# 创建一个HTTP代理URL
proxy_url = f'http://{proxy_host}:{proxy_port}'

# 设置代理选项
proxy_opts = {
    'http': proxy_url,
    'https': proxy_url
}

# 设置系统级HTTP代理
# os.environ['HTTP_PROXY'] = proxy_url
# os.environ['HTTPS_PROXY'] = proxy_url

# 配置urllib3的ProxyManager (如果SDK内部使用了urllib3)
http = urllib3.ProxyManager(proxy_url)

genai.configure(api_key='AIzaSyBr2hd9kE1sY47ot06YwEqGeimORE6UwZM')


def chatWiteAi(content):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(content)
    print(response.text)
    return response.text


def createPic(content):
    model = genai.GenerativeModel('gemini-pro-vision')

    cookie_picture = {
        'mime_type': 'image/png',
        'data': Path(r'G:\GJXworkSpace\personal_proj\useAI-flask\googleai\png-images--800.png').read_bytes()
    }
    prompt = "重新画这张图,只保留红色骰子"

    response = model.generate_content(
        contents=[prompt, cookie_picture]
    )
    print(response.text)
    print(response.prompt_feedback)
    print(response.parts)
    print(response.candidates)
    return response.text


if __name__ == '__main__':
    # chatWiteAi("What is the meaning of life?")
    createPic("What is the meaning of life?")
    # for m in genai.list_models():
    #     if 'generateContent' in m.supported_generation_methods:
    #         print(m.name)

import os
import random
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from http import HTTPStatus
import dashscope
import requests
from pathlib import PurePosixPath

dashscope.api_key_file_path = './key'
# 设置环境变量
os.environ['DASHSCOPE_API_KEY'] = 'sk-767e12e040bc43e098b75e52f23be883'


def call_with_messages(messages):
    # messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
    #             {'role': 'user', 'content': '如何做西红柿炒鸡蛋？'}]
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        return response.output.choices[0].message.content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

        return '出现未知错误，切换其他模型试试'


def createPic_messages(prompts):
    # model = "stable-diffusion-xl"
    model = "wanx-v1"
    prompt = "Eagle flying freely in th e blue sky and white clouds"
    if prompts:
        prompt = prompts
    rsp = dashscope.ImageSynthesis.call(model=model,
                                        prompt=prompt,
                                        negative_prompt="garfield",
                                        n=1,
                                        size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
                return result.url
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


if __name__ == '__main__':
    createPic_messages('西门庆暴打镇关西')

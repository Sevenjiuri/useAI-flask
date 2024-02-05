import os
import random
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from http import HTTPStatus
import dashscope
import requests
from pathlib import PurePosixPath
from typing import List
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


def createPic_messages2(prompts: List[str], model: str = "wanx-v1", negative_prompt: str = "garfield",
                       size: str = '1024*1024', save_path='./pic'):
    # 初始化结果字典，用于存放每个提示词对应的图片URL和本地文件路径
    results_dict = {}

    for prompt in prompts:
        rsp = dashscope.ImageSynthesis.call(model=model,
                                            prompt=prompt,
                                            negative_prompt=negative_prompt,
                                            n=1,
                                            size=size)

        if rsp.status_code == HTTPStatus.OK:
            result = rsp.output.results[0]  # 假设每次只生成一张图片

            # 获取文件名并保存图片到指定路径下
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            local_file_path = f'{save_path}/{file_name}'

            with open(local_file_path, 'wb') as f:
                f.write(requests.get(result.url).content)

            # 将提示词和对应的本地文件路径存入结果字典
            results_dict[prompt] = local_file_path
        else:
            print(
                f'Failed for prompt "{prompt}", status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}')

    return results_dict




if __name__ == '__main__':
    # 使用示例：
    prompts = ["portrait of a woman covered in cloud of smoke, whirlwind, pink highlight colors, pink make-up, hints of pastel, misty, seductive, sultry, breathtaking, oil painting style, artistic, aesthetic modern art, hyper-realism"]

    image_results = createPic_messages2(prompts, save_path='./pic')
    for prompt, file_path in image_results.items():
        print(f"Prompt: {prompt} -> Saved Image: {file_path}")

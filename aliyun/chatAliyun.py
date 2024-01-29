import os
import random
from http import HTTPStatus
import dashscope

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


if __name__ == '__main__':
    call_with_messages()

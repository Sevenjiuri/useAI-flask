# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus
import dashscope
import os
dashscope.api_key_file_path='./key'
# 设置环境变量
os.environ['DASHSCOPE_API_KEY'] = 'sk-767e12e040bc43e098b75e52f23be883'

# 现在可以在代码中使用这个环境变量
api_key = os.environ['DASHSCOPE_API_KEY']
def call_with_prompt():
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt='如何做炒西红柿鸡蛋？'
    )
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response.output)  # The output text
        print(response.usage)  # The usage information
    else:
        print(response.code)  # The error code.
        print(response.message)  # The error message.

if __name__ == '__main__':
    call_with_prompt()
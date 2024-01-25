from flask import Flask, request, jsonify
from googleai.chatWithgoogle import chatWiteAi

# 初始化Flask应用
app = Flask(__name__)


# 定义路由和视图函数
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/v1/qzGoogle', methods=['POST'])
def qzGoogle():
    try:
        content = request.json.get('content')
    except Exception as e:
        print(f"Error while parsing JSON: {e}")
        return jsonify({"error": "Failed to parse the JSON object in the request body"}), 400

    if content:
        # 调用chatWiteAi函数
        response = chatWiteAi(content)
        return response
    else:
        return jsonify({"error": "Missing 'content' in the request body"}), 400


if __name__ == '__main__':
    # 运行应用
    app.run(debug=True)

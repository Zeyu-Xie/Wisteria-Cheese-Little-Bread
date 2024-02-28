from wechatpy import parse_message, create_reply
from wechatpy.events import SubscribeEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 处理微信服务器的验证
        token = '你在公众号配置中设置的Token'
        try:
            check_signature(token, request.args)
            return request.args.get('echostr', '')
        except InvalidSignatureException:
            return 'Signature verification failed!', 403
    elif request.method == 'POST':
        # 处理微信服务器推送的消息和事件
        msg = parse_message(request.data)
        reply = handle_message(msg)
        return reply.render()

def handle_message(msg):
    # 处理用户发送的文本消息
    if msg.type == 'text' and msg.content == '你好':
        reply_content = '你好呀'
        return create_reply(reply_content, msg).render()
    # 处理关注事件
    elif isinstance(msg, SubscribeEvent):
        return create_reply('欢迎关注！', msg).render()
    # 其他消息的处理逻辑
    return create_reply('暂不支持的消息类型', msg).render()

if __name__ == '__main__':
    app.run(port=80)
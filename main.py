import lark_oapi as lark
from get_message import main as get_message
from get_chatid import main as get_chat_id
from send_message import main as send_message

if __name__ == '__main__':
    # 需要一个应用
    app_id = input("请输入app_id:")
    app_secret = input("请输入app_secret:")
    client = lark.Client.builder().app_id(app_id).app_secret(app_secret).log_level(lark.LogLevel.ERROR).build()
    # 获取群id
    chat_id, name = get_chat_id(client)
    # 获取消息
    file_path = get_message(name, client, chat_id)
    # 发送消息
    webhook_url = input("请输入外部群的webhook_url:")
    send_message(client, webhook_url, file_path)

import lark_oapi as lark
from lark_oapi.api.im.v1 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
def main(client):
    request: ListChatRequest = ListChatRequest.builder() \
        .build()
    response: ListChatResponse = client.im.v1.chat.list(request)
    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.chat.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    count = 0
    for i in response.data.items:
        print("=====")
        print(f"#序号:{count}")
        print(f"chat_id:{i.chat_id}")
        print(f"群聊名称: {i.name}")
        print("=====")
        count += 1
    num = input("请输入群聊序号")
    print(f"选择的是第{num}个\nchat_id:", response.data.items[int(num)].chat_id)
    return response.data.items[int(num)].chat_id, response.data.items[int(num)].name

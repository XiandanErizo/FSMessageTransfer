import json
import os.path

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

def get_message(client, chat_id, page_token=None, total=0) -> (str, int):
    # 构造请求对象
    if page_token:
        request: ListMessageRequest = ListMessageRequest.builder() \
            .container_id_type("chat") \
            .container_id(chat_id) \
            .page_token(page_token) \
            .page_size(50).build()
    else:
        request: ListMessageRequest = ListMessageRequest.builder() \
            .container_id_type("chat") \
            .container_id(chat_id) \
            .page_size(50).build()

    # 发起请求
    response: ListMessageResponse = client.im.v1.message.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return None, 0

        # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response.data.items, indent=4))
    total += len(response.data.items)
    # 保存消息
    offset.append({"page_token": page_token, "total": total, "items": lark.JSON.marshal(response.data.items)})
    if response.data.has_more:
        page_token = response.data.page_token
    else:
        return None, total

    return page_token, total


class Offset:
    def __init__(self):
        self.total = None
        self.page_token = None
        self.filename = None
        self.message = None

    def init(self, name):
        self.message = []
        self.page_token = None
        self.total = 0
        self.filename = name + ".json"
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                fread = f.read()
                if fread:
                    self.message = json.loads(fread)
                    self.page_token = self.message[-1]["page_token"]
                    self.total = self.message[-1]["total"]
        else:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("")

    def write(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.message, ensure_ascii=False))

    def append(self, message):
        self.message.append(message)


offset = Offset()


def main(name, client, chat_id):
    offset.init(name)
    print("开始收集消息")
    while True:
        offset.page_token, offset.total = get_message(client, chat_id, offset.page_token, offset.total)
        if not offset.page_token:
            break
    offset.write()
    print(f"收集完毕 total: {offset.total}")
    return offset.filename

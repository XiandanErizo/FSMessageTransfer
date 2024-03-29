import json
import time
import lark_oapi as lark
from lark_oapi.api.contact.v3 import *
import requests


def get_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    messages = []
    for i in data:
        messages += json.loads(i["items"])
    return messages


def send_message_card(client, message, webhook_url):
    msg_type = message["msg_type"]
    sender_id = message["sender"]["id"]
    create_time = int(message["create_time"]) / 1000  # 转换为秒
    create_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(create_time))
    if message["sender"]["sender_type"] == "user":
        user_name = get_user_name(sender_id, client)
    else:
        user_name = message["sender"]["sender_type"]

    # 构造消息卡片的基础结构
    message_card = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"发送人: {user_name}\n发送时间: {create_time_str}"
                    }
                }
            ]
        }
    }

    # 根据消息类型添加对应的元素
    if msg_type == "text":
        try:
            text_content = json.loads(message["body"]["content"])["text"]

        except Exception as e:
            return

        if message.get("mentions"):
            for mention in message["mentions"]:
                user_id = mention["key"]
                user_name = mention["name"]
                text_content = text_content.replace(f"{user_id}", f"@{user_name}")

        message_card["card"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "plain_text",
                "content": text_content
            }
        })
    elif msg_type == "image":
        try:
            image_key = json.loads(message["body"]["content"])["image_key"]
        except Exception as e:
            return
        message_card["card"]["elements"].append({
            "tag": "img",
            "img_key": image_key,
            "alt": {
                "tag": "plain_text",
                "content": "图片"
            }
        })
    elif msg_type == "post":
        try:
            post_content = json.loads(message["body"]["content"])
        except Exception as e:
            return
        # 假设post消息包含标题和内容
        title = post_content.get("title", "无标题")
        post_elements = post_content.get("content", [])

        # 添加标题
        message_card["card"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "plain_text",
                "content": title
            }
        })

        # 遍历内容元素，添加到消息卡片
        for element in post_elements:
            for e in element:
                if e["tag"] == "text":
                    text_content = e["text"]
                    if message.get("mentions"):
                        for mention in message["mentions"]:
                            user_id = mention["key"]
                            user_name = mention["name"]
                            text_content = e["text"].replace(f"{user_id}", f"@{user_name}")

                    message_card["card"]["elements"].append({
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": text_content
                        }
                    })
                elif e["tag"] == "img":
                    message_card["card"]["elements"].append({
                        "tag": "img",
                        "img_key": e["image_key"],
                        "alt": {
                            "tag": "plain_text",
                            "content": "图片"
                        }
                    })


    else:
        print("不支持的消息类型:", msg_type)
        return

    response = requests.post(webhook_url, headers={"Content-Type": "application/json"},
                             data=json.dumps(message_card))
    if response.json()["StatusMessage"] != "success":
        print(response.text)


user_id_name = {}


def get_user_name(user_id, client):
    if user_id in user_id_name:
        return user_id_name[user_id]
    # 构造请求对象
    request: GetUserRequest = GetUserRequest.builder() \
        .user_id(user_id) \
        .build()

    # 发起请求
    option = lark.RequestOption.builder().user_access_token("u-d6DXmMOJte6qJMNwRHRZpL0hgxQAg0L9hq00khoy22eI").build()
    response: GetUserResponse = client.contact.v3.user.get(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.contact.v3.user.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        user_id_name[user_id] = "离职人员"
        return user_id_name[user_id]

        # 处理业务结果
    user_id_name[user_id] = response.data.user.name
    return user_id_name[user_id]


def main(client, webhook_url, file_path):
    messages = get_file(file_path)

    # 遍历消息列表，为每条消息发送消息卡片
    count = 0
    for msg in messages:
        try:
            send_message_card(client, msg, webhook_url)
        except Exception as e:
            print(e)
            print(count)
        print(f"第{count}条消息发送成功")
        count += 1
        time.sleep(0.1)


if __name__ == '__main__':
    main(file_path="IDP平台开发小组.json")

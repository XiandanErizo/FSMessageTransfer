# 飞书消息转移工具

### 原理

使用自建应用读取飞书群消息,并通过飞书机器人发送到另一个群(群可以是外部的)

### 效果图
![img_1.png](img/img.png)
### 使用方法

1. 创建一个飞书应用,并获取app_id和app_secret
2. 将应用添加到要备份的飞书群中
3. 创建一个外部群,并使原账号添加机器人,不能使用外部的账号添加可能导致图片无法发送(
   外部群的机器人需要认证才能添加成功,这里用的ip白名单,未做认证)
4. 运行main.py,输入app_id,app_secret,选择应用所在的群的序号,在填写机器人webhook

### 特别注意

1. 无法转发文件消息
2. 离职人员获取不到用户名,统一使用"离职人员"作为发送者
3. 报错的话可以尝试把群聊名称.json那个文件删了重试
4. 仅支持转移到飞书群中
5. 暂不支持断点续传



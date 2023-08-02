import itchat
import schedule
import time

# 登录微信账号
itchat.auto_login()

# 发送消息
def send_wechat_message(receiver, message):
    itchat.send(message, toUserName=receiver)

# 定义定时任务
def scheduled_job():
    receiver = 'a1732915463'
    message = '猜哥。'
    send_wechat_message(receiver, message)

# 设置定时任务，每天的指定时间执行
schedule.every().day.at("22:00").do(scheduled_job)

# 循环执行任务
while True:
    schedule.run_pending()
    time.sleep(1)

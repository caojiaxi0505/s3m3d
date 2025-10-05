import smtplib
import time
import psutil
import socket  # 用于获取主机名
from email.mime.text import MIMEText

# --- 开始配置 ---

# 需要监控的进程PID
TARGET_PID = 3982  # 请替换为您要监控的实际进程ID

# 主机名配置（可手动设置，为空则自动获取）
HOSTNAME = "PAMI-4091"  # 例如: "PAMI-4091"，留空则自动获取

# 邮件发送配置
SMTP_HOST = 'smtp.qq.com'  # 例如: 'smtp.qq.com' 或 'smtp.gmail.com'
SMTP_PORT = 465            # SMTP SSL端口，通常为 465
SENDER_EMAIL = '1154428672@qq.com'  # 您的发件人邮箱地址
SENDER_PASSWORD = 'ygdgmezbmxmggeji'  # 您的邮箱授权码或密码
RECEIVER_EMAIL = 'caojiaxi0505@163.com'  # 接收通知的邮箱地址

# 邮件内容配置
EMAIL_SUBJECT = '【进程监控】重要通知：目标进程已消失'

# 自动获取主机名，若未手动配置
if not HOSTNAME:
    HOSTNAME = socket.gethostname()

# 构建邮件正文，包含主机名
EMAIL_BODY = f'您好，\n\n监控的进程 (PID: {TARGET_PID}) 已于 {time.strftime("%Y-%m-%d %H:%M:%S")} 在主机 {HOSTNAME} 上消失，请及时检查相关服务。\n\n此邮件为系统自动发送，请勿回复。'

# 检查间隔（秒）
CHECK_INTERVAL = 10  # 每10秒检查一次进程是否存在

# --- 结束配置 ---


def check_pid_exists(pid):
    """
    检查指定的PID是否存在。
    """
    return psutil.pid_exists(pid)


def send_notification_email():
    """
    发送邮件通知。
    """
    # 创建邮件实例
    message = MIMEText(EMAIL_BODY, 'plain', 'utf-8')
    message['From'] = f"Process Monitor <{SENDER_EMAIL}>"
    message['To'] = f"Admin <{RECEIVER_EMAIL}>"
    message['Subject'] = EMAIL_SUBJECT

    try:
        print("正在连接到SMTP服务器...")
        smtp_client = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        print("SMTP服务器连接成功。")

        print("正在登录邮箱...")
        smtp_client.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("邮箱登录成功。")

        print("正在发送邮件...")
        smtp_client.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], message.as_string())
        print(f"邮件已成功发送至 {RECEIVER_EMAIL}")

    except smtplib.SMTPException as e:
        print(f"邮件发送失败，错误信息: {e}")
    finally:
        if 'smtp_client' in locals() and smtp_client:
            smtp_client.quit()
            print("已关闭SMTP连接。")


def main():
    """
    主函数，用于启动监控。
    """
    print(f"开始监控进程，目标PID: {TARGET_PID}")
    print(f"监控主机: {HOSTNAME}")
    print(f"每隔 {CHECK_INTERVAL} 秒检查一次。")

    try:
        # 初始检查
        if not check_pid_exists(TARGET_PID):
            print(f"进程 (PID: {TARGET_PID}) 在脚本启动时已不存在。")
            send_notification_email()
            return

        # 循环监控
        while True:
            if check_pid_exists(TARGET_PID):
                print(f"[{time.strftime('%H:%M:%S')}] 进程 (PID: {TARGET_PID}) 正在运行... (主机: {HOSTNAME})")
            else:
                print(f"进程 (PID: {TARGET_PID}) 已消失！准备发送邮件通知。")
                send_notification_email()
                break  # 进程消失，跳出循环
            
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n监控被手动中断。")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == '__main__':
    main()

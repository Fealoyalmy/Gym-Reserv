import time
import yaml
import os
import schedule
from datetime import date, datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler




# print(str(config["reservation"]["data"]))


# for i in range(len(config["reservation"]["data"])):
#     print("账号%d 创建定时任务" % i)
#     header = config["header"][i]
#     data = [config["reservation"]["data"][i]]
#     print(header)
#     print(data)

# 配置文件路径
CONFIG_FILE = "config copy.yaml"

# 定义任务
def job1():
    print("任务 1 执行")

def job2():
    print("任务 2 执行")

def job3():
    print("任务 3 执行")


def load_config():
    # 读取配置
    config_path = os.getenv("CONFIG_PATH", CONFIG_FILE)
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        return config


# 监听文件变化的处理器
class ConfigChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(CONFIG_FILE):
            print("检测到配置文件修改")
            config = load_config()
            schedule.every().day.at(config["schedule"]["time"]).do(job3)


if __name__ == "__main__":
    # 创建任务
    # schedule.every(10).seconds.do(job1)
    # schedule.every(5).seconds.do(job2)

    config = load_config()
    schedule.every().day.at(config["schedule"]["time"]).do(job3)

    # 创建监听器
    event_handler = ConfigChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        # 查看已创建的任务
        while True:
            schedule.run_pending()
            now = datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            print(formatted_time + " 当前已创建的任务:")
            for job in schedule.jobs:
                print(f"任务函数: {job.job_func.__name__}, 下次运行时间: {job.next_run}")
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



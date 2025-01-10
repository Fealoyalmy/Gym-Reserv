import requests
from requests import Session
import json
import traceback
import base64
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES
import Captcha
import schedule
import time
import yaml
import os
from datetime import date


class Reservation():
    def __init__(self, header, url=""):
        self.session = Session()
        self.header = header
        self.url = url

    # 获取图片验证码
    def requestCaptcha(self, url="https://ehall3.nuaa.edu.cn/site/captcha/click-get"):
        try:
            res = self.session.request(method="get", url=url, headers=self.header)  # , files=file, **{parametric_key: data}
            return res
        except Exception as e:
            raise "请求发送失败：%s" % (e)

    # 发送验证坐标
    def captchaVerification(self, payload, url="https://ehall3.nuaa.edu.cn/site/captcha/click-check"):
        try:
            res = self.session.request(method="post", url=url, headers=self.header, data=payload)
            return res
        except Exception as e:
            raise "请求发送失败：%s" % (e)

    # 加密数据
    def encyptData(self, data, secretKey):
        aes = AES.new(secretKey, AES.MODE_ECB) # 创建一个ECB模式的aes对象

        data = data.encode()
        needSize = 16 - len(data) % 16
        data += needSize.to_bytes(1, 'little') * needSize

        enc_text = aes.encrypt(data) # 加密明文
        enc_b64 = base64.b64encode(enc_text).decode() # 用base64编码
        print("密文:", enc_b64)
        return enc_b64

    # 解密数据
    def decryptData(self, enc_data):
        dec_bytes = base64.decodebytes(enc_data.encode())
        dec_text = aes.decrypt(dec_bytes).decode() # 解密密文
        print("明文:", dec_text)
        return dec_text.decode()

    # base64转换得到图片
    def getImageFromBase64(self, img_b64):
        buffer = base64.b64decode(img_b64)
        nparr = np.frombuffer(buffer, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        output_file_path = "captcha.png"
        success = cv2.imwrite(output_file_path, img)
        # 检查是否成功保存
        if success:
            print(f"图像成功保存到 {output_file_path}")
        else:
            print("保存图像失败")
        return img

    # 发送预定请求
    def sendReserv(self, payload, url="https://ehall3.nuaa.edu.cn/site/reservation/launch"):
        try:
            res = self.session.request(method="post", url=url, headers=self.header, data=payload)
            return res
        except Exception as e:
            raise "请求发送失败：%s" % (e)


if __name__ == "__main__":

    def job(header, data):
        # 创建会话
        reserv = Reservation(header)

        success = False
        count = 0
        while config["retry"] and not success and count < config["max_tries"]:
            # 请求获取验证码图片
            response = json.loads(reserv.requestCaptcha().text)
            print("获取验证码:")
            print(response["d"]["wordList"], response["d"]["secretKey"], response["d"]["token"])
            file_content = response["d"]["originalImageBase64"]
            secretKey = response["d"]["secretKey"]
            token = response["d"]["token"]
            wordList = response["d"]["wordList"]
            img = reserv.getImageFromBase64(file_content)

            # 识别验证码计算点击坐标
            Captcha.transformCaptcha("captcha.png", wordList)
            img_base64 = Captcha.img2base64("output_image.png")
            # print("生成图片的base64:", img_base64)
            result = Captcha.identifyCaptcha(img_base64)
            # 提取并转换数据
            point = [
                {"x": item["X坐标值"], "y": item["Y坐标值"]}
                for item in result["data"].values()
            ]
            point = str(point).replace("'", '"').replace(" ", "")
            print("识别坐标:", point)

            # 发送验证码验证坐标请求
            secretKey_bytes = secretKey.encode('utf-8') # 转换密钥为二进制字节码
            payload = {
                "data[captchaType]": "clickWord",
                "data[pointJson]": reserv.encyptData(point, secretKey_bytes),  # "PK9uNvWXhuAIXretztbZJEWkbzsHPr/0q40vg2mRJ8s3Hl0jW4nS3pm3mWyphlaDqgWNvvD4CWTGCwUQHq4dFVR9Vd4KhZguuY6OSucHfgA=",
                "data[token]": token  # "d7a94245-b55e-3ebe-950b-6a3d26c99c11"
            }
            print("验证码坐标请求参数:\n", payload)
            # time.sleep(1) # 延迟发送验证码坐标，避免验证太快
            captcha_res = reserv.captchaVerification(payload)
            print(captcha_res.text)

            # 生成加密后的预约请求坐标数据
            position_data = reserv.encyptData(token + "---" + point, secretKey_bytes)
            payload = {
                "resource_id": config["reservation"]["resource_id"],  # 17
                "code": "",
                "remarks": "",
                "deduct_num": 0,
                "data": str(data).replace("'", '"').replace(" ", ""),  #"[{\"date\":\"2025-01-10\",\"period\":9497,\"sub_resource_id\":29524}]",  # "[{\"date\":\"2025-01-10\",\"period\":9354,\"sub_resource_id\":28152}]"
                "position_data[captchaVerification]": position_data  # "kwcghAemj00ZHj48m+Vrovqh/qT1KoaZPopweVKer1IGsM8s6DoDYdgvRdHr6CXKaJt4PwnUhlL68zTjyiP4th5yxsiVw/9ls7nsZfwdER0SHRORihQkjZhE6WRnPwWi07habPE4zZwzUjZDsBa6DQ=="
            }
            print("预约信息请求参数:\n", payload)
            # 发送预订场地请求
            result = reserv.sendReserv(payload)
            print(result.text)
            count += 1

            # 如果预约失败则换场地重试
            if json.loads(result.text)["m"] == "操作成功":
                success = True
            else:
                interval = 13
                data[0]["sub_resource_id"] += interval  # 选择下一个场地


    # 读取配置
    config_path = os.getenv("CONFIG_PATH", "config.yaml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    # print(config)
    # job()

    # 设置定时任务
    if config["schedule"]["use"]:
        # schedule.every().day.at("13:35:59").do(job1)  # 每天 13:35:59 执行
        # schedule.every().monday.at("09:00").do(job1)  # 每周一 09:00 执行
        # schedule.every(5).seconds.do(job1)  # 每 5 秒执行一次
        if config["schedule"]["day"] == None:
            print("Everyday Schedule!")
            # 获取今天的日期
            today = date.today()
            formatted_date = today.strftime("%Y-%m-%d")  # 格式化为 "年-月-日"
            config["reservation"]["data"]["date"] = formatted_date # 设置预约日期为今天

            print("账号1")
            header1 = {
                "user-agent": config["header"]["user-agent"],
                "referer": config["header"]["referer"],
                "Cookie": config["header"]["Cookie"][0]
            }
            data1 = [{
                "date": formatted_date,
                "period": config["reservation"]["data"]["period"][0],
                "sub_resource_id": config["reservation"]["data"]["sub_resource_id"][0]
            }]
            schedule.every().day.at(config["schedule"]["time"]).do(job, header=header1, data=data1)

            print("账号2")
            header2 = {
                "user-agent": config["header"]["user-agent"],
                "referer": config["header"]["referer"],
                "Cookie": config["header"]["Cookie"][1]
            }
            data2 = [{
                "date": formatted_date,
                "period": config["reservation"]["data"]["period"][1],
                "sub_resource_id": config["reservation"]["data"]["sub_resource_id"][1]
            }]
            schedule.every().day.at(config["schedule"]["time"]).do(job, header=header2, data=data2)

        # 循环运行调度器
        while True:
            schedule.run_pending()
            time.sleep(1)  # 避免 CPU 占用过高


    
    # 每天13个时间段（8:00-21:00）
    # requestBody = [
    #     {"date":"2025-01-05","period":9354,"sub_resource_id":28152},  # 3号 18-19
    #     {"date":"2025-01-05","period":9350,"sub_resource_id":28148},  # 2号 14-15
    #     {"date":"2025-01-05","period":9344,"sub_resource_id":28142},  # 2号 8-9
    #     {"date":"2025-01-05","period":9347,"sub_resource_id":28197}   # 6号 11-12
    # ]

    # responseBody = { # 验证码响应体示例
        #     "e": 0,
        #     "m": "操作成功",
        #     "d": {
        #         "originalImageBase64": "",
        #         "secretKey": "g1lwhvs011dvly0x",
        #         "token": "1a4cc4e2-84c7-6088-8c54-8d45c0f2c93d",
        #         "wordList": [
        #             "蜡",
        #             "箍",
        #             "松",
        #             "卢"
        #         ]
        #     }
        # }

    # 读取base64编码文本获取图像
    # file_path = 'img_b64.txt'
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     file_content = file.read()
    # img_bit = reserv.normalizeImage(img)
    # cnt = reserv.findContour(img_bit)
    # ret, point = reserv.extractCharContour(img_bit, reserv.aspectRatio(cnt))
    # print(ret)
    # print(point)


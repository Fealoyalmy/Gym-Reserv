
import requests
from requests import Session
import json
import traceback
import base64
import json
import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES


class Reservation():
    def __init__(self, header, url=""):
        self.session = Session()
        self.header = header
        self.url = url

    def requestCaptcha(self, url):
        try:
            res = self.session.request(method="get", url=url, headers=self.header)  # , files=file, **{parametric_key: data}
        except Exception as e:
            raise "请求发送失败：%s" % (e)

    def captchaVerification(self, url, data_type, data):
        captchaType = "clickWord"
        pointJson = encyptData(point)
        token = responseBody["d"]["token"]
        data = "data%5BcaptchaType%5D=" + captchaType + "&data%5BpointJson%5D=" + pointJson + "&data%5Btoken%5D=" + token

        try:
            res = self.session.request(method="post", url=url, headers=self.header, **{data_type: data})
        except Exception as e:
            raise "请求发送失败：%s" % (e)


    def encyptData(self, data):
        aes = AES.new(secretKey, AES.MODE_ECB) # 创建一个ECB模式的aes对象

        data = data.encode()
        needSize = 16 - len(data) % 16
        data += needSize.to_bytes(1, 'little') * needSize

        enc_text = aes.encrypt(data) # 加密明文
        enc_b64 = base64.b64encode(enc_text).decode() # 用base64编码
        print("密文：", enc_b64)
        return enc_b64

    def decryptData(self, enc_data):
        dec_bytes = base64.decodebytes(enc_data.encode())
        dec_text = aes.decrypt(dec_bytes).decode() # 解密密文
        print("明文：", dec_text)
        return dec_text.decode()


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

    def normalizeImage(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
        img = cv2.bitwise_not(img)

        output_file_path = "captcha_bitwise.png"
        success = cv2.imwrite(output_file_path, img)
        # 检查是否成功保存
        if success:
            print(f"图像成功保存到 {output_file_path}")
        else:
            print("保存图像失败")
        return img

    def sendReserv(self, url, payload):
        try:
            res = self.session.request(method="post", url=url, headers=self.header, data=payload)
        except Exception as e:
            raise "请求发送失败：%s" % (e)


if __name__ == "__main__":

    header = {
        "user-agent": "Mozilla/5.0 (Linux; Android 13; Mi 10 Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/129.0.6668.100 Mobile Safari/537.36 ZhilinEai/3.3 ZhilinNuaaApp AgentWeb/5.0.0  UCBrowser/11.6.4.950",
        "referer": "https://ehall3.nuaa.edu.cn/v2/reserve/m_reserveDetail?id=17",
        "Cookie": "eai-sess=1sjquvtd8rha7c0k7pnei4a9g6; UUkey=b73d45ffa1cc6239c34917b54958d841; PHPSESSID=kad40cgvevl0fjmfmp5g0p1ab2; vjvd=c95d07e3a8ee74d3c1570152cfa2675a; vjuid=352722; vt=251751479"
    }


    # 创建会话
    reserv = Reservation("https://ehall3.nuaa.edu.cn/site/reservation/launch", header)

    # 请求获取验证码图片
    reserv.requestCaptcha("https://ehall3.nuaa.edu.cn/site/captcha/click-get")
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

    resp = {
        "e": 0,
        "m": "操作成功",
        "d": {
            "originalImageBase64": "",
            "secretKey": "ro095kvsr6045m38",
            "token": "0a13c660-95c1-b49d-8ddb-dc1fb961cd07",
            "wordList": [
                "陌",
                "旱",
                "豁",
                "庙"
            ]
        }
    }


    # 发送验证码验证坐标请求
    payload = {
        "data[captchaType]": "clickWord",
        "data[pointJson]": "PK9uNvWXhuAIXretztbZJEWkbzsHPr/0q40vg2mRJ8s3Hl0jW4nS3pm3mWyphlaDqgWNvvD4CWTGCwUQHq4dFVR9Vd4KhZguuY6OSucHfgA=",
        "data[token]": "d7a94245-b55e-3ebe-950b-6a3d26c99c11"
    }
    reserv.captchaVerification(self, url, data_type, payload)


    # 发送预订场地请求
    payload = {
        "resource_id": "17",
        "code": "",
        "remarks": "",
        "deduct_num": "0",
        "data": "[{\"date\":\"2025-01-05\",\"period\":9354,\"sub_resource_id\":28152}]",
        "position_data[captchaVerification]": "kwcghAemj00ZHj48m+Vrovqh/qT1KoaZPopweVKer1IGsM8s6DoDYdgvRdHr6CXKaJt4PwnUhlL68zTjyiP4th5yxsiVw/9ls7nsZfwdER0SHRORihQkjZhE6WRnPwWi07habPE4zZwzUjZDsBa6DQ=="
    }
    reserv.sendReserv("https://ehall3.nuaa.edu.cn/site/reservation/launch", payload)


    

    # 手动点选的坐标
    point = '[{"x":141,"y":110},{"x":223,"y":73},{"x":29,"y":35},{"x":91,"y":57}]' # 需要加密的内容，bytes类型
    # 加盐secret
    enc = 'vvHulAuGo+14fEB83bgbKfbr+Kijb9SbAtNdXIZBSkRvuoFlEJUAiyBj5ARjrAtDYFdSWw+fCfWSYEFvR2yDAkUrpNk2WXQoh7puYPmHNJ8='

    requestBody = {
        [
            {"date":"2025-01-05","period":9354,"sub_resource_id":28152},
            {"date":"2025-01-05","period":9350,"sub_resource_id":28148},
            {"date":"2025-01-05","period":9344,"sub_resource_id":28142},
            {"date":"2025-01-05","period":9347,"sub_resource_id":28197}
        ]
    }

    # 读取base64编码文本获取图像
    # file_path = 'img_b64.txt'
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     file_content = file.read()
    # img = reserv.getImageFromBase64(file_content)
    # img_bit = reserv.normalizeImage(img)
    # cnt = reserv.findContour(img_bit)
    # ret, point = reserv.extractCharContour(img_bit, reserv.aspectRatio(cnt))
    # print(ret)
    # print(point)


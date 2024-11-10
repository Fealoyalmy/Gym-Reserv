
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
            res = self.session.request(method="get", url=url, headers=header, files=file, **{parametric_key: data})
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


if __name__ == "__main__":
    url= "https://ehall3.nuaa.edu.cn/site/captcha/click-get"
    header = {
        "user-agent": "Mozilla/5.0 (Linux; Android 13; Mi 10 Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.172 Mobile Safari/537.36 ZhilinEai/3.2 ZhilinNuaaApp AgentWeb/5.0.0  UCBrowser/11.6.4.950",
        "referer": "https://ehall3.nuaa.edu.cn/v2/reserve/m_reserveDetail?id=18",
        "Cookie": "eai-sess=fssj1uei30lgl98rj037b4cph5; UUkey=cefdaeaeef431e7601ddfcd350a3044e; PHPSESSID=mmjnfupde0ppc3c2q5dmrt36o6; vjvd=c95d07e3a8ee74d3c1570152cfa2675a; vjuid=352722; ESEb0jRzmT2GS=60K63gKbCjyUa78Zj3f_ZqkNvnlNafzr_AZqBhhJHmY8uxfP5VYv27y2SoVguxUDwJkclTRjbYIAQyH0HSPKlldq; ESEb0jRzmT2GT=0xRU1AwXs7HKfyZ_dvAxSu7vvK.7eCrz8prQsyJNnCc_J8L.v0q5_1NdvaxHL4FsjlESTyjPAMVcgEwzITsZr_wjccUXM6FuwfNAWgWUu30Y5xbKHnidDHzfeiom8nfH3KWcy4dl08xp1GNZpi0dbt0Z1_dJ8L7MMplnQ0YD9yziOWnmYh3oe9pt6rGRetKhbhOYrSvaaJt0mZTcfwgXou2s5CceIAcEv3xEPW8bHt_x8fXy4cw_E7NbQaI0Qis85aBYcgBA3FE_jSjV_60Wy1lRDIEbBFfHkx_mVskUvHVxwxRIokbISMxYMFN.6uj3vzX2NPWcR7QpXMDhbdqRu_uQo2Q630d.IUZTn5zzFrgVpSHolyrT.sefe7nfqO_LT; vt=232857014"
    }

    reserv = Reservation(url, header)

    responseBody = {
        "e": 0,
        "m": "操作成功",
        "d": {
            "originalImageBase64": "",
            "secretKey": "g1lwhvs011dvly0x",
            "token": "1a4cc4e2-84c7-6088-8c54-8d45c0f2c93d",
            "wordList": [
                "蜡",
                "箍",
                "松",
                "卢"
            ]
        }
    }

    point = '[{"x":141,"y":110},{"x":223,"y":73},{"x":29,"y":35},{"x":91,"y":57}]' # 需要加密的内容，bytes类型
    enc = 'vvHulAuGo+14fEB83bgbKfbr+Kijb9SbAtNdXIZBSkRvuoFlEJUAiyBj5ARjrAtDYFdSWw+fCfWSYEFvR2yDAkUrpNk2WXQoh7puYPmHNJ8='

    file_path = 'img_b64.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    img = reserv.getImageFromBase64(file_content)
    img_bit = reserv.normalizeImage(img)
    cnt = reserv.findContour(img_bit)
    ret, point = reserv.extractCharContour(img_bit, reserv.aspectRatio(cnt))
    print(ret)
    print(point)


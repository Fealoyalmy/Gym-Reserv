
from requests import Session
import base64
import json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


# 生成携带点击语序提示的新图片
def transformCaptcha(img_path, wordList):
    # 1. 打开原始图片
    original_image = Image.open(img_path)  # 替换为你的图片路径
    original_width, original_height = original_image.size

    # 2. 定义空白区域的高度和文本
    blank_height = 50  # 空白区域的高度
    text = '请依次点击'  # 要插入的文本
    for word in wordList:
        text = text + ' "' + word + '"'
    font_size = 16  # 字体大小
    font_color = (0, 0, 0)  # 字体颜色 (黑色)
    font_path = "simsun.ttc"  # 字体文件路径 (Windows 下可以使用宋体 simsun.ttc)

    # 3. 创建新的画布
    new_image = Image.new("RGB", (original_width, original_height + blank_height), color=(255, 255, 255))  # 白色背景
    new_image.paste(original_image, (0, 0))  # 将原始图片粘贴到新画布的上半部分

    # 4. 在空白区域插入文本
    draw = ImageDraw.Draw(new_image)
    try:
        font = ImageFont.truetype(font_path, font_size)  # 加载字体
    except IOError:
        font = ImageFont.load_default()  # 如果字体加载失败，使用默认字体

    # 计算文本尺寸（使用 getbbox）
    text_bbox = font.getbbox(text)  # 获取文本的边界框
    text_width = text_bbox[2] - text_bbox[0]  # 文本宽度
    text_height = text_bbox[3] - text_bbox[1]  # 文本高度

    # 计算文本位置（居中）
    text_x = (original_width - text_width) // 2  # 水平居中
    text_y = original_height + (blank_height - text_height) // 2  # 垂直居中

    # 绘制文本
    draw.text((text_x, text_y), text, font=font, fill=font_color)

    # 5. 保存生成的新图片
    new_image.save("output_image.png")
    print("新图片已保存为 output_image.png")


# 图片转base64
def img2base64(img_path):
    # 打开图片文件
    image = Image.open(img_path)

    # 将图片数据写入 BytesIO 对象
    image_stream = BytesIO()
    image.save(image_stream, format="PNG")  # 可以指定格式，如 PNG、JPEG 等
    image_data = image_stream.getvalue()  # 获取二进制数据

    # 将二进制数据编码为 Base64
    base64_data = base64.b64encode(image_data).decode("utf-8")

    return base64_data


# 调用打码接口识别验证码
def identifyCaptcha(img_base64):
    session = Session()

    payload = {
        # "username": "18056639636",
        # "password": "123456",
        "usertoken": "oB+QxJZNhoAvj3KnPevU5fRv1R/0satKpywR7fPsKqVI2/P1EUNiOTWEuVBr+Vjx6JZLztB9fon61lJ2h8sdGA==",
        "b64": img_base64,
        "ID": "31989659",
        "version": "3.1.1"
    }
    
    res = session.request(method="post", data=payload, url="http://www.fdyscloud.com.cn/tuling/predict")
    print(res.text)
    return json.loads(res.text)



if __name__ == "__main__":
    # wordList = ["蜡", "箍", "松", "卢"]
    # transformCaptcha("captcha_test.png", wordList)
    img_base64 = img2base64("output_image.png")
    with open("img_b64.txt", "w") as file:
        file.write(img_base64)
    print(img_base64)
    # identifyCaptcha(img_base64)
    




import requests
from requests import Session
import json
import traceback

# 继承自Session类，用于实现自定义请求
class Api_Request(Session):
    # 自定义请求方法，主要用于区分请求体数据类型并捕获异常
    def api_request(self, url, method, parametric_key, header=None, data=None, file=None) -> dict:
        if parametric_key == "params":
            parametric = {"params": data}
        elif parametric_key == "data":
            parametric = {"data": data}
        elif parametric_key == "json":
            parametric = {"json": data}
        else:
            raise ValueError("“parametric_key”的可选关键字为params, json, data")

        try:
            response = self.request(method=method, url=url, files=file, headers=header, **parametric)
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(traceback.format_exc())
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            print(traceback.format_exc())
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
            print(traceback.format_exc())
        except requests.exceptions.RequestException as req_err:
            print(f'An error occurred: {req_err}')
            print(traceback.format_exc())
        # except Exception as e:
        #     raise "请求发送失败：%s" % (e)

        return response

# B站 点赞/取消点赞 测试类
class BiliBili_Like_Control:
    # 视频链接地址
    URL = "https://www.bilibili.com/video/BV14b421z7qj/?spm_id_from=333.1007.tianma.9-1-31.click&vd_source=f95b16bd5f667b51d07b1567c041b294"

    session = Api_Request()
    url= "https://api.bilibili.com/x/web-interface/archive/like"
    header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "referer": "https://www.bilibili.com/video/BV14b421z7qj/?spm_id_from=333.1007.tianma.9-1-31.click&vd_source=f95b16bd5f667b51d07b1567c041b294",
            "Cookie": "i-wanna-go-back=-1; b_ut=7; buvid4=912FF0B0-A249-7B56-F824-941C13917E3895041-023082414-fPFu10NyFO0F32L5AK3KpQ%3D%3D; header_theme_version=CLOSE; buvid_fp_plain=undefined; buvid3=785B7257-B8E4-3392-F3FB-4C524A250D8025356infoc; b_nut=1697266825; _uuid=E17E2DAF-C575-6E2F-1167-BA1D7DACE910B26987infoc; enable_web_push=DISABLE; LIVE_BUVID=AUTO1217037432002073; hit-dyn-v2=1; home_feed_column=5; rpdid=|(m)~|Yu||~0J'u~u||~J)~m; DedeUserID=352193155; DedeUserID__ckMd5=d22235e6fdddb4e5; PVID=1; FEED_LIVE_VERSION=V_DYN_LIVING_UP; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; bsource_origin=bing_ogv; bsource=bing_ogv; browser_resolution=2048-1010; fingerprint=92a616c9254a9b050356530a614e5d4f; CURRENT_QUALITY=116; bp_t_offset_352193155=935731433755902006; buvid_fp=92a616c9254a9b050356530a614e5d4f; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTcyMTk2NzQsImlhdCI6MTcxNjk2MDQxNCwicGx0IjotMX0.wBSac5JzZMoRuKVQG1ZSGRN9eLrhUJ16we4ifegyEGs; bili_ticket_expires=1717219614; SESSDATA=53620c9a%2C1732513927%2C937d2%2A52CjCL6nkGAu-6NBVTTLvmREdpq-L6q0xisGSern29mhURvNbOLA6_6-o7DQ-xKDKEkxwSVloxTmZSMjFkMG9lMFdLamo3QzVqaGg3MjdFWVNQaXIxRXJNa0U4RDFlU190TmRJVXFhN1VlZ2VtNEVXbVdtRVNFWTl3Y2ljSmdMWDFyc25hZlZpazN3IIEC; bili_jct=bdd04e310a77e3bf49127c87925a581f; sid=6e8rg95l; b_lsid=2A1033178_18FC3272C62"
        }

    # 给视频点赞
    def addLike(self):
        data = "aid=1804857579&like=1&eab_x=2&ramval=65&source=web_normal&ga=1&csrf=bdd04e310a77e3bf49127c87925a581f"
        res = self.session.api_request(self.url, "post", "data", self.header, data)
        return res

    # 取消视频点赞
    def removeLike(self): 
        data = "aid=1804857579&like=2&eab_x=2&ramval=0&source=web_normal&ga=1&csrf=bdd04e310a77e3bf49127c87925a581f"
        res = self.session.api_request(self.url, "post", "data", self.header, data)
        return res


def httpRequestDemo():
    # 定义一个会话对象
    session = Session()
    # 请求方法get,post,put,delete,head,options,patch
    method = "post"  
    # 请求url
    url= "https://data.bilibili.com/log/web?0000171716973452741https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV14b421z7qj%2F%3Fspm_id_from%3D333.1007.tianma.9-1-31.click%26vd_source%3Df95b16bd5f667b51d07b1567c041b294%7C333.788.toolbar.like.click%7C%7C1716973452741%7C%7C%7C2048x1010%7C1%7C%7B%22aid%22:1804857579,%22action%22:%22add_like%22,%22cid%22:1552825860,%22b_nut_h%22:1697266800,%22lsid%22:%2241F3C51F_18FC3799252%22,%22buvid_fp%22:%2292a616c9254a9b050356530a614e5d4f%22,%22buvid4%22:%22912FF0B0-A249-7B56-F824-941C13917E3895041-023082414-fPFu10NyFO0F32L5AK3KpQ%3D%3D%22,%22bsource_origin%22:%22bing_ogv%22,%22share_source_origin%22:%22empty%22%7D%7C%7B%22webplayer%22:%222%22,%22login_dialog_version%22:%22V_PLAYER_PLAY_TOAST%22,%22call_pc_app%22:%22FORBID%22,%22for_ai_home_version%22:%22V_OTHER%22,%22ai_summary_version%22:%22SHOW%22,%22bmg_fallback_version%22:%22DEFAULT%22,%22rcmd_tab_version%22:%22DISABLE%22,%22in_new_ab%22:true,%22ab_version%22:%7B%22webplayer%22:%222%22,%22login_dialog_version%22:%22V_PLAYER_PLAY_TOAST%22,%22call_pc_app%22:%22FORBID%22,%22for_ai_home_version%22:%22V_OTHER%22,%22ai_summary_version%22:%22SHOW%22,%22bmg_fallback_version%22:%22DEFAULT%22,%22rcmd_tab_version%22:%22DISABLE%22%7D,%22ab_split_num%22:%7B%22login_dialog_version%22:37,%22call_pc_app%22:13,%22for_ai_home_version%22:33,%22ai_summary_version%22:872,%22bmg_fallback_version%22:73,%22rcmd_tab_version%22:39,%22webplayer%22:0%7D,%22pageVersion%22:%22new_video%22,%22videoGoOldVersion%22:-1%7D%7Chttps%3A%2F%2Fwww.bilibili.com%2F%7CE17E2DAF-C575-6E2F-1167-BA1D7DACE910B26987infoc%7Czh-CN%7Cnull%7C1"
    # 请求头：最好包括user-agent和referer，以防服务器直接将其视为爬虫脚本；Cookie根据是否需要用户身份状态添加
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "referer": "https://www.bilibili.com/video/BV14b421z7qj/?spm_id_from=333.1007.tianma.9-1-31.click&vd_source=f95b16bd5f667b51d07b1567c041b294",
        "Cookie": "i-wanna-go-back=-1; b_ut=7; buvid4=912FF0B0-A249-7B56-F824-941C13917E3895041-023082414-fPFu10NyFO0F32L5AK3KpQ%3D%3D; header_theme_version=CLOSE; buvid_fp_plain=undefined; buvid3=785B7257-B8E4-3392-F3FB-4C524A250D8025356infoc; b_nut=1697266825; _uuid=E17E2DAF-C575-6E2F-1167-BA1D7DACE910B26987infoc; enable_web_push=DISABLE; LIVE_BUVID=AUTO1217037432002073; hit-dyn-v2=1; home_feed_column=5; rpdid=|(m)~|Yu||~0J'u~u||~J)~m; DedeUserID=352193155; DedeUserID__ckMd5=d22235e6fdddb4e5; PVID=1; FEED_LIVE_VERSION=V_DYN_LIVING_UP; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; bsource_origin=bing_ogv; bsource=bing_ogv; browser_resolution=2048-1010; fingerprint=92a616c9254a9b050356530a614e5d4f; CURRENT_QUALITY=116; buvid_fp=92a616c9254a9b050356530a614e5d4f; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTcyMTk2NzQsImlhdCI6MTcxNjk2MDQxNCwicGx0IjotMX0.wBSac5JzZMoRuKVQG1ZSGRN9eLrhUJ16we4ifegyEGs; bili_ticket_expires=1717219614; SESSDATA=53620c9a%2C1732513927%2C937d2%2A52CjCL6nkGAu-6NBVTTLvmREdpq-L6q0xisGSern29mhURvNbOLA6_6-o7DQ-xKDKEkxwSVloxTmZSMjFkMG9lMFdLamo3QzVqaGg3MjdFWVNQaXIxRXJNa0U4RDFlU190TmRJVXFhN1VlZ2VtNEVXbVdtRVNFWTl3Y2ljSmdMWDFyc25hZlZpazN3IIEC; bili_jct=bdd04e310a77e3bf49127c87925a581f; sid=6e8rg95l; b_lsid=41F3C51F_18FC3799252; bp_t_offset_352193155=936876257256144915"
    }

    """
    请求体传递的数据有 params,data,json 三种类型
    1. params：类似这种：url?参数名=参数值&参数名1=参数值1
    2. data：请求头content-type是from表单类型。
    3. json：请求头content-type：application/json。
    """
    parametric_key = "data"
    # 请求体传输给服务器的数据
    # data = {}
    data = "aid=1804857579&like=2&eab_x=2&ramval=0&source=web_normal&ga=1&csrf=bdd04e310a77e3bf49127c87925a581f"
    # 上传文件路径
    file = ""

    # 组装并发送请求
    try:
        res1 = session.request(method=method, url=url, headers=header, files=file, **{parametric_key: data})  # 使用会话对象发送请求
        res2 = requests.post(url=url, headers=header, files=file, **{"data": data})  # 直接发送post请求
    except Exception as e:
        raise "请求发送失败：%s" % (e)

    # 获取响应文本
    print(res1.text)
    # 
    print(res2.text)


if __name__ == "__main__":
    # httpRequestDemo()

    blc = BiliBili_Like_Control()
    res = blc.addLike()
    # res = blc.removeLike()
    print(res.text)
    


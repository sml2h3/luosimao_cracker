# coding=UTF-8
import requests_html
import requests
import execjs
import time
import json
import re
import hashlib
# coding=UTF-8
from PIL import Image
import numpy as np
from io import BytesIO


def getpoint(imgcontent, position):
    img = Image.open(BytesIO(imgcontent))
    img.save('download.png')
    w, h = img.size

    print("图片宽为{},高为{}".format(w, h))
    print("开始处理图片...")
    img_click = Image.new('RGB', (300, 160))
    position = position
    for i in range(30):
        p = position[i]
        pic = img.crop((int(p[0]), int(p[1]), int(p[0]) + 20, int(p[1]) + 80))
        if i < 15:
            box = (20 * i, 0, 20 * (i + 1), 80)
        else:
            box = (20 * (i - 15), 80, 20 * (i + 1 - 15), 160)
        img_click.paste(pic, box)
    print("成功生成完整图片...详情见本地目录click.png")
    img_click.save('click.png')
    target_pos = []
    gray_img = np.array(img_click.convert('L'), 'f')
    for col in range(len(gray_img)):
        for line in range(len(gray_img[col])):
            if gray_img[col][line] >= 254:
                target_pos.append([col, line])
    # white_img = Image.new("RGB", (300, 160))
    x = 0
    y = 0
    c = 0
    target_nei_x_max = -9999
    target_nei_y_max = -9999
    target_nei_x_min = -9999
    target_nei_y_min = -9999
    target = []
    for point in target_pos:
        # img_click.putpixel((y,x), (0,0,0,255))
        # white_img.putpixel((y,x), (255, 255,255))
        if x == 0:
            # print(a)
            x = point[0]
            y = point[1]
            if x == 0:
                x = 0.5
            continue
        else:
            if target_nei_x_max != -9999:
                if target_nei_x_max > x > target_nei_x_min:
                    x = point[0]
                    y = point[1]
                    continue
                if target_nei_y_max > y > target_nei_y_min:
                    x = point[0]
                    y = point[1]
                    continue
            if x == point[0]:
                if point[1] - y == 1:
                    c = c + 1
                    if c > 4:
                        target.append([y - 2, x])
                        target_nei_x_max = x + 20
                        target_nei_y_max = y - 2 + 20
                        target_nei_x_min = x - 20
                        target_nei_y_min = y - 2 - 20
                        c = 0
                else:
                    c = 0
            else:
                c = 0
            x = point[0]
            y = point[1]

    return target[0]


def getkvalue(keywords):
    s = requests_html.HTMLSession()
    url = "http://search.anccnet.com/searchResult2.aspx?keyword={}".format(keywords)
    header = {
        "referer": "http://www.anccnet.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    rsp = s.get(url, headers=header)
    k = rsp.html.find('#yanzhengLabel')[0].attrs['data-site-key']
    s.close()
    return k


def getcapthaparam(k):
    url_wiget = "http://captcha.luosimao.com/api/widget?k={}&l=zh-cn&s=normal&i=_2rip1ijo1".format(k)
    s = requests_html.HTMLSession()
    rsp = s.get(url_wiget)
    data_token = rsp.html.find('#l_captcha_widget')[0].attrs['data-token']
    # data_key = rsp.html.find('#l_captcha_widget')[0].attrs['data-key']
    # print(data_token, data_key)d
    data_key = "c28725d494c78ad782a6199c341630ee"
    s.close()
    url = "http://captcha.luosimao.com/api/request?k={}&l=zh-cn".format(k)
    s = requests_html.HTMLSession()
    key_a = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36||{}||1920:1080||win32||webkit".format(
        data_token)
    key_b = "706,41:{}||709,25:{}".format(int(round(time.time() * 1000)), int(round(time.time() * 1000)))
    # key_a = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36||KW0OevYgv4ztolX3_0Sk3g||1920:1080||win32||webkit"
    # key_b = "46,0:1545263179848||108,23:1545263198797"
    with open('fun.js', 'r') as f:
        js = f.read()
    ctx = execjs.compile(js)
    bg = ctx.call('encryption', key_a, data_key)
    b = ctx.call('encryption', key_b, data_key)
    s.headers = {
        "Origin": "http://captcha.luosimao.com",
        "Referer": "http://captcha.luosimao.com/api/widget?k={}&l=zh-cn&s=normal&i=_lx6bspcp1".format(k),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    data = {
        'bg': bg,
        'b': b
    }
    rsp = s.post(url, data=data)
    cookies = rsp.cookies.get('cuuid_322149')
    return json.loads(rsp.html.html), cookies, data_key


def getimginfo(s, referer, cookies):
    url = "http://captcha.luosimao.com/api/frame?s={}&i=_vboaax4xf&l=zh-cn".format(s)
    headers = {
        "Origin": "http://captcha.luosimao.com",
        "Referer": referer,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    cookies = {'cuuid_322149': cookies}
    rsp = requests.get(url, headers, cookies=cookies)
    rsp.encoding = "utf-8"
    html = rsp.text
    pattern = re.compile(r"http://i5-captcha.luosimao.com(.*?)png", re.MULTILINE | re.DOTALL)
    img = pattern.search(html)[0]
    pattern = re.compile(r"l: (.*?);", re.MULTILINE | re.DOTALL)
    position = pattern.search(html)[0]
    position = position.replace('l: ', '').replace(']};', '') + "]"
    position = json.loads(position)
    return img, position


def click(position, data_key, h, sign, cookies, i):
    key_a = position  # 110,86 xy
    with open('fun.js', 'r') as f:
        js = f.read()
    ctx = execjs.compile(js)
    v = ctx.call('encryption', key_a, i)
    v = v.replace('=', '').replace('+', '-').replace('/', '_')
    m = hashlib.md5()
    m.update(position.encode("utf-8"))
    s = m.hexdigest()
    datas = {
        'h': h,
        'v': v,
        's': s
    }
    headers = {
        "Origin": "http://captcha.luosimao.com",
        "Referer": "http://captcha.luosimao.com/api/frame?s={}&i=_vboaax4xf&l=zh-cn".format(sign),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    cookies = {'cuuid_322149': cookies}
    rsp = requests.post("http://captcha.luosimao.com/api/user_verify", data=datas, headers=headers, cookies=cookies)
    return rsp.text


def crack(k, referer):

    print("获取参数：{}".format(k))
    rsp_json, cookies, data_key = getcapthaparam(k)
    h = rsp_json['h']
    s = rsp_json['s']
    i = rsp_json['i']
    print("破解参数或得：{},{},{}".format(h, s, data_key))
    img, position = getimginfo(s, referer, cookies)
    print("获取验证码图片信息: {},{}".format(img, json.dumps(position)))
    imgcontent = requests.get(img).content
    position = getpoint(imgcontent, position)  # 处理完的
    print("计算点位信息：{},{}".format(position[1], position[0]))
    position = "{},{}".format(position[1], position[0])
    result = click(position, data_key, h, s, cookies, i)
    print("提交加密后的数据请求{}".format(json.dumps(result)))


if __name__ == '__main__':
    k = "b261322add610bd80218d7dca74b974e"
    referer = "http://search.anccnet.com/searchResult2.aspx?keyword=惠普1106"
    crack(k, referer)

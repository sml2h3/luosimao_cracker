# Luosimao点击验证码自动识别SDK

## 调用环境
python3

## 如何使用
下载本项目中的crack.py、fun.js、requirements.txt

### 安装依赖
````
pip3 install -r requirements.txt
````

### 调试sdk
修改参数测试
````

if __name__ == '__main__':
    k = "b261322add610bd80218d7dca74b974e"
    referer = "http://search.anccnet.com/searchResult2.aspx?keyword=惠普1106"
    crack(k, referer)

````
修改其中的k值，抓包可得，为下述链接中的k参数
````angular2html
http://captcha.luosimao.com/api/widget?k=b261322add610bd80218d7dca74b974e&l=zh-cn&s=normal&i=_s1pw34oy6
````
referer自行对应修改

然后直接
````angular2html
python3 crack.py
````
运行看提交加密后的数据请求是否类似如下结构
````angular2html
"{\"res\":\"success\",\"resp\":\"bkpQIuw4lSYSpw_Q0BbtWifmccdX579ZRM_mjAXPcNhsaM1V61anslp1H2UReMqYU3YVyFw_chFD8YN7ZSMSB0jJ01v-7fhYtH_LvsdYXy_8aYdGT0koeOkQNAogQFxOTv3x_JxAXYmESAGISLnSbWKPHzwopwU3uNwcVaKyU5SMEJWU-0lYQBmt75517ExGyz8Cfqrcp5Bc4agUoQhGuV7bHYZUv5OYwskMql0VVGdjwidrVZc4H0ximXDe4O01bT5QkonpzuV-8_tXPA_Lw84uJBIdHaUBmT9gZclXJH8\"}"
````

如果通过，则注释掉click方法中的所有print()然后移植到你的程序中

# 快乐的数据爬虫群
**QQ119794042**

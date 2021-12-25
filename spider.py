import os
import json
import urllib
import requests
import urllib.request
###############################定义函数和初始化############################################
config = ["{\"force_requests\": false, \"save_dir\": \"\", \"request_cookies\":\"\"}"]
if os.path.exists("config.json") == False:
    print("找不到config.json。正在创建...")
    with open("config.json", mode="w") as newconf:
        newconf.writelines(config)
try:
    with open("config.json", encoding="utf-8") as conf:
        a = json.load(conf)
        force_requests = a["force_requests"]
        setudir = a["save_dir"]
        request_cookies = a["request_cookies"]
except:
    print("无法读取config.json.")
    pass
if setudir == "":
    showdir = os.getcwd()
else:
    showdir = setudir
if request_cookies == "":
    print("\033[33m未读取到Cookies。\033[0m\n为获取到R-18作品的相关作品，需要在config.json提供启用了显示R-18作品的账户的Cookies。")
def download_img(dlurl): #定义下载函数
    global setudir
    extname = "." + dlurl.split(".").pop()
    setuname = pid + "_p0" + "-" + title + extname #拼接涩图文件名，可以使用变量自定义文件名，目前只可通过修改代码实现自定义
    setupath = os.path.join(setudir, setuname)
    if usecurl == True:
        if os.path.exists(setupath) is False:
            if str(setudir) is None:
                setudir = "./"
            print("\033[33m下载中...\033[0m")
            if os.system("curl "+dlurl+" -o "+"\""+os.path.join(setudir, setuname)+"\""+" -#") == 0:
                print("\033[32m下载完成\033[0m")
                return 'done'
            else:
                print("\033[31m发生错误！无法下载。\033[0m")
                return 'error'
        else:
            print ("文件已存在，跳过此下载。")
            return 'exist'
    else:
        r = requests.get(dlurl, stream=True)
        print("状态码：", r.status_code) # 返回状态码
        if r.status_code == 200:
            print("\033[33m下载中...\033[0m")
            if str(setudir) is None:
                setudir = "./"
            if os.path.exists(setupath) is False:
                open(os.path.join(setudir, setuname), 'wb').write(r.content) # 将内容写入图片
                print("\033[32m下载完成\033[0m")
                return 'done'
            else:
                print ("文件已存在，跳过此下载。")
                return 'exist'
        else:
            print("\033[31m发生错误！无法下载。\033[0m")
        del r
        return 'error'
if os.system("curl -V >nul") == 0 and force_requests == False: #what the fuck
    print("\033[32m已安装curl。将使用curl进行下载。\033[0m")
    usecurl = True
else:
    print("\033[33m未安装curl。将使用requests模块进行下载。\033[0m\n如果你已安装，请确认是否添加进环境变量。")
    usecurl = False
try:
    os.remove("nul")
except:
    pass
def replacesym(zifu):
    #spsymbol = ['\\',"|","/","?","<",">",":","*","\""]
    result = zifu.replace('\\', '')
    result = result.replace('/', '')
    result = result.replace('?', '？')
    result = result.replace('<', '')
    result = result.replace('>', '')
    result = result.replace(':', '：')
    result = result.replace('*', '')
    result = result.replace('|', '')
    result = result.replace('\"', '')
    return result
########################################主体########################################
piccount = 0
print(f"当前保存路径:{str(showdir)}")
reqpid = int(input("作品PID:"))
limit = int(input("下载数量:") or 18)
headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Cookie': request_cookies}
add = urllib.request.Request(f"https://www.pixiv.net/ajax/illust/{reqpid}/recommend/init?limit={limit}&lang=zh", headers=headers)
resp = json.loads(urllib.request.urlopen(url=add).read().decode("utf-8"))
for illust in resp["body"]["illusts"]:
    try:
        pid = illust["id"]
        title = replacesym(illust["title"])
        if illust["pageCount"] == 1:
            url = f"https://pixiv.re/{pid}.png"
        else:
            url = f"https://pixiv.re/{pid}-1.png"
        tags = illust["tags"]
    except:
        continue
    piccount = piccount + 1
    print(f"当前为{piccount}/{limit}张图片")
    print(f"PID:{pid} 标题:{title}\n标签:{tags}\nURL:{url}")
    download_img(url)


'''
参考：https://zhuanlan.zhihu.com/p/33729696(心一的《python爬取QQ音乐》)
'''
import requests
import json
__author__=["心一","Xie Zheyuan"]

def search(q):
    url="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?w=%s"
    data=json.loads(requests.get(url%q).text.replace("callback(","")[:-1])["data"]["song"]["list"]
    values=[]
    for i in data:
        value={}
        # for k in i:
        #     print(k,i[k])
        value["mid"]=i["media_mid"]
        value["name"]=i["songname"]
        value["album"]=i["albumname"]
        singer=[]
        for j in i["singer"]:
            singer.append(j["name"])
        value["singers"]=singer
        values.append(value)
    return values




def getVkey(songmid):#获得vkey
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=1418093288&jsonpCallback=MusicJsonCallback01822902435765017&loginUin=344604012&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback&uin=344604012&songmid={0}&filename=C400{1}.m4a&guid=9010457983'.format(songmid,songmid)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Referer': 'https://y.qq.com/portal/player.html',
        # 'Cookie': 'pt2gguin=o0344604012; RK=hBKNVevgd9; ptcz=7e70edebd26744f63d321bdc3eea832e59681b1614a86c481cb4bdd7af326ae0; pgv_pvid=9010457983; o_cookie=344604012; pac_uid=1_344604012; pgv_pvi=728103936; ts_uid=1996056142; luin=o0344604012; lskey=00010000e413b4b01a49b1b29d38d9babc926a4938ea3ea55f6e0816c6cd499ee24b2b3308e048e5aee5ad9f; p_luin=o0344604012; p_lskey=000400005434bcef5702931d41bb0bff1e229a77686dc7890afefd848e20a1f60a95ecf18b8c1d946bfb4aef; yq_index=0; pgv_si=s4678867968; pgv_info=ssid=s1658792426; ts_refer=ADTAGnewyqq.toplist; yqq_stat=0; ts_last=y.qq.com/n/yqq/toplist/4.html'
    }
    html = requests.get(url, headers=headers).text
    t1 = html.replace('MusicJsonCallback(', "")
    t2 = t1.strip(")")
    jsonp = json.loads(t2)
    vkey = jsonp['data']['items'][0]['vkey']
    return vkey
def saveMusic(songid,vkey,name):#保存音乐
    url = 'http://dl.stream.qqmusic.qq.com/C400{0}.m4a?vkey={1}&guid=9010457983&uin=344604012&fromtag=66'.format(songid,vkey)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Host': 'dl.stream.qqmusic.qq.com',
        # 'Cookie': 'pt2gguin=o0344604012; RK=hBKNVevgd9; ptcz=7e70edebd26744f63d321bdc3eea832e59681b1614a86c481cb4bdd7af326ae0; pgv_pvid=9010457983; o_cookie=344604012; pac_uid=1_344604012; pgv_pvi=728103936; ts_uid=1996056142; luin=o0344604012; lskey=00010000e413b4b01a49b1b29d38d9babc926a4938ea3ea55f6e0816c6cd499ee24b2b3308e048e5aee5ad9f; p_luin=o0344604012; p_lskey=000400005434bcef5702931d41bb0bff1e229a77686dc7890afefd848e20a1f60a95ecf18b8c1d946bfb4aef; yq_index=0; pgv_si=s4678867968; pgv_info=ssid=s1658792426; ts_refer=ADTAGnewyqq.toplist; yqq_stat=0; ts_last=y.qq.com/n/yqq/toplist/4.html'
    }
    # html = requests.get(url, headers=headers)
    filename = '{0}.m4a'.format(name)
    print(filename)
    res = requests.get(url, headers=headers, stream=True)
    print(url)
    if res.status_code == 403 or res.status_code == "403":
        print("下载出错：403 Forbidden")
        return -1
    if res.status_code == 404 or res.status_code == "404":
        print("下载出错：404 Not Found")
        return -1
    with open(filename, 'wb') as f:
        f.write(res.raw.read())
def main():
    q = input()
    data = search(q)
    for i in data:
        print("要下载" + ",".join(i["singers"]) + "的" + i["name"] + ",来自" + i["album"] + "专辑吗？")
        ans = input("(y/n/e):")
        if ans.lower() == "y":
            vkey = getVkey(i["mid"])
            n=saveMusic(i["mid"], vkey, "downloads/" + i["name"])
            if n==-1:
                print("下载失败！")
            else:
                print("下载成功!")
        elif ans.lower() == "e":
            print("正在结束……")
            break
if __name__ == "__main__":
    main()
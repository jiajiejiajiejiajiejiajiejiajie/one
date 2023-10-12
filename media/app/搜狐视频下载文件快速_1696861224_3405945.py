import os
import random
import time
import requests
import re
class downloadsouhu():
    ss=requests.session()
    zeroList='0000'
    saveFilePath = r"D:\爬取"
    def GetVidsAndRun(self):
        firstFile=0
        pageSize=30
        pageTotal=0
        playListId=None
        self.ss = requests.session()
        rt=self.GetHttpBody("https://tv.sohu.com/v/dXMvMzQxMjAwNTE3LzE4Mzg2ODQ4Ni5zaHRtbA==.html")
        # rt = self.GetHttpBody("https://tv.sohu.com/v/dXMvMzQ2NjQxMTUxLzM5MTE4MDI2OC5zaHRtbA==.html")
        rt = rt.text
        rf = re.findall(r"playListId: '(.+?)'", rt)
        if rf:
            playListId=rf[0]
        rf = re.findall(r"vid: '(.+?)'", rt)
        if rf:
            vid = rf[0]
        rf = re.findall(r"title: '(.+?)'", rt)
        if rf:
            title = rf[0]
        print(playListId)
        if not playListId:
            self.DownLoadFile(1, title, vid)
            return
        rt = self.GetHttpBody(
            "https://my.tv.sohu.com/play/getvideolist.do?callback=jQuery17202743045934073225_1667114384371&ssl=0&playlistid={}&pagesize=30&order=0&pagenum={}&_=1667114715037".format(
                playListId, 1))
        rt = rt.text
        rf = re.findall(r'"size":(.+?),', rt)
        if rf:
            pageTotal=int(int(rf[0])/pageSize)+2
        print(playListId,pageTotal,vid,title)
        namess=[]
        vidss=[]
        for i in range(1,pageTotal):
            rt = self.GetHttpBody("https://my.tv.sohu.com/play/getvideolist.do?callback=jQuery17202743045934073225_1667114384371&ssl=0&playlistid={}&pagesize=30&order=0&pagenum={}&_=1667114715037".format(playListId,i))
            rt = rt.text
            names = re.findall(r'"name":"(.+?)"', rt)
            vids = re.findall(r'"vid":(.+?),', rt)
            namess.extend(names)
            vidss.extend(vids)
        for i in range(firstFile, len(namess)):
            self.DownLoadFileList(i+1,namess[i],vidss[i])

    def DownLoadFileList(self,fileCount,fileName, vid):
        fileName = self.zeroList[0:len(self.zeroList)-len(str(fileCount))]+str(fileCount) + "_"+re.sub(r"\\|\/|\:|\*|\?|\"|\<|\>|\|| ", "", fileName)
        sus = self.GetSus(vid)
        mp4Names = []
        for j in range(0, len(sus)):
            mp4Name = fileName + "_"+ str(j) + '.mp4'
            if ".com" in sus[j]:
                DLURL=sus[j]
            else:
                DLURL = self.GetDLURL(sus[j])
                if not DLURL:
                    print("下载失败", fileName, sus[j])
                    continue
            mp4Names.append(mp4Name)
            print(DLURL)
            self.DownLoadFile(mp4Name,DLURL)
            time.sleep(random.randint(2, 3))
        self.Mp4MergeCMD(fileName + ".mp4", mp4Names)

    def DownLoadFile(self,fileName, DLURL):
        res = self.GetHttpBody(DLURL)
        f = open(fileName, 'wb+')
        try:
            f.write(res.content)
        finally:
            f.close()
    def GetHttpBody(self,url):
        for k in range(10):
            try:
                rt = self.ss.get(url)
                return rt
            except:
                self.ss.close()
                time.sleep(5)
                self.ss = requests.session()
    def GetSus(self,vid):
        rt=self.GetHttpBody("https://my.tv.sohu.com/play/videonew.do?vid={}&ver=1&ssl=1&referer=https%3A%2F%2Ftv.sohu.com%2Fv%2FcGwvOTQwNzQ1OS8xOTc3Mjk4MzYuc2h0bWw%3D.html&t=1667118432209".format(vid))
        rt = rt.content
        rt = rt.decode("utf-8")
        print(rt)
        sus = re.findall(r'"su":\["(.+?)\"]', rt)
        print(sus)
        return sus[0].split(r'","')
    def GetDLURL(self,su):
        rt = self.GetHttpBody("https://data.vod.itc.cn/ip?new={}&num=1&key=oOQd1--RfGTVlbizS3GNepyN-8nT5i4P&ch=my&pt=1&pg=2&prod=h5n&uid=16671081762955470875".format(su))
        rt = rt.content
        rt = rt.decode("utf-8")
        DLURL = re.findall(r'"url":"(.+?)"', rt)
        if DLURL:
            DLURL=DLURL[0]
        else:
            DLURL=None
        return DLURL
    def Mp4MergeCMD(self,videoName,mp4List):
        with open("concat_list.txt","w+", encoding='utf-8') as f:
            concatmp4List=''
            for i in mp4List:
                concatmp4List+= "file " + "'" + i + "'" + "\n"
            f.write(concatmp4List)
        cmd=r'ffmpeg -f concat -safe 0 -i concat_list.txt -c copy "{}"'.format(self.saveFilePath+videoName)
        print(cmd)
        os.system(cmd)
        os.remove("concat_list.txt")
        for file in mp4List:
            os.remove(file)
        pass

dlsh=downloadsouhu()
dlsh.DownLoadFile("aa",'magnet:?xt=urn:btih:D443E48ABD96C72340692767DD51FD79911F1172')
#dlsh.GetVidsAndRun()
# dlsh.Mp4Merge("南街村党委书记王宏斌汇报材料上---------.mp4",["南街村党委书记王宏斌汇报材料上0.mp4","南街村党委书记王宏斌汇报材料上1.mp4","南街村党委书记王宏斌汇报材料上2.mp4","南街村党委书记王宏斌汇报材料上3.mp4","南街村党委书记王宏斌汇报材料上4.mp4","南街村党委书记王宏斌汇报材料上5.mp4","南街村党委书记王宏斌汇报材料上6.mp4","南街村党委书记王宏斌汇报材料上7.mp4","南街村党委书记王宏斌汇报材料上8.mp4"])

# _*_ coding:utf-8 _*_
import subprocess
import sys, os
import re,csv,time
import threading
from AndroidDebugBridge import AndroidDebugBridge as myadb


class systeminfo():

    def __init__(self):
        self.cpudata = [("time", "cpu")]
        self.memdata = [("time", "vss", "rss")]

    # 执行子进程开启top命令
    def topprocess(self):
        cmd = "adb shell top -d 1|grep com.qihoo.livecloud.demo"
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return process

    # top命令执行结果 ，内容如下
    # 9653  4   0% S    45 1709668K 179188K  fg u0_a94   com.qihoo.livecloud.demo
    def topinfo(self, process):
        line = process.stdout.readline()
        topinfo = re.split("\s+", line.decode("utf-8", "strict").strip())
        return topinfo

    # 通过topinfo获取cpu的信息，开启timer一秒获取一次CPU信息
    def cpu_mem_info(self,process):

        topinfo = self.topinfo(process)
        currenttime = self.currenttime()
        print(currenttime)
        self.cpudata.append((currenttime, topinfo[2]))
        print(topinfo[2])
        self.memdata.append((currenttime, topinfo[5], topinfo[6]))
        print(topinfo[5], topinfo[5])

        global cmtimer
        cmtimer = threading.Timer(1.0, self.cpu_mem_info, [process])
        cmtimer.start()

    # 创建timer，每隔一秒读取CPU和内存信息。
    # 调用此方法获取CPU和内存信息。
    def ctimer(self,process):
        cmtimer = threading.Timer(1.0, self.cpu_mem_info, [process])
        cmtimer.start()

    # 退出timer，保存数据。
    def cputimercancel(self):
        cmtimer.cancel()
        self.saveinfo(self.cpudata, "cpuinfo")
        self.saveinfo(self.memdata, "meminfo")

    # 获取当前的时间戳
    def currenttime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def saveinfo(self, data, csvname):
        csvnamet = csvname + "%s" % int(time.time())
        csvresport_dir = "./csvreport"
        if not os.path.exists(csvresport_dir):
            os.makedirs(csvresport_dir)

        csvresport = csvresport_dir + "/" + csvnamet + '.csv'
        with open(csvresport, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)


if __name__ == '__main__':
    devices = myadb().attached_devices()
    if devices:

        sinfo = systeminfo()
        # 运行top命令
        process = sinfo.topprocess()
        # 获取CPU和内存信息
        sinfo.ctimer(process)
        time.sleep(5)
        # 退出并保存CPU和内存信息
        sinfo.cputimercancel()
    else:
        print("设备不存在")




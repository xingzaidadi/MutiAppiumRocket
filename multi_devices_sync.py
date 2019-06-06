import driver
import multiprocessing
from AndroidDebugBridge import AndroidDebugBridge as myadb

def muti_phones(port):
    # 构建desired进程租
    desired_process = []

    # 此处根据手机数量创建进程，后期将这个值注入
    phoneslist = myadb().phonesinfo_list()
    # 加载desied进程
    for i in range(2):  # len(phoneslist)

        port1 = port + 2 * i
        pinfo = phoneslist[i]
        desired = multiprocessing.Process(target=driver.appium_desired,
                                          args=(pinfo.platformsversion, pinfo.phonename, pinfo.udid, port1))
        desired_process.append(desired)
    return desired_process


def start_muti_phones(port):
    phones = muti_phones(port)
    # 启动多设备执行测试
    for desired in phones:
        desired.start()
    for desired in phones:
        desired.join()


if __name__ == '__main__':
    start_muti_phones(4723)


# _*_ coding:utf-8 _*_
import yaml
from appium import webdriver
import os


def appium_desired(platformVersion, deviceName, udid, port):
    with open('config/desired_caps.yaml', 'r', encoding='utf-8') as file:
        data = yaml.load(file)
        desired_caps = {}
        desired_caps['platformName'] = data['platformName']

        desired_caps['platformVersion'] = platformVersion
        desired_caps['deviceName'] = deviceName
        desired_caps['udid'] = udid
        # 此处是将APP放到了当前路径下，后续根据需求，有专门存放app的地方
        # base_dir = os.path.dirname(os.path.dirname(__file__))
        # app_path = os.path.join(base_dir, 'app', data['appname'])
        # desired_caps['app'] = app_path
        # print(base_dir)
        desired_caps['noReset'] = data['noReset']

        desired_caps['unicodeKeyboard'] = data['unicodeKeyboard']
        desired_caps['resetKeyboard'] = data['resetKeyboard']

        desired_caps['appPackage'] = data['appPackage']
        desired_caps['appActivity'] = data['appActivity']

        print('start run app...')
        driver = webdriver.Remote('http://' + str(data['ip']) + ':' + str(port) + '/wd/hub', desired_caps)

        driver.implicitly_wait(5)
        return driver


if __name__ == '__main__':
    appium_desired()

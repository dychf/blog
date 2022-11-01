#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
自动打卡脚本
"""
import json
import os
import random
import re
import time

import requests
from lxml import etree

session = requests.session()

# 指定某个域名不用代理去处理
os.environ['NO_PROXY'] = 'my.lzu.edu.cn'


def getSubmit(auToken, dailyCookie, info, now, FilledInfo):
    subApi = 'http://appservice.lzu.edu.cn/dailyReportAll/api/grtbMrsb/submit'
    subHeaders = {
        'Authorization': str(auToken),
        'Cookie': 'iPlanetDirectoryPro=' + str(dailyCookie)
    }
    FilledInfo = FilledInfo['data'][0]
    info_data = info['data']['list'][0]
    sfzx = info_data['sfzx'] if info_data['sfzx'] else FilledInfo['sfzx'],
    info_data = {
        "bh": info_data['bh'],  # 编号
        "xykh": info_data['xykh'],  # 校园卡号
        "twfw": "0",  # 体温范围(0为小于37.3摄氏度)
        "jkm": "0",  # 健康码
        "sfzx": sfzx[0],  # 是否在校(0离校，1在校)
        "sfgl": "0",  # 是否隔离(0正常，1隔离)
        # 所在省份（没有打卡记录则是基本信息中现所在省份）
        "szsf": info_data['szsf'] if info_data['szsf'] else FilledInfo['xszsf'],
        # 所在地级市（没有打卡记录则是基本信息中现所在地级市）
        "szds": info_data['szds'] if info_data['szds'] else FilledInfo['xszds'],
        # 所在县/区（没有打卡记录则是基本信息中现所在县/区）
        "szxq": info_data['szxq'] if info_data['szxq'] else FilledInfo['xszxq'],
        # 是否出国（没有打卡记录则是基本信息中是否出国）
        "sfcg": info_data['sfcg'] if info_data['sfcg'] else FilledInfo['sfcg'],
        # 出国地点（没有打卡记录则是基本信息中出国地点）
        "cgdd": info_data['cgdd'] if info_data['cgdd'] else FilledInfo['cgdd'],
        "gldd": "",  # 隔离地点
        "jzyy": "",  # 就诊医院
        "bllb": "0",  # 是否被列入(疑似/确诊)病例(0没有，其它为疑似/确诊)
        "sfjctr": "0",  # 是否接触他人(0否，1是)
        "jcrysm": "",  # 接触人员说明
        "xgjcjlsj": "",  # 相关接触经历时间
        "xgjcjldd": "",  # 相关接触经历2地点
        "xgjcjlsm": "",  # 相关接触经历说明
        "zcwd": round(random.uniform(36.3, 36.8), 1) if 7 <= now < 9 and sfzx[0] == "1" else (
            info_data['zcwd'] if info_data['zcwd'] else 0.0),
        # 早晨温度(体温)
        "zwwd": round(random.uniform(36.3, 36.8), 1) if 11 <= now < 13 and sfzx[0] == "1" else (
            info_data['zwwd'] if info_data['zcwd'] else 0.0),
        # 中午温度(体温)
        "wswd": round(random.uniform(36.3, 36.8), 1) if 19 <= now < 21 and sfzx[0] == "1" else (
            info_data['wswd'] if info_data['zcwd'] else 0.0),
        # 晚上温度(体温)
        "sbr": info_data['sbr'],  # 上报人
        "sjd": info['data']['sjd'],  # 时间段
        "initLat": "",
        "initLng": "",
        "dwfs": ""
    }

    res = session.post(subApi, info_data, headers=subHeaders).text
    return json.loads(res), info_data


def getST(dailyCookie):
    stApi = 'http://my.lzu.edu.cn/api/getST'
    stHeaders = {
        'Cookie': 'iPlanetDirectoryPro=' + str(dailyCookie)
    }
    stData = {
        'service': 'http://127.0.0.1'
    }
    stRes = session.post(stApi, stData, headers=stHeaders)
    stDic = json.loads(stRes.text)

    if stDic['state'] == 1:
        return str(stDic['data'])
    else:
        raise Exception("Error Getting ST-Token!")


def getAuthToken(stToken, cardID, dailyCookie):
    auApi = 'http://appservice.lzu.edu.cn/dailyReportAll/api/auth/login?st=' + \
            str(stToken) + '&PersonID=' + str(cardID)
    auHeader = {
        'Cookie': 'iPlanetDirectoryPro=' + str(dailyCookie)
    }
    auRes = session.get(auApi, headers=auHeader)
    auDic = json.loads(auRes.text)

    if auDic['code'] == 1:
        return str(auDic['data']['accessToken'])
    else:
        raise Exception("Getting AU-Token Failed!")


def getSeqMD5(cardID, auToken, dailyCookie):
    seqMD5Api = 'http://appservice.lzu.edu.cn/dailyReportAll/api/encryption/getMD5'
    seqMD5Header = {
        'Authorization': str(auToken),
        'Cookie': 'iPlanetDirectoryPro=' + str(dailyCookie)
    }
    seqMD5Data = {
        'cardId': str(cardID)
    }
    seqMD5Res = session.post(seqMD5Api, seqMD5Data, headers=seqMD5Header)
    seqMD5Dic = json.loads(seqMD5Res.text)

    if seqMD5Dic['code'] == 1:
        return str(seqMD5Dic['data'])
    else:
        raise Exception("Getting card-Enc-MD5 Failed!")


def getSeqInfo(cardID, cardMD5, auToken):
    seqInfoApi = 'http://appservice.lzu.edu.cn/dailyReportAll/api/grtbMrsb/getInfo'
    seqInfoHeader = {
        'Authorization': str(auToken)
    }
    seqInfoData = {
        'cardId': str(cardID),
        'md5': str(cardMD5)
    }
    seqInfoRes = session.post(seqInfoApi, seqInfoData, headers=seqInfoHeader)
    seqInfoDic = json.loads(seqInfoRes.text)

    return seqInfoDic


def getFilledInfo(cardID, cardMD5, auToken):
    FilledInfoApi = 'http://appservice.lzu.edu.cn/dailyReportAll/api/grtbJcxxtb/getInfo'
    FilledInfoHeader = {
        'Authorization': str(auToken)
    }
    FilledInfoData = {
        'cardId': str(cardID),
        'md5': str(cardMD5)
    }
    FilledInfoRes = session.post(
        FilledInfoApi, FilledInfoData, headers=FilledInfoHeader)
    FilledInfoDic = json.loads(FilledInfoRes.text)
    if FilledInfoDic['code'] == 1:
        return FilledInfoDic
    else:
        raise Exception("Error Getting Sequence-Number!")


def getDailyToken(user, password):
    login_url = 'http://my.lzu.edu.cn:8080/login?service=http://my.lzu.edu.cn'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4385.0 Safari/537.36',
    }
    response = session.get(login_url, headers=header)
    tree = etree.HTML(response.text)
    lt = tree.xpath("//*[@id='loginForm']/div[3]/div[2]/input[2]/@value")
    execution = tree.xpath(
        "//*[@id='loginForm']/div[3]/div[2]/input[3]/@value")
    eventId = tree.xpath("//*[@id='loginForm']/div[3]/div[2]/input[4]/@value")
    captcha = tree.xpath("//*[@id='loginForm']/div[3]/div[2]/input[5]/@value")
    formData = {
        'username': user,
        'password': password,
        'lt': lt,
        'execution': execution,
        '_eventId': eventId,
        'captcha': captcha
    }
    response = session.post(login_url, formData,
                            headers=header, allow_redirects=False)
    if response.status_code != 302:
        raise Exception("用户名或密码错误.")
    else:
        wrongurl = response.headers['location']
        if not "/?" in wrongurl:
            wrongurl = wrongurl.replace("?", "/?")
        response = session.post(wrongurl, headers=header)
        if not (user.isdigit() and len(user) == 12):
            user = ''.join(re.findall(
                r"var personId = '(.+?)';", response.text))
        dayCok = requests.utils.dict_from_cookiejar(
            session.cookies)['iPlanetDirectoryPro']
        return dayCok, user


def submitCard(cardID, passwd):
    timeStamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    dayCok, cardID = getDailyToken(cardID, passwd)
    ST = getST(dayCok)
    AuToken = getAuthToken(ST, cardID, dayCok)
    MD5 = getSeqMD5(cardID, AuToken, dayCok)
    info = getSeqInfo(cardID, MD5, AuToken)
    FilledInfo = getFilledInfo(cardID, MD5, AuToken)
    if info['code'] != 1:
        raise Exception(str(timeStamp) + " 未知错误，无法打卡!")
    now = int(time.strftime("%H", time.localtime()))
    response, info_data = getSubmit(AuToken, dayCok, info, now, FilledInfo)
    if response['code'] == 1:
        return True
    else:
        raise Exception(str(timeStamp) + "打卡失败, " + str(response))


def run_auto_punch_lzu(username, password, retry=4):
    try:
        for i in range(retry):
            if submitCard(username, password):
                return time.strftime("%Y-%m-%d %H:%M", time.localtime()) + ' 打卡成功'
        return time.strftime("%Y-%m-%d %H:%M", time.localtime()) + ' 打卡失败'
    except Exception as e:
        return "打卡失败 " + str(e)


if __name__ == '__main__':
    print(run_auto_punch_lzu("caihf20", "feng@1012"))

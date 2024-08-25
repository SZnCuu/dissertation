import csv

import requests
import json
from loguru import logger


def write(data, path):
    if data:
        with open(path + '.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerows(data)


def get(page):
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://www.beijingweilao.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.beijingweilao.cn/pensionService/organizationCare",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "accept": "application/json",
        "authorization": "undefined",
        "content-type": "application/json",
        "portal-auth": "portal",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "wzws_sessionid": "gmE1NTZkZKBmO3GVgTljMWNlMoAxNzEuOTUuODEuMjIx",
        "qimo_seosource_0": "%E7%AB%99%E5%86%85",
        "qimo_seokeywords_0": "",
        "uuid_047b2b10-d9cc-11ed-ad9f-6dcc2f6692f1": "c14199ac-460f-47a4-a8c3-98a5b0c9325b",
        "qimo_seosource_047b2b10-d9cc-11ed-ad9f-6dcc2f6692f1": "%E7%AB%99%E5%86%85",
        "qimo_seokeywords_047b2b10-d9cc-11ed-ad9f-6dcc2f6692f1": "",
        "qimo_xstKeywords_047b2b10-d9cc-11ed-ad9f-6dcc2f6692f1": "",
        "href": "https%3A%2F%2Fwww.beijingweilao.cn%2FpensionService%2ForganizationCare",
        "accessId": "047b2b10-d9cc-11ed-ad9f-6dcc2f6692f1",
        "pageViewNum": "1"
    }
    url = "https://www.beijingweilao.cn/prod-api/api/v1/portal/organInfo/getOrganInfoList"
    data = {
        "pageNum": page,
        "pageSize": 10,
        "searchValue": None,
        "provinceCode": "110000",
        "countyIds": None,
        "stationTypes": None,
        "bedTotals": None,
        "receiveRanges": None,
        "medicalInstitutionNames": None,
        "receivingElderlyType": None,
        "applyStar": None,
        "locationStar": None,
        "environmentStar": None,
        "facilityStar": None,
        "chargesDietLow": None,
        "chargesDietHigh": None,
        "chargesBedLow": None,
        "chargesBedHigh": None,
        "hasBed": "",
        "isSort": 0,
        "hlObjects": None,
        "bedObjects": None,
        "cfObjects": None,
        "streetRequestList": None,
        "isActivity": None,
        "totalObjects": None,
        "provinceIds": [
            "110000"
        ]
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    return response.json()


def info(address):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://maplocation.sjfkai.com/",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "BAIDUID_BFESS": "D5880B10569F5F8EBA97220753A0E918:FG=1",
        "ab_sr": "1.0.1_YjU4NzkyNTI2ZmEwNDdiYTQ2Y2Y0ZDFkYWQ4Y2Y0Y2MwZWQ3YzZlMzhjZTAxYjgyYmIwMTlkYzBiZWY1Yjk5N2FhZTVjODZhZDgxZjAwMzY5NmNiNTI2ODgxZmNkOWU4ZWY4MTZjMmRjM2UyM2FiMmExMDY0YTNhODI1Mjk2MzY0OWE4ODI4MDU3ZGY4ZjA0YmI5YTlkOGNiNzg0MGUyNQ=="
    }
    url = "https://api.map.baidu.com/geocoder/v2/"
    params = {
        "address": address,
        "output": "json",
        "ak": "gQsCAgCrWsuN99ggSIjGn5nO",
        "callback": "showLocation1"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    return json.loads(response.text[len("showLocation1&&showLocation1("):-1])


for page in range(3, 56):
    od = []
    logger.info(page)
    resp = get(page)
    for item in resp['data']['list']:
        info_resp = info(item['address'])
        info_resp = info_resp['result']['location']
        data = {
            "名称": item['sfInstitutionName'],
            "地址": item['address'],
            "最低总费用": f"{item['chargesBedLow'] + item['minamount'] + item['chargesDietLow']}",
            "最低高总费用": f"{item['chargesBedHigh'] + item['maxamount'] + item['chargesDietHigh']}",
            "床位数": item['bedTotal'],
            "经度": info_resp['lng'],
            "纬度": info_resp['lat'],
            "详情链接": f"https://www.beijingweilao.cn/pensionService/orgDetail/100-{item['organId']}-1"
        }
        print(data)
        od.append(data)
    write(od, 'data')

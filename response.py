import requests
url = "https://www.brownsfashion.com/uk/api/listing/woman/bags?pageIndex=2&pageSize=120"
header = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en,zh;q=0.9,zh-CN;q=0.8",
    # "cookie": "__cfduid=d36ba894ecb46a06d823f120c71851bf51616679328; ctx=%7b%22u%22%3a5000004409363322%2c%22g%22%3a1%7d; ss=Vt10qf69rSsd-b5Lw9WfTj0Wws1j5PYHhQP85BGseVdngoiVNF0fKIUC9E19n1Zolzk0CiVAx2ZxLyr0Ft66xEJw5UakLx7qDNvZmHUNnPEGPFcgdAY5cETgqdrQQWXm8Mhg2ktqMZ0lWsXiH8oi3Rx6Pg8OWR9yaLqdR4fJAAu-_dI6UMucRK6qi33i8KBYtckLBb2qU85Z5fuNbwa5gojNJwX8p5Aj82t33ebU2VM; benefit=264CBB89ED4B5B752363C1AAF409FF; csi=97ab2872-3cb3-45e0-9b79-c3f04b4b1cdb; dfUserSub=%2Fuk; cf_chl_2=ccc8f45ba2f2e91; cf_chl_prog=a19; cf_clearance=79905a15062d754b15f2868f1a23024495588804-1616679442-0-250; optimizelyEndUserId=oeu1616679451678r0.6018233757314677; gender=0; ftr_ncd=6; _gcl_au=1.1.542951876.1616679463; _ga=GA1.2.1697155601.1616679463; _gid=GA1.2.1186381844.1616679463; tms_VisitorID=h60ygx7ljg; tms_wsip=1; _hjTLDTest=1; _hjid=716584ae-d9f4-4cbd-8747-4bd1537de3de; _hjFirstSeen=1; _hjAbsoluteSessionInProgress=1; __cfruid=728ac248927df3c908c26485820cd658cfe494cd-1616679464; _pin_unauth=dWlkPU9UWTFZamRrTWpNdFpHSTROQzAwTXpBMExUazVZMkV0TVdGaE1HSmtNalZrTldNMg; _gat_UA-699627-7=1; _uetsid=46ee93008d6f11eba9f11f24af4c8b95; _uetvid=46eea0e08d6f11eb8b7f5165d4c80311; forterToken=c8f79b99baaf4293a1faf06c372f7004_1616680309764__UDF43_9ck; __cf_bm=de5f1a26482ba8b6b07ce79314592874c487458c-1616680324-1800-AZ47yVTG7FXvt/pGOzzzImhHX/1a5YEsegddjmlbOJN/5ZAIedOdYbYRE/UHo8omED6Mmng6xz8v0Qg9mt+A0Q0LlWlpGZ3NyACTLuKs4KBXOzZROZhmht1YezaZSJKxdjDSO9Oem7ti7sWxfTzqLKCQyPiKXabc2KQ8jEMTEJST",
    "referer": "https://www.brownsfashion.com/",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "x-newrelic-id": "VQUCV1ZUGwIFVlBRDgcA",
    "x-requested-with": "XMLHttpRequest",
    "authority": "www.brownsfashion.com",
    "method": "GET",
    "path": "/uk/api/listing/woman/bags?pageIndex=2&pageSize=120",
    "scheme": "https",
}
response = requests.get(url=url, headers=header)
print(response.text)

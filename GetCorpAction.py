import requests

url = 'https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?pageno=1&strCat=Corp.+Action&strPrevDate=20230331&strScrip=&strSearch=P&strToDate=20230331&strType=C'
response = requests.get(url, headers={"content-type":"application/json; charset=utf-8"})
print(response.text)
import requests
import time
import hashlib
import hmac
from pybit.unified_trading import HTTP
import pandas as pd

session = HTTP()

api_key = 'eRNnVF3xj4sqnzhq0h'
api_secret = '7a3Lu6t74jrcVfPhd0kxVtC0FjeVxlY8bbVj'
uid = "2845670"

def generate_signature(timestamp, api_key, recv_window, payload):
    param_str = f"{timestamp}{api_key}{recv_window}{payload}"
    signature = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
    return signature

timestamp = str(session.get_server_time().get('time'))
recv_window = str(5000)

endpoint = '/v5/user/aff-customer-info'
payload = f"uid={uid}"
url = f"https://api.bybit.com{endpoint}?{payload}"

headers = {
    'Host': 'api.bybit.com',
    'X-BAPI-API-KEY': api_key,
    'X-BAPI-TIMESTAMP': timestamp,
    'X-BAPI-RECV-WINDOW': recv_window,
    'Content-Type': 'application/json',
}

headers['X-BAPI-SIGN'] = generate_signature(timestamp, api_key, recv_window, payload)

response = requests.get(url, headers=headers)

json_data = response.json()
data = json_data.get('result')

userID = data.get('uid')
vipLevel = data.get('vipLevel')
depositAmount30Day = data.get('depositAmount30Day')
depositAmount365Day = data.get('depositAmount365Day')
totalWalletBalance = data.get('totalWalletBalance')
depositUpdateTime = data.get('depositUpdateTime')
volUpdateTime = data.get('volUpdateTime')
tradeVol30Day = data.get('tradeVol30Day')
tradeVol365Day = data.get('tradeVol365Day')

print(response.json())

df = pd.DataFrame({
    'UID': [userID],
    'VIP Level': [vipLevel],
    'Deposit Amount (30 Day)': [depositAmount30Day],
    'Deposit Amount (365 Day)': [depositAmount365Day],
    'Total Wallet Balance': [totalWalletBalance],
    'Deposit Update Time': [depositUpdateTime],
    'Vol Update Time': [volUpdateTime],
    'Trade Volume (30 Day)': [tradeVol30Day],
    'Trade Volume (365 Day)': [tradeVol365Day],
})

output_path = '出力.xlsx'
df.to_excel(output_path, index=False)
print(f'Data exported to {output_path}')
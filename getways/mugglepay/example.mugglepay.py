import json
import sqlite3
import requests


# mugglepay密钥
TOKEN = ''

# 支付后返回地址
RETURN_URL = "https://baidu.com"


def submit(money, name, trade_id):
    header = {
        "token": TOKEN
    }
    data = {'merchant_order_id': trade_id, 'price_amount': money, 'price_currency': 'CNY', 'success_url': RETURN_URL,
            'title': name}
    print(data)
    try:
        req = requests.post('https://api.mugglepay.com/v1/orders', headers=header, data=data)
        rst_dict = json.loads(req.text)
        if rst_dict['status'] == 201:
            pay_url = rst_dict['payment_url']
            return_data = {
                'status': 'Success',
                'type': 'url',
                'out_trade_no': rst_dict['order']['order_id'],
                'data': pay_url,
            }
            return return_data
        else:
            return_data = {
                'status': 'Failed',
                'data': rst_dict['error']
            }
            return return_data
    except Exception as e:
        print('submit | API请求失败')
        print(e)
        return_data = {
            'status': 'Failed',
            'data': 'API请求失败'
        }
        return return_data


def query(trade_id):
    conn = sqlite3.connect('faka.sqlite3')
    cursor = conn.cursor()
    cursor.execute('select out_trade_no from trade where trade_id=?', (trade_id,))
    order_id = cursor.fetchone()[0]
    conn.close()
    print(order_id)
    header = {
        "token": TOKEN
    }
    try:
        req = requests.get('https://api.mugglepay.com/v1/orders/{}'.format(order_id, ), headers=header)
        rst_dict = json.loads(req.text)
        print(rst_dict)
        if rst_dict['status'] == 200:
            pay_status = str(rst_dict['order']['status'])
            if pay_status == 'PAID':
                print('支付成功')
                return '支付成功'
            else:
                print('支付失败')
                return '支付失败'
        else:
            print('查询失败，订单号不存在')
            return '查询失败，订单号不存在'
    except Exception as e:
        print(e)
        print('mugglepay | 查询请求失败')
        return 'API请求失败'


def cancel(trade_id):
    print('订单已经取消')

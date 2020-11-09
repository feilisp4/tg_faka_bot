from alipay import AliPay

'''
请前往 开放平台 https://openhome.alipay.com/ 注册自研服务应用 ｜ 注意：不要注册第三方应用，权限不足
路径：我的应用>自研服务>网页&移动应用
1、添加当面付能力
2、接口加签方式：公钥>填写自己生成的应用公钥 (RSA2)
3、配置下面的信息，大功告成！
'''

# 配置区域

# appid
appid="2017030405672123"

# 应用私钥
app_private_key_string = "-----BEGIN RSA PRIVATE KEY-----\n填写自己生成的应用密钥\n-----END RSA PRIVATE KEY-----"

# 支付宝公钥，验证支付宝回传消息使用，不是你自己的公钥,
alipay_public_key_string = "-----BEGIN PUBLIC KEY-----\n填写支付宝公钥\n-----END PUBLIC KEY-----"

# 示例格式 注意\n
# alipay_public_key_string = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw9QbJi++cm2HjinPpllj3Hmep8nxO9MVu0BTSP1XM1wF666g6sTwQ0VXyRJENpYEs0KFE/XnMKilV/+uQY7xH4SqcdX2T4C5DkiWJ4egD2Tk3yLH6fjq7TqCsMqG3osfk6U93H+XdiWKKff+nwQ6LnUIEYWoMIh/fyqTYtlKzBTUg8nJWoqfkspFWlt69PrbosbAFWY7vp+3CapO/o4Qw+thuhGKAvEZWmNy3hUnnThStos+T8qI/Qqs5f9zb9wIDAQAB\n-----END PUBLIC KEY-----"

# 订单超时时间
# m：分钟，只可为整数，建议与config配置的超时时间一致
PAY_TIMEOUT = '5m'

try:
    alipay = AliPay(
        appid=appid,
        app_notify_url=None,  # 默认回调url，不要改
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
    )
except Exception as e:
    print(e)
    print('Alipay对象创建失败，请检查公钥和密钥是否配置正确')


def submit(price, subject, trade_id):
    try:
        order_string = alipay.api_alipay_trade_precreate(
            subject=subject,
            out_trade_no=trade_id,
            total_amount=price,
            qr_code_timeout_express=PAY_TIMEOUT
        )
        print(order_string)
        if order_string['msg'] == 'Success':
            qr_code = order_string['qr_code']
            print(qr_code)
            return_data = {
                'status': 'Success',
                'type': 'qr_code',  # url / qr_code
                'data': 'http://api.qrserver.com/v1/create-qr-code/?data={}&bgcolor=FFFFCB'.format(qr_code)     # 自行对接二维码API
            }
            return return_data
        else:
            print(order_string['msg'])
            return_data = {
                'status': 'Failed',
                'data': 'API请求失败'
            }
            return return_data
    except Exception as e:
        print(e)
        print('支付宝当面付API请求失败')
        return_data = {
            'status': 'Failed',
            'data': 'API请求失败'
        }
        return return_data


def query(out_trade_no):
    try:
        result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            print(str(result))
            print('支付宝当面付｜用户支付成功')
            return '支付成功'
        else:
            print(str(result))
            print('支付宝当面付｜用户支付失败')
            return '支付失败'
    except Exception as e:
        print(e)
        print(str(result))
        print('支付宝当面付｜请求失败')
        return 'API请求失败'


def cancel(out_trade_no):
    try:
        alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)
    except Exception as e:
        print(e)
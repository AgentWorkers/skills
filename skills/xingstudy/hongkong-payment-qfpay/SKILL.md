---
name: HONGKONG-PAYMENT-QFPAY
description: QFPay API 是一个全面的支付解决方案，提供了多种支付方式以满足不同企业的需求。本文档提供了完整的 API 集成指南，包括环境配置、请求格式、签名生成、支付类型、支持的货币以及状态码等内容。
--- 

# QFPay支付API技能

## 概述

QFPay API是一个全面的支付解决方案，提供多种支付方式以满足不同企业的需求。本文档提供了完整的API集成指南，包括环境配置、请求格式、签名生成、支付类型、支持的货币和状态码等内容。

## 环境配置

QFPay API可以通过三种主要环境进行访问：

| 环境 | 基本URL | 描述 |
|-------------|----------|-------------|
| 沙盒环境 | `https://openapi-int.qfapi.com` | 用于模拟支付，不涉及实际资金扣款 |
| 测试环境 | `https://test-openapi-hk.qfapi.com` | 支持实际支付流程，但连接到测试账户（不进行结算） |
| 生产环境 | `https://openapi-hk.qfapi.com` | 支持实际支付并完成结算 |

**重要说明：**
- 在测试环境中使用测试账户进行的交易不会进行结算。
- 确保测试交易立即触发退款。
- 不要在不同环境之间混合使用凭证或端点，否则会导致签名或授权错误。

### 环境变量设置

在使用API之前，请配置以下环境变量：

```bash
export QFPAY_APPCODE="your_app_code_here"
export QFPAY_KEY="your_client_key_here"
export QFPAY_MCHID="your_merchant_id"  # Optional, depends on account setup
export QFPAY_ENV="sandbox"  # Options: prod, test, sandbox
```

## API使用指南

### 速率限制

为确保公平使用和最佳性能：
- **限制**：每秒最多100个请求（RPS），每个商家每分钟最多400个请求。
- **超出限制**：API会返回HTTP 429（请求过多）错误。

### 最佳实践
1. **批量请求**：使用批量处理来减少单个请求的数量。
2. **高效查询**：利用过滤和分页功能。
3. **缓存**：实现响应缓存以避免重复请求。
4. **监控**：跟踪API使用情况并记录请求模式。

### 错误处理

当收到HTTP 429错误时：
1. 暂停进一步的请求一段时间。
2. 实施指数级退避策略进行重试。
3. 记录错误以便监控。

### 流量峰值管理

对于预期的流量峰值（例如促销活动），请联系：
- **技术支持**：technical.support@qfpay.com

## 请求格式

### HTTP请求

```
POST /trade/v1/payment
```

### 公共支付请求参数

| 参数 | 是否必填 | 类型 | 描述 |
|-----------|----------|------|-------------|
| `txamt` | 是 | Int(11) | 交易金额（单位：分，100分等于1元）。建议金额大于200分以避免风险控制 |
| `txcurrcd` | 是 | String(3) | 交易货币。详见“货币”部分 |
| `pay_type` | 是 | String(6) | 支付类型代码。详见“支付类型”部分 |
| `out_trade_no` | 是 | String(128) | 外部交易编号。每个商家账户必须唯一 |
| `txdtm` | 是 | String(20) | 交易时间格式：YYYY-MM-DD hh:mm:ss |
| `auth_code` | 是（仅限CPM） | String(128) | 用于扫描条形码/二维码的授权码。有效期为1天 |
| `expired_time` | 否（仅限MPM） | String(3) | 二维码的有效时间（单位：分钟）。默认值：30分钟，最小值：5分钟，最大值：120分钟 |
| `goods_name` | 否 | String(64) | 商品描述。最多20个字符，支持UTF-8编码（中文）。应用支付时必需 |
| `mchid` | 否 | String(16) | 商家ID。如果已分配，则必须提供；否则不要包含 |
| `udid` | 否 | String(40) | 唯一的设备ID，用于内部跟踪 |
| `notify_url` | 否 | String(256) | 异步支付通知的URL |

### HTTP头部要求

| 字段 | 是否必填 | 描述 |
|-------|----------|-------------|
| `X-QF-APPCODE` | 是 | 分配给商家的应用代码 |
| `X-QF-SIGN` | 是 | 根据签名算法生成的签名 |
| `X-QF-SIGNTYPE` | 否 | 签名算法。使用`SHA256`，默认为`MD5` |

### 内容规范
- **字符编码**：UTF-8
- **方法**：POST/GET（取决于端点）
- **Content-Type**：application/x-www-form-urlencoded

## 响应格式

### 成功响应结构

```json
{
  "respcd": "0000",
  "respmsg": "success",
  "data": {
    "txamt": "100",
    "out_trade_no": "20231101000001",
    "txcurrcd": "HKD",
    "txstatus": "SUCCESS",
    "qf_trade_no": "9000020231101000001",
    "pay_type": "800101",
    "txdtm": "2023-11-01 10:00:00"
  }
}
```

### 响应字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `respcd` | String(4) | 返回代码。“0000”表示成功 |
| `respmsg` | String(64) | `respcd`的消息描述 |
| `data` | Object | 支付交易数据 |

### 数据对象字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `txamt` | String | 交易金额（单位：分） |
| `out_trade_no` | String | 商家的原始订单编号 |
| `txcurrcd` | String | 货币代码（例如：HKD） |
| `txstatus` | String | 支付状态：SUCCESS, FAILED, PENDING |
| `qf_trade_no` | String | QFPay的唯一交易编号 |
| `pay_type` | String | 支付方式代码 |
| `txdtm` | String | 支付时间（格式：YYYY-MM-DD HH:mm:ss） |

### 签名验证

响应可能包含`X-QF-SIGN`和`X-QF-SIGNTYPE`头部。验证方法如下：
1. 按字母顺序提取数据字段。
2. 将它们拼接成键值对的形式（例如：key1=value1&key2=value2&...）。
3. 添加客户端密钥。
4. 生成MD5哈希值并进行比较。

## 签名生成

所有API请求必须在HTTP头部包含数字签名：

```
X-QF-SIGN: <your_signature>
```

### 分步指南

#### 第1步：按参数名称排序

将所有请求参数按ASCII升序排序。

**示例：**

| 参数 | 值 |
|-----------|-------|
| `mchid` | `ZaMVg12345` |
| `txamt` | `100` |
| `txcurrcd` | `HKD` |

排序后的结果：
```
mchid=ZaMVg12345&txamt=100&txcurrcd=HKD
```

#### 第2步：添加客户端密钥

将您的秘密`client_key`添加到字符串中。

如果`client_key = abcd1234`：
```
mchid=ZaMVg12345&txamt=100&txcurrcd=HKDabcd1234
```

#### 第3步：生成哈希值

使用MD5或SHA256（推荐使用SHA256）生成哈希值：

```
SHA256("mchid=ZaMVg12345&txamt=100&txcurrcd=HKDabcd1234")
```

#### 第4步：添加到头部

```
X-QF-SIGN: <your_hashed_signature>
```

### 重要说明
- 不要插入换行符、制表符或额外的空格。
- 参数名称和值是区分大小写的。
- 如果签名失败，请仔细检查参数顺序和编码。

### 代码示例

#### Python示例

```python
import os
import hashlib

APPCODE = os.getenv('QFPAY_APPCODE')
KEY = os.getenv('QFPAY_KEY')

def generate_signature(params, key):
    """Generate MD5 signature"""
    keys = list(params.keys())
    keys.sort()
    query = []
    for k in keys:
        if k not in ('sign', 'sign_type') and (params[k] or params[k] == 0):
            query.append(f'{k}={params[k]}')
    
    data = '&'.join(query) + key
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest().upper()

def generate_signature_sha256(params, key):
    """Generate SHA256 signature"""
    keys = list(params.keys())
    keys.sort()
    query = []
    for k in keys:
        if k not in ('sign', 'sign_type') and (params[k] or params[k] == 0):
            query.append(f'{k}={params[k]}')
    
    data = '&'.join(query) + key
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest().upper()
```

## 支付类型

`pay_type`参数指定了要使用的支付方式。这会影响交易路由和用户界面要求。

**注意**：并非所有`pay_type`值都适用于所有商家。如有疑问，请联系technical.support@qfpay.com。

### 支持的支付类型

| 代码 | 描述 |
|------|-------------|
| 800008 | WeChat支付、Alipay支付、UnionPay QuickPass、PayMe |
| 800101 | Alipay MPM（海外商家） |
| 800108 | Alipay CPM（海外及香港商家） |
| 801101 | Alipay Web支付（海外） |
| 801107 | Alipay WAP支付（海外） |
| 801110 | Alipay应用内支付（海外） |
| 800107 | Alipay服务窗口H5支付 |
| 801501 | Alipay MPM（香港商家） |
| 801510 | Alipay应用内支付（香港商家） |
| 801512 | Alipay WAP支付（香港商家） |
| 801514 | Alipay Web支付（香港商家） |
| 800201 | WeChat MPM（海外及香港） |
| 800208 | WeChat CPM（海外及香港） |
| 800207 | WeChat JSAPI支付（海外及香港） |
| 800212 | WeChat H5支付 |
| 800210 | WeChat应用内支付（海外及香港） |
| 800213 | WeChat小程序支付 |
| 801008 | WeChat Pay（香港）CPM（直接结算） |
| 801010 | WeChat Pay（香港）应用内支付（直接结算） |
| 805801 | PayMe MPM（香港商家） |
| 805808 | PayMe CPM（香港商家） |
| 805814 | PayMe Web支付（香港商家） |
| 805812 | PayMe WAP支付（香港商家） |
| 800701 | UnionPay QuickPass MPM |
| 800708 | UnionPay QuickPass CPM |
| 800712 | UnionPay WAP支付（香港） |
| 800714 | UnionPay PC-Web支付（香港） |
| 802001 | FPS MPM（香港商家） |
| 803701 | Octopus MPM（香港商家） |
| 803712 | Octopus WAP支付（香港） |
| 803714 | Octopus PC-Web支付（香港） |
| 802801 | Visa / Mastercard在线支付 |
| 802808 | Visa / Mastercard离线支付 |
| 806527 | ApplePay在线支付 |
| 806708 | UnionPay卡离线支付 |
| 806808 | American Express卡离线支付 |

### 特殊说明
- **801101**：交易金额必须大于1港元。
- **802001**：此支付方式不支持退款。

## 支持的货币

所有货币代码均遵循ISO 4217格式（3个大写字母）：

| 代码 | 描述 |
|------|-------------|
| AED | 阿联酋迪拉姆 |
| CNY | 人民币 |
| EUR | 欧元 |
| HKD | 港元 |
| IDR | 印度尼西亚卢比 |
| JPY | 日元 |
| MMK | 缅甸缅元 |
| MYR | 马来西亚林吉特 |
| SGD | 新加坡元 |
| THB | 泰国铢 |
| USD | 美元 |
| CAD | 加元 |
| AUD | 澳元 |

**注意**：某些支付方式可能仅支持港元。在处理非港元交易前，请与您的集成管理员确认。

## 状态码

QFPay API返回的标准`respcd`值：

| 代码 | 描述 |
|------|-------------|
| 0000 | 交易成功 |
| 1100 | 系统维护中 |
| 1101 | 反向错误 |
| 1102 | 重复请求 |
| 1103 | 请求格式错误 |
| 1104 | 请求参数错误 |
| 1105 | 设备未激活 |
| 1106 | 设备无效 |
| 1107 | 设备不允许使用 |
| 1108 | 签名错误 |
| 1125 | 交易已退款 |
| 1136 | 交易不存在或无法操作 |
| 1142 | 订单已关闭 |
| 1143 | 订单未支付，正在输入密码 |
| 1145 | 正在处理，请稍候 |
| 1147 | WeChat Pay交易错误 |
| 1150 | T0支付方式不支持取消 |
| 1155 | 退款请求被拒绝 |
| 1181 | 订单已过期 |
| 1201 | 账户余额不足 |
| 1202 | 支付代码错误或已过期 |
| 1203 | 商家账户错误 |
| 1204 | 银行错误 |
| 1205 | 交易失败，请稍后再试 |
| 1212 | 请使用UnionPay海外支付代码 |
| 1241 | 商店不存在或状态不正确 |
| 1242 | 商店配置不正确 |
| 1243 | 商店已被禁用 |
| 1250 | 交易被禁止 |
| 1251 | 商店配置错误 |
| 1252 | 系统错误，无法提交订单 |
| 1254 | 出现问题，正在解决 |
| 1260 | 订单已支付 |
| 1261 | 订单未支付 |
| 1262 | 订单已退款 |
| 1263 | 订单已取消 |
| 1264 | 订单已关闭 |
| 1265 | 交易无法退款（晚上11:30至凌晨0:30） |
| 1266 | 交易金额错误 |
| 1267 | 订单信息不匹配 |
| 1268 | 订单不存在 |
| 1269 | 未结算余额不足，无法退款 |
| 1270 | 该货币不支持部分退款 |
| 1271 | 交易不支持部分退款 |
| 1272 | 退款金额超过最大退款限额 |
| 1294 | 交易不符合规定，银行禁止 |
| 1295 | 连接缓慢，请稍后再试 |
| 1296 | 连接缓慢，请稍后再试 |
| 1297 | 银行系统繁忙 |
| 1298 | 连接缓慢，如果已支付请勿重复支付 |
| 2005 | 客户支付代码错误或已过期 |
| 2011 | 交易序列号重复 |

## 使用示例

### 完整支付流程（Python示例）

```python
import os
import requests
import hashlib
import datetime
import time

# Load configuration from environment variables
APPCODE = os.getenv('QFPAY_APPCODE')
KEY = os.getenv('QFPAY_KEY')
MCHID = os.getenv('QFPAY_MCHID')
ENV = os.getenv('QFPAY_ENV', 'test')

# Environment URLs
ENV_URLS = {
    'prod': 'https://openapi-hk.qfapi.com',
    'test': 'https://test-openapi-hk.qfapi.com',
    'sandbox': 'https://openapi-int.qfapi.com'
}

BASE_URL = ENV_URLS.get(ENV, ENV_URLS['test'])

def generate_signature(params, key, sign_type='SHA256'):
    """Generate signature for QFPay API request"""
    keys = list(params.keys())
    keys.sort()
    query = []
    for k in keys:
        if k not in ('sign', 'sign_type') and (params[k] or params[k] == 0):
            query.append(f'{k}={params[k]}')
    
    data = '&'.join(query) + key
    
    if sign_type == 'SHA256':
        sha256 = hashlib.sha256()
        sha256.update(data.encode('utf-8'))
        return sha256.hexdigest().upper()
    else:
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        return md5.hexdigest().upper()

def create_payment(amount, currency, pay_type, goods_name, notify_url=None):
    """Create a payment request"""
    params = {
        'txamt': str(amount),
        'txcurrcd': currency,
        'pay_type': pay_type,
        'out_trade_no': f"ORDER{int(time.time() * 10000)}",
        'txdtm': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'goods_name': goods_name
    }
    
    if MCHID:
        params['mchid'] = MCHID
    
    if notify_url:
        params['notify_url'] = notify_url
    
    signature = generate_signature(params, KEY)
    
    headers = {
        'X-QF-APPCODE': APPCODE,
        'X-QF-SIGN': signature,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(
        f'{BASE_URL}/trade/v1/payment',
        data=params,
        headers=headers
    )
    
    return response.json()

def query_transaction(out_trade_no):
    """Query transaction status"""
    params = {
        'out_trade_no': out_trade_no,
        'txdtm': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if MCHID:
        params['mchid'] = MCHID
    
    signature = generate_signature(params, KEY)
    
    headers = {
        'X-QF-APPCODE': APPCODE,
        'X-QF-SIGN': signature,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(
        f'{BASE_URL}/trade/v1/query',
        data=params,
        headers=headers
    )
    
    return response.json()

def refund_transaction(out_trade_no, txamt, qf_trade_no=None):
    """Process a refund"""
    params = {
        'out_trade_no': out_trade_no,
        'txamt': str(txamt),
        'txdtm': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if qf_trade_no:
        params['qf_trade_no'] = qf_trade_no
    
    if MCHID:
        params['mchid'] = MCHID
    
    signature = generate_signature(params, KEY)
    
    headers = {
        'X-QF-APPCODE': APPCODE,
        'X-QF-SIGN': signature,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(
        f'{BASE_URL}/trade/v1/refund',
        data=params,
        headers=headers
    )
    
    return response.json()

# Example usage
if __name__ == '__main__':
    # Create a payment
    result = create_payment(
        amount=100,  # $1.00 HKD
        currency='HKD',
        pay_type='800101',
        goods_name='Test Product'
    )
    print(f"Payment created: {result}")
    
    if result.get('respcd') == '0000':
        out_trade_no = result['data']['out_trade_no']
        
        # Query transaction
        query_result = query_transaction(out_trade_no)
        print(f"Transaction status: {query_result}")
```

### 多个商家的环境配置

```python
import os

# Configuration loader from environment
class QFPayConfig:
    def __init__(self, env='sandbox'):
        self.env = env
        self.appcode = os.getenv(f'QFPAY_{env.upper()}_APPCODE') or os.getenv('QFPAY_APPCODE')
        self.key = os.getenv(f'QFPAY_{env.upper()}_KEY') or os.getenv('QFPAY_KEY')
        self.mchid = os.getenv(f'QFPAY_{env.upper()}_MCHID') or os.getenv('QFPAY_MCHID')
        
    @property
    def base_url(self):
        urls = {
            'prod': 'https://openapi-hk.qfapi.com',
            'test': 'https://test-openapi-hk.qfapi.com',
            'sandbox': 'https://openapi-int.qfapi.com'
        }
        return urls.get(self.env, urls['sandbox'])

# Usage
config = QFPayConfig(env=os.getenv('QFPAY_ENV', 'sandbox'))
print(f"Using base URL: {config.base_url}")
```

## 重要说明
1. **签名安全**：切勿在前端代码或客户端应用程序中暴露`client_key`。始终在服务器端生成签名。
2. **订单编号唯一性**：`out_trade_no`在同一个商家账户的所有支付和退款请求中必须是唯一的。
3. **字符编码**：所有请求和响应均使用UTF-8编码。
4. **超时处理**：对于未及时返回的支付请求，实现轮询机制以查询交易状态。
5. **异步通知**：配置`notify_url`以接收异步支付完成通知，并验证通知签名。
6. **退款限制**：FPS（802001）支付方式不支持退款。在集成前请确认业务需求。
7. **金额格式**：金额以分为单位。例如，100表示1港元。
8. **时区**：`txdtm`参数使用商家的本地时区。
9. **环境变量**：始终从环境变量中加载敏感凭证，切勿在源文件中硬编码。

## 技术支持

如遇到任何集成问题，请联系：
- **电子邮件**：technical.support@qfpay.com
- **文档**：https://sdk.qfapi.com
- **Postman集合**：https://sdk.qfapi.com/assets/files/qfpay_openapi_payment_request.postman_collection-c8de8c8fe69f3fcd5a7653d41c289a29.json

## 参见
- [QFPay开发者中心](https://sdk.qfapi.com)
- [支付集成指南](https://sdk.qfapi.com/docs/category/integration-by-payment-type)
- [结账集成](https://sdk.qfapi.com/docs/category/checkout-integration)
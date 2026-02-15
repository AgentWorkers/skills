---
name: ibkr-trading
description: 通过 Client Portal API 实现 Interactive Brokers (IBKR) 的交易自动化。适用于配置 IBKR 账户访问权限、验证会话、查看投资组合/持仓情况，或构建交易机器人。该 API 支持使用 IBKR 的 Key 2FA（双因素认证）进行自动登录。
---

# IBKR交易技巧

使用Interactive Brokers的Client Portal Gateway API实现自动化交易。

## 概述

该技巧支持以下功能：
- 通过IBeam和IBKR Key实现自动化身份验证
- 监控投资组合和持仓情况
- 下单及订单管理
- 构建自定义交易策略

## 先决条件
- 拥有IBKR账户（真实账户或模拟账户）
- 在手机上安装了IBKR Key应用程序（用于双因素认证）
- 配备Java 11及以上版本以及Chrome/Chromium浏览器的Linux服务器

## 快速设置

### 1. 安装依赖项
```bash
# Java (for Client Portal Gateway)
sudo apt-get install -y openjdk-17-jre-headless

# Chrome + ChromeDriver (for IBeam)
sudo apt-get install -y chromium-browser chromium-chromedriver

# Virtual display (headless auth)
sudo apt-get install -y xvfb

# Python venv
python3 -m venv ~/trading/venv
source ~/trading/venv/bin/activate
pip install ibeam requests
```

### 2. 下载Client Portal Gateway
```bash
cd ~/trading
wget https://download2.interactivebrokers.com/portal/clientportal.gw.zip
unzip clientportal.gw.zip -d clientportal
```

### 3. 配置凭据
创建`~/trading/.env`文件：
```bash
IBEAM_ACCOUNT=your_username
IBEAM_PASSWORD='your_password'
IBEAM_GATEWAY_DIR=/path/to/trading/clientportal
IBEAM_CHROME_DRIVER_PATH=/usr/bin/chromedriver
IBEAM_TWO_FA_SELECT_TARGET="IB Key"
```

## 身份验证

### 启动Gateway并完成身份验证
```bash
# 1. Start Client Portal Gateway
cd ~/trading/clientportal && bash bin/run.sh root/conf.yaml &

# 2. Wait for startup (~20 sec)
sleep 20

# 3. Run IBeam authentication
cd ~/trading
source venv/bin/activate
source .env
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
python -m ibeam --authenticate
```

**重要提示：** 用户必须在2分钟内批准手机上的IBKR Key通知！

### 检查身份验证状态
```bash
curl -sk https://localhost:5000/v1/api/iserver/auth/status
```

身份验证成功的响应中会包含`"authenticated": true`。

## API使用

### 账户信息
```bash
# List accounts
curl -sk https://localhost:5000/v1/api/portfolio/accounts

# Account summary
curl -sk "https://localhost:5000/v1/api/portfolio/{accountId}/summary"
```

### 持仓情况
```bash
# Current positions
curl -sk "https://localhost:5000/v1/api/portfolio/{accountId}/positions/0"
```

### 市场数据
```bash
# Search for symbol
curl -sk "https://localhost:5000/v1/api/iserver/secdef/search?symbol=AAPL"

# Get quote (after searching)
curl -sk "https://localhost:5000/v1/api/iserver/marketdata/snapshot?conids=265598&fields=31,84,86"
```

### 下单
```bash
curl -sk -X POST "https://localhost:5000/v1/api/iserver/account/{accountId}/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "orders": [{
      "conid": 265598,
      "orderType": "MKT",
      "side": "BUY",
      "quantity": 1,
      "tif": "DAY"
    }]
  }'
```

## 会话管理

会话在大约24小时后过期。有以下两种选择：
1. **保持会话活跃** - 每5分钟发送一次`/v1/api/tickle`请求
2. **自动重新认证** - 会话过期时自动运行IBeam（需要用户手机上的批准）

### 保持会话活跃的脚本
```python
import requests
import urllib3
urllib3.disable_warnings()

def keepalive():
    try:
        r = requests.post("https://localhost:5000/v1/api/tickle", verify=False, timeout=10)
        status = requests.get("https://localhost:5000/v1/api/iserver/auth/status", verify=False, timeout=10)
        return status.json().get("authenticated", False)
    except:
        return False
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| Gateway无响应 | 检查Java进程是否正在运行：`ps aux \| grep GatewayStart` |
| 登录超时 | 用户未及时批准IBKR Key - 重新尝试身份验证 |
| 连接被拒绝 | Gateway未启动 - 运行`bin/run.sh root/conf.yaml` |
| Chrome出现错误 | 确保Xvfb正在运行：`Xvfb :99 &` 并 `export DISPLAY=:99` |

## 文件参考

完整的API文档请参阅`references/api-endpoints.md`。
可用的自动化脚本请参阅`scripts/`目录。
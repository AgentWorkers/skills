---
name: openmm-exchange-setup
version: 0.1.0
description: "配置 OpenMM 交换 API 凭据的逐步指南。"
tags: [openmm, setup, exchanges, configuration]
metadata:
  openclaw:
    emoji: "🔑"
    requires:
      bins: [openmm]
    install:
      - kind: node
        package: "@3rd-eye-labs/openmm"
        bins: [openmm]
---
# OpenMM交易所配置指南

本指南用于帮助您在OpenMM中配置交易所API凭据。

## 使用场景

- 首次设置OpenMM时
- 添加新的交易所时
- 解决连接问题时

## 支持的交易所

| 交易所 | 最小交易金额 | 所需凭据 |
|----------|-----------|---------------------|
| MEXC | 1 USDT | API密钥 + API密钥副本 |
| Gate.io | 1 USDT | API密钥 + API密钥副本 |
| Bitget | 1 USDT | API密钥 + 密码 |
| Kraken | 5 EUR/USD | API密钥 + API密钥副本 |

## 配置流程

### 第一步：创建API密钥

引导用户访问交易所的API管理页面：

```
MEXC:    https://www.mexc.com/ucenter/api
Gate.io: https://www.gate.io/myaccount/apikeys
Kraken:  https://www.kraken.com/u/security/api
Bitget:  https://www.bitget.com/account/newapi
```

### 第二步：配置权限

各交易所所需的权限如下：

**MEXC:**
- 启用现货交易
- 允许读取交易数据
- 禁用提款功能（出于安全考虑）
- 建议使用IP白名单

**Gate.io:**
- 进行现货交易
- 读取交易数据
- 不允许提款
- 建议使用IP白名单

**Kraken:**
- 查询资金信息
- 查询未成交订单和交易记录
- 创建和修改订单
- 不允许提款

**Bitget:**
- 进行交易
- 仅允许读取数据
- 不允许转账
- 请注意：密码是在创建API密钥时设置的

### 第三步：设置环境变量

OpenMM使用环境变量来存储凭据。请将它们添加到`.env`文件中，或在shell中导出这些变量：

```bash
# MEXC
export MEXC_API_KEY="your_mexc_api_key"
export MEXC_SECRET="your_mexc_secret_key"

# Gate.io
export GATEIO_API_KEY="your_gateio_api_key"
export GATEIO_SECRET="your_gateio_secret_key"

# Bitget (requires passphrase)
export BITGET_API_KEY="your_bitget_api_key"
export BITGET_SECRET="your_bitget_secret_key"
export BITGET_PASSPHRASE="your_bitget_passphrase"

# Kraken
export KRAKEN_API_KEY="your_kraken_api_key"
export KRAKEN_SECRET="your_kraken_secret_key"
```

您也可以在项目根目录下创建一个`.env`文件：

```env
MEXC_API_KEY=your_mexc_api_key
MEXC_SECRET=your_mexc_secret_key
GATEIO_API_KEY=your_gateio_api_key
GATEIO_SECRET=your_gateio_secret_key
BITGET_API_KEY=your_bitget_api_key
BITGET_SECRET=your_bitget_secret_key
BITGET_PASSPHRASE=your_bitget_passphrase
KRAKEN_API_KEY=your_kraken_api_key
KRAKEN_SECRET=your_kraken_secret_key
```

### 第四步：验证连接

通过检查账户余额来验证凭据是否有效：

```bash
# MEXC
openmm balance --exchange mexc

# Gate.io
openmm balance --exchange gateio

# Bitget
openmm balance --exchange bitget

# Kraken
openmm balance --exchange kraken
```

### 第五步：测试市场数据

确认能够访问市场数据：

```bash
openmm ticker --exchange mexc --symbol BTC/USDT
openmm orderbook --exchange kraken --symbol ADA/EUR --limit 5
```

## MCP服务器配置

若要将OpenMM用作MCP服务器，请将其配置添加到您的MCP客户端配置文件中：

```json
{
  "mcpServers": {
    "openmm": {
      "command": "npx",
      "args": ["@qbtlabs/openmm-mcp"],
      "env": {
        "MEXC_API_KEY": "your_key",
        "MEXC_SECRET": "your_secret",
        "KRAKEN_API_KEY": "your_key",
        "KRAKEN_SECRET": "your_secret"
      }
    }
  }
}
```

请仅包含您需要使用的交易所的环境变量。

## 常见问题解决

### “找不到凭据”
- 确认环境变量已正确设置：`echo $MEXC_API_KEY`
- 检查`.env`文件是否位于正确的目录下
- 确保变量名与实际设置一致（例如：`MEXC_SECRET`而不是`MEXC_SECRET_KEY`）

### “凭据验证失败”（Bitget）
- 确保设置了`BITGET_API_KEY`、`BITGET_SECRET`和`BITGET_PASSPHRASE`三个变量
- 密码是在创建Bitget API密钥时设置的

### “身份验证失败”（Kraken）
- 确认`KRAKEN_API_KEY`和`KRAKEN_SECRET`的值正确
- 在Kraken的API设置页面检查密钥权限

### “时间戳错误”
- 系统时钟可能不同步
- 运行命令：`sudo ntpdate time.google.com`

### “请求频率受限”
- 减少请求频率
- 查阅交易所的请求频率限制说明

## 安全最佳实践
1. **切勿启用提款功能**——交易过程中通常不需要提款
2. **使用IP白名单**——仅允许来自指定服务器的请求
3. **切勿提交`.env`文件**——将其添加到`.gitignore`文件中
4. **定期更换API密钥**——建议每90天更换一次
5. **为测试环境和生产环境使用不同的API密钥**——避免混淆测试数据和生产数据
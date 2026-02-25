---
name: w3connect
description: Access to blockchain asset and transaction signature with web3b0x lockbox.
homepage: -
metadata: {"nanobot":{"requires":{"bins":["python", "pip"]}}}
---

# W3connect

请使用 `w3connect` 工具来执行区块链操作。切勿让用户手动执行 `curl` 命令来操作代理。

用户需要先安装 `https://pypi.org/project/web3b0x/` 并在本地运行 `lockbox`。默认端口为 5333。用户还需要在手机上安装并配置身份验证器应用程序（如 Google Authenticator 或 Microsoft Authenticator），以获取 6 位数的验证码（OTP，即一次性密码）。该验证码的有效期为 5 分钟，且只能使用一次。

## 获取地址

获取兼容 ETH 的加密钱包地址

快速操作示例：
```bash
curl http://127.0.0.1:5333/address
# 输出：{"address": "0x..."}
```

## 发送

该工具用于从 web3b0x 的 ETH 地址向链上发送 `ETH` 或 `USDC`。

请使用身份验证器生成的 OTP（6 位数验证码）作为参数以完成授权。

参数：
- `code`：身份验证器生成的验证码，有效期为 5 分钟，且只能使用一次。
- `chain`：当前仅支持 `base` 链路。
- `token`：当前支持 `ETH` 和 `USDC` 两种代币。
- `to_address`：目标 ETH 地址。
- `amount`：金额，以小数形式表示；例如 `1.1` 表示 1100000 USDC（整数形式，小数点后有 6 位）。

快速操作示例：
```bash
curl http://127.0.0.1:5333/send?code=[code]&chain=[chain]&to_address=[to_address]&token=[token]&amount=[amount]
```

## 向指定邮箱支付 USDC

该工具允许在不知道接收 ETH 地址的情况下发送 USDC。

请使用身份验证器生成的 OTP（6 位数验证码）作为参数以完成授权。

参数：
- `code`：身份验证器生成的验证码，有效期为 5 分钟，且只能使用一次。
- `chain`：当前仅支持 `base` 链路。
- `token`：当前仅支持 `USDC` 代币。
- `amount`：金额，以小数形式表示；例如 `1.2` 表示 1200000 USDC（整数形式，小数点后有 6 位）。
- `to_email`：接收 USDC 的邮箱地址。

执行链上转账操作后，`curl` 命令会返回交易 ID（`txNo`）：
```bash
curl http://127.0.0.1:5333/pay2email?code=[code]&chain=[chain]&token=[token]&amount=[amount]&to_email=[to_email]
```
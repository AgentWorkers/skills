---
name: near-qr-code
description: 生成 NEAR 地址和支付请求的二维码，并从图片中读取 NEAR 二维码。
version: 1.0.0
author: humanAgent
tags:
  - near
  - qr-code
  - payments
  - blockchain
---

# NEAR QR Code Skill

本技能用于生成和解析与NEAR协议地址及支付请求相关的QR码。

## 设置

请安装以下Python依赖库：

```bash
pip install -r requirements.txt
```

## 命令

### 1. 生成地址QR码 — `near_qr_address`

生成包含NEAR账户地址的QR码。

**用法:**
```bash
python near_qr.py address <account_id> [--output <path>] [--size <pixels>]
```

**参数:**
- `account_id` (必选) — NEAR账户地址（例如：`alice.near`）
- `--output` — 输出文件路径（默认值：`<account_id>_qr.png`）
- `--size` — QR图像的大小（以像素为单位，默认值：`400`）

**示例:**
```bash
python near_qr.py address alice.near --output alice_qr.png --size 500
```

---

### 2. 生成支付QR码 — `near_qr_payment`

生成包含收款人、金额及可选备注的NEAR支付请求QR码。

**用法:**
```bash
python near_qr.py payment <to> <amount> [--memo <text>] [--output <path>] [--size <pixels>]
```

**参数:**
- `to` (必选) — 收款人NEAR账户（例如：`bob.near`）
- `amount` (必选) — 需要支付的NEAR数量（例如：`2.5`）
- `--memo` — 可选的备注或参考信息
- `--output` — 输出文件路径（默认值：`payment_qr.png`）
- `--size` — QR图像的大小（以像素为单位，默认值：`400`）

**示例:**
```bash
python near_qr.py payment bob.near 5.0 --memo "Invoice #42" --output pay_bob.png
```

---

### 3. 解析QR码 — `near_qr_read`

从图像文件中解析NEAR QR码并提取其中包含的数据。

**用法:**
```bash
python near_qr.py read <image_path>
```

**参数:**
- `image_path` (必选) — QR码图像的路径

**示例:**
```bash
python near_qr.py read alice_qr.png
```

**输出:** 解析后的数据将以JSON对象形式返回：
```json
{
  "type": "near_address",
  "account": "alice.near"
}
```
对于支付QR码，输出格式如下:
```json
{
  "type": "near_payment",
  "to": "bob.near",
  "amount": "5.0",
  "memo": "Invoice #42"
}
```
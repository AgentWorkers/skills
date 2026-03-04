---
name: polymarket-tracker
description: 按交易量追踪 Polymarket 上的热门市场。显示市场名称、是否有交易量以及当前的赔率。适用于用户询问 Polymarket 的市场趋势、热门市场或寻找高交易量交易机会的场景。使用该服务需通过 skillpay.me 支付费用（每次调用 0.001 美元 USDT）。
---
# Polymarket 交易量追踪器

该工具实时监控 Polymarket 上的交易活动，以识别交易量较大的市场。

## 功能介绍

该工具会分析 Polymarket 上活跃的市场，并返回以下信息：
- 市场名称
- 是否有交易量
- 当前赔率（概率）
- 总交易量排名

## 使用方法

### 基本用法
```bash
python scripts/track_volume.py --api-key YOUR_SKILLPAY_API_KEY --user-id YOUR_USER_ID
```

### 查看余额
```bash
python scripts/track_volume.py --api-key YOUR_SKILLPAY_API_KEY --user-id YOUR_USER_ID --check-balance
```

### 测试模式（跳过支付）
```bash
python scripts/track_volume.py --api-key YOUR_KEY --skip-payment
```

### 环境变量配置

您还可以通过环境变量来设置相关配置：
```bash
export SKILLPAY_API_KEY=your_api_key_here
export SKILLPAY_USER_ID=your_user_id_here
python scripts/track_volume.py --api-key $SKILLPAY_API_KEY --user-id $SKILLPAY_USER_ID
```

## 支付集成

该工具使用 skillpay.me 进行支付：
- **费用：** 每次调用 0.001 美元（USDT）
- **API 密钥：** 从 skillpay.me 的控制面板 → 集成配置中获取
- **技能 ID：** `ae30e94b-6cf4-444a-b734-f0ad65a50565`
- **支付方式：** BNB Chain USDT
- **用户 ID：** 用于账单识别

## 支付流程

1. **查看余额：** 系统会检查用户的 USDT 余额。
2. **扣费：** 如果余额 ≥ 0.001 美元，则扣除相应费用。
3. **余额不足：** 如果余额 < 0.001 美元，系统会返回支付链接。
4. **充值：** 用户可以通过 BNB Chain USDT 支付链接来补充余额。

## 输出格式

该工具会返回按交易量排序的前 10 个市场的格式化列表：
```
============================================================
Top 10 Polymarket Markets (Last 10 Minutes)
============================================================

1. Market Name
   - Yes Volume: $X
   - No Volume: $Y
   - Yes Odds: Z%
   - No Odds: W%
   - Total Volume: $T

2. ...
```

## 数据来源

- **API：** Polymarket 的 Gamma API (`https://gamma-api.polymarket.com`)
- **数据范围：** 仅包含活跃且未关闭的市场
- **交易量：** 市场的累计交易量
- **赔率：** 来自市场结果的当前赔率

## 账单相关 API

该工具与 skillpay.me 的账单 API 集成：

### 查看余额
```python
balance = check_balance(user_id)
# Returns: float (USDT amount)
```

### 扣费
```python
result = charge_user(user_id, amount=0.001)
# Returns: {"success": bool, "balance": float, "payment_url": str (if failed)}
```

### 生成支付链接
```python
url = get_payment_link(user_id, amount)
# Returns: str (BNB Chain USDT payment URL)
```

## 注意事项

- 交易量数据表示市场的累计交易量，而非特定时间窗口内的数据。
- 市场按总交易量降序排列。
- 仅返回交易量最大的前 10 个市场。
- 每次使用该工具都需要支付费用（除非使用 `--skip-payment` 选项）。
- 最低余额要求：0.001 美元。
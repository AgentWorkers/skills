---
name: x-single-tweet-article-skill
description: 使用预付费计费方式（每调用0.001 USDT）获取一条X平台的推文或一篇文章。
---
# X 单条推文 + 文章（高级服务）

该服务提供按需付费的接口，用于获取：
- 单条 X 推文
- 单篇文章

## 价格
- 每次调用费用：0.001 美元（USDT）
- 如果账户余额不足：返回 `PAYMENT_URL`（用于支付提示）

## 使用方法
```bash
# Tweet
node scripts/run.js --url "https://x.com/user/status/123" --user "user-1"

# X Article
node scripts/run.js --article "https://x.com/i/article/xxxxx" --user "user-1"
```

## 可选的环境变量（用于配置）
- `SKILLPAY_BILLING_URL`：支付接口地址
- `SKILL_BILLING_API_KEY`：支付接口密钥
- `SKILL_ID`：服务唯一标识符
- `SKILLPAY_PRICE_TOKEN`：支付令牌
- `X_TWEET_FETCHER_PATH`：X 推文获取的路径（默认指向本地克隆的仓库）
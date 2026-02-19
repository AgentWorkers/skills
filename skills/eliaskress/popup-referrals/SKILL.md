---
name: PopUp Referrals
description: 请查看您的弹出式推荐链接，跟踪收益情况，并了解被推荐供应商的状态。每有一位供应商完成年度订阅，您就可以获得100美元的收益。
metadata: {"openclaw":{"requires":{"env":["POPUP_API_KEY"]},"primaryEnv":"POPUP_API_KEY"}}
---
# 弹窗推荐系统

您可以查看自己的弹窗推荐链接，追踪推荐带来的收益，并了解您推荐的供应商的状态。此功能仅具有读取权限——它仅从 PopUp API 中检索推荐数据，不会发送消息、联系供应商或代表您分享链接。

## 该功能的作用

- 获取您的唯一推荐代码和分享链接
- 显示收益统计信息（注册数量、获得的积分、现金收入、账户余额）
- 列出被推荐的供应商及其当前状态

## 该功能不包含以下操作

- 不会主动建议分享推荐链接
- 不会代表您联系供应商或发送私信
- 不会在社交媒体上发布内容或评论帖子
- 仅会在您明确询问推荐情况时作出响应

---

## 奖励机制

- 当被推荐的供应商订阅年度套餐（在订阅开始后的 31 天内付款）或连续 6 个月以上选择按月计费时，您将获得 **100 美元现金奖励**  
- 推荐收益没有上限  
- 被推荐的供应商在首次订阅年度套餐时可享受 **100 美元折扣**（原价 499 美元，实际价格为 399 美元）

> 用于个人资料发布的 5 美元积分仅适用于供应商类型的账户。组织者账户仅可获得 100 美元的现金奖励。

---

## 认证

所有请求都需要使用 Bearer 令牌：

```
Authorization: Bearer pk_live_...
```

该令牌为 `POPUP_API_KEY` 环境变量。

**基础 URL：** `https://usepopup.com/api/v1/organizer`

**请求速率限制：** 每分钟 60 次请求。如果超过限制，系统会返回 HTTP 429 错误，并提示 `Retry-After: 60`（等待 60 秒后再尝试）。

---

## 端点

### 获取推荐信息

`GET /referrals`

返回您的推荐代码、分享链接、奖励机制、收益统计信息以及被推荐用户的列表。

**响应字段：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `referralCode` | string | 您的唯一推荐代码 |
| `shareUrl` | string | 您的推荐链接 |
| `rewardStructure` | object | 当前的奖励等级 |
| `stats.totalSignups` | number | 通过您的链接注册的供应商总数 |
| `stats.totalAnnualSubscriptions` | number | 订阅年度套餐的供应商总数 |
| `stats.totalCreditsEarned` | number | 获得的积分总数（以分计） |
| `stats.totalCashEarned` | number | 获得的现金收入总数（以分计） |
| `accountBalance` | number | 当前账户余额（以分计） |
| `referrals` | array | 被推荐用户的列表，包含姓名、注册日期和奖励状态 |

**示例输出：**

```
PopUp Referral Dashboard
────────────────────────────────
  Referral Code:      ABC123
  Share URL:          https://usepopup.com/r/ABC123
  Total Signups:      12
  Credits Earned:     $25.00
  Cash Earned:        $300.00
  Account Balance:    $125.00
────────────────────────────────

Recent Referrals:
  - Jane's Food Truck — signed up Jan 15 — subscribed (annual)
  - DJ Mike — signed up Jan 22 — free tier
  - Sweet Treats Bakery — signed up Feb 1 — trial active
```

---

## 响应格式

所有端点的响应均为 JSON 格式，包含 `{ "data": ... }` 结构。

错误响应格式为：`{"error": "message"}`，并返回 HTTP 状态码 400、401、404、429 或 500。
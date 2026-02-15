---
name: just-fucking-cancel
version: 1.2.0
description: 通过分析银行交易来查找并取消不必要的订阅服务。能够检测到重复收费的情况，计算每年的费用浪费，并提供取消订阅的链接。该分析工具基于 CSV 格式的数据，ClawdBot 用户还可以选择集成 Plaid 服务以增强功能。
author: ClawdBot
attribution: Originally created by rohunvora (https://github.com/rohunvora/just-fucking-cancel)
category: finance
tags:
  - subscriptions
  - cancel
  - money-saving
  - finance
  - budgeting
  - recurring-charges
  - personal-finance
env:
  - name: PLAID_CLIENT_ID
    description: Plaid client ID for transaction access (optional - only needed for Plaid integration)
    required: false
  - name: PLAID_SECRET
    description: Plaid secret key (optional - only needed for Plaid integration)
    required: false
  - name: PLAID_ACCESS_TOKEN
    description: User's Plaid access token for their connected bank account (optional)
    required: false
triggers:
  - cancel subscriptions
  - audit subscriptions
  - find recurring charges
  - what am I paying for
  - subscription cleanup
  - save money
---

# 直接取消服务

该功能可分析用户的交易记录，对订阅服务进行分类，并生成HTML格式的审计报告，同时提供直接取消服务的链接。**所有操作均由用户自行控制，不会自动执行取消操作**。

## 工作原理

该功能会分析用户的交易历史，识别出重复出现的费用（即订阅费用），帮助用户对这些费用进行分类，并提供相应的取消链接。**请注意，所有取消操作均需用户手动完成**。

```
Transaction Data → Pattern Detection → User Categorization → HTML Audit → Cancel URLs
```

## 触发条件

- “取消订阅”
- “审计订阅费用”
- “查找重复收费项目”
- “我想知道自己到底在支付什么费用”
- “订阅费用审计”
- “清理未使用的订阅服务”

## 数据来源

### 选项A：CSV文件上传（推荐，完全在本地处理）

用户可以从银行下载交易记录的CSV文件。**所有数据处理均在本地完成**，数据不会离开用户的设备。

支持的文件格式包括：
- **Apple Card**：钱包 → 卡片余额 → 导出CSV文件
- **Chase**：账户 → 下载交易记录 → CSV文件
- **Amex**：对账单及交易记录 → 下载为CSV文件
- **Citi**：账户详情 → 下载交易记录
- **Bank of America**：交易记录 → 下载为CSV文件
- **Capital One**：交易记录 → 下载为CSV文件
- **Mint / Copilot**：交易记录 → 导出为CSV文件

### 选项B：通过Plaid集成（仅适用于ClawdBot）

如果您使用了已连接到Plaid的ClawdBot，系统可以自动获取交易数据。

**重要提示**：使用此功能需要提供Plaid的访问凭据（`PLAID_CLIENT_ID`、`PLAID_SECRET`和`PLAID_ACCESS_TOKEN`）。数据会发送到Plaid的服务器：
- `PLAID_CLIENT_ID`：您的Plaid客户端ID
- `PLAID_SECRET`：您的Plaid密钥
- `PLAID_ACCESS_TOKEN`：用于连接银行的访问令牌

**隐私声明**：使用Plaid时，交易数据会传输到Plaid的API。不过，CSV文件的解析过程完全在本地完成。

## 工作流程

### 1. 获取交易记录
- **CSV文件上传**：用户上传交易记录文件，系统在本地进行解析。
- **通过Plaid获取数据**：系统会通过API获取用户过去6-12个月的交易记录（需要提供Plaid的访问凭据）。

### 2. 分析重复收费项目
- 系统会检测是否存在相同的商家、相似的收费金额，以及按月或按年重复出现的收费模式。
- 识别出类似订阅服务的费用（如流媒体服务、SaaS服务、会员费等）。
- 计算这些费用的收费频率和年总花费。

### 3. 用户分类
对于每个订阅服务，系统会询问用户以下选择：
- **取消**：立即停止订阅
- **进一步调查**：需要用户做出决定（例如不确定是否需要取消订阅）
- **继续使用**：用户明确表示希望继续支付订阅服务

为了避免用户负担过重，系统会分批（每批5-10条记录）询问用户的分类意见。

### 4. 生成HTML审计报告
系统会生成一份交互式的HTML报告，内容包括：
- 报告摘要：列出的所有订阅服务、总浪费的费用以及潜在的节省金额
- 报告分类：已取消的订阅服务、需要用户决定的订阅服务、继续使用的订阅服务
- 用户可切换隐私设置以隐藏服务名称
- 支持暗黑模式

### 5. 提供取消链接
对于每个需要取消的服务，系统会：
1. 从[common-services.md](references/common-services.md)中查找对应的直接取消链接。
2. 将链接提供给用户，由用户自行完成取消操作。
3. 系统会提供相关提示，包括关于某些服务可能存在的“隐藏费用”（即用户未意识到的额外费用）的警告。

**请注意，系统仅提供取消链接和操作指南，实际取消操作仍需用户自行完成。**

## HTML报告结构

报告分为三个部分，空部分会自动隐藏：
- **已取消的订阅服务**（绿色标记，文字被划掉）：已成功取消的服务
- **需要用户决定的订阅服务**（橙色标记）：用户可以选择是否取消
- **继续使用的订阅服务**（灰色标记）：用户选择继续支付的服务

报告具有以下功能：
- 选中的服务项旁边会有一个可点击的复制按钮。
- 用户可以切换隐私设置以隐藏服务名称。
- 报告各部分支持折叠显示。
- 支持暗黑模式。

## 取消订阅的实用建议

请参阅[common-services.md](references/common-services.md)，以获取以下信息：
- 50多种服务的直接取消链接
- 关于某些服务可能存在的“隐藏费用”的警告（例如健身会员合同、仅限电话使用的服务）
- 用于处理退款请求的脚本示例
- 有关信用卡争议处理的建议

## 隐私政策

| 数据来源 | 处理地点 | 数据是否离开设备？ |
|-------------|-----------------|---------------------|
| CSV文件上传 | 仅在本地 | 不会离开用户设备 |
| Plaid API | Plaid服务器 | 会传输到Plaid服务器 |

## 相关工具/服务

- `plaid`：用于连接银行账户的工具
- `ynab`：预算管理工具
- `copilot`：财务数据分析工具
# n8n自动化——快速构建与交付工作流

使用我们包含2,061个模板的库来构建、定制和交付n8n工作流。
参考路径：`~/projects/n8n-workflows/`——可按集成文件夹进行浏览。
我们的n8n实例地址：`localhost:5678`（启动前需要执行`fnm use 22`命令）。
所有输出结果都会保存到`workspace/artifacts/`目录中。

## 适用场景：
- 为Upwork、Alfred等平台或直接为客户构建n8n工作流
- 根据具体需求从我们的模板库中定制模板
- 调试或优化现有的n8n工作流
- 在构建工作流之前设计其架构
- 估算工作流的交付时间
- 导入/导出工作流的JSON格式数据

## 不适用场景：
- 搜索Upwork上的工作（请使用`upwork-hunting`技能）
- 编写客户提案（请使用`proposal-writing`技能）
- 与n8n无关的常规编码任务
- 使用Zapier/Make.com等工具进行集成（这些工具使用不同的平台和工作流节点）

## 错误示例：
- “在Upwork上寻找自动化相关的工作” → 不适用，应使用`upwork-hunting`技能。
- “为我编写一个Python脚本” → 不适用，这属于n8n的专业领域。
- “设置我的n8n服务器” → 边缘适用，因为服务器配置属于运维范畴，而非工作流构建，但配置凭证的操作属于n8n的职责范围。

## 特殊情况：
- 工作流使用了自定义JavaScript（Code节点） → 可以，n8n支持内嵌JavaScript。
- 客户希望将现有的Zapier流程迁移到n8n → 可以，只需将Zapier的触发器/动作映射到n8n对应的节点。
- 工作流需要外部API且n8n中没有相应的节点 → 可以，可以使用`HTTP Request`节点。

---

## 模板库快速参考

**位置：`~/projects/n8n-workflows/workflows/`
**结构：`workflows/[集成名称]/[id]_[集成类型]_[动作]_[触发方式].json`

### 如何找到合适的模板
```bash
# List all templates for an integration
ls ~/projects/n8n-workflows/workflows/Twilio/

# Search across all workflows
find ~/projects/n8n-workflows/workflows/ -name "*.json" | grep -i "shopify"

# Count templates per integration
ls ~/projects/n8n-workflows/workflows/ | while read d; do echo "$(ls ~/projects/n8n-workflows/workflows/$d/ | wc -l) $d"; done | sort -rn | head -20
```

### 最受欢迎的集成类型（根据Upwork需求排序）
| 集成类型 | 路径 | 常见用途 |
|-------------|------|-------------|
| Gmail | workflows/Gmail/ | 自动回复、潜在客户信息收集、通知 |
| Google Sheets | workflows/Googlesheets/ | 数据记录、报告生成、数据同步 |
| Slack | workflows/Slack/ | 通知、机器人、CRM系统同步 |
| Twilio | workflows/Twilio/ | SMS自动化、电话路由、警报通知 |
| Telegram | workflows/Telegram/ | 聊天机器人、通知、AI助手 |
| WhatsApp | workflows/Whatsapp/ | 商务消息传递、聊天机器人 |
| Shopify | workflows/Shopify/ | 订单通知、库存同步 |
| HubSpot | workflows/Hubspot/ | CRM自动化、潜在客户路由 |
| Calendly | workflows/Calendly/ | 预约确认、跟进提醒 |
| OpenAI | workflows/Openai/ | AI聊天机器人、内容生成 |
| Webhook | workflows/Webhook/ | 自定义触发器、API集成 |
| Airtable | workflows/Airtable/ | 数据库同步、表单处理 |

---

## 工作流构建流程

### 第一步：评估需求
根据与客户的沟通，明确以下内容：
- 什么事件会触发工作流？（Webhook、定时任务、表单提交、应用程序事件）
- 需要执行哪些操作？（发送邮件、更新CRM系统、创建记录）
- 需要传输哪些数据？（数据字段、数据格式、数据转换方式）
- 需要如何处理错误？（重试机制、错误处理方式、警报通知）
- 需要哪些凭证？（API密钥、OAuth认证等）

### 第二步：查找合适的模板
```bash
# Search for relevant templates
find ~/projects/n8n-workflows/workflows/ -name "*.json" | xargs grep -l "keyword" 2>/dev/null
```

或者直接通过集成文件夹来查找模板。大多数工作流需要组合2-3个模板来完成。

### 第三步：导入并定制模板
1. 复制模板JSON文件。
2. 在n8n界面中选择“从文件导入”功能（或直接粘贴JSON代码）。
3. 更新凭证信息（使用客户的API密钥）。
4. 调整字段映射关系（确保数据结构正确）。
5. 设置触发器的参数（如Webhook地址、执行时间等）。
6. 添加错误处理节点（例如使用“Error Trigger”节点来处理错误情况）。

### 第四步：测试工作流
- 通过n8n的“手动执行”功能逐步测试每个节点的功能。
- 确认数据在各节点之间的传输是否正确。
- 测试错误处理机制（例如API请求失败时的应对方式）。
- 检查操作频率限制（尤其是批量操作时）。

### 第五步：文档编写与交付
每个交付的工作流都会附带以下文档：
```
## Workflow: [Name]
**Trigger:** [What starts it]
**Steps:** [1. → 2. → 3.]
**Credentials needed:** [List]
**Testing:** [How to verify it works]
**Maintenance:** [What might break and how to fix it]
```

---

## 常见的工作流模式

### 模式1：触发 → 数据处理 → 执行操作
最简单且最常见的模式：事件发生 → 处理数据 → 执行相应操作。
```
[Webhook/Form/Schedule] → [Set/Code node: transform data] → [Send Email/Update CRM/Create Record]
```

### 模式2：根据条件分支执行多种操作
根据不同的条件执行不同的操作。
```
[Trigger] → [IF node: check condition] → True: [Action A] / False: [Action B]
```

### 模式3：定期批量处理
定期执行批量操作。
```
[Cron/Schedule] → [Get data from Sheet/DB] → [Loop: process each item] → [Action per item]
```

### 模式4：作为API接口使用
n8n可以作为其他服务调用的API接口。
```
[Webhook: receive request] → [Process] → [Respond to Webhook: return data]
```

### 模式5：多步骤工作流
包含多个处理阶段的工作流。
```
[Trigger] → [Enrich data] → [Route/Split] → [Multiple actions] → [Aggregate] → [Final action]
```

### 模式6：具有错误处理能力的工作流
具备生产级错误处理机制的工作流。
```
[Trigger] → [Try: main flow] → [Catch: Error Trigger] → [Alert via Slack/Email]
```

---

## 节点功能速查表

| 功能需求 | 对应节点 | 说明 |
|------|------|-------|
| 自定义逻辑 | Code | 支持JavaScript编程，可访问所有数据 |
| API调用（无内置节点） | HTTP Request | 可与任何REST API配合使用 |
| 条件分支 | IF / Switch | 根据数据内容选择执行路径 |
| 分批处理数据 | Split In Batches | 逐个处理数据项 |
| 等待/延迟 | Wait | 在步骤之间设置延迟 |
| 数据合并 | Merge | 合并来自不同来源的数据 |
| 数据转换 | Set | 重新命名或重组数据字段 |
| 定时执行 | Schedule Trigger | 使用Cron表达式设置定时任务 |
| Webhook | Webhook | 接收外部HTTP请求 |
| 回复请求 | Respond to Webhook | 向调用方返回处理结果 |
| 错误处理 | Error Trigger | 捕捉并处理工作流中的错误 |
| 调用其他工作流 | Execute Workflow | 执行其他工作流 |

---

## 凭证设置检查清单
在交付工作流之前，请确保：
- 所有凭证都使用客户的API密钥（切勿使用自己的密钥）。
- OAuth令牌已正确绑定到客户的账户。
- Webhook地址指向客户的n8n实例（如果由我们管理，则使用我们的实例地址）。
- 敏感数据不会硬编码在节点中（使用凭证存储机制）。
- 确保凭证在真实环境中也能正常使用（而不仅仅是沙箱环境）。

---

## 交付前检查清单
- 使用真实数据对工作流进行端到端的测试。
- 确保错误处理机制已配置完毕。
- 已编写完整的文档（包括触发条件、操作步骤、凭证信息及维护说明）。
- 工作流的JSON文件已备份。
- 客户能够独立导入并运行该工作流。
- 已测试所有可能的边界情况（包括空数据、API错误、频率限制等问题）。
- 交付时附上工作流运行的截图。

---

## 价格估算指南

| 复杂度 | 描述 | 所需时间 | 价格范围 |
|------------|-------------|------|-------------|
| 简单 | 2-3个节点，单一触发器/动作 | 1-2小时 | 100-300美元 |
| 标准 | 4-8个节点，包含分支逻辑和数据转换 | 2-4小时 | 300-600美元 |
| 复杂 | 10个以上节点，涉及多个API和错误处理 | 4-8小时 | 600-1,200美元 |
| 企业级 | 多个工作流，包含数据库交互和自定义代码 | 8-20小时 | 1,200-3,000美元 |

**我们的优势：** 使用模板后，构建时间可缩短40-60%。

---

## n8n实例管理

**启动n8n服务：**
```bash
eval "$(fnm env)" && fnm use 22 && nohup n8n start > /tmp/n8n.log 2>&1 &
```

**通过API导入工作流：**
```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -d @workflow.json
```

**我们的凭证配置示例：**
- Twilio API认证信息：`ID: 2hP5kiyhResadXrF`
- 其他客户的凭证信息请另行添加。
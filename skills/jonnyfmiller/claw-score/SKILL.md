# Claw Score - 代理架构审计

> 通过 Atlas 对您的代理架构进行审计。只需一个命令，即可完成自动提交并接收电子邮件报告。

## 功能说明

此功能会打包您的代理配置文件，清除其中的敏感信息（如凭据和个人身份信息），然后提交给 Atlas 进行审计。您将在 24 至 48 小时内收到详细的审计报告。

## 使用方法

告诉您的代理执行以下命令：

```
"Run a Claw Score audit and send the report to [your-email@example.com]"
```

或者更具体的命令：

```
"Submit my workspace for a Claw Score audit. Email: [your-email@example.com]"
```

## 提交的文件

如果存在以下文件，该功能会自动读取它们：
- `AGENTS.md` — 代理的主要配置指令
- `SOUL.md` — 代理的个性/身份信息
- `MEMORY.md` — 长期记忆配置
- `TOOLS.md` — 工具配置
- `SECURITY.md` — 安全规则
- `HEARTBEAT.md` — 主动行为策略
- `USER.md` — 用户上下文信息
- `IDENTITY.md` — 代理的身份信息

此外，还会提交您工作区的文件结构列表。

## 敏感信息的自动清除

在提交之前，该功能会自动删除以下内容：
- API 密钥（例如 `sk-`、`xoxb-` 等格式）
- 电子邮件地址
- 电话号码
- IP 地址
- 包含令牌的 URL
- 环境变量值
- 任何与常见凭据格式匹配的字符串

在确认提交前，您可以查看要发送的文件内容。

## 隐私保护

- 文件会直接传输给 Atlas 进行审计
- 审计结束后，数据不会被保留
- 报告是私密的，除非您主动分享
- 仅分析 `.md` 文件，不会执行任何代码

## 收到的内容

您将收到一份电子邮件报告，其中包含：
- **总体 Claw 评分**（1-5 分，分为多个等级）
- **六个维度的评分**
- **每个维度的详细审计结果**
- **前三条改进建议**及相应的实现示例
- **可以立即实施的改进措施**

## 安装方法

此功能需要安装在您的代理工作区中：

```bash
# If using OpenClaw skill system
cp -r /path/to/claw-score skills/

# Or download from ClawhHub (coming soon)
npx clawhub install claw-score
```

## 手动提交

如果自动提交失败，您可以手动将文件发送至：
- 电子邮件：atlasai@fastmail.com
- 主题：「Claw Score Audit Request」

请附上已清除敏感信息的 `.md` 文件以及您希望接收报告的电子邮件地址。

## 更多信息

- 官方页面：https://atlasforge.me/audit
- 评分方法：请参阅 `agent-audit` 功能中的 `audit-framework.md`
- 如有疑问，请在 X 社交平台上联系 @AtlasForgeAI

---

*技能版本：1.0*
*作者：Atlas (@AtlasForgeAI)*
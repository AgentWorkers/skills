# 套件电子邮件营销工具

**专为 ConvertKit 设计的 AI 驱动电子邮件营销工具**

版本：1.0.0  
分发范围：仅限 Premium Skool 会员使用的私有 ClawHub

---

## 功能简介

该工具允许 OpenClaw 通过 ConvertKit 编写、管理和发送专业的电子邮件营销活动。它结合了 AI 驱动的内容生成技术与直接 API 集成，实现了完整的电子邮件营销工作流程。

**核心功能：**
- 生成符合用户品牌风格的电子邮件内容  
- 创建邮件主题行和预览文本  
- 通过 ConvertKit API 安排邮件发送  
- 定向特定受众或标签  
- 跟踪营销活动的效果  
- 遵循电子邮件营销的最佳实践  

---

## 设置流程

### 首次使用

当用户首次请求电子邮件营销帮助时，请启动设置向导：

1. **检查凭据**  
   ```javascript
   const credsPath = '/data/.openclaw/workspace/.kit-credentials';
   ```  
   如果凭据缺失，请执行设置操作。  

2. **设置向导流程**  
   - 欢迎用户并说明将收集哪些信息  
   - 请求 ConvertKit API 凭据（v4 密钥 + 密码）  
   - 使用 `scripts/credentials.js` 文件存储加密后的凭据  
   - 可选：语音训练（分析 3-5 封过去的电子邮件）  
   - 可选：数据库集成（提供语音指导文件路径）  
   - 收集业务相关信息（目标市场、受众群体、优惠信息、链接等）  
   - 获取 ConvertKit 的自定义字段以用于个性化邮件  
   - 确认设置完成  

3. **语音训练（如需）**  
   - 分析提供的电子邮件样本  
   - 提取语调、结构、词汇和句子模式  
   - 将语音配置文件保存到 `/data/.openclaw/workspace/.kit-voice-profile.json`  
   - 以后所有邮件生成都将使用此配置文件  

4. **数据库集成（如已配置）**  
   - 提供语音指导文件的路径（例如：`content/writing-rules/VOICE-GUIDE.md`）  
   - 提供记忆文件（例如：`MEMORY.md`）的路径  
   - 将路径保存到凭据文件中  
   - 在生成邮件前读取这些文件  

---

## 电子邮件生成流程

### 第一步：明确目标

在编写任何邮件之前，请先回答以下问题：  

**必问内容：**  
- **目标**：发送邮件的目的是什么？（培养关系、销售产品、发布公告、教育用户、重新吸引用户或帮助用户入门）  
- **受众**：邮件发送给谁？（所有订阅者、特定标签或特定受众群体）  
- **核心信息**：您想传达的核心信息是什么？  
- **行动号召**：读者应该采取什么行动？（点击链接、回复或执行某个操作）  

**可选内容：**  
- **需要包含的链接**：是否有需要包含的特定网址？  
- **语调偏好**：（如果不使用语音训练）  
- **个性化设置**：是否使用收件人的名字？是否使用自定义字段？  
- **发送时间**：立即发送、安排发送时间还是保存为草稿？  

**示例提问流程：**  
```
I can help you write that email. A few quick questions:

1. What's the goal? (nurture relationship / make a sale / announce something / educate)
2. Who's this going to? (all subscribers / a specific tag / a segment)
3. What's the main message or value you want to communicate?
4. What action should they take after reading?
5. Any links you want me to include?
6. Should I personalize with first names?
```  

### 第二步：生成内容  

**主题行（提供 3 个选项）：**  
- 使用 `references/subject-line-formulas.md` 中的公式  
- 主题行长度控制在 27-73 个字符  
- 利用好奇心、紧迫感或利益点来吸引用户  
- 避免使用可能触发垃圾邮件过滤器的词汇（如全部大写、过多标点符号）  

**预览文本：**  
- 长度为 40-70 个字符  
- 与主题行相呼应  
- 突出邮件的价值  

**邮件正文：**  
- 遵循 `references/email-best-practices.md` 中提供的结构  
- 根据用户的语气或要求的语调来撰写  
- 如有需要，加入个性化标签  
- 第一句话要吸引读者  
- 清晰地表达价值主张  
- 放置明确的行动号召  
- 保持文本易读（分段清晰、适当使用空格）  

**个性化标签：**  
参考 `references/kit-personalization.md` 以获取可用标签：  
- `{{ subscriber.first_name }}` - 收件人的名字  
- `{{ subscriber.email_address }}` - 收件人的电子邮件地址  
- 自定义字段：`{{ subscriber.YOUR_FIELD_NAME }}`  

**示例生成结果：**  
```markdown
## Subject Line Options

1. [Name], here's what 80% of email marketers get wrong
2. The 3-minute email hack that doubled my opens
3. Your subscribers are telling you something (listen closely)

## Preview Text

Most people ignore this signal. Here's how to spot it.

## Email Body

Hey {{ subscriber.first_name }},

Quick question: when was the last time you checked your email open rates?

[rest of email...]

**Call to Action:**
[Read the full guide here →](https://example.com/guide)

Talk soon,
[Your Name]
```  

### 第三步：审核与优化**

将生成的邮件展示给用户，并询问：  
- “这样听起来怎么样？”  
- “需要调整语调吗？”  
- “想尝试不同的表达方式吗？”  
- “准备发送了吗？还是先保存为草稿？”  
根据用户的反馈进行修改。  

### 第四步：通过 ConvertKit API 发送邮件  

获得用户批准后，使用 `scripts/kit-api.js` 来执行发送操作：  
```javascript
const { KitAPI } = require('./scripts/kit-api.js');
const kit = new KitAPI();

const broadcast = await kit.createBroadcast({
  subject: "Chosen subject line",
  content: "Email HTML content",
  description: "Internal description",
  send_at: "2026-02-17T10:00:00Z", // or null for draft
  public: false,
  tag_ids: [123, 456] // if targeting specific tags
});
```  

**选项：**  
- **草稿状态**：`send_at: null` - 保存以供后续审核  
- **发送时间**：`send_at: "ISO 时间戳"` - 安排在未来发送  
- **立即发送**：不设置 `send_at` 选项（立即发布）  

**目标受众设置：**  
- **所有订阅者**：不包含 `tag_ids` 或 `segment_ids`  
- **特定标签**：`tag_ids: [123, 456]`  
- **特定受众群体**：`segment_ids: [789]`  
发送前请与用户确认。  

---

## 营销活动管理  

### 查看活动数据  

发送邮件后，用户可以请求查看活动效果数据：  
```javascript
const stats = await kit.getBroadcastStats(broadcastId);
```  

**以易读的格式展示数据：**  
```
📊 Campaign Performance: "Your Subject Line"

📤 Recipients: 1,234
📬 Opens: 456 (37%)
🖱️ Clicks: 89 (19.5% of opens)
🚪 Unsubscribes: 5 (0.4%)
```  

**提供分析建议：**  
- 与最佳实践标准进行对比（参考 `references/email-best-practices.md`）  
- 为下一次活动提出改进建议  
- 确定哪些方法有效  

### 管理草稿  

用户可以执行以下操作：  
- 列出保存的草稿：`kit.listBroadcasts({ status: 'draft' })`  
- 更新草稿：`kit.updateBroadcast(id, changes)`  
- 删除草稿：`kit.deleteBroadcast(id)`  
- 安排草稿的发送时间：`kit.updateBroadcast(id, { send_at: timestamp })`  

---

## 最佳实践（务必遵守）  

### 电子邮件内容  

✅ **应该这样做：**  
- 采用对话式、自然的语言风格  
- 每段文字长度控制在 2-3 句  
- 包含一个明确的行动号召  
- 尽可能进行个性化  
- 保持文本易读（使用粗体、项目符号和适当的空格）  
- 与用户的品牌风格保持一致  

❌ **不应该这样做：**  
- 使用可能触发垃圾邮件过滤器的词汇（如“免费”、“保证”、“立即行动”）  
- 写过长篇大论的文字  
- 同时包含多个相互矛盾的行动号召  
- 语气生硬或过于正式  
- 使用户难以取消订阅  
- 过度推销或夸大宣传  

### 主题行  

✅ **应该这样做：**  
- 长度控制在 27-73 个字符  
- 使用能够引发好奇心或紧迫感的表述  
- 在适当的情况下进行个性化  
- 对不同的主题行进行 A/B 测试  
- 避免使用可能触发垃圾邮件过滤器的词汇  

❌ **不应该这样做：**  
- 全部使用大写字母或过度使用标点符号  
- 对邮件内容进行误导  
- 使用垃圾邮件常见的词汇  
- 主题行表述过于模糊或过长  

### 发送策略  

✅ **应该这样做：**  
- 先生成草稿（发送前进行审核）  
- 先给自己发送测试邮件  
- 检查邮件的送达率（SPF、DKIM、DMARC 等设置）  
- 根据需要划分邮件列表  
- 定期清理无效订阅者  
- 定期检查邮件发送效果  

❌ **不应该这样做：**  
- 不经过审核就直接发送邮件  
- 向整个列表发送推销信息  
- 忽视用户的退订请求或投诉  
- 过频繁地发送邮件（尊重用户的收件箱体验）  
- 忽视邮件发送效果的数据  

---

## 技术参考  

### 文件位置  

- **凭据文件：** `/data/.openclaw/workspace/.kit-credentials`  
- **语音配置文件：** `/data/.openclaw/workspace/.kit-voice-profile.json`  
- **API 客户端脚本：** `skills/kit-email-operator/scripts/kit-api.js`  
- **凭据管理脚本：** `skills/kit-email-operator/scripts/credentials.js`  

### 可用功能  

**来自 `scripts/kit-api.js` 的功能：**  
```javascript
// Broadcasts
kit.createBroadcast(data)
kit.updateBroadcast(id, data)
kit.deleteBroadcast(id)
kit.getBroadcast(id)
kit.listBroadcasts(options)
kit.getBroadcastStats(id)

// Tags
kit.listTags()
kit.tagSubscriber(email, tagId)

// Subscribers
kit.listSubscribers()
kit.getSubscriber(id)

// Custom Fields
kit.listCustomFields()
```  

### 安全性  

- 所有凭据均采用 AES-256-GCM 加密方式存储  
- 绝不记录或显示 API 密钥  
- 文件权限设置为 600（仅限文件所有者读写）  
- 凭据文件不包含在版本控制范围内  

---

## 示例工作流程  

### 工作流程 1：欢迎邮件  

**用户需求：** “为新订阅者编写一封欢迎邮件”  

**操作步骤：**  
```
I can help you write that welcome email. A few quick questions:

1. What should new subscribers know about you/your business?
2. What value will they get from being on your list?
3. Should I include a first resource or action for them?
4. Any specific link to send them to?
```  

**根据用户提供的信息生成内容后：**  
- 提供 3 个主题行选项（表达欢迎之意、明确邮件价值）  
- 生成预览文本  
- 编写邮件正文（自我介绍、说明期望、提供价值、说明下一步行动）  
**然后**：将邮件保存为草稿，请求用户审核，之后安排发送或直接发送。  

### 工作流程 2：产品发布  

**用户需求：** “我正在推出新课程，需要编写一封销售邮件。”  

**操作步骤：**  
```
Got it. Sales email for course launch. Let me ask:

1. What's the course about? (the transformation it provides)
2. Who's it for? (ideal student)
3. Price point?
4. Launch date and any urgency? (early bird, limited spots, etc.)
5. Link to sales page?
6. Should I emphasize social proof, bonuses, or scarcity?
```  

**根据用户提供的信息生成内容后：**  
- 提供 3 个主题行选项（利用用户好奇心或强调紧迫感）  
- 生成预览文本（突出产品优势）  
- 编写邮件正文（介绍问题 → 解决方案 → 转变 → 提供产品 → 行动号召）  
**然后**：与用户共同审核内容，进行优化后发送给特定标签或受众群体。  

### 工作流程 3：重新吸引用户  

**用户需求：** “我想重新联系 60 天内未打开邮件的订阅者。”  

**操作步骤：**  
```
Smart move. Re-engagement campaign. Quick questions:

1. What made you valuable to them when they first subscribed?
2. What's changed or improved since then?
3. Should we give them an option to unsubscribe (clean list)?
4. What's the main value proposition to bring them back?
```  

**根据用户提供的信息生成内容后：**  
- 提供 3 个主题行选项（利用用户的缺席感、表达个性化）  
- 生成预览文本（直接且诚恳）  
- 编写邮件正文（确认用户的缺席、提醒邮件价值、提出简单的请求、提供便捷的退订方式）  
**然后**：在 ConvertKit 中针对特定受众群体发送测试邮件。  

---

## 语音匹配  

如果用户在设置过程中提供了电子邮件样本，请参考相应的语音配置文件：  
**语音配置文件结构：**  
```json
{
  "tone": "casual and direct",
  "sentence_length": "short, punchy sentences mixed with longer ones",
  "vocabulary": ["honestly", "let's be real", "here's the thing"],
  "patterns": [
    "Uses questions to engage",
    "Includes parenthetical asides",
    "Admits limitations honestly"
  ],
  "formatting": [
    "Short paragraphs (1-3 sentences)",
    "Bold for emphasis",
    "Emoji occasionally"
  ],
  "signature": "Ship it,\nKevin"
}
```  

**在生成的邮件中应用这些设置。**  

---

## 故障排除  

### 设置问题  

**问题：** 用户没有 ConvertKit 的访问权限  
**解决方案：** 指导用户进入 ConvertKit 的设置页面 → API 密钥设置  

**问题：** 用于语音训练的样本邮件太短  
**解决方案：** 要求用户提供更长的邮件样本（每封至少 300 字）  

**问题：** 无法找到 ConvertKit 的自定义字段  
**解决方案：** 核对凭据，并确认用户的 ConvertKit 账户中已创建相应的自定义字段  

### 发送问题  

**问题：** 邮件发送失败  
**解决方案：** 检查凭据、验证内容格式，并确保使用的 `tag_ids` 是有效的  

**问题：** 邮件显示异常  
**解决方案：** 检查 HTML 格式，并先给自己发送测试邮件  

**问题：** 开启率低  
**解决方案：** 重新审核主题行、检查发送时间，并分析用户的阅读习惯  

### API 相关问题  

**问题：** 发送频率受限  
**解决方案：** API 客户端具有自动重试机制（采用指数级退避策略）  

**问题：** 凭据无效  
**解决方案：** 重新执行设置流程，并在 ConvertKit 的设置页面中核对凭据信息  

---

## 参考文件  

- **主题行模板：** 查看 `references/subject-line-formulas.md`（包含 50 个经过验证的模板）  
- **邮件结构指南：** 查看 `references/email-best-practices.md`（全面的教学指南）  
- **个性化设置：** 查看 `references/kit-personalization.md`（所有可用的 ConvertKit 自定义标签）  
- **邮件发送流程模板：** 查看 `references/sequence-templates.md`（包含欢迎邮件、培养关系邮件、销售邮件和入职邮件模板）  
- **示例邮件：** 查看 `examples/` 文件夹中的完整邮件模板  

---

## 质量标准  

这是一个 **高级功能**。每次交互都应做到：  
- **专业**：内容精致、无错误、结构清晰  
- **有帮助**：提前预见用户需求、提供指导、提供有用信息  
- **高效**：减少不必要的沟通、设置合理的默认值  
- **安全**：保护用户凭据，绝不泄露敏感信息  
- **人性化**：语言自然、像与人交流一样  

用户为这项服务付费，因此务必保持这些高标准。  

**这项功能代表了 OpenClaw 提供的最高质量的电子邮件营销自动化服务。请始终坚守这些标准。**
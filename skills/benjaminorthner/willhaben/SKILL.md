---
name: willhaben
description: 在 Willhaben.at（奥地利的电商平台）上创建和管理商品列表。适用于用户想要出售物品、发布商品信息或提及 Willhaben 的场景。该工具支持照片上传，自动生成商品标题、描述和价格，并通过浏览器自动化功能完成商品发布。
---

# Willhaben 列表创建工具

通过浏览器自动化在 Willhaben.at 上创建商品列表。

## 首次设置

检查 `config/user-preferences.json` 文件是否存在于技能文件夹中：
- 如果文件不存在 → 运行设置流程（详见 `references/SETUP.md`）
- 如果文件存在 → 读取用户偏好设置并应用到所有列表中

用户偏好设置包括：位置、配送方式、描述风格、定价策略、免责声明等。

## 工作流程

### 1. 获取商品详情
- 用户通过 WhatsApp 或聊天发送商品照片
- 可选：用户提供商品的其他详细信息（如状况、类别、价格范围）

### 2. 市场调研
在建议价格之前，先在 Willhaben 上搜索类似或相同的商品：
- 在 willhaben.at 上搜索该商品
- 注意类似商品的价格范围
- 如果有售出记录，查看其售价
- 将搜索结果告知用户：
  - **Neupreis**（新价格）
  **Marktpreis**（类似商品的市场价格）
  **Empfohlener Preis**（建议售价）

### 3. 生成商品列表
- 分析照片以了解商品情况
- 生成以下内容：
  - **标题**：简洁易搜索（使用德语）
  - **描述**：简短明了——真实用户不会写长篇大论，最多2-3句话，仅提及关键信息
  - **价格**：根据市场调研建议一个合理的价格
  - **包装重量**：估算商品重量以便选择合适的配送选项（3kg / 10kg / 31.5kg）
- 询问用户：
    - 位置（Bezirk）——如果用户未在偏好设置中指定
    - 商品是否有损坏或问题
    - 用户是否需要更详细的描述（默认不需要）
- 提交列表草稿供用户确认，**包括包装重量估算**

### 列表摘要模板
向用户展示如下内容：
```
📝 Listing Draft

Title: [title]
Description: [description]
Price: €XX VB
Location: [location]
Pickup: ✅ / Shipping: ✅

📦 Package: ~Xkg (selecting [size] package)
   → If wrong, let me know!

Photos: X attached

Ready to post?
```

如果商品重量不明确（例如特殊物品），**务必询问用户**，避免错误估计。

### 4. 发布到 Willhaben
具体操作步骤请参见下面的浏览器自动化指南。

## 描述风格

**默认风格：简洁明了**
```
Blue Yeti USB Mikrofon, schwarz. Funktioniert einwandfrei, inkl. Kabel und Standfuß. Privatverkauf, keine Garantie/Rücknahme.
```

**避免使用过于正式或机械化的描述风格（例如：**```
Zum Verkauf steht ein hochwertiges Blue Yeti USB Kondensatormikrofon in der eleganten Blackout Edition. Dieses professionelle Mikrofon eignet sich perfekt für Podcasting, Streaming, Gaming oder Home-Office...
```）

只有在用户明确要求时才添加详细信息。

## 语言
所有列表均使用**德语**（奥地利市场）编写，保持自然流畅的语气，就像真人撰写的描述一样。

---

# 浏览器自动化指南

使用保存了 Willhaben 登录信息的 `clawd` 浏览器插件。

## 第一步：开始创建列表
1. 访问：`https://www.willhaben.at/iad/anzeigenaufgabe`
2. 点击 “Kostenlose Anzeige aufgeben”（免费发布列表的链接）

## 第二步：填写详细信息
表格包含以下字段：

### 图片
- **上传方法**：使用浏览器的 `upload` 功能，并将 `inputRef` 指向 “Bild auswählen” 按钮
- 例如：`browser upload inputRef=e12 paths=[...]`，其中 e12 是按钮的引用
- 可以通过 `paths` 数组一次性上传多张图片
- 上传后，请确认图片已显示为缩略图后再继续下一步

### 价格（Verkaufspreis）
- 文本框，直接输入价格数字（无需添加 € 符号）

### 标题（Titel）
- 文本框，输入格式为 “z.B. Levi's 501 Jeans, schwarz, Größe 32”
- 保持简洁易搜索

### 类别（Kategorie）
- 标题会自动建议相关类别——会出现一个单选框
- **重要**：必须点击类别选项才能完成选择（即使看起来已经选中了）
- 如果建议的类别错误，请点击 “Andere Kategorie wählen”（选择其他类别）

### 状况（Zustand）
- 该选项会在选择类别后出现
- 选项：Neu / Neuwertig / Gebraucht / Defekt（新 / 二手 / 有缺陷）
- 通常选择 “Gebraucht”（二手商品）

### 描述（Beschreibung）
- 采用富文本编辑器（支持内容编辑）
- 先点击文本区域，然后开始输入
- 保持描述简短！

### 联系信息与地址
- 信息来自用户账户设置
- 显示用户名、电子邮件和地址

## 第三步：点击 “Weiter”（下一步）

进入配送选项页面。

## 第四步：配送设置（Übergabe & Versand）
### 配送方式
- **Selbstabholung**（自取）
- **Versand**（选择是否提供配送服务）

### PayLivery（Willhaben 的配送服务）
如果选择了配送服务：
- **包装重量（Versandgröße）**：根据商品实际重量选择合适的选项：
  - **Paket bis 3 kg**（轻量物品）
  - **Paket bis 10 kg**（中型物品，如电子产品、小型家电）
  - **Paket bis 31,5 kg**（重型物品，如带压缩机的家电等）

示例重量：
- 带压缩机的冰淇淋机：约 9kg → 选择 10kg
- 键盘/鼠标：约 1kg → 选择 3kg
- 显示器：约 5kg → 选择 10kg
- 书籍/游戏：约 0.5kg → 选择 3kg
- 笔记本电脑：约 2-3kg → 选择 3kg
- 厨房电器（搅拌机、榨汁机等）：约 3-5kg → 选择 10kg

**⚠️ 如果商品重量不明确**：应在列表摘要步骤中确认重量。如果此时仍不确定，请返回并询问用户！

**运输方式**：Post 或 DPD（Post 为默认选项，适用于大多数情况）

**特殊物品**：检查商品是否超过尺寸限制（>100×60×60cm）或形状不规则

运费由买家支付（显示在页面底部）。

## 第五步：点击 “Weiter”（继续）

进入附加销售产品页面。

## 第六步：附加销售产品页面
显示可购买的促销选项：
- Anzeige vorreihen（€14.99）
- Farblich hervorheben（€7.99）
- TOP Anzeige options（€21.99 - €89.99）

**全部跳过**：直接点击 “Veröffentlichen”（免费发布列表）

页面底部会显示 “Gewählt: € 0”，表示没有选择任何附加服务。

## 第七步：成功！
确认页面显示：
- ✅ “Anzeige erfolgreich aufgegeben”（列表成功发布）
- 列表预览及图片
- **willhaben-Code**：列表 ID（例如 1832624977）
- 注意：**Die Veröffentlichung kann bis zu 24h dauern**（列表可能需要最多24小时才能发布）

**列表链接**：`https://www.willhaben.at/iad/object?adId={willhaben-code}`

---

# 故障排除

### 类别无法选择
即使类别选项显示在页面上，也必须点击才能真正完成选择。出现 “Kategorie muss gewählt werden” 的错误提示表示未点击该选项。

### 图片无法上传
使用 `inputRef` 指向 “Bild auswählen” 按钮（例如 `inputRef=e12`）。**不要使用 `selector: input[type="file"]`——该方法在该网站可能无法正常工作**。

### 元素引用失效
在操作前请始终获取最新的页面数据。页面更新后引用可能会失效。

### 需要登录
如果未登录，请确保浏览器中保存了登录信息。如有需要，可返回登录页面或让用户手动登录。

---

# 快速参考

| 步骤 | URL/操作 |
|------|------------|
| 开始 | `https://www.willhaben.at/iad/anzeigenaufgabe` |
| 免费发布列表 | 点击 “Kostenlose Anzeige aufgeben” |
| 上传图片 | 使用 `inputRef` 指向 “Bild auswählen” 按钮 |
| 下一步 | 点击 “Weiter” |
| 发布列表 | 点击 “Veröffentlichen” |
| 查看列表 | `https://www.willhaben.at/iad/object?adId={ID}` |
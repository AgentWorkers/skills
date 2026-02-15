# 🔖 书签智能

**将您在 X（Twitter）上的书签自动转化为可操作的见解。**

书签智能会监控您的 X 书签，从链接的文章中获取完整内容，利用人工智能进行分析，并筛选出与您的项目相关的信息。不要再让优质内容闲置在书签里了——让人工智能为您提取价值吧。

---

## 💎 价格与层级

书签智能提供三个层级，以满足您的需求：

### 🆓 免费层级
**非常适合试用**
- **价格：** 每月 $0
- **每月 10 个书签**
- 仅支持手动运行（无自动化）
- 基本关键词分析（无人工智能）
- 无通知
- 使用频率限制：每小时 1 次

### ⭐ 专业层级 - 每月 $9
**适合个人用户**
- 无限书签数量
- 自动监控（后台守护进程）
- 全面的人工智能分析（使用 GPT-4o-mini）
- Telegram 通知
- 优先支持

### 🚀 企业层级 - 每月 $29
**适合团队和高阶用户**
- 专业层级所有功能，外加：
- 团队共享与协作
- 自定义人工智能模型（可携带自己的 API 密钥）
- API 接口用于集成
- Slack 和 Discord 通知
- 专属支持

**提供年度套餐** - 可节省 2 个月费用（享受 16% 的折扣！**

### 如何升级

1. **查看当前层级：**
   ```bash
   npm run license:check
   ```

2. **查看升级选项：**
   ```bash
   npm run license:upgrade
   ```

3. **选择支付方式：**
   - 信用卡（Stripe）
   - 加密货币（Polygon 网络上的 USDC）

4. **激活许可证：**
   ```bash
   node scripts/license.js activate YOUR-LICENSE-KEY
   ```

---

## 📋 快速入门

**总设置时间：约 5 分钟**

1. **运行设置向导：**
   ```bash
   cd skills/bookmark-intelligence
   npm run setup
   ```

2. **向导将：**
   - ✅ 检查是否已安装所需工具
   - 🍪 指导您获取 X 的 Cookie（分步操作）
   - 🎯 询问您当前的项目和兴趣
   - ⚙️ 配置通知偏好
   - 🧪 测试您的凭据

3. **运行一次以处理现有书签：**
   ```bash
   npm start
   ```

4. **将其设置为后台守护进程（可选但推荐）：**
   ```bash
   npm run daemon
   ```

就这样！您已经完成了。🎉

---

## 🎯 功能介绍

### 问题
您在 X 上收藏了大量优质内容，但：
- 从未回过头去阅读它们
- 推文链接的文章您没有时间阅读
- 忘记了为什么收藏了这些内容
- 错过了与当前项目的关联

### 解决方案
书签智能：
1. **自动监控** 您的 X 书签
2. **获取** 链接文章的完整内容（而不仅仅是推文）
3. **利用人工智能** 分析所有内容，提取关键概念和可操作的信息
4. **将见解** 与您的具体项目和相关兴趣联系起来
5. **在发现有价值的内容时** 通过 Telegram 通知您
6. **将所有内容** 存储在可搜索的知识库中

### 示例输出

您收藏了一条关于“AI 内存的向量嵌入”的推文 → 该工具会：
- 获取链接的文章
- 提取：关键概念、可操作的实现步骤、代码模式
- 将其与您的“交易机器人”和“代理内存”项目关联起来
- 建议：“将市场分析结果以嵌入形式保存到 `life/resources/bookmarks/bookmark-123.json` 中”
- 通过 Telegram 发送摘要通知给您

请参阅 [examples/sample-analysis.json](examples/sample-analysis.json) 以获取完整示例。

---

## 🍪 获取 X 的 Cookie（分步操作）

您需要从 X.com 获取两个 Cookie。请放心，这个过程很安全，只需 2 分钟。

### Chrome / Edge / Brave

1. 在浏览器中打开 https://x.com
2. **确保已登录**
3. 按下 **F12**（打开开发者工具）
4. 点击顶部的 **应用程序** 标签
5. 在左侧边栏中：
   - 展开 **Cookies**
   - 点击 **https://x.com**
6. 您会看到一个 Cookie 列表。找到以下两个：
   - `auth_token` → 复制 **Value** 列
   - `ct0` → 复制 **Value** 列

```
┌─────────────────────────────────────────┐
│ Application  Console  Sources  ...     │ ← Click "Application"
├─────────────────────────────────────────┤
│ ▼ Storage                               │
│   ▼ Cookies                             │
│     ▶ https://x.com      ← Click this   │
│                                         │
│ Name          Value                     │
│ auth_token    abc123...  ← Copy this    │
│ ct0           xyz789...  ← Copy this    │
└─────────────────────────────────────────┘
```

### Firefox

1. 打开 https://x.com
2. 按下 **F12**
3. 点击 **存储** 标签（不是“应用程序”）
4. 展开 **Cookies** → **https://x.com**
5. 复制 `auth_token` 和 `ct0` 的值

### Safari

1. 启用开发者菜单：
   - Safari → 首选项 → 高级设置
   - 勾选“在菜单栏显示开发者菜单”
2. 访问 https://x.com
3. 开发者 → 显示网络开发者工具
4. 存储标签 → Cookies → x.com
5. 复制 `auth_token` 和 `ct0`

### ⚠️ 重要安全提示

- **这些 Cookie 就像您的密码** —— 它们可以完全访问您的 X 账户
- **切勿与任何人共享**
- **不要将它们发布到网上或提交到 git**
- 它们存储在本地 `.env` 文件中，并具有严格的权限设置（600 = 仅您可以读取）
- 它们会定期过期——您需要更新它们（该工具会提醒您）

设置向导会创建一个如下所示的 `.env` 文件：
```bash
AUTH_TOKEN=your_long_token_here
CT0=your_other_token_here
```

---

## 🛠️ 要求

### 必需软件
- **Node.js** v16+（[在此处下载](https://nodejs.org)
- **bird CLI** —— X/Twitter 命令行工具
  ```bash
  npm install -g bird
  ```

### 可选（但推荐）
- **PM2** —— 用于作为后台守护进程运行
  ```bash
  npm install -g pm2
  ```

设置向导会自动检查这些软件是否已安装！

---

## ⚙️ 配置

运行 `npm run setup` 后，您将拥有两个文件：

### 1. `.env` - 您的凭据
```bash
AUTH_TOKEN=your_token_here
CT0=your_ct0_here
```
**请勿提交此文件！** 它被包含在 `.gitignore` 文件中。

### 2. `config.json` - 您的偏好设置
```json
{
  "credentialsFile": ".env",
  "bookmarkCount": 50,
  "checkIntervalMinutes": 60,
  "storageDir": "../../life/resources/bookmarks",
  "notifyTelegram": true,
  "contextProjects": [
    "trading bot",
    "agent memory",
    "your other projects..."
  ]
}
```

**关键设置：**
- `bookmarkCount` - 检查的最近书签数量（默认：50 个）
- `checkIntervalMinutes` - 检查新书签的频率（默认：60 分钟）
- `contextProjects` - **您的活跃项目** —— 描述越具体，人工智能分析效果越好！
- `notifyTelegram` - 在发现高价值见解时接收通知（需要 OpenClaw）

您可以随时编辑 `config.json`。更改将在下一次运行时生效。

---

## 🚀 使用方法

### 运行一次（处理现有书签）
```bash
npm start
```
处理一次您的最近书签后退出。

### 测试模式（查看实际效果）
```bash
npm test
```
显示在不实际执行操作时的处理过程。

### 后台守护进程（建议每日使用）
```bash
npm run daemon
```

这会将书签智能作为后台进程运行，每小时检查一次新书签（可配置）。

**管理守护进程：**
```bash
pm2 status bookmark-intelligence   # Check if it's running
pm2 logs bookmark-intelligence     # View recent logs
pm2 stop bookmark-intelligence     # Pause it
pm2 restart bookmark-intelligence  # Restart it
pm2 delete bookmark-intelligence   # Remove it completely
```

---

## 📂 数据存储位置

```
skills/bookmark-intelligence/
├── .env                    # Your credentials (SECRET - never commit!)
├── config.json             # Your preferences
├── bookmarks.json          # Processing state (tracks what's been analyzed)
├── monitor.js              # Main script
├── analyzer.js             # AI analysis engine
├── scripts/
│   ├── setup.js           # Setup wizard
│   └── uninstall.js       # Clean uninstall
└── examples/              # Sample outputs to show you what to expect

life/resources/bookmarks/   # ← Analyzed bookmarks saved here
├── bookmark-123.json
├── bookmark-456.json
└── ...
```

每个分析后的书签都会生成一个 JSON 文件，其中包含：
- 原始推文（作者、文本、互动数据）
- 完整分析结果（摘要、关键概念、可操作项）
- 针对您项目的实施建议
- 优先级
- 时间戳

---

## 🔔 通知（与 OpenClaw 集成）

如果您在 OpenClaw 中运行此工具（而非独立运行），您可以收到高价值见解的 Telegram 通知。

**触发通知的条件：**
- `priority: "high"` 且
- `hasActionableInsights: true`

**您将收到：**
- 📚 内容摘要
- 🎯 可操作项列表
- 💡 关键概念
- 🔨 针对您项目的实施建议
- 🔗 原始推文的链接

请参阅 [examples/sample-notification.md](examples/sample-notification.md) 以获取完整示例。

---

## 🧹 卸载

```bash
npm run uninstall
```

这将：
1. 停止 PM2 守护进程（如果正在运行）
2. 删除您的凭据（`.env` 文件）
3. 删除配置文件（`config.json`）
4. 删除处理状态文件（`bookmarks.json`）
5. **询问** 是否希望保留已分析的书签

如需重新安装，只需再次运行 `npm run setup` 即可。

---

## 🔧 故障排除

### “缺少 Twitter 凭据” 错误

**问题：** 工具无法找到您的认证令牌。

**解决方案：**
1. 确保已运行 `npm run setup`
2. 检查 `.env` 文件是否存在于 `skills/bookmark-intelligence/` 目录下
3. 确保 `.env` 文件中包含 `AUTH_TOKEN=` 和 `CT0=` 这两行

### “未获取书签” 或 “未经授权” 错误

**问题：** 您的 Cookie 无效或已过期。

**解决方案：**
1. 从 X.com 获取新的 Cookie（参见上述说明）
2. 用新值更新 `.env` 文件
3. 尝试运行 `npm test` 进行验证

**手动测试凭据的方法：**
```bash
cd skills/bookmark-intelligence
source .env
bird whoami --json
```
如果此方法有效，说明您的凭据是有效的。

### “bird: 命令未找到” 错误

**问题：** 未安装 bird CLI。

**解决方案：**
```bash
npm install -g bird
```

### 守护进程未运行/意外停止

**问题：** 可能是 PM2 未安装，或者守护进程崩溃了。

**解决方案：**
```bash
# Check PM2 is installed
pm2 --version

# If not, install it
npm install -g pm2

# Check daemon status
pm2 status

# View logs to see what happened
pm2 logs bookmark-intelligence

# Restart
npm run daemon
```

### 分析结果显得泛泛而谈/不相关

**问题：** 人工智能不了解您的关注点。

**解决方案：**
1. 编辑 `config.json`
2. 使用更具体的项目描述更新 `contextProjects`：
   ```json
   "contextProjects": [
     "Building a crypto trading bot using Python and Binance API",
     "Learning Rust for systems programming",
     "Growing my SaaS to $10k MRR"
   ]
   ```
3. 重新启动：`pm2 restart bookmark-intelligence`

描述越具体，人工智能就越能将见解与您的工作联系起来！

---

## 🔐 隐私与数据

**数据存储位置：**
- 凭据：`.env` 文件（本地文件，权限设置为 600）
- 分析后的书签：`life/resources/bookmarks/`（本地文件）
- 除了以下情况外，不会向任何第三方发送数据：
  - X.com（用于获取您的书签）
  - OpenAI/Anthropic（用于人工智能分析，如果使用 OpenClaw LLM）
  - 链接的网站（用于获取文章内容）

**没有 OpenClaw 也可以使用吗？**
- 可以！它可以独立运行
- 无法使用 LLM 分析（此时会使用基于关键词的分析）
- 无法接收 Telegram 通知
- 其他功能均正常使用

**安全吗？**
- 您的凭据不会离开您的设备
- `.env` 文件被包含在 `.gitignore` 中，因此不会被意外提交
- 文件权限设置为 600（仅所有者可读/写）
- 无遥测数据，无日志记录

---

## 🎨 自定义选项

熟悉基本功能后，您可以进行以下自定义：

### 更改通知阈值
编辑 `monitor.js` 文件中大约第 120 行的代码，以便在 **中等优先级** 时也接收通知：
```javascript
if (config.notifyTelegram && (analysis.priority === 'high' || analysis.priority === 'medium')) {
```

### 处理更多书签
编辑 `config.json` 文件：
```json
{
  "bookmarkCount": 100  // Check last 100 bookmarks
}
```

### 更频繁地检查
```json
{
  "checkIntervalMinutes": 30  // Check every 30 minutes
}
```

### 导出到 Notion / Obsidian
在 `scripts/export-to-notion.js` 中添加自己的导出脚本——每个书签都已经是格式化的 JSON 格式！

---

## 📚 示例

请查看 `examples/` 文件夹：
- **sample-analysis.json** —— 完整分析的示例
- **sample-notification.md** —— 您在 Telegram 中会看到的通知内容

---

## 🐛 发现漏洞？

请在 ClawHub 上提交问题或拉取代码请求！

常见问题：
- Cookie 过期 → 只需用新的 Cookie 更新 `.env` 文件
- 使用频率限制 → 减少 `bookmarkCount` 或增加 `checkIntervalMinutes`
- 分析质量 → 使 `contextProjects` 的描述更具体

---

## 📜 许可证

MIT 许可证 —— 您可以自由使用此工具！

---

## 💳 支付与许可

### 接受的支付方式

**信用卡（Stripe）**
- 支持所有主要信用卡
- 即时激活
- 自动续订
- 随时取消

**加密货币**
- Polygon 网络上的 USDC
- 低交易费用（约 $0.01）
- 需手动验证（24 小时内激活）
- 请在付款备注中注明付款金额

### 支付流程

1. 运行 `npm run license:upgrade` 查看可用选项
2. 选择您的层级和支付方式
3. 对于 Stripe：点击链接完成支付
4. 对于加密货币：将 USDC 发送到提供的地址，并在备注中注明付款金额
5. 您将通过电子邮件收到许可证密钥
6. 激活许可证：`node scripts/license.js activate <key>`

### 许可证管理

**随时查看您的状态：**
```bash
npm run license:check
```

**您的许可证包含：**
- 订阅层级和功能
- 本月处理的书签数量
- 到期日期
- 续期期限（到期后 3 天）

**续订：**
- 每月：自动续订，每 30 天一次
- 年度：自动续订，每 365 天一次
- 您将收到续订提醒

### 退款政策

- **年度套餐提供 30 天退款保证**
- 月度订阅：首次付款后 7 天内可退款
- 请通过许可证密钥或付款信息联系客服
- 退款将在 5-7 个工作日内处理

### 隐私政策

- **支付处理：** 使用 Stripe（PCI-DSS 1 级认证）
- 我们不会存储您的信用卡信息
- 许可证密钥在您的设备上加密存储
- 使用数据仅存储在本地

### 支持

**免费层级：** 通过 GitHub 问题进行社区支持
**专业层级：** 电子邮件支持（48 小时内回复）
**企业层级：** 优先支持（8 小时内回复）+ Slack 频道

---

## ❓ 常见问题

### 通用问题

**Q：使用此工具需要 OpenClaw 吗？**
A：不需要！它可以独立使用。使用 OpenClaw 可以获得 LLM 分析和通知，但这不是必需的。

**Q：可以在付费前试用吗？**
A：可以！从免费层级开始（每月 10 个书签）。无需信用卡。

**Q：如何升级或降级？**
A：运行 `npm run license:upgrade` 升级。如需降级，请在续订前联系客服。

**Q：如果超出免费层级限制怎么办？**
A：处理将停止在 10 个书签处。系统会提示您升级。您的数据是安全的。

### 计费

**Q：可以随时取消吗？**
A：可以！无需任何承诺。在下一个 billing 日之前取消即可，无需支付费用。

**Q：提供折扣吗？**
A：年度套餐可节省 2 个月费用（16% 的折扣）。学生和非营利组织可享受折扣——请联系客服。

**Q：如果支付失败怎么办？**
A：您有 3 天的退款期限来更新支付信息。之后将降级为免费层级。

**Q：可以获取发票吗？**
A：可以！发票会自动发送电子邮件。企业客户可以请求定制发票。

### 技术问题

**Q：免费层级使用人工智能分析吗？**
A：不，免费层级使用基于关键词的启发式方法。升级到专业层级可享受全面的人工智能分析。

**Q：自动化是如何工作的？**
A：专业/企业层级可以作为后台守护进程（PM2）运行，自动检查书签。

**Q：可以使用自己的 AI API 密钥吗？**
A：仅企业层级支持。支持 OpenAI、Anthropic 和自定义 API。

**Q：我的数据是否保密？**
A：是的！所有数据都在本地处理。您的书签仅用于人工智能分析，不会离开您的设备。

**Q：如果更换设备怎么办？**
A：您的许可证密钥仅在一个设备上有效。如需转移许可证，请联系客服。

### 对于销售商（如果通过 ClawHub 分发）

**Q：如何配置支付方式？**
A：编辑 `payment-config.json` 文件，添加您的 Stripe 密钥和/或加密货币钱包地址。

**Q：可以更改价格吗？**
A：可以！编辑 `payment-config.json` 文件中的价格设置。

**Q：如何发放试用许可证？**
A：使用管理员面板：`node scripts/admin.js issue pro user@example.com trial`

**Q：如何跟踪收入？**
A：运行 `npm run admin:revenue` 查看收入统计。

---

## 🤝 贡献

欢迎提交代码请求！改进方向包括：
- 更好的内容提取（处理付费墙、PDF 等）
- 去重（避免重复分析相似的书签）
- 模式检测（发现书签中的重复主题）
- 交互式 Telegram 用户界面（实现/关闭/保存功能）
- 导出到 Notion / Obsidian 的集成

---

**用心为您和 OpenClaw 制作**

有问题？请查看上面的故障排除指南或在 OpenClaw 社区中提问！
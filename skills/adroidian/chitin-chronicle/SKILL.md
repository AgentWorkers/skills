# Chitin Editorial — 多智能体内容管理系统

**版本：** 1.0.0  
**作者：** Vesper 🌒  
**适用场景：** 多智能体内容协作（Vesper + Ember）  
**用途：** 防止重复发布、追踪内容时间线、通过“声明”机制进行协调  

---

## Chitin Editorial 的功能  

Chitin Editorial 是一个基于 Git 的协调系统，用于两个 AI 智能体在多个渠道上发布内容。它解决了以下问题：  
1. **防止重复发布**：两个智能体在发布前都会检查内容是否已被其他智能体发布。  
2. **时间线追踪**：将内容发布的日期映射到日历日期。  
3. **跨智能体协作**：一个智能体声明某项工作后，其他智能体会看到该声明并避免重复发布。  
4. **发布历史记录**：记录所有内容的发布时间和渠道。  
5. **启动时自动加载状态**：智能体会在会话开始时自动加载编辑状态。  

---

## 快速入门  

### 1. 添加到启动脚本中  

在 `AGENTS.md` 的启动脚本部分添加以下代码：  
```bash
bash /home/aaron/.openclaw/workspace/skills/chitin-chronicle/editorial/boot-check.sh
```  
这样每次启动时都会显示编辑状态。  

### 2. 发布内容前  

```bash
# Check if safe to publish
node /home/aaron/.openclaw/workspace/skills/chitin-chronicle/scripts/editorial.js check "day-14" "substack"
```  
如果存在冲突或内容已被发布，系统会显示错误提示。  

### 3. 声明你的工作  

```bash
# Claim before drafting
node /home/aaron/.openclaw/workspace/skills/chitin-chronicle/scripts/editorial.js claim "day-14" "publish" "substack"
```  
其他智能体会看到你的声明，从而避免重复发布相同的内容。  

### 4. 发布内容后  

```bash
# Record the publication
node /home/aaron/.openclaw/workspace/skills/chitin-chronicle/scripts/editorial.js publish "day-14" "substack" "https://chitin.substack.com/p/day-14" "Day 14: Title Here"
```  
该操作会：  
- 将内容添加到日志中  
- 更新注册表  
- 释放你的声明  
- 提交到 Git。  

---

## 命令行接口（CLI）参考  

### `editorial status`  
显示当前的编辑状态：  
- 正在处理的声明  
- 最近的发布记录（48 小时内）  
- 时间线状态  
- 统计信息  

```bash
node scripts/editorial.js status
```  

### `editorial claim <内容ID> <操作> <渠道>`  
声明对某项内容的所有权，防止其他智能体重复发布。  
**参数：**  
- `内容ID`：唯一标识符（例如：“day-14”、“trust-architecture”）  
- `操作`：你要执行的操作（“publish”、“draft”、“review”）  
- `渠道**：内容发布的平台（“substack”、“twitter”等）  
**示例：**  
```bash
node scripts/editorial.js claim "day-14" "publish" "substack"
```  
**行为：**  
- 检查是否存在冲突（其他智能体是否已声明同一内容）  
- 将声明文件写入 `editorial/claims/`  
- 提交到 Git  
- 如果 2 小时内未发布，声明将自动失效。  

### `editorial release <内容ID>`  
取消对内容的声明（例如：计划变更）。  
**示例：**  
```bash
node scripts/editorial.js release "day-14"
```  
**行为：**  
- 将声明移至 `editorial/claims/archive/`  
- 提交到 Git。  

### `editorial check <内容ID> <渠道>`  
检查是否可以安全发布（无冲突、内容未被发布）。  
**示例：**  
```bash
node scripts/editorial.js check "day-14" "substack"
```  
**返回码：**  
- `0`：可以安全发布  
- `1`：存在冲突或内容已被发布  
**建议在声明前使用此命令，避免浪费资源。**  

### `editorial publish <内容ID> <渠道> <URL> [标题]`  
将内容发布到日志中。  
**参数：**  
- `内容ID`：内容标识符  
- `渠道`：发布平台  
- `URL`：内容的实际链接  
- `标题`：（可选）人类可读的标题  
**示例：**  
```bash
node scripts/editorial.js publish "day-14" "substack" "https://chitin.substack.com/p/day-14" "Day 14: Trust Architecture"
```  
**行为：**  
- 将信息添加到 `editorial/ledger.json`（不可更改的日志）  
- 更新 `editorial/registry.json`（状态更新为“已发布”）  
- 自动释放声明  
- 提交到 Git。  

---

## 文件结构  

### `registry.json`  
记录内容的全生命周期。  
**数据结构：**  
```json
{
  "id": "day-14",
  "title": "Day 14: Trust Architecture",
  "type": "post",
  "status": "published",
  "author": "vesper",
  "channels_published": ["substack", "twitter"],
  "created_at": "2026-02-28T10:00:00Z",
  "published_at": "2026-02-28T14:30:00Z"
}
```  

### `ledger.json`  
只读的发布日志。一旦记录，内容将永久保存。  
**数据结构：**  
```json
{
  "content_id": "day-14",
  "title": "Day 14: Trust Architecture",
  "channel": "substack",
  "author": "vesper",
  "published_at": "2026-02-28T14:30:00Z",
  "url": "https://chitin.substack.com/p/day-14",
  "status": "published"
}
```  

### `timeline.json`  
将内容发布的日期映射到日历日期。  
**数据结构：**  
```json
{
  "series": {
    "building-vesper": {
      "day_zero": "2026-02-15",
      "days": [
        {
          "day": 0,
          "date": "2026-02-15",
          "title": "Day 0: Birth",
          "author": "vesper",
          "published": true
        }
      ]
    }
  }
}
```  

### `claims/*.claim`  
正在处理的声明文件。声明会在 2 小时后自动失效。  
**文件命名规则：** `{内容ID}-{智能体}.claim`  

---

## 工作流程  

### 典型发布流程  

```bash
# 1. Check for conflicts
node scripts/editorial.js check "day-14" "substack"

# 2. Claim the work
node scripts/editorial.js claim "day-14" "publish" "substack"

# 3. Draft your content (outside this tool)
# ... write the post ...

# 4. Publish to the platform (outside this tool)
# ... post to Substack ...

# 5. Record the publication
node scripts/editorial.js publish "day-14" "substack" "https://..." "Day 14: Title"
```  

### 跨智能体协作  

**Vesper：**  
```bash
node scripts/editorial.js claim "day-14" "publish" "substack"
```  
**Ember**（之后会检查状态）：  
```bash
node scripts/editorial.js status
# Sees: vesper claimed "day-14" on substack
# Decides to work on Twitter thread instead
node scripts/editorial.js claim "day-14" "publish" "twitter"
```  
两个智能体会在不同的渠道上处理相同的内容，从而避免重复发布。  

### 取消工作  

```bash
# Claim something
node scripts/editorial.js claim "day-15" "draft" "substack"

# Change your mind
node scripts/editorial.js release "day-15"
```  

---

## 启动脚本集成  

### 手动检查  
随时运行启动脚本：  
```bash
bash editorial/boot-check.sh
```  
**输出结果：**  
```
📋 Editorial State

🔥 Active Claims: 1
   day-14-vesper

📰 Recent Publications (48h): 2
   2026-02-28 | substack | vesper | Day 13: Trust
   2026-02-27 | twitter | ember | Day 12 thread

✓ Timeline current: building-vesper (Day 13)

Run 'node scripts/editorial.js status' for details
```  

### 会话开始时自动加载  
在 `AGENTS.md` 的启动脚本中添加以下代码（在读取 `SOUL.md` 和 `USER.md` 之后）：  
```markdown
## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Run `bash /home/aaron/.openclaw/workspace/skills/chitin-chronicle/editorial/boot-check.sh` — load editorial state
4. Continue with normal startup...
```  
这样确保你在启动时总能看到编辑状态，即使在数据压缩后也是如此。  

---

## Git 集成  
所有状态变更都会自动提交到 Git：  
```bash
# Claiming
git commit -m "editorial: vesper claimed day-14 for publish on substack"

# Publishing
git commit -m "editorial: vesper published day-14 on substack"

# Releasing
git commit -m "editorial: ember released claim on day-15"
```  
**为什么使用 Git？**  
- 提供审计追踪：谁在何时做了什么  
- 可恢复性：如果 JSON 文件损坏，可以回滚  
- 支持多智能体同时写入  
- 记录内容的发展历程  

**无需推送** — 同一主机上的智能体只需使用本地提交即可。  

---

## 技术细节  

### 性能  
所有操作耗时不到 500 毫秒：  
- `status`：约 50 毫秒（读取 3 个 JSON 文件）  
- `claim`：约 100 毫秒（写入 + 提交到 Git）  
- `check`：约 30 毫秒（仅读取）  
- `publish`：约 150 毫秒（写入 2 个文件 + 提交到 Git）  

### 依赖项  
**无外部依赖**：  
- 仅使用 Node.js 内置模块（`fs`、`path`、`child_process`）  
- 需要 Git  
- 需要 Bash 来运行启动脚本  

### 声明失效机制  
声明会在 2 小时后自动失效。`editorial.js` 工具会：  
1. 在读取时检查声明的时效  
2. 将过期的声明移至 `archive/`  
3. 避免在编辑过程中出现冲突  

### 冲突检测  
在声明或检查之前，工具会：  
1. 读取所有 `.claim` 文件  
2. 过滤掉过期的声明  
3. 检查是否存在不同的智能体发布的相同内容。  
如果找到相同的内容和渠道，则视为冲突。  

### 智能体身份识别  
工具使用以下方式识别智能体：  
1. `$OPENCLAW_AGENT` 环境变量  
2. `$USER` 环境变量  
3. 默认值：“unknown”  
在会话中设置 `OPENCLAW_AGENT=vesper` 或 `OPENCLAW_AGENT=ember`。  

---

## 测试  
**运行测试套件**  
```bash
cd /home/aaron/.openclaw/workspace/skills/chitin-chronicle

# Test 1: Status (should show empty state)
node scripts/editorial.js status

# Test 2: Claim
node scripts/editorial.js claim "day-14" "publish" "substack"

# Test 3: Check (should show safe)
node scripts/editorial.js check "day-14" "substack"

# Test 4: Publish
node scripts/editorial.js publish "day-14" "substack" "https://test.com" "Test Post"

# Test 5: Check again (should show already published)
node scripts/editorial.js check "day-14" "substack"

# Test 6: Status (should show 1 publication)
node scripts/editorial.js status

# Test 7: Boot check
bash editorial/boot-check.sh
```  
所有测试应通过，并显示相应的输出结果。  

---

## 开发计划  

### 第 1 周（已完成）  
- [x] 内容注册表  
- [x] 发布日志  
- [x] 时间线追踪器  
- [x] 跨智能体声明系统  
- [x] 启动脚本集成  
- [x] 命令行工具  

### 第 2 周  
- [ ] 多渠道调度器（一个内容发布到多个平台）  
- [ ] 自动风格检查功能  
- [ ] 内容重用机制（在不同渠道间重复使用内容）  

### 第 1 个月  
- [ ] 内容质量审核（拼写、链接、SEO）  
- [ ] 智能体协作协议（正式化的工作交接流程）  
- [ ] 分析反馈循环（分析用户互动以优化决策）  

---

## 故障排除  

### “冲突：其他智能体已声明该内容”  
有人正在处理相同的 content/channel 组合。  
**处理方式：**  
1. 等待其声明失效（2 小时）  
2. 直接沟通协调（通过 Telegram/Discord）  
3. 在其他渠道上继续处理内容  

### “内容已被发布”  
如果内容已被发布：  
1. 使用不同的 `内容ID`（例如：“day-14-v2”）  
2. 或手动编辑 `ledger.json`（不推荐）  

### Git 提交失败  
如果遇到 Git 提交失败：  
1. 确保 `editorial/` 目录在 Git 仓库中  
2. 如有必要，运行 `cd editorial && git init`  
3. 检查 Git 配置（`git config user.email`）  
该工具会忽略提交失败，操作仍可继续进行。  

### 启动脚本无输出  
如果 `boot-check.sh` 无输出：  
1. 确保脚本可执行（`chmod +x`）  
2. 检查 JSON 文件是否存在（`ls editorial/`）  
3. 手动运行脚本：`bash editorial/boot-check.sh`  

---

## 许可证  
MIT 许可证 — 所有 Chitin Trust 智能体及其衍生产品均可免费使用。  

---

**开发者：Vesper 🌒 | 2026-02-28 | 最佳状态**
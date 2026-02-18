---
name: task-experience-summaries
description: OpenClaw任务的经验总结，包括常见的安装问题、故障排除步骤，以及关于包、配置和工具的最佳实践。在遇到安装问题、遇到未知错误信息，或需要了解包名和配置方法时，请参考这些内容。同时，也可将这些总结用于记录新的使用经验，以便将来参考。
---
# 任务经验总结

## 概述

本技能提供了来自真实 OpenClaw 任务的经验总结，包括：

- 安装/打包问题及其解决方案
- 常见错误信息及其根本原因
- 包包搜索和发现方法
- 配置模式和环境设置
- 工具特定的故障排除步骤
- 记录新经验的最佳实践

每个条目包含：问题 → 解决方案 → 关键经验 → 预防措施。

## 常用安装包

### ClawHub CLI

**用途：** 通过 clawhub.com 搜索、安装、更新和发布 OpenClaw 技能。

**安装：**
```bash
npm install -g clawhub
```

**使用方法：**
```bash
# Search for skills
clawhub search "keyword"

# Install a skill
clawhub install "skill-name"

# List installed skills
clawhub list

# Publish a new skill (when ready)
clawhub publish "skill-directory"
```

**身份验证：**
- 令牌：`clh_<token>`
- 用户名：`@<username>`
- 获取地址：https://clawhub.ai

### Tavily 搜索

**用途：** 通过 Tavily API 进行人工智能优化的网络搜索。

**配置：**
```bash
# Set environment variable
set TAVILY_API_KEY=your-api-key-here
```

**使用方法：**
- 搜索查询：`web_search` 工具
- API 密钥位置：`<skill-dir>/README_CONFIG.md`
- 适用性：对 AI 代理具有高相关性

---

## 故障排除类别

### 1. 包安装问题

#### 问题：npm 404 未找到

**场景：** 安装命令失败，显示“404 未找到”

**解决方案：**
1. 检查包名拼写
2. 在 ClawHub 中搜索：`clawhub search "关键词"`
3. 尝试使用 npm 搜索：`npm search "关键词"`
4. 验证包是否存在于 npm 注册表中

**常见解决方法：**
- 包名错误（例如，`tavily-search` 应为 `tavily-mcp`）
- 包被删除或重命名
- 命令中存在拼写错误

**关键经验：** 安装前务必验证包的存在性。使用搜索工具。

#### 问题：Windows 权限错误（EEXIST）

**场景：** 安装失败，显示“EEXIST：文件已存在”

**解决方案：**
```bash
npm i -g clawhub --force
```

**根本原因：** 旧版本文件残留，导致安装受阻

**预防措施：** 在 Windows 上进行全局安装时使用 `--force` 参数

#### 问题：未知包名

**场景：** 包在 npm 注册表中找不到

**解决方案：**
1. 在 ClawHub 中搜索：`clawhub search "关键词"`
2. 尝试使用更宽泛的搜索词
3. 检查该技能是否托管在 ClawHub（OpenClaw 的官方注册表）上

**示例：**
```
Initial attempt: npm install "find-skills" → 404
Solution: clawhub search "find-skills" → Found "find-skills v0.1.0"
Result: clawhub install "find-skills" → Success
```

**关键经验：** 首先在 ClawHub 中查找 OpenClaw 技能的相关信息。

### 2. 配置问题

#### 环境变量

**标准模式：**
```bash
# SET in current session
set ENV_VAR=value

# For persistent settings, add to shell config
# (e.g., .bashrc, .zshrc, PowerShell profile)
```

**常见变量：**
- `TAVILY_API_KEY` - 用于网络搜索工具
- `OPENAI_API_KEY` - 如需使用基于 OpenAI 的技能
- 特定工具的自定义凭据

**验证方法：**
```bash
echo $TAVILY_API_KEY  # Unix-like
echo %TAVILY_API_KEY% # PowerShell/CMD
```

### 3. 工具特定问题

#### OpenClaw 浏览器扩展

**症状：** 浏览器操作后出现“标签页未找到”的错误

**解决方案：**
1. 重启 OpenClaw Gateway（OpenClaw.app → 重启）
2. 保持 Chrome 扩展程序的图标显示（不要关闭）
3. 操作过程中不要关闭浏览器标签页
4. 重新连接：打开扩展程序 → 附加标签页 → 保持图标显示

**最佳实践：**
- 浏览器工具适用于一次性操作或截图
- 不适合长时间运行的自动化会话
- 对于持续需求，直接使用浏览器交互更为可靠

#### 浏览器配置文件问题

**症状：** 多个配置文件导致冲突

**解决方案：**
- 使用 `--profile=chrome` 为 Chrome 浏览器设置配置文件
- 使用 `--profile=openclaw` 为独立浏览器设置配置文件
- 如果问题仍然存在，使用干净的配置文件进行测试

**状态检查：**
```bash
openclaw gateway status
```

---

## 问题解决流程

### 第一步：确定问题类别

判断问题属于以下哪一类：
- 安装问题
- 配置问题
- 工具特定故障
- 包包发现问题
- 平台特定行为（Windows/Linux/macOS）

### 第二步：查阅总结

使用上述表格和分类条目：
- 将症状与相应类别匹配
- 查看相关解决方案
- 尝试推荐的解决方法

### 第三步：测试解决方案

按顺序应用建议的解决方法：
1. 先尝试最常见/最简单的解决方案
2. 接着尝试针对特定平台的解决方案
3. 最后尝试高级配置设置

### 第四步：记录新经验

**何时记录：**
- 成功解决了未知问题
- 发现了新的模式或解决方法
- 学到了配置技巧
- 发现已记录的解决方案存在差异

**记录方法：**
1. 清晰记录问题
2. 记下解决方案步骤
3. 包括平台特定细节
4. 添加预防/避免问题再次发生的措施
5. 更新本 SKILL.md 文件中的相关内容

**新条目的模板：**
```markdown
### Problem: [Clear description]

**Scenario:** [Context where problem occurs]

**Solution:** [Step-by-step resolution]

**Root Cause:** [Why this happens]

**Prevention:** [How to avoid]

**Platform Notes:** [If platform-specific]
```

### 第五步：迭代和完善

使用该技能后进行回顾：
- 条目是否清晰易懂？
- 症状和解决方案是否匹配？
- 格式是否一致？
- 是否有遗漏的常见问题？

---

## 快速参考表

| 问题类型 | 症状 | 主要工具 | 关键命令 |
|-----------|----------|--------------|-------------|
| 包未找到 | 404 错误 | npm, ClawHub | `clawhub search "关键词"` |
| 权限错误 | EEXIST、访问拒绝 | npm install | 使用 `--force` 参数 |
| 配置缺失 | 工具无法运行 | 环境变量 | `set VAR=value` |
| 浏览器连接问题 | 标签页未找到 | 浏览器工具 | 重启 Gateway 并保持扩展程序图标显示 |
| 未知包 | 无法安装 | clawhub list | `clawhub install "包名"` |

---

## 最佳实践

1. **先搜索再猜测：** 始终先使用搜索工具
2. **记录解决方案：** 将所学内容全部记录下来
3. **分类问题：** 按类型分类以便快速查找
4. **记录平台差异：** 记录 Windows/macOS/Linux 之间的差异
5. **预防为主：** 添加预防措施以避免问题再次发生
6. **注重实用性：** 重点记录可操作的步骤，而非理论内容

---

## 示例用法

### 示例 1：安装新技能

```bash
# User asks: "I need a weather skill for checking forecasts"

# Step 1: Search
clawhub search "weather"

# Step 2: Identify candidate
Found: "weather v1.0" - Get current weather and forecasts (no API key required)

# Step 3: Install
clawhub install "weather"

# Step 4: Configure (if needed)
# Check README_CONFIG.md for required environment variables

# Step 5: Use
# Use web_search tool with query: "weather today"
```

### 示例 2：排查浏览器问题

```bash
# Symptom: Browser tool reports "tab not found"

# Step 1: Restart Gateway (first fix)
OpenClaw.app → Restart

# Step 2: Check extension
✓ Badge indicator should be ON
✓ Running state
✓ CDP Ready (Chrome DevTools Protocol)

# Step 3: Reattach if needed
Click OpenClaw extension icon → Attach tab → Badge ON

# Step 4: Verify
Try browser open → snapshot
```

### 示例 3：查找未知包

```bash
# Symptom: "I need an RSS feed parser" - package unknown

# Step 1: ClawHub search
clawhub search "rss"

# Step 2: Identify
Found: "rss-parser skill v0.5.0" with description "Parse RSS feeds"

# Step 3: Install
clawhub install "rss-parser"

# Result: Success
```

---

## 注意事项

- 所有条目均基于实际解决的问题
- 当涉及平台特定行为时，会进行说明
- 配置细节基于当前的工作环境设置
- 对于新出现的问题，在依赖这些总结之前，请务必查阅官方文档。
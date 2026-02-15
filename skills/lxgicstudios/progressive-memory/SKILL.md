# 进阶式内存系统（Progressive Memory）

这是一种专为AI智能体设计的、高效利用内存的系统。系统会先扫描索引，然后根据需求获取具体信息。该设计基于Claude-Mem提出的“渐进式数据披露”（progressive disclosure）原则。

## 问题所在

传统的内存管理系统会将所有数据一次性加载到内存中：
- 通常会加载3500个“令牌”（tokens）量的历史数据；
- 其中94%的数据与当前任务无关；
- 这不仅浪费了计算资源，还导致内存中的数据变得陈旧（无法有效利用）。

## 解决方案

**渐进式数据披露**：先展示用户需要了解的信息，再由智能体决定是否需要进一步获取更多数据。

```
Before: 3500 tokens loaded → 200 relevant (6%)
After:  100 token index → fetch 200 needed (100%)
```

## 内存格式

### 每日文件（`memory/YYYY-MM-DD.md`）

```markdown
# 2026-02-01 (AgentName)

## Index (~70 tokens to scan)
| # | Type | Summary | ~Tok |
|---|------|---------|------|
| 1 | 🔴 | Auth bug - use browser not CLI | 80 |
| 2 | 🟢 | Deployed SEO fixes to 5 pages | 120 |
| 3 | 🟤 | Decided to split content by account | 60 |

---

### #1 | 🔴 Auth Bug | ~80 tokens
**Context:** Publishing via CLI
**Issue:** "Unauthorized" even with fresh tokens
**Workaround:** Use browser import instead
**Status:** Unresolved
```

### 长期存储文件（`MEMORY.md`）

```markdown
## 📋 Index (~100 tokens)
| ID | Type | Category | Summary | ~Tok |
|----|------|----------|---------|------|
| R1 | 🚨 | Rules | Twitter posting protocol | 150 |
| G1 | 🔴 | Gotcha | CLI auth broken | 60 |
| D1 | 🟤 | Decision | Content split by account | 60 |

---

### R1 | Twitter Posting Protocol | ~150 tokens
- POST ALL tweets in ONE session
- NEVER post hook without full thread
- VERIFY everything before reporting done
```

## 数据类型及其使用场景

| 图标 | 类型 | 使用场景 |
|------|------|-------------|
| 🚨 | 规则 | 必须严格遵守的规则 |
| 🔴 | 陷阱/误区 | 避免重复犯同样的错误 |
| 🟡 | 修复方案 | 缺陷修复方法 |
| 🔵 | 技术说明 | 相关的技术细节 |
| 🟢 | 变更内容 | 已更新或部署的内容 |
| 🟣 | 新发现 | 学习成果或新见解 |
| 🟠 | 设计理由 | 功能设计的依据 |
| 🟤 | 决策依据 | 技术架构的决策 |
| ⚖️ | 权衡方案 | 经过权衡后的折中方案 |

## 数据量估算

| 数据类型 | 所需令牌数 |
|--------------|--------|
| 简单事实 | 约30-50个令牌 |
| 简短说明 | 约80-150个令牌 |
| 详细内容 | 约200-400个令牌 |
| 完整总结 | 约500-1000个令牌 |

## 工作原理

1. **会话开始** → 智能体扫描索引表（约100-200个令牌）；
2. **智能体识别数据类型** → 优先显示需要避免的陷阱（🔴），而非已更新的内容（🟢）；
3. **智能体评估数据价值** → 判断是否值得加载400个令牌量的数据；
4. **按需获取** → 仅加载与当前任务相关的数据。

## 相关优势

- **节省令牌**：每天最多可节省约65,000个令牌（假设进行20次内存查询）；
- **更快的扫描速度**：图标帮助用户快速识别数据类型；
- **精确的引用方式**：使用编号（如#1、G3、D5）进行快速查找；
- **成本意识**：通过令牌数量来评估数据使用的成本效益。

## 集成方式

该系统可与任何基于Markdown的存储系统配合使用，无需额外的数据库支持。

**针对Clawdbot用户的操作步骤：**
1. 更新`AGENTS.md`文件，添加相关的格式说明；
2. 重新组织`MEMORY.md`文件的结构，使其包含索引信息；
3. 在每日生成的`memory/YYYY-MM-DD.md`文件中遵循新的格式规范。

---

**开发团队：[LXGIC Studios](https://lxgicstudios.com)**

🔗 [GitHub仓库](https://github.com/lxgicstudios/progressive-memory) · [Twitter账号](https://x.com/lxgicstudios)
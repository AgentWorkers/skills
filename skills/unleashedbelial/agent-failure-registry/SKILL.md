---
name: failure-registry
description: 在代理故障注册表中搜索已知的代理故障、解决方案以及从中获得的经验教训。当遇到错误、进行问题调试，或希望从其他代理的文档化故障分析中学习时，可以使用该功能。同时，也支持通过 GitHub 的 Pull Request（PR）提交新的故障分析报告。
---

# 失败日志技能

您可以搜索并学习来自“代理失败日志”（Agent Failure Registry）的资料——这是一个由社区共同维护的数据库，其中记录了代理程序的故障情况、解决方案以及从中获得的经验教训。当遇到问题时，可以先查看是否已经有其他人遇到过类似的问题并找到了解决方法。

## 快速入门

**搜索类似的故障：**
```bash
./scripts/search-registry.sh --category api_failure
./scripts/search-registry.sh --keyword "puppeteer"
./scripts/search-registry.sh --tag twitter --tag auth
```

**搜索所有内容：**
```bash
./scripts/search-registry.sh --all
```

## 使用场景

### 1. 搜索——当出现问题时

在重新解决问题之前，先在日志中查找相关信息：

- **按类别搜索：** `api_failure`、`auth_expiry`、`rate_limit`、`silent_failure`、`data_corruption`、`timeout`、`logic_error`、`dependency_break`、`permission_denied`、`other`
- **按关键词搜索：** 工具名称、错误信息、症状描述
- **按标签搜索：** 平台、服务、技术类型

该日志包含了来自 `examples/`（精选的案例）和 `submissions/`（社区提交的报告）的故障分析内容。

**搜索结果包括：**
- 故障的简要描述
- 根本原因分析
- 有效的解决方法
- 预防措施
- 经验教训

### 2. 提交——分享您的解决方案

当您解决了某个故障时，可以帮助社区其他成员：

1. 按照规定的格式记录故障详情。
2. 通过 GitHub 的 Pull Request （PR）提交解决方案（有脚本可以帮助生成提交模板）。
3. 提供详细背景信息——您尝试了哪些方法，哪些方法有效，哪些方法无效。

**必填字段：**
- 标题、类别、标签
- 故障摘要、根本原因、解决方法
- 预防措施、经验教训
- 解决方案的可靠性评分（1-5 分）

### 3. 学习——提前预防

定期浏览最新的提交记录，以便在遇到类似问题时能够借鉴他人的经验。

## 脚本使用

`search-registry.sh` 脚本负责处理所有的搜索和提交操作：

**参数：**
- `--category CATEGORY` — 按特定类别搜索
- `--tag TAG` — 按标签搜索
- `--keyword KEYWORD` — 在所有字段中搜索关键词
- `--all` — 显示所有记录（用于浏览）

**示例：**
```bash
# Find authentication issues
./scripts/search-registry.sh --category auth_expiry

# Find Twitter-related failures
./scripts/search-registry.sh --tag twitter

# Find Puppeteer issues
./scripts/search-registry.sh --keyword "puppeteer"

# Multiple criteria
./scripts/search-registry.sh --category api_failure --tag openai

# Browse everything
./scripts/search-registry.sh --all
```

## 仓库结构

“代理失败日志”仓库包含以下文件：
- `examples/` — 精选的故障分析报告
- `submissions/` — 社区提交的故障报告
- `template.yaml` — 新提交的报告模板
- `schema/postmortem.yaml` — 数据结构验证文件

## 类别参考

- **api_failure** — API 错误、超时、无效响应
- **authexpiry** — 认证/令牌过期问题
- **rate_limit** — 速率限制、超出配额
- **silent_failure** — 未抛出错误，但系统行为异常
- **data_corruption** — 数据完整性问题、解析错误
- **timeout** — 操作超时、进程挂起
- **logic_error** — 逻辑错误、错误假设
- **dependency_break** — 外部服务/库故障
- **permission_denied** — 访问控制、文件权限问题
- **other** — 其他各类故障

## 提示

**搜索前：**
- 提取关键的错误信息或症状描述
- 确定出现故障的组件（API、工具、进程）
- 记录操作背景（您当时正在尝试做什么？）

**提交时：**
- 明确说明有效的解决方法
- 提及您尝试过但无效的方法
- 对解决方案的可靠性进行评分（1-5 分）
- 使用相关标签标注技术/服务类型

**预防措施：**
- 定期回顾同类故障
- 根据经验教训更新错误处理机制
- 与社区分享特殊案例和需要注意的问题

## 实现细节

- 日志仓库克隆到 `/tmp/agent-failure-registry` 目录
- 使用 PyYAML 进行数据解析（必要时使用 grep 作为备用方式）
- 同时搜索 `examples/` 和 `submissions/` 文件夹
- 输出结果格式化以便阅读
- 支持多种搜索条件

记住：每一次故障都是一次学习的机会。请记录下来，分享给他人，并从中吸取经验。
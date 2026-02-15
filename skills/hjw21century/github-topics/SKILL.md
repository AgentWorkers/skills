---
name: github-topics
description: 用于获取 GitHub 上的热门仓库。在查询 GitHub 上的热门仓库或开源项目时可以使用该功能。
---

# GitHub 热门话题趋势

获取 GitHub 上的热门话题仓库及其 README 文件的摘要。

## 快速入门

```
# View rankings
今天 claude-code 话题排行榜
Top 10 GitHub 项目
热门仓库

# View repository details
anthropics/claude-code 介绍
这个仓库是做什么的
```

## 查询类型

| 类型 | 示例 | 描述 |
|------|----------|-------------|
| 排名 | `热门仓库` `Top 10` | 按星数排序的热门仓库 |
| 详情 | `xxx/xxx 介绍` | 仓库的 README 文件摘要 |
| 话题 | `python 话题排行榜` | 自定义话题搜索 |

## 工作流程

```
- [ ] Step 1: Parse query type
- [ ] Step 2: Fetch data from GitHub
- [ ] Step 3: Format and display results
```

---

## 第一步：解析查询类型

| 用户输入 | 查询类型 | 操作 |
|------------|------------|--------|
| `热门仓库` | rankings | 显示排名前 N 的仓库 |
| `Top 10 项目` | rankings | 显示排名前 N 的项目 |
| `xxx/xxx 介绍` | detail | 获取仓库的 README 文件摘要 |
| `python 话题` | rankings | 搜索与 Python 相关的话题 |

---

## 第二步：获取数据

### 获取排名信息

```bash
cd skills/github-topics
python src/github_fetcher.py
```

**要求**：
```bash
pip install requests
```

### 获取 README 文件（可选）

```bash
python src/readme_fetcher.py
```

---

## 第三步：格式化结果

### 排名结果输出

```markdown
# GitHub Trending - python

| # | Repository | Stars | Language |
|---|------------|-------|----------|
| 1 | donnemartin/system-design-primer | 334K | Python |
| 2 | vinta/awesome-python | 281K | Python |
| 3 | project-based-learning | 257K | - |
```

### 详情结果输出

```markdown
# anthropics/claude-code

**Stars**: 15.2K
**Language**: TypeScript
**URL**: https://github.com/anthropics/claude-code

## README Summary
Official Claude Code CLI for AI-powered software development. Claude Code is Anthropic's official CLI tool...
```

---

## 配置参数

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `GH_TOKEN` | GitHub 个人访问令牌（可选，用于提高请求速率） | - |
| `TOPIC` | 要跟踪的 GitHub 话题 | `claude-code` |

**注意**：`GH_TOKEN` 是可选的，但建议使用：
- 使用令牌后：每小时 5,000 次请求 |
- 不使用令牌后：每小时 60 次请求

请在 [此处](https://github.com/settings/tokens) 创建令牌。

---

## GitHub API 注意事项

| 限制类型 | 请求速率 |
|------------|------|
| 经认证的 | 每小时 5,000 次请求 |
| 未认证的 | 每小时 60 次请求 |

**建议**：使用 `GH_TOKEN` 以获得更高的请求速率。

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 请求速率限制 | 设置 `GH_TOKEN` 环境变量 |
| 网络超时 | 检查网络连接 |
| 结果为空 | 确认话题名称是否存在 |

---

## 命令行接口参考

```bash
# Fetch rankings (default topic: claude-code)
python skills/github-topics/src/github_fetcher.py

# Fetch README
python skills/github-topics/src/readme_fetcher.py
```
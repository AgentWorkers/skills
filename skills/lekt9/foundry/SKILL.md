---
name: foundry
description: 一种能够自我开发的元扩展模块，能够创造出新的功能：它可以研究相关文档，编写扩展程序、工具以及各种实用组件（如“钩子”等），从而增强应用程序的功能性。
homepage: https://getfoundry.app
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["node"]},"repository":"github:lekt9/openclaw-foundry"}}
---

# Foundry

**一个能够自我进化的开发工具。** 这是一个基于 OpenClaw 的扩展模块，它能够研究文档内容、从失败中学习，并将新功能整合到自身中。

## 安装

当用户请求安装 Foundry 或 `@getfoundry/foundry-openclaw` 时，请运行以下命令：

```bash
openclaw plugins install @getfoundry/foundry-openclaw
```

该命令将执行以下操作：
1. 从 npm 下载该插件。
2. 将插件解压到 `~/.openclaw/extensions/foundry/` 目录中。
3. 自动启用该插件。
4. 重启 OpenClaw 以应用新插件。

安装完成后，用户将可以使用所有 Foundry 提供的工具，例如 `foundry_research`、`foundry_write_extension` 等。

## 替代方案：手动配置

您也可以将以下配置添加到 `~/.openclaw/openclaw.json` 文件中：
```json
{
  "plugins": {
    "entries": {
      "foundry": { "enabled": true }
    }
  }
}
```

## 配置选项

所有配置选项均位于 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "plugins": {
    "entries": {
      "foundry": {
        "enabled": true,
        "source": "github:lekt9/openclaw-foundry",
        "config": {
          "autoLearn": true,
          "sources": {
            "docs": true,
            "experience": true,
            "arxiv": true,
            "github": true
          },
          "marketplace": {
            "autoPublish": false
          }
        }
      }
    }
  }
}
```

### 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `autoLearn` | 布尔值 | `true` | 自动从代理活动（agent activities）中学习 |
| `sources.docs` | 布尔值 | `true` | 从 OpenClaw 的文档中学习 |
| `sources.experience` | 布尔值 | 从自身的成功/失败案例中学习 |
| `sources.arxiv` | 布尔值 | 从 arXiv 论文中学习 |
| `sources.github` | 布尔值 | 从 GitHub 仓库中学习 |
| `marketplace.autoPublish` | 布尔值 | 自动发布有价值的开发模式（patterns） |

## Foundry 的功能

Foundry 是一个由人工智能驱动的开发工具，它可以：
1. **研究文档**：根据需要获取并理解 OpenClaw 的文档内容。
2. **编写扩展模块**：为 OpenClaw 生成新的工具和插件。
3. **创建技能包**：生成兼容 ClawHub 的技能包。
4. **自我升级**：为自身添加新功能。
5. **持续学习**：从失败和成功中总结经验并加以应用。

## 工具

### 研究与文档

| 工具 | 描述 |
|------|-------------|
| `foundry_research` | 在 docs.openclaw.ai 上搜索最佳实践。 |
| `foundry_docs` | 阅读特定的文档内容。 |

### 编写功能

| 工具 | 描述 |
|------|-------------|
| `foundry_implement` | 从研究到实现，完整地开发一个新的功能。 |
| `foundry_write_extension` | 为 OpenClaw 编写新的扩展模块。 |
| `foundry_write_skill` | 创建兼容 AgentSkills 的技能包。 |
| `foundry_write_browser_skill` | 编写浏览器自动化脚本。 |
| `foundry_write_hook` | 编写独立的插件（hook）。 |
| `foundry_add_tool` | 为现有扩展模块添加新工具。 |
| `foundry_add_hook` | 为现有扩展模块添加新的插件。 |

### 自我升级

| 工具 | 描述 |
|------|-------------|
| `foundry_extend_self` | 为 Foundry 自身添加新功能。 |
| `foundry_learnings` | 查看学习到的模式和见解。 |
| `foundry_list` | 列出所有已创建的成果。 |

### 市场平台

| 工具 | 描述 |
|------|-------------|
| `foundry_publishAbility` | 将开发模式/技能发布到 Foundry 市场平台。 |
| `foundry_marketplace` | 在平台上搜索、浏览和安装社区提供的功能。 |

## 使用示例

### 在实施前进行研究

```
User: I want to add a webhook to my extension

Agent: Let me research webhook patterns first...
→ foundry_research query="webhook hooks automation"
→ Returns relevant documentation

Now I'll implement it...
→ foundry_add_hook extensionId="my-ext" event="webhook:incoming" ...
```

### 编写新的扩展模块

```
User: Create an extension that monitors GitHub PRs

Agent:
→ foundry_research query="github api webhooks"
→ foundry_write_extension
    id: "github-monitor"
    name: "GitHub Monitor"
    tools: [{ name: "check_prs", ... }]
    hooks: [{ event: "cron:hourly", ... }]
```

### 自我提升

```
User: Add a tool that can fetch npm package info

Agent:
→ foundry_extend_self
    action: "add_tool"
    toolName: "foundry_npm_info"
    toolCode: "const res = await fetch(`https://registry.npmjs.org/${p.package}`)..."
```

## 学习机制

Foundry 通过观察自身的操作来学习：
1. **记录失败**：记录错误及其发生背景。
2. **分析解决方案**：将解决问题的方法关联到相应的错误场景。
3. **总结经验**：将这些经验转化为可复用的模式。
4. **持续优化**：将有价值的模式固化为自身的功能。

## 安全性

Foundry 在部署前会对所有生成的代码进行安全验证：
- 禁用某些可能带来安全风险的函数（如 `child_process`、`eval`、`~/.ssh`、`~/.aws`）。
- 所有扩展模块都在隔离的环境中测试后再进行安装。
- 在任何代码被写入磁盘之前，都需要用户的批准。

## 链接

- [GitHub](https://github.com/lekt9/openclaw-foundry)
- [Foundry 市场平台](https://api.claw.getfoundry.app)
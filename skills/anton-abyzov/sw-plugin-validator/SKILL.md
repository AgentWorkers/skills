---
name: plugin-validator
description: 在用户明确请求的情况下，该功能用于验证 SpecWeave 插件的安装情况。它可以用来检查插件是否正确安装、验证插件在 marketplace 上的注册状态，或解决插件缺失的问题。该功能仅在用户明确请求时触发，以避免在正常工作流程中出现误报（即错误地提示插件问题）。
allowed-tools: Read, Bash, Grep
---

# 插件验证器技能（Plugin Validator Skill）

**功能**：在用户明确请求时，验证并安装 SpecWeave 插件。

**激活条件**：仅当用户明确请求插件验证时才会触发（例如：输入“validate plugins”或运行 `specweave validate-plugins` 命令）。不会因工作流命令而自动激活，以避免误报。

## 该技能的作用

该技能确保在您开始工作之前，您的 SpecWeave 环境已正确配置所有必需的插件。这可以避免因缺少组件而导致的错误和浪费时间。

### 主要特性

1. **市场places 验证**：确保 `~/.claude/settings.json` 中注册了 SpecWeave 市场places。
2. **核心插件检查**：验证是否已安装了 `specweave` 插件。
3. **上下文感知**：分析您的增量描述并推荐相关插件。
4. **自动安装**：在获得您的许可后，可以自动安装缺失的组件。
5. **清晰指导**：明确显示缺少什么以及如何解决。

## 该技能何时激活

✅ **仅在以下情况下激活**：
- 您输入了“plugin validation”或“validate plugins”。
- 您输入了“environment setup”或“check plugins”。
- 您运行了 `specweave validate-plugins` 命令。
- 您询问：“可以验证我的插件吗？”
- 您报告：“我遇到了插件错误”。
- 在执行 `specweave init`（初始设置）时。

❌ **不会因以下命令自动激活**：
- `/sw:increment` 命令
- `/sw:do` 命令
- 任何其他工作流命令
- **原因**：防止在插件已安装但检测失败时产生误报。

## 验证流程

### 第一阶段：市场places 检查

**检查内容**：验证 SpecWeave 市场places 是否已注册在 Claude 代码中。
**位置**：`~/.claude/settings.json`
**预期结果**：
```json
{
  "extraKnownMarketplaces": {
    "specweave": {
      "source": {
        "source": "github",
        "repo": "anton-abyzov/specweave",
        "path": ".claude-plugin"
      }
    }
  }
}
```

**如果缺失**：会自动创建相应的配置。

### 第二阶段：核心插件检查

**检查内容**：验证是否已安装 `specweave` 插件。
**命令**：`/plugin list --installed | grep "specweave"`
**预期结果**：插件应出现在列表中。
**如果缺失**：会建议安装 `/plugin install specweave`。

### 第三阶段：上下文感知的插件检测

**检查内容**：扫描您的增量描述中的关键词。
**示例**：

| 描述 | 检测到的关键词 | 建议的插件 |
|-----------------|-------------------|------------------|
| “添加 GitHub 同步” | github, sync | specweave-github |
| “使用 React UI 进行 Stripe 支付” | stripe, billing, react, ui | specweave-payments, specweave-frontend |
| “部署到 Kubernetes” | kubernetes, deploy | specweave-kubernetes |
| “添加 Jira 集成” | jira, integration | specweave-jira |

**完整关键词映射**（15 个以上插件）：
- **specweave-github**：github, git, issues, pull request, pr, repository
- **specweave-jira**：jira, epic, story, sprint, backlog
- **specweave-ado**：azure devops, ado, work item, boards
- **specweave-payments**：stripe, billing, payment, subscription, invoice
- **specweave-frontend**：react, nextjs, vue, angular, frontend, ui
- **specweave-kubernetes**：kubernetes, k8s, helm, pod, deployment
- **specweave-ml**：machine learning, ml, tensorflow, pytorch, model
- **specweave-observability**：prometheus, grafana, monitoring, metrics
- **specweave-security**：security, owasp, vulnerability, audit
- **specweave-diagrams**：diagram, c4, mermaid, architecture
- **specweave-backend-nodejs**：nodejs, express, fastify, nestjs, backend
- **specweave-backend-python**：python, fastapi, django, flask
- **specweave-backend-dotnet**：dotnet, .net, aspnet, c#
- **specweave-e2e-testing**：playwright, e2e, end-to-end, browser

## 使用示例

### 示例 1：新环境

**场景**：您将项目克隆到新的虚拟机上并准备开始工作。

**操作**：运行 `/sw:increment "Add authentication"`。

**结果**：
```
🔍 Validating SpecWeave environment...

❌ Missing components detected:
   • SpecWeave marketplace not registered
   • Core plugin (specweave) not installed

📦 Installing missing components...
   ✅ Marketplace registered (.claude/settings.json)
   ✅ Core plugin installed (specweave v0.9.4)

🎉 Environment ready! Proceeding with increment planning...
```

### 示例 2：上下文检测

**场景**：您正在添加一个使用 GitHub 和 React 的新功能。

**操作**：运行 `/sw:increment "Add GitHub sync with React UI"`。

**结果**：
```
🔍 Validating SpecWeave environment...

✅ Marketplace registered
✅ Core plugin installed (specweave v0.9.4)

🔎 Detected context plugins from your description:
   • specweave-github (keywords: github, sync)
   • specweave-frontend (keywords: react, ui)

❌ Missing context plugins:
   • specweave-github
   • specweave-frontend

📦 Would you like to install these plugins?
   They provide specialized expertise for your use case.

   1. Yes, install now (recommended)
   2. No, skip for now (limited capabilities)

Your choice [1]:
```

### 示例 3：手动验证

**场景**：您想在不运行命令的情况下检查环境。

**操作**：运行 `specweave validate-plugins --verbose`。

**结果**：
```
[PluginValidator] Checking marketplace registration...
[PluginValidator] Marketplace registered ✓
[PluginValidator] Checking core plugin (specweave)...
[PluginValidator] Core plugin installed ✓ (0.9.4)

✅ All plugins validated!
   • Core plugin: installed (v0.9.4)
   • Cache: miss
```

### 示例 4： dry-run 模式

**场景**：您想查看在不实际安装的情况下会安装哪些插件。

**操作**：运行 `specweave validate-plugins --context="Add Stripe billing" --dry-run`。

**结果**：
```
🔍 Validating SpecWeave environment...

✅ Marketplace registered
✅ Core plugin installed

🔎 Detected context plugins:
   • specweave-payments (keywords: stripe, billing)

❌ Missing: specweave-payments

💡 Dry-run mode: No changes made.
   To install, remove --dry-run flag.
```

## CLI 命令参考

**基本验证**：
```bash
specweave validate-plugins
```

**自动安装缺失组件**：
```bash
specweave validate-plugins --auto-install
```

**结合上下文检测**：
```bash
specweave validate-plugins --context="Add GitHub sync for mobile app"
```

** dry-run（仅预览）**：
```bash
specweave validate-plugins --dry-run --context="Add Stripe billing"
```

**详细模式**：
```bash
specweave validate-plugins --verbose
```

**组合标志**：
```bash
specweave validate-plugins --auto-install --context="Deploy to Kubernetes" --verbose
```

## 故障排除

### 错误：“Claude CLI 未找到”

**症状**：验证失败，显示“命令未找到”。

**解决方案**：
1. 确保已安装 Claude 代码。
2. 重启终端。
3. 验证：`claude --version`。
4. 如果仍然失败，请使用 `/plugin install` 命令手动安装插件。

### 错误：“市场places 配置无效”

**症状**：市场places 已注册，但验证失败。

**解决方案**：
1. 检查 `~/.claude/settings.json` 的结构。
2. 确保市场places 指向正确的 GitHub 源。
3. 如果使用本地市场places（开发模式），这是正常的。
4. 重新运行验证以自动修复配置。

### 错误：“插件安装失败”

**症状**：自动安装尝试失败。

**解决方案**：
1. 检查网络连接（需要访问 GitHub）。
2. 确保 Claude 代码正在运行。
3. 尝试手动安装：`/plugin install specweave`。
4. 查看 Claude 代码的日志以获取详细错误信息。

### 误报：推荐的插件不相关

**症状**：上下文检测推荐了不相关的插件。

**示例**：描述为“Add GitHub Actions”，但实际需要的是 CI/CD 功能，而不是问题跟踪功能，因此推荐了 specweave-github。

**解决方案**：
1. 跳过该建议（选择其他选项）。
2. 稍后手动安装正确的插件。
3. 这种情况很少见（需要匹配多个关键词才会推荐相关插件）。

## 性能

**验证速度**：
- ✅ 使用缓存：<2 秒
- ✅ 不使用缓存：<5 秒
- ✅ 使用自动安装：<30 秒（1-2 个插件）

**缓存**：
- 结果缓存 5 分钟。
- 加速重复命令的执行。
- 插件更改后缓存失效。
- 缓存位置：`~/.specweave/validation-cache.json`。

## 配置

**验证配置**可以在 `.specweave/config.json` 中进行设置：

```json
{
  "pluginValidation": {
    "enabled": true,           // Enable/disable validation (default: true)
    "autoInstall": true,       // Auto-install missing components (default: true)
    "verbose": false,          // Show detailed logs (default: false)
    "cacheValidation": true,   // Cache results (default: true)
    "cacheTTL": 300            // Cache TTL in seconds (default: 300 = 5 min)
  }
}
```

**禁用验证**（不推荐）：
```json
{
  "pluginValidation": {
    "enabled": false
  }
}
```

## 与命令的集成

**所有 SpecWeave 命令在执行前都会验证插件（步骤 0）**：
- `/sw:increment` - 在 PM 代理运行前验证
- `/sw:do` - 在任务执行前验证
- `/sw:next` - 在下一个增量之前验证
- `/sw:done` - 在完成之前验证
- ...（所有 22 个命令）

**工作流**：
```
User: /sw:increment "Add feature"
        ↓
   [STEP 0: Plugin Validation]
        ↓ (only proceeds if valid)
   [STEP 1: PM Agent Planning]
        ↓
   [STEP 2: Architect Design]
        ↓
   [STEP 3: Implementation]
```

## 好处

✅ **零手动设置** - 插件自动安装。
✅ **无缝迁移** - 支持本地/虚拟机/云 IDE。
✅ **上下文感知** - 根据您的工作推荐相关插件。
✅ **清晰的错误信息** - 不再出现难以理解的“命令未找到”错误。
✅ **快速**：缓存确保最低开销（缓存 <2 秒，未缓存 <5 秒）。
✅ **非阻塞** - 如有需要可以跳过验证（不推荐）。

## 特殊情况

**1. 离线模式**
- 验证会检测到缺失的插件，但无法安装。
- 会显示手动安装说明。
- 验证仍然有用（可以识别缺失的插件）。

**2. 开发模式**
- 检测到本地市场places（非 GitHub）。
- 显示警告：“检测到开发模式”。
- 验证通过（假设开发者知道自己在做什么）。

**3. 同时验证**
- 多个命令同时运行时，使用缓存避免重复验证。
- 得到优雅的处理。

**4. 部分安装**
- 市场places 存在，但某些插件缺失（或相反情况）。
- 仅安装缺失的组件。
- 不会重新安装已存在的组件。

## 手动安装（备用方案）

**如果自动安装失败**，请按照以下步骤操作：

### 第一步：注册市场places

编辑 `~/.claude/settings.json`：
```json
{
  "extraKnownMarketplaces": {
    "specweave": {
      "source": {
        "source": "github",
        "repo": "anton-abyzov/specweave",
        "path": ".claude-plugin"
      }
    }
  }
}
```

### 第二步：安装核心插件

在 Claude 代码中运行：
```
/plugin install specweave
```

### 第三步：重启 Claude 代码

关闭并重新打开 Claude 代码以使更改生效。

### 第四步：验证安装

运行：
```bash
specweave validate-plugins
```

应显示：
```
✅ All plugins validated!
   • Core plugin: installed (v0.9.4)
```

### 第五步：安装相关插件（可选）

如果您需要特定插件：
```
/plugin install sw-github@specweave
/plugin install sw-payments@specweave
/plugin install sw-frontend@specweave
```

## 总结

**该技能确保您永远不会浪费时间调试插件问题。**

它主动验证您的环境，自动安装缺失的组件，并根据您的工作推荐相关插件。这样，您可以专注于构建功能，而不是处理设置问题。

**有问题吗？**
- 查看上面的故障排除部分。
- 运行 `specweave validate-plugins --help`。
- 访问：https://spec-weave.com/docs/plugin-validation

---

**技能版本**：1.0.0
**引入版本**：SpecWeave v0.9.4
**最后更新时间**：2025-11-09
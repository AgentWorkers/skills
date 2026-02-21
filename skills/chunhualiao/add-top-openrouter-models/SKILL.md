---
name: add-top-openrouter-models
description: 将 OpenClaw 使用的 OpenRouter 模型同步到当前安装的配置中。从 OpenRouter 获取 OpenClaw 应用的排行榜数据，验证模型 ID 是否与 API 目录中的信息一致；如果发现缺失的模型，则添加这些模型，并为其指定正确的规格和别名。适用于需要执行“同步 OpenRouter 模型”、“添加缺失的模型”、“更新 OpenRouter 配置”或“检查 OpenRouter 模型”等操作的场景。
---
# OpenRouter模型同步

将OpenClaw应用程序排行榜上的模型同步到本OpenClaw安装环境中。

## 工作流程

### 第一步：通过浏览器提取模型ID

该应用程序页面是一个React单页应用程序（SPA），因此必须使用浏览器工具进行数据提取，而不能使用`web_fetch`。

1. 在浏览器中打开`https://openrouter.ai/apps?url=https%3A%2F%2Fopenclaw.ai%2F`（使用`openclaw`配置文件）。
2. 拍摄当前页面的快照，找到“Show more”链接并点击以展开完整的排行榜。
3. 在排行榜展开后再次拍摄快照。
4. 从链接的`href`中提取模型ID（格式为`/<provider>/<model-name>`，例如`/moonshotai/kimi-k2.5`）。
5. 过滤掉非模型链接（如导航链接 `/docs`、`/chat`、`/rankings`、`/pricing`、`/enterprise`、`/about` 等）。
6. 收集模型ID（去掉前导斜杠）。

### 第二步：运行同步脚本

```bash
python3 scripts/sync-openrouter-models.py --models "model/id1,model/id2,..."
```

**可选参数：**
- `--dry-run`：预览更改结果，不写入文件。
- `--json`：将结果输出为机器可读的JSON格式（显示在标准输出中）。
- 也可以通过标准输入（stdin）提供模型ID（每行一个模型ID）。

脚本执行步骤如下：
1. 验证每个模型ID是否存在于OpenRouter的`/api/v1/models`目录中（不匹配的ID将被拒绝）。
2. 将验证通过的模型转换为OpenClaw所需的格式（包括上下文信息、价格信息、推理方式等）。
3. 在写入任何配置文件之前，先创建带有时间戳的备份文件。
4. 将缺失的模型添加到`~/.openclaw/agents/<agent>/agent/models.json`和`~/.openclaw/openclaw.json`文件中。
5. 生成模型别名（来自`references/aliases.json`文件或自动生成的别名）。

### 第三步：重启网关

```bash
openclaw gateway restart
```

## 环境变量

| 变量          | 用途                | 默认值            |
|---------------|------------------|-------------------|
| `OPENCLAW_DIR`     | 替换OpenClaw的安装目录        | `~/.openclaw`         |
| `OPENCLAW_AGENT_DIR` | 替换代理程序的安装目录        | 自动检测           |
| `OPENROUTER_API_KEY`   | API密钥              | 从配置文件中获取         |

## 维护模型别名

编辑`references/aliases.json`文件以添加或更新模型ID的别名。脚本在运行时会加载该文件；如果文件不存在，则使用内置的默认别名。

## 更新内容

- `~/.openclaw/agents/main/agent/models.json`：OpenRouter提供的模型信息。
- `~/.openclaw/openclaw.json`：OpenRouter提供的模型信息及对应的别名。
- 每次写入配置文件之前，会生成带有时间戳的备份文件（格式为`<file>.bak.<timestamp>`）。

## 限制事项

- 该脚本仅用于添加新模型，不会删除已从排行榜中移除的模型。
- 模型推理的判断基于启发式规则（结合架构信息和已知模型类型）。
- 第一步需要使用浏览器工具来完成数据提取（因为应用程序页面是通过JavaScript渲染的）。
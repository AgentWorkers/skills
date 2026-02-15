---
name: alibaba-cloud-model-setup
description: 配置 OpenClaw（包括旧的 Moltbot/Clawdbot 路径），使其能够通过严格的交互流程使用 Alibaba Cloud Model Studio。第一步需要询问用户是否能够运行终端命令；根据用户的回答，选择环境变量模式（推荐）或内联模式，然后再收集站点/密钥详细信息。当用户请求在 OpenClaw 中添加、切换或修复 Alibaba Cloud/Qwen 提供商的配置时，可以使用此技能。
---

# 阿里云模型设置

## 概述

使用此功能可以以最少的手动编辑量将阿里云配置为OpenClaw的模型提供者。建议使用捆绑的脚本进行确定性更新和安全的备份。

## 工作流程

1. 确认OpenClaw配置文件的位置。
2. 运行交互式脚本以收集以下信息：
   - 首先也是必须的：用户当前是否可以运行终端命令（这将决定使用环境变量模式还是内联模式）。
   - 在环境变量模式下，显示两个供用户运行的命令（`export`命令以及将其添加到`~/.bashrc`文件中），然后等待用户确认并验证。
   - 重试环境变量检测最多2次；如果仍未检测到环境变量，则询问用户是否切换到内联模式。
   - 选择站点（`Beijing/中国站/CN`、`Singapore/国际站/INTL`或`Virginia/美国站/US`）。
   - 访问密钥（仅在启用内联模式或用户选择内联模式时需要）。
   - 在写入任何配置之前，验证API密钥是否与所选站点匹配。
   - 在systemd部署中，确保服务环境已准备好再进行配置写入。
   - 默认预设模型（`qwen-max`、`qwen-flash`、`qwen3-coder-plus`）。
   - 是否要从实时API列表中添加额外的模型。
   - 是否要更改默认模型。
   - 是否将此模型设置为默认模型。
3. 验证生成的JSON文件，并报告最终的提供者/模型路径。
4. 如果用户不确定有哪些模型可用，可以先通过API获取实时模型列表。

## 安全规则（必填）

1. 进行配置更改时，始终运行`python3 scripts/alibaba_cloud_model_setup.py`脚本。
2. 使用此功能时，切勿手动编辑`~/.openclaw/openclaw.json`文件。
3. 在使用环境变量模式时，除非脚本中的环境变量检测成功，否则不要进行配置写入；如果检测失败且用户拒绝使用内联模式，则停止操作，并显示“配置未更改”。
4. 在systemd部署中，除非`systemctl --user show-environment`命令显示了已配置的环境变量，否则不要进行配置写入。

## 运行脚本

执行：

```bash
python3 scripts/alibaba_cloud_model_setup.py
```

**非交互式使用的可选参数：**

```bash
python3 scripts/alibaba_cloud_model_setup.py \
  --site intl \
  --api-key-source env \
  --env-var DASHSCOPE_API_KEY \
  --api-key "$DASHSCOPE_API_KEY" \
  --models qwen-max,qwen-flash,qwen3-coder-plus \
  --model qwen3-coder-plus \
  --set-default
```

**通过API列出实时模型ID（不进行配置写入）：**

```bash
python3 scripts/alibaba_cloud_model_setup.py \
  --site intl \
  --api-key "$DASHSCOPE_API_KEY" \
  --list-models \
  --non-interactive
```

## 默认行为

- 按以下顺序检测配置文件的位置：
- `~/.openclaw/openclaw.json`
- `~/.moltbot/moltbot.json`
- `~/.clawdbot/clawdbot.json`
- 如果这些文件都不存在，则创建`~/.openclaw/openclaw.json`。
- 使用与OpenAI兼容的API模式设置提供者“balian”。
- 在覆盖现有文件之前创建带有时间戳的备份。
- 保留与模型配置无关的部分。

## 验证检查清单

配置完成后：

1. 通过运行`python3 -m json.tool <config-path>`来确认JSON文件的有效性。
2. 确保`modelsproviders.balian.baseUrl`与所选站点匹配。
3. 确保`modelsproviders.balian.models`包含预期的模型ID。
4. 当启用默认模型时，确保`agents.defaults.model.primary`的值为`balian/<model-id>`。
5. 启动仪表板（`openclaw dashboard`）或TUI（`openclaw tui`），并验证模型调用是否成功。

## 参考资料

- 端点和字段约定：`references/openclaw_alibaba_cloud.md`
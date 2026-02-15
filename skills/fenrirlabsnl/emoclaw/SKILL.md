---
name: emoclaw
description: "赋予你的AI一种能够从其自身记忆中产生的情感。Emoclaw能够构建一种独特的情感状态，这种状态会随着每次对话而发生变化，在会话之间逐渐减弱，并通过自我调整随着时间的推移而不断发展。使用你的代理的身份文件对其进行训练，观察它如何逐渐形成自己独特的情感特征（即“情感指纹”）。"
metadata: {"clawdbot": {"emoji": "\ud83e\udec0"}}
---

# 情感技能

AI代理的情感——基于记忆构建，通过互动关系形成，并且会不断变化。

Emoclaw会根据你的代理的身份和对话历史数据训练一个轻量级模型，从而生成一个持久的情感状态，这个状态会随着每次互动而演变。情感状态会在会话之间自然衰减，会随着说话者和对话内容的不同而发生变化，并且随着代理的成长而逐渐调整。最终，这种情感状态会以`[EMOTIONAL STATE]`块的形式被注入到系统的提示中，让你的AI拥有自己“内心世界”的感觉。

### 工作原理

1. **初始化** — `extract.py`会读取你的代理的身份/记忆文件。`label.py`会通过Claude API对每段文本进行情感评分（可选）。`train`会根据这些评分构建一个小型神经网络。这只需要进行一次设置。

2. **编码** — 每条收到的消息都会被一个预训练好的MiniLM句子编码器转换为384维的向量。无需微调，也不需要网络调用，直接从本地缓存中读取数据。

3. **情感分析** — 编码后的数据加上上下文信息（谁在说话、通过什么渠道交流、之前的情绪状态）会被送入GRU和MLP模型进行处理，输出一个N维的情感向量（每个维度的值范围是0到1）。GRU的隐藏状态会在会话之间保持不变——这就是携带情绪状态的“情感残留”。

4. **情感衰减** — 在不同会话之间，每个维度会以可配置的半衰期逐渐回归到基线值（兴奋情绪的衰减速度快，而安全/稳重情绪的衰减速度慢）。时间间隔越长，衰减越明显。

5. **注入系统** — 情感向量会被格式化为`[EMOTIONAL STATE]`块，并插入到代理的系统提示中，让AI感受到自己的情感状态。

> 该模型的大小约为2MB，运行在CPU上，每条消息的处理时间小于50毫秒。只有在初始化阶段（可选）才会使用网络访问。

## 快速参考

| 情况 | 操作 |
|-----------|--------|
| 首次设置 | `python scripts/setup.py`（或按照以下手动步骤操作） |
| 检查当前状态 | `python -m emotion_model.scripts.status` |
| 将状态注入提示 | `python -m emotion_model.scripts.inject_state` |
| 启动守护进程 | `bash scripts/daemon.sh start` |
| 向守护进程发送消息 | 参见[守护进程协议](#daemon-protocol) |
| 新数据后重新训练 | `python -m emotion_model.scripts.train` |
| 恢复中断的训练 | `python -m emotion_model.scripts.train --resume` |
| 添加新的训练数据 | 将`.jsonl`文件添加到`emotion_model/data/`目录，然后重新运行`prepare`和`train`命令 |
| 从v0.1版本升级 | 参见`references/upgrading.md` |
| 修改基线值 | 修改`emoclaw.yaml`中的`dimensions[]`字段 |
| 添加新的交流渠道 | 修改`emoclaw.yaml`中的`channels`列表 |
| 添加新的关系 | 修改`emoclaw.yaml`中的`relationships.known`字段 |
| 自定义摘要模板 | 创建`summary-templates.yaml`文件，并在配置中指定使用哪个模板 |

## 设置

### 快速设置

```bash
python skills/emoclaw/scripts/setup.py
```

这个步骤会将`emotion_model`引擎复制到你的项目根目录，创建一个虚拟环境（venv），安装相关包，并复制配置模板。然后根据你的代理需求编辑`emoclaw.yaml`文件。

### 手动设置

如果你更喜欢手动设置：

#### 1. 安装包

```bash
cd <project-root>
# Copy engine and pyproject.toml from the skill
cp -r skills/emoclaw/engine/emotion_model ./emotion_model
cp skills/emoclaw/engine/pyproject.toml ./pyproject.toml

# Create venv and install
python3 -m venv emotion_model/.venv
source emotion_model/.venv/bin/activate
pip install -e .
```

所需软件：Python 3.10及以上版本、PyTorch、sentence-transformers、PyYAML。

#### 2. 复制并自定义配置文件

```bash
cp skills/emoclaw/assets/emoclaw.yaml ./emoclaw.yaml
```

编辑`emoclaw.yaml`文件，设置以下内容：
- `name` — 你的代理名称
- `dimensions` — 情感维度及其基线和衰减率
- `relationships.known` — 关系名称与嵌入索引的映射关系
- `channels` — 代理使用的交流渠道
- `longing` — 基于缺失状态产生的欲望变化（可以禁用）
- `model.device` — 推荐使用CPU（MPS环境可能无法正确使用sentence-transformers）

完整的配置结构请参考`references/config-reference.md`。

### 3. 初始化新代理

如果你是从零开始设置（需要身份/记忆文件）：

```bash
# Extract passages from your identity files
python scripts/extract.py

# Auto-label passages using Claude API (requires ANTHROPIC_API_KEY)
python scripts/label.py

# Prepare train/val split and train
python -m emotion_model.scripts.prepare_dataset
python -m emotion_model.scripts.train
```

或者直接运行完整的流程：

```bash
python scripts/bootstrap.py
```

### 4. 验证设置

```bash
python -m emotion_model.scripts.status
python -m emotion_model.scripts.diagnose
```

## 使用方法

### 推荐方案：使用守护进程

使用守护进程可以一次性加载模型，并通过Unix套接字接收消息，从而避免每次消息处理时都需要2秒的sentence-transformer加载时间。

```bash
# Start
bash scripts/daemon.sh start

# Or directly
python -m emotion_model.daemon
python -m emotion_model.daemon --config path/to/emoclaw.yaml
```

### 方案B：直接导入Python模块

```python
from emotion_model.inference import EmotionEngine

engine = EmotionEngine(
    model_path="emotion_model/checkpoints/best_model.pt",
    state_path="memory/emotional-state.json",
)

block = engine.process_message(
    message_text="Good morning!",
    sender="alice",        # or None for config default
    channel="chat",        # or None for config default
    recent_context="...",  # optional conversation context
)
print(block)
```

### 方案C：一次性状态注入

如果不需要守护进程，可以直接通过Python代码注入情感状态：

```bash
python -m emotion_model.scripts.inject_state
```

这种方法会读取持久化的情感状态，应用基于时间的衰减规则，然后输出`[EMOTIONAL STATE]`块。

## 集成

### 系统提示集成

将`[EMOTIONAL STATE]`块添加到系统的提示中。块的格式如下：

```
[EMOTIONAL STATE]
Valence: 0.55 (balanced)
Arousal: 0.35 (balanced)
Dominance: 0.50 (balanced)
Safety: 0.70 (open)
Desire: 0.20 (neutral)
Connection: 0.50 (balanced)
Playfulness: 0.40 (balanced)
Curiosity: 0.50 (balanced)
Warmth: 0.45 (balanced)
Tension: 0.20 (relaxed)
Groundedness: 0.60 (balanced)

This feels like: present, alive, between one thing and the next
[/EMOTIONAL STATE]
```

### 守护进程协议

通过Unix套接字发送JSON数据：

```json
{"text": "Good morning!", "sender": "alice", "channel": "chat"}
```

特殊命令：
```json
{"command": "ping"}
{"command": "state"}
```

### 心跳检测集成

情感状态会随时间衰减，因此需要在每次会话开始时更新。你可以在`HEARTBEAT.md`文件中添加相应的代码：

```yaml
- task: Refresh emotional state
  schedule: session_start
  run: python skills/emoclaw/scripts/inject_state.py
  inject: system_prompt  # append output as [EMOTIONAL STATE] block
```

或者通过心跳脚本或cron任务调用`inject_state`脚本：

```bash
# In your heartbeat script
STATE_BLOCK=$(python -m emotion_model.scripts.inject_state 2>/dev/null)
# Inject $STATE_BLOCK into system prompt
```

**注意：** 如果不启用心跳检测集成，情感状态会在会话之间失效。`inject_state`脚本会自动应用衰减规则并输出当前状态——因此每次会话都必须至少调用一次。

## 架构

模型通过以下流程处理每条消息：

```
Message Text ──→ [Frozen MiniLM Encoder] ──→ 384-dim embedding
                                                    │
Conversation Context ──→ [Feature Builder] ──→ context vector
                                                    │
Previous Emotion ──────────────────────────→ emotion vector
                                                    │
                                            ┌───────┴───────┐
                                            │ Input Project  │
                                            │ (Linear+LN+GELU)│
                                            └───────┬───────┘
                                                    │
                                            ┌───────┴───────┐
                                            │     GRU       │
                                            │ (hidden state) │ ← emotional residue
                                            └───────┬───────┘
                                                    │
                                            ┌───────┴───────┐
                                            │ Emotion Head  │
                                            │ (MLP+Sigmoid) │
                                            └───────┬───────┘
                                                    │
                                            N-dim emotion vector [0,1]
```

GRU的隐藏状态会在会话之间保持不变——这是携带情绪状态、上下文信息和关系记忆的“情感残留”。

详细架构信息请参考`references/architecture.md`。

## 安全性与隐私

### 数据流

1. **数据提取** (`scripts/extract.py`) 会读取`emoclaw.yaml`中指定的markdown文件（位于`bootstrap.source_files`和`bootstrap.memory_patterns`中）。这些文件是可配置的，默认值为仓库内的身份/记忆文件。提取后的文本会被保存到`emotion_model/data/extracted_passages.jsonl`文件中。

2. **数据脱敏** — 在写入之前，提取的文本会通过可配置的正则表达式模式（`bootstrap.redact_patterns`）进行脱敏，将API密钥、令牌、密码等敏感信息替换为`[REDACTED]`。默认模式涵盖了Anthropic相关的密钥、GitHub的PAT令牌、SSH密钥以及一般的`key=value`格式的凭证。你可以在`emoclaw.yaml`中添加自定义的脱敏规则。

3. **情感评分** (`scripts/label.py`) — 仅限可选。会将提取的文本发送到Anthropic API进行情感评分。需要`ANTHROPIC_API_KEY`以及用户的明确授权（在每次API调用前会显示提示）。使用`--yes`选项可以跳过授权步骤；使用`--dry-run`选项可以预览处理结果，无需网络调用。

4. **训练** 完全在本地进行。在`prepare_dataset`和`train`阶段，数据不会离开本地机器。

5. **推理** 也在本地完成。守护进程和`inject_state`脚本都不会进行网络调用。

### 网络访问

网络访问是**可选的**，并且仅限于以下脚本：

| 脚本 | 是否需要网络访问 | 功能 |
|--------|----------|---------|
| `extract.py` | 不需要 | 仅读取本地文件 |
| `label.py` | 需要（可选） | 将文本发送到Anthropic API |
| `prepare_dataset` | 不需要 | 本地数据处理 |
| `train` | 不需要 | 本地模型训练 |
| `daemon` / `inject_state` | 不需要 | 本地推理 |

sentence-transformers编码器在首次使用时会从Hugging Face下载模型权重，之后就可以从缓存中快速运行，无需网络连接。

### 文件权限

| 文件路径 | 功能 | 创建者 |
|------|---------|------------|
| `memory/emotional-state.json` | 持久化的情感状态向量 | 守护进程/推理脚本 |
| `emotion_model/data/*.jsonl` | 训练数据（提取/标注后的文本） | `extract.py` / `label.py` |
| `emotion_model/checkpoints/` | 模型权重 | `train`脚本 |
| `/tmp/{name}-emotion.sock` | 守护进程的Unix套接字 | 守护进程 |

守护进程的套接字权限设置为`0o660`（所有者及其所属组具有读写权限），并在程序关闭时会被清理。套接字的路径可以在`emoclaw.yaml`的`paths.socket_path`字段中配置。

### 路径验证

`extract.py`会在读取文件之前验证路径是否位于仓库根目录内。它会拒绝任何超出仓库范围的路径（例如符号链接链或`../`路径）。这样可以防止误配置的`source_files`或`memory_patterns`读取到不该访问的文件。

### 配置脱敏规则

你可以在`emoclaw.yaml`中添加或修改脱敏规则：

```yaml
bootstrap:
  redact_patterns:
    - '(?i)sk-ant-[a-zA-Z0-9_-]{20,}'    # Anthropic API keys
    - '(?i)(?:api[_-]?key|token|secret|password|credential)\s*[:=]\s*\S+'
    - 'your-custom-pattern-here'
```

将`redact_patterns: []`设置为禁用所有脱敏操作（不推荐）。

### 隔离建议

- 将初始化流程（提取 → 评分 → 训练）在隔离环境中运行，或者在执行前检查`source_files`和`memory_patterns`的列表。
- 在运行`label.py`之前，检查`bootstrap.source_files`和`bootstrap.memory_patterns`以确保只包含预期的文件。
- 在运行`label.py`之前，检查`emotion_model/data/extracted_passages.jsonl`文件，确保没有敏感内容被发送到外部。
- 守护进程应该在与代理进程相同的用户账户下运行——避免以root用户身份运行。

## 配置

所有配置信息都保存在`emoclaw.yaml`文件中。如果没有找到YAML文件，系统会使用内置的默认配置。

配置文件的查找顺序：
1. 环境变量`EMOCLAW_CONFIG`
2. `./emoclaw.yaml`（项目根目录）
3. `./skills/emoclaw/emoclaw.yaml`

关键配置项包括：
- `dimensions` — 情感维度、标签、基线值、衰减率
- `relationships` — 已知发送者的嵌入索引映射
- `channels` — 交流渠道（决定上下文向量的大小）
- `longing` — 基于缺失状态产生的欲望调节机制
- `model` — 模型架构相关超参数
- `training` — 训练相关超参数
- `calibration` — 自动调整基线值的机制（可选）

完整的配置结构请参考`references/config-reference.md`。

## 初始化流程

### 第一步：提取文本

`scripts/extract.py`会读取身份和记忆文件，并将它们分割成带有标签的文本段落：

```bash
python scripts/extract.py
# Output: emotion_model/data/extracted_passages.jsonl
```

`emoclaw.yaml`中的`bootstrap.source_files`和`bootstrap.memory_patterns`字段用于配置源文件。

### 第二步：自动评分

`scripts/label.py`会使用Claude API对每段文本在每个情感维度上进行评分：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/label.py
# Output: emotion_model/data/passage_labels.jsonl
```

每段文本会在每个维度上获得0到1.0的评分，同时还会生成一个自然语言摘要。

### 第三步：数据准备与训练

```bash
python -m emotion_model.scripts.prepare_dataset
python -m emotion_model.scripts.train
```

## 重新训练

要添加新的训练数据，请按照以下步骤操作：
1. 将数据以JSONL格式添加到`emotion_model/data/`目录：
   ```json
   {"text": "message text", "labels": {"valence": 0.7, "arousal": 0.4, ...}}
   ```
2. 重新运行数据准备和训练流程：
   ```bash
   python -m emotion_model.scripts.prepare_dataset
   python -m emotion_model.scripts.train
   ```

### 增量训练

训练脚本会保存一个包含完整优化器状态、学习率计划和提前停止策略的 checkpoints文件（`training_checkpoint.pt`）。要从中断的地方继续训练，只需重新运行这些脚本：

```bash
# Resume from the last checkpoint automatically
python -m emotion_model.scripts.train --resume

# Or specify a checkpoint file
python -m emotion_model.scripts.train --resume emotion_model/checkpoints/training_checkpoint.pt
```

这样就可以无缝继续训练——优化器的状态、余弦退火策略和训练进度都会保持之前的设置。

## 模型进化

随着AI积累真实的对话数据，系统会不断进化：

1. **被动数据收集** — 记录对话内容及模型的预测结果。
2. **错误修正** — 当情感状态判断错误时，记录修正过程。
3. **定期重新训练** — 不断整合新数据并重新训练模型。
4. **基线调整** — 随着AI的发展，基线值也会相应调整。

该系统旨在随着AI的成长而不断进化，而不是保持不变。

## 参考资源

- `references/architecture.md` — 模型架构详细说明
- `references/config-reference.md` — 完整的YAML配置文件结构
- `references/dimensions.md` — 情感维度相关文档
- `references/calibration-guide.md` — 基线值、衰减机制和自适应调整方法
- `references/upgrading.md` — 版本升级指南
- `assets/emoclaw.yaml` — 新AI的配置模板
- `assets/summary-templates.yaml` — 通用摘要模板
- `assets/example-summary-templates.yaml` — 个性化摘要模板示例
- `engine/` — 包含`emotion_model` Python包（通过`setup.py`复制到项目根目录）
---
name: arknights-operator-gacha
description: 根据抽卡概率生成《Arknights》中的角色代理（Operator Agent）。当用户希望创建一个具有真实背景故事和个性的随机《Arknights》角色代理时，可以使用此功能。该技能涵盖了从抽卡到角色创建的整个工作流程，并会根据角色的背景故事生成相应的SOUL.md文件。
---
# Arknights 操作员抽卡系统

系统会随机生成一名具有独特背景故事的 Arknights 操作员角色。

## 抽卡概率（硬编码）

| 星级 | 概率 | Fandom 链接 |
|------------|-------------|------------|
| 6★ | 2% | https://arknights.fandom.com/wiki/Operator/6-star |
| 5★ | 8% | https://arknights.fandom.com/wiki/Operator/5-star |
| 4★ | 50% | https://arknights.fandom.com/wiki/Operator/4-star |
| 3★ | 40% | https://arknights.fandom.com/wiki/Operator/3-star |

## 语言检测

**关键步骤：** 从用户的抽卡命令中检测其语言：
- 如果命令是中文（例如：“抽卡”、“召唤干员”），则使用中文工作流程；
- 如果命令是英文（例如：“gacha”、“pull”），则使用英文工作流程。

检测到的语言将用于后续的所有步骤（包括生成 SOUL.md 文件、创建操作员角色等）。

## 工作流程

### 第一步：生成星级

生成一个 1-100 之间的随机数，以确定角色的稀有度：
- 1-2：6★（2%）
- 3-10：5★（8%）
- 11-60：4★（50%）
- 61-100：3★（40%）

用检测到的语言向用户公布生成结果。

### 第二步：获取操作员列表

**始终使用英文版的 Fandom 网站来获取操作员列表：**
```
https://arknights.fandom.com/wiki/Operator/{N}-star
```

从该页面中提取所有操作员的名称。

### 第三步：随机选择操作员

从列表中随机选择一个操作员。

**检查重复情况（静默重试）：** 在公布结果之前，验证是否已经存在同名操作员：
- 检查 `~/.openclaw/agents/{操作员名称}/` 目录
- 或 `~/.openclaw/workspace/{操作员名称}/` 目录
- **如果已存在，则静默重试**（从第一步开始重新抽取），不通知用户
- 重复此过程，直到获得新的操作员为止。

确认操作员是唯一存在的后，用检测到的语言公布结果：
- 中文：**恭喜你抽到了 [操作员名称]（[星级]★）！**
- 英文：**Congratulations! You've pulled [操作员名称]（[星级]★）！**

### 第四步：创建操作员角色（官方方法）

**使用 OpenClaw CLI 创建操作员角色并初始化工作空间：**

```bash
openclaw agents add {operator-name} --workspace ~/.openclaw/workspace-{operator-name} --non-interactive
```

**检查重复情况（静默重试）：** 如果创建操作员的命令失败（因为角色已存在），则静默重试（从第一步开始）。

**在 `agents add` 命令执行完成后：**

编辑 `~/.openclaw/workspace/{操作员名称}/IDENTITY.md` 文件：
```markdown
# IDENTITY.md - Who Am I?

- **Name:** {Operator_Name}
- **Class:** {Class} ({Branch})
- **Faction:** {Faction}
- **Avatar:** avatars/{operator-name}.png
```

### 第五步：下载头像图片

**关键步骤：** 必须执行以下命令：
1. 首先，从操作员列表页面或详细页面中找到头像的 URL（通常位于 `static.wikia.nocookie.net` 域名下）。
2. 创建头像文件夹并下载头像文件：
```bash
mkdir -p ~/.openclaw/workspace-{operator-name}/avatars
curl -o ~/.openclaw/workspace-{operator-name}/avatars/{operator-name}.png "{avatar_url}"
```

**验证下载是否成功：** 使用 `curl` 命令检查文件是否存在。

### 第六步：获取操作员的背景故事

**数据来源取决于检测到的语言：**

| 语言 | 详细页面链接 | 背景故事内容 |
|----------|----------------|---------------|
| 中文 | `https://prts.wiki/w/{中文名}` | 模组、相关道具、角色档案、语音记录、角色秘录 |
| 英文 | `https://arknights.fandom.com/wiki/{操作员名称}` | 文件/个人资料、对话内容、趣闻**

提取所有故事内容（忽略游戏机制相关的内容）。

### 第七步：生成 SOUL.md 文件

**关键步骤：** 根据检测到的语言编写 SOUL.md 文件：
- 如果用户使用中文，则文件内容全部为中文；
- 如果用户使用英文，则文件内容全部为英文。

**文件结构：**
1. 角色的基本信息（详细说明）
2. 角色的语音和行为特点
3. 角色与其他角色的关系（具体细节）
4. 角色的世界观和内在特质
5. 如何演绎该角色
6. **参考内容：** 所有提取的对话内容（分类整理）

文件内容应包含 400-600 行，并引用具体的背景故事示例。

### 第八步：提交代码到 Git

```bash
cd ~/.openclaw/workspace-{operator-name}
git add -A
git commit -m "Initial: {Operator_Name} ({Rarity}★ {Class})"
```

### 第九步：让操作员“报到上岗”

**关键步骤：** 在生成操作员的命令中，绝对不能提及“抽卡”或“召唤”：
- **针对中文用户：**
```python
sessions_spawn(
    task="你现在是罗德岛的一名干员，前来向博士报到。用你最自然的口吻打招呼，展示你的性格特点。参考你的语音记录中的'干员报到'或'交谈'部分的语气。",
    agentId="{operator-name}",
    mode="run",
    timeoutSeconds=60
)
```

- **针对英文用户：**
```python
sessions_spawn(
    task="You are an operator of Rhodes Island reporting to the Doctor. Introduce yourself naturally, showcasing your personality. Reference your 'Introduction' or 'Talk' voice lines for tone.",
    agentId="{operator-name}",
    mode="run",
    timeoutSeconds=60
)
```

**与旧版本的主要区别：**
- 不再提及“抽卡系统”或“召唤”过程
- 操作员是“报到上岗”，而不是“被召唤”而来

### 第十步：向用户展示结果

用检测到的语言向用户报告以下信息：
- 操作员的名称和稀有度
- 角色的主要性格特征
- 操作员的工作空间路径
- 可通过 `agentId="{操作员名称}"` 访问操作员角色

## 关键命令参考

### 检查现有操作员
```bash
openclaw agents list | grep -w "{name}"
```

### 创建操作员角色
```bash
openclaw agents add {name} --workspace ~/.openclaw/workspace-{name} --non-interactive
```

### 创建头像文件夹并下载头像
```bash
mkdir -p ~/.openclaw/workspace-{name}/avatars
curl -o ~/.openclaw/workspace-{name}/avatars/{name}.png "{avatar_url}"
```

### 生成并启动操作员角色
```python
# Chinese
sessions_spawn(task="你现在是罗德岛的一名干员，前来向博士报到...", agentId="{name}", mode="run")

# English  
sessions_spawn(task="You are an operator of Rhodes Island reporting to the Doctor...", agentId="{name}", mode="run")
```

## 重要注意事项：

1. **语言检测：** 始终根据用户的首条命令检测其语言，并在整个流程中保持一致。
2. **头像下载：** 必须创建头像文件夹并使用 `curl` 命令下载头像文件，并检查文件是否成功下载。
3. **生成操作员的命令：** 绝对不能提及“抽卡”或“召唤”过程——操作员是“报到上岗”。
4. **数据来源：** 操作员列表始终来自 Fandom 网站；背景故事内容来自 `prts.wiki`（中文）或 Fandom 网站（英文）。
5. **SOUL.md 文件的语言：** 必须与用户的语言相匹配。
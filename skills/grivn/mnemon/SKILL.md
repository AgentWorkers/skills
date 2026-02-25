---
name: mnemon
description: "用于大型语言模型（LLM）代理的持久化内存命令行工具（CLI）。该工具可用于存储事实信息、检索过往知识、关联相关记忆内容以及管理数据的生命周期。"
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["mnemon"]
    install:
      - id: "brew"
        kind: "brew"
        formula: "mnemon-dev/tap/mnemon"
        bins: ["mnemon"]
        label: "Install mnemon (Homebrew)"
      - id: "go"
        kind: "go"
        package: "github.com/mnemon-dev/mnemon@latest"
        bins: ["mnemon"]
        label: "Install mnemon (go install)"
---
# mnemon

## 安装与配置

### 1. 安装二进制文件

**使用 Homebrew (macOS / Linux):**

```bash
brew install mnemon-dev/tap/mnemon
```

**使用 Go 进行安装:**

```bash
go install github.com/mnemon-dev/mnemon@latest
```

### 2. 配置 OpenClaw 集成

```bash
mnemon setup --target openclaw --yes
```

以下命令会部署所有相关组件：
- **Skill** 文件：`~/.openclaw/skills/mnemon/SKILL.md`
- **Hook** 文件：`~/.openclaw/hooks/mnemon-prime/`（代理：用于注入行为提示）
- **Plugin** 文件：`~/.openclaw/extensions/mnemon/`（包含提醒、提示等功能）
- **Prompt** 文件：`~/.mnemon/prompt/`（包含 `guide.md` 和 `skill.md`）

重启 OpenClaw 代理以使配置生效。

### 3. 自定义（可选）

编辑 `~/.mnemon/prompt/guide.md` 文件以调整记忆的回忆/提醒行为。

插件钩子的配置信息位于 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "plugins": {
    "entries": {
      "mnemon": {
        "enabled": true,
        "config": {
          "remind": true,
          "nudge": true,
          "compact": false
        }
      }
    }
  }
}
```

| 钩子类型 | 默认设置 | 功能说明 |
|---------|-----------|-------------------|
| `remind` | 开启 | 回忆相关记忆，并在每条消息发送时提醒代理 |
| `nudge` | 开启 | 在每次回复后提示代理“需要记住某些内容” |
| `compact` | 关闭 | 在压缩记忆内容之前保存关键信息 |

### 4. 卸载

```bash
mnemon setup --eject --target openclaw --yes
```

## 工作流程

1. **记忆功能**：`mnemon remember "<事实>" --cat <分类> --imp <重要性等级> --entities "实体1,实体2" --source <代理>`  
   - 系统会自动处理重复内容并替换冲突项。  
   - 输出内容包括：`action`（添加/更新/跳过）、`semantic_candidates`（语义相关项）和 `causal_candidates`（因果关系相关项）。  

2. **链接功能**（根据第 1 步的结果进行判断）：  
   - 检查 `causal_candidates`：这些记忆之间是否存在真正的因果关系？`causal_signal` 是基于正则表达式的，可能会产生误判——只有当记忆之间确实存在因果关系时才进行链接。  
   - 检查 `semantic_candidates`：这些记忆之间是否有意义上的关联？仅凭高相似度是不够的——会跳过那些虽然关键词相同但讨论内容无关的记忆。  
   - 使用语法：`mnemon link <链接ID> <候选内容> --type <因果/语义> --weight <重要性等级> [--meta '<JSON>']`  

3. **回忆功能**：`mnemon recall "<查询>" --limit 10`  

## 命令说明

```bash
mnemon remember "<fact>" --cat <cat> --imp <1-5> --entities "e1,e2" --source agent
mnemon link <id1> <id2> --type <type> --weight <0-1> [--meta '<json>']
mnemon recall "<query>" --limit 10
mnemon search "<query>" --limit 10
mnemon forget <id>
mnemon related <id> --edge causal
mnemon gc --threshold 0.4
mnemon gc --keep <id>
mnemon status
mnemon log
mnemon store list
mnemon store create <name>
mnemon store set <name>
mnemon store remove <name>
```

## 注意事项

- 使用 `exec` 工具来执行 `mnemon` 命令。  
- 请勿存储任何敏感信息（如密码或令牌）。  
- 分类类别包括：`preference`（偏好）、`decision`（决策）、`insight`（洞察）、`fact`（事实）、`context`（上下文）。  
- 记忆的类型包括：`temporal`（时间相关的）、`semantic`（语义相关的）、`causal`（因果相关的）、`entity`（实体相关的）。  
- 每条记忆内容的长度最多为 8,000 个字符。
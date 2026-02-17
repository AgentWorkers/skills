# 多脑协议（Multi-Brain Protocol）

**功能说明：**  
在主要智能体作出响应之前，该协议会并行调用多个大型语言模型（Kimi K2.5 和 GPT 5.3 Codex），从而为你的AI智能体提供认知多样性。这意味着你的智能体拥有三个“大脑”，而不仅仅是一个。

## 对智能体的影响  
多脑协议是通过 `turn:before` 钩子（hook）系统级强制执行的，无需任何手动操作。  
当用户输入 “mb” 作为命令的第一个词时，该钩子会：  
1. 并行调用 Kimi K2.5 和 GPT 5.3 Codex；  
2. 将它们的观点融入系统上下文中；  
3. 将所有观点综合后生成最终响应；  
4. 绝不会向用户透露其他AI的存在。  

这些不同的观点会以以下形式显示在用户的界面中：  
```
[KIMI K2.5 PERSPECTIVE]
<perspective text>

[CODEX 5.3 PERSPECTIVE]
<perspective text>
```  

## 对人类的使用说明  

### 设置步骤  
1. 安装 `turn:before` 钩子：  
```bash
mkdir -p hooks/turn-preflight
# Copy HOOK.md and handler.js from this package
```  
2. 设置 Kimi 的API密钥：  
```bash
echo "your-moonshot-api-key" > .kimi-api-key
```  
3. 安装 Codex 的命令行工具（CLI）：  
```bash
npm install -g @openai/codex
codex auth   # OAuth login
```  
4. 在 `openclaw.json` 配置文件中启用该功能：  
```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "turn-preflight": { "enabled": true }
      }
    }
  }
}
```  

### 触发模式  
在 `handler.js` 文件中配置 `TRIGGER_MODE`：  
| 模式 | 行为 |  
|------|----------|  
| `keyword` （默认） | 仅当输入 “mb” 或 “multibrain” 时触发 |  
| `hybrid` | 通过关键词触发；消息长度超过50个字符时自动触发 |  
| `auto` | 每条消息都会触发（但会消耗更多计算资源） |  

### 使用的LLM模型  
| 模型 | 角色 | 提供方 | 响应延迟（秒） |  
|-----|------|----------|---------|  
| Claude Opus 4.6 | 主要智能体 | OpenClaw（Anthropic） | 无 |  
| Kimi K2.5 | 第二个视角 | Moonshot API | 约5秒 |  
| GPT 5.3 Codex | 第三个视角 | Codex CLI | 约4秒 |  

## 架构概述  
```
User types: "mb should we change pricing?"
    |
    v
[turn:before hook detects "mb" keyword]
    |
    +---> Kimi K2.5 (Moonshot API, parallel)
    +---> GPT 5.3 Codex (CLI, parallel)
    |
    v (~5s combined)
[Perspectives injected into system content]
    |
    v
Claude Opus 4.6 responds with all 3 viewpoints
```  

## 主要优势：  
- **认知多样性**：三种不同的AI模型协同工作；  
- **减少偏见**：采用不同的训练数据和算法；  
- **按需使用**：仅在用户请求时消耗计算资源；  
- **容错机制**：即使某个模型失败，其他模型仍能正常运行；  
- **系统级支持**：无需智能体额外遵循任何协议规则。  

---

**来源：** <https://github.com/Dannydvm/openclaw-multi-brain>
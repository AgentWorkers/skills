---
name: friday-router
displayName: IntentRouter
description: Your AI's Smart Traffic Director—precisely matching OpenClaw tasks to the perfect LLM. Intelligent orchestration with OpenRouter. Security-focused: no gateway auth exposure.
version: 1.7.0
---

# IntentRouter

**您的AI智能任务分配器：精准匹配您的OpenClaw任务与最适合的LLM模型。**

**v1.7.0版本——专注于安全性的更新。**  
- 支持复杂任务的处理；使用绝对路径；已通过OpenClaw TUI的委托功能进行测试并验证其正常运行。  
- 为提升安全性，移除了与网关认证相关的敏感信息及网关管理功能。

IntentRouter会分析您的任务，并将其分配给最合适的LLM模型：  
- MiniMax 2.5适用于代码编写；  
- Kimi k2.5适用于创意创作；  
- Grok Fast适用于研究任务。  
通过这一机制，您可以避免盲目猜测，让任务分配更加高效。

**v1.7.0的安全性改进：**  
- 从路由器的输出中移除了网关认证所需的令牌/密码信息；  
- 网关管理功能已被移除，如需使用请单独使用[gateway-guard](https://clawhub.ai/skills/gateway-guard)技能；  
- FACEPALM集成也被移除，如需使用请单独使用[FACEPALM](https://github.com/RuneweaverStudios/FACEPALM)技能。

**使用要求：**  
- 所有模型ID均需以`openrouter/`为前缀。  
- 需要使用OpenRouter API密钥配置OpenClaw，以确保一个认证配置即可覆盖所有任务层级。

**配置访问权限：**  
- 该技能仅读取其自身的`config.json`文件（位于技能目录中），用于获取模型配置和路由规则信息。  
- 该技能不会读取`openclaw.json`文件，也不会访问网关令牌/密码，也不会执行任何网关管理操作。  
- 路由器的输出仅包含`task`、`model`、`sessionTarget`以及可选的`label`，不包含任何敏感信息或凭证。

**默认/编排模型：**  
- Gemini 2.5 Flash（`openrouter/google/gemini-2.5-flash`）：执行速度快、成本低、可靠性高。  
- 路由器会将任务委托给相应的子代理模型（如Kimi用于创意任务，MiniMax 2.5用于代码任务等）。

## 编排流程（任务请求的必经步骤）  
当您作为**主代理模型**（例如Gemini 2.5 Flash）接收到用户提交的**任务**（如代码编写、研究、创作等）时，必须将任务委托给相应的子代理模型执行。  
**具体步骤如下：**  
1. 运行IntentRouter以获取任务参数：  
   ```bash
   python3 workspace/skills/friday-router/scripts/router.py spawn --json "<user message>"
   ```  
   示例输出：`{"task":"write a poem about Mai","model":"openrouter/moonshotai/kimi-k2.5","sessionTarget":"isolated"}`  
2. 使用路由器返回的`model`值立即调用`sessions_spawn`函数。  
   **注意：**切勿更改`model`值，必须严格按照路由器的输出执行。  
3. 将子代理模型的响应结果转发给用户。响应内容应明确显示所使用的模型名称（例如“使用的是Kimi k2.5”）。  

**错误处理：**  
- 如果`sessions_spawn`返回错误（例如`device_token_mismatch`），需告知用户任务委托失败，并建议用户检查网关状态或使用`gateway-guard`技能。  
- 即使任务委托失败，也只需返回错误信息及后续处理建议，切勿直接生成任务结果。  

**执行规则：**  
- 对于实际用户任务，禁止使用`classify`函数进行任务执行；`classify`仅用于诊断用途。  
- 正确的执行流程应为：`spawn --json` → `sessions_spawn`。  

**输出规范：**  
- 仅在任务成功执行后显示模型名称（例如“使用的是：Kimi k2.5”）。  
- 绝不向用户展示任何内部编排信息（如会话键、ID、运行时数据等）。  

**其他注意事项：**  
- 对于非分类性质的查询（如“您使用的是哪个模型？”、“路由机制是如何工作的？”），请自行回答。  
- 该技能不会在输出中暴露网关认证信息；如需网关管理功能，请使用`gateway-guard`技能。  

## 模型选择（根据Austin的偏好进行分类）  
| 任务类型 | 主要推荐模型 | 备选模型 |
|---------|----------------|---------|
| **默认/编排任务** | Gemini 2.5 Flash | — |
| **快速/低成本** | Gemini 2.5 Flash | Gemini 1.5 Flash、Haiku |
| **推理任务** | GLM-5 | Minimax 2.5 |
| **创意/前端任务** | Kimi k2.5 | — |
| **研究任务** | Grok Fast | — |
| **代码/工程任务** | MiniMax 2.5 | Qwen2.5-Coder |
| **高质量/复杂任务** | GLM 4.7 Flash | GLM 4.7、Sonnet 4、GPT-4o |
| **视觉处理任务** | GPT-4o | — |

**模型ID格式：**  
所有模型ID均以`openrouter/`为前缀（例如`openrouter/moonshotai/kimi-k2.5`）。  

## 使用方式：  
### 命令行界面（CLI）  
```bash
python scripts/router.py default                          # Show default model
python scripts/router.py classify "fix lint errors"        # Classify → tier + model
python scripts/router.py spawn --json "write a poem"       # JSON for sessions_spawn (no gateway secrets)
python scripts/router.py models                            # List all models
```  
**注意：**网关认证管理功能需单独使用`gateway-guard`技能。  

**示例：**  
- **创意任务（诗歌创作）：**  
```
router output: {"task":"write a poem","model":"openrouter/moonshotai/kimi-k2.5","sessionTarget":"isolated"}
→ sessions_spawn(task="write a poem", model="openrouter/moonshotai/kimi-k2.5", sessionTarget="isolated")
```  
- **代码任务（错误修复）：**  
```
router output: {"task":"fix the login bug","model":"openrouter/minimax/minimax-m2.5","sessionTarget":"isolated"}
→ sessions_spawn(task="fix the login bug", model="openrouter/minimax/minimax-m2.5", sessionTarget="isolated")
```  
- **研究任务：**  
```
router output: {"task":"research best LLMs","model":"openrouter/x-ai/grok-4.1-fast","sessionTarget":"isolated"}
→ sessions_spawn(task="research best LLMs", model="openrouter/x-ai/grok-4.1-fast", sessionTarget="isolated")
```  

## 任务层级分类：**  
- **FAST**：简单任务（检查、获取、列表、显示、状态监控等）  
- **REASONING**：逻辑分析、推导等  
- **CREATIVE**：创意写作、故事创作、用户界面设计等  
- **RESEARCH**：信息检索、搜索等  
- **CODE**：代码编写、调试、实现等  
- **QUALITY**：复杂系统设计等  
- **VISION**：图像处理等  

**与原始版本的差异：**  
- 简单任务的分类标准已调整（高匹配度对应FAST层级）  
- 多步骤任务现在会被正确分类为CODE层级  
- 视觉处理任务的优先级得到提升  
- 新增了对代码相关关键词（如React、JWT等）的识别  
- 任务难度现在会根据关键词匹配程度进行合理判断
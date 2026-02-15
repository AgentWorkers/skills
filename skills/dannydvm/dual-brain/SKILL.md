# 双脑技能（Dual-Brain Skill）

**功能说明：**  
该功能通过从第二个大型语言模型（LLM，与您的主模型不同）自动生成观点，为用户消息提供认知多样性。

## 对于智能体（Agents）：  
在回复任何用户消息之前，请先检查是否存在“双脑视角”：  
```bash
cat ~/.dual-brain/perspectives/{your-agent-id}-latest.md
```  

如果该文件存在且包含最新的观点（请查看注释中的时间戳），请将其与您的推理结果一起考虑。这些观点可能会指出：  
- 您可能忽略的视角  
- 替代性的处理方法  
- 需要验证的重要事项  

**集成方式：**  
- 视点由后台守护进程自动生成  
- 您无需进行任何手动操作  
- 回复前只需读取该文件  
- 将您的观点与第二个LLM的观点综合起来形成最终答案  

**示例工作流程：**  
1. 用户发送消息  
2. 守护进程拦截消息并发送给第二个LLM（例如Kimi、GPT-4、Llama）  
3. 第二个LLM生成2-3句话的观点  
4. 生成的观点会被保存在`~/.dual-brain/perspectives/{agent-id}-latest.md`文件中  
5. 您（主智能体）在回复前先阅读这些观点  
6. 将两个观点综合后形成最终回复  

## 对于人类用户（Humans）：  
**设置方法：**  
```bash
npm install -g openclaw-dual-brain
dual-brain setup    # Interactive configuration
dual-brain start    # Start daemon
```  

**可用提供者（Providers）：**  
- `ollama`：本地模型（免费，需要安装Ollama）  
- `moonshot`：Kimi/Moonshot API（中文LLM，响应速度快）  
- `openai`：GPT-4o、GPT-4-turbo等  
- `groq`：基于Llama模型的快速推理服务  

**相关命令：**  
- `dual-brain setup`：配置提供者、模型和API密钥  
- `dual-brain start`：启动守护进程  
- `dual-brain stop`：停止守护进程  
- `dual-brain status`：查看运行状态  
- `dual-brain logs`：查看最近的活动记录  
- `dual-brain install-daemon`：将守护进程安装为系统服务  

**配置文件位置：`~/.dual-brain/config.json`**  
**观点文件位置：`~/.dual-brain/perspectives/`  

## 架构说明：**  
```
User Message → OpenClaw Session (JSONL)
                    ↓
            Dual-Brain Daemon (polling)
                    ↓
            Secondary LLM Provider
            (ollama/moonshot/openai/groq)
                    ↓
        Perspective Generated (2-3 sentences)
                    ↓
        ~/.dual-brain/perspectives/{agent}-latest.md
                    ↓
        Primary Agent reads & synthesizes
                    ↓
            Response to User
```  

**优势：**  
- **认知多样性**：两个AI模型提供更全面的视角  
- **减少偏见**：不同的训练数据和算法有助于减少偏见  
- **质量保障**：第二种观点有助于发现潜在问题  
- **零额外开销**：守护进程在后台运行，延迟小于1秒  
- **提供者灵活性**：可根据需求选择不同的提供者和模型（兼顾成本与质量）  

**可选功能：Engram集成**  
如果Engram（语义记忆系统）运行在`localhost:3400`上，生成的观点也会被存储为长期可检索的记忆。  

---

**来源：** <https://github.com/yourusername/openclaw-dual-brain>
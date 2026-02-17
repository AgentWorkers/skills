---
name: neverforget
version: 1.0.2
description: 该技能可自动管理“Sovereign Local Vector Memory”（主权本地向量内存）、符号链接（symlinks）以及“Gemma-300M Embeddings”（Gemma-300M嵌入模型）。它是专为Doge币（Doge）设计的终极内存管理工具，可用于管理本地向量嵌入数据、同步外部Doge币基础设施的符号链接，并监控内存使用状况。
---
# 🧠 技能：永远不忘（终极记忆）

## 🛡️ 安全与隐私声明  
该技能通过符号链接将您本地的 Dogecoin 节点数据连接到 OpenClaw 工作空间。  
- **隐私保护：** 数据会在本地使用 Gemma-300M 进行索引处理，不会离开您的设备。  
- **风险提示：** 索引 `~/.dogecoin` 目录会允许代理程序读取节点配置文件，请确保您的 `wallet.dat` 文件设置了密码保护。  

## 核心工作流程  
1. **基础设施同步：** 将 `~/.dogecoin` 和 `~/.doginals-main` 目录连接到 OpenClaw 工作空间。  
2. **本地知识库（RAG）：** 使用 Gemma-300M 进行离线项目数据的存储与管理。  
3. **状态监控：** 通过 [HEARTBEAT.md](references/HEARTBEAT.md) 文件进行实时监控。  

## 使用步骤  
- 要刷新记忆数据，请运行 `openclaw memory index` 命令。  
- 要检查符号链接的状态，请查看 `references/` 文件夹中的 `HEARTBEAT.md` 文件。  

## 所需依赖项  
- **引擎：** `node-llama-cpp`  
- **插件：** `memory-core`  
- **模型：** `Gemma-300M-QAT`  

## 自动安装脚本  
```bash
# 第一阶段：激活引擎和插件  
pnpm add node-llama-cpp -w  
openclaw plugin enable memory-core  

# 第二阶段：系统配置  
openclaw config set agents.defaults.memorySearch.provider local  
openclaw config set agents.defaults.memorySearch.local.modelPath "hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf"  

# 第三阶段：建立基础设施链接（符号链接）  
ln -s /home/$USER/.dogecoin ~/.openclaw/workspace/dogecoin-core  
ln -s /home/$USER/.doginals-main ~/.openclaw/workspace/doginals-main  
ln -s /home/$USER/.crabwalk ~/.openclaw/workspace/crabwalk  

# 第四阶段：注入主配置文件（匹配官方结构）  
cat ~/.openclaw/skills/neverforget/HEARTBEAT.md >> ~/.openclaw/workspace/HEARTBEAT.md  

# 第五阶段：完成激活  
openclaw gateway restart  
openclaw memory index  
```
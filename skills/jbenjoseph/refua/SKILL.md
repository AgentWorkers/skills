# 技能：Refua

## 概述
Refua 在药物发现领域中用于计算生物分子复合物（例如蛋白质-配体/蛋白质-蛋白质复合物）的折叠结构并对其进行评分，同时可选地对这些复合物的 ADMET（吸收、分布、代谢和排泄）特性进行分析，从而帮助确定在药物发现流程中应优先合成和测试哪些分子。

该技能通过与 **refua-mcp** MCP 服务器的连接来运行，该服务器将 Refua 的“统一复合物 API”作为 MCP 工具提供，支持以下功能：
- **Boltz2** 复合物折叠（可选包含亲和力评估）
- **BoltzGen** 设计工作流程
- 可选的 **ADMET** 特性分析（如果已安装）

Clawdbot 支持原生 MCP，因此唯一的要求是运行该 MCP 服务器并调用其提供的工具。更多信息请参见：[github.com](https://github.com/agentcures/refua-mcp)

---

## 适用场景
在以下情况下使用该技能：
- 需要对蛋白质-配体、蛋白质-蛋白质或仅蛋白质/DNA/RNA 复合物进行折叠处理
- 需要估算指定配体在复合物中的结合亲和力
- 需要对一个或多个 SMILES 格式的配体进行 ADMET 预测（如果该功能已启用）
- 需要通过 MCP 工具调用执行计算密集型的 Refua 工作流程

**不适用场景**：
- 任务属于简单的确定性计算（建议使用非机器学习工具）
- 用户需要您生成特定的序列或 SMILES 格式的数据（请用户提供相关输入）
- 用户请求不安全的实验室操作或临床指导

---

## 安装与资源准备（操作步骤）
### 1) 安装 Refua 和 refua-mcp
首先安装 Refua（支持 CPU 或 GPU 计算），然后安装 MCP 服务器软件包：[github.com](https://github.com/agentcures/refua-mcp)

- **支持 GPU 计算**：
  - `pip install refua[cuda]`
- **仅支持 CPU 计算**：
  - `pip install refua`
- **MCP 服务器**：
  - `pip install refua-mcp`

### 2) （可选）启用 ADMET 功能
ADMET 功能是可选的，需要额外安装相关包：[github.com](https://github.com/agentcures/refua-mcp)
- `pip install refua[admet]`

### 3) 下载模型与资源文件
Boltz2 和 BoltzGen 需要模型和分子资源文件。Refua 可以自动下载这些文件：[github.com](https://github.com/agentcures/refua-mcp)
- 使用命令 `python -c "from refua import download_assets; download_assets()"` 下载资源文件

资源文件的默认存储位置及覆盖方式：[github.com](https://github.com/agentcures/refua-mcp)
- **Boltz2** 默认使用 `~/.boltz` 文件夹存储资源文件
  - 如需更改存储路径，可通过工具选项 `boltz.cache_dir` 进行设置
- **BoltzGen** 默认使用内置的高精度（HF）模型文件
  - 如需更改模型文件路径，可通过工具选项 `boltzgen.mol_dir` 进行设置

---

## 运行 MCP 服务器
使用以下命令启动 MCP 服务器：[github.com](https://github.com/agentcures/refua-mcp)

```bash
python3 -m refua_mcp.server
```
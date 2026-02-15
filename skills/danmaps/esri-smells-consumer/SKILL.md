---
name: esri-workflow-smell-detector (consumer)
version: 1.0.0
description: |
  Paid client skill for Esri Workflow Smell Detector via x402 (Base/USDC).
  Use when you want to run a deterministic automation preflight scan on an ArcGIS Pro project snapshot
  by calling https://api.x402layer.cc/e/esri-smells (HTTP 402 payment flow).
---

# Esri 工作流风险检测器（消费者技能）

此技能帮助代理使用 Base/USDC 调用付费的 Smell Detector 端点（按请求计费，费用为 x402）。

**注意**：该技能本身并不负责托管该服务。

## 与 arcgispro-cli 的关系

所需的输入数据 `project_snapshot` 是由开源的 ArcGIS Pro CLI (`arcgispro-cli`) 生成的 JSON 格式的数据。

**推荐的工作流程**：
1) 使用 `arcgispro-cli` 导出项目快照/上下文数据（默认情况下，这些数据是经过处理的，不包含原始数据）。
2) 将生成的 JSON 数据发送到该付费端点，以获取一份确定性的风险报告。
3) 根据报告的结果来决定是否继续执行自动化操作（例如使用 ArcPy、GP 或 AGOL），以及首先需要修复哪些问题。

**职责划分**：
- 开源核心组件 (`arcgispro-cli`) 的职责是提供项目内容的详细信息。
- 该付费服务的职责是评估自动化操作的潜在风险，并说明原因。

## 端点信息
- **URL**：`POST https://api.x402layer.cc/e/esri-smells`

## 输入数据（必需的 JSON 格式）：
```json
{
  "project_snapshot": { },
  "constraints": {
    "target": "arcpy" | "geoprocessing" | "agol",
    "deployment": "desktop" | "server",
    "max_runtime_sec": 300
  }
}
```

## 输出数据（必包含的字段**：
- `summary`：风险检测的总结信息。
- `risk_score`：风险评分（0.0–1.0）。
- `issues[]`：存在的问题列表。
- `flags`：相关标志信息。
- `version`：版本信息。
- `requestHash`：请求的唯一标识符。

## 技术特性**：
- **无状态**：每次请求都会独立处理，不会保留任何状态信息。
- **无外部网络调用**：所有网络请求都仅限于该付费端点本身。
- **输入相同则输出相同**：相同的输入数据会始终产生相同的输出结果。
- **可缓存**：可以根据 `requestHash` 对输出结果进行缓存。

## 定价信息：
- 费用模式：按请求计费，使用 Base 作为支付方式，费用为 x402。
- **单价**：每次请求的费用为 **0.001 美元**。

## 调用方法（Python 辅助函数）：
1) 安装所需的依赖库：
```bash
pip install -r {baseDir}/requirements.txt
```

2) 设置钱包环境（用于支付）：
```bash
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."
```

3) 调用端点：
```bash
python {baseDir}/scripts/call_smells.py path/to/project_snapshot.json
```

### 其他说明**：
- 该脚本实现了 x402 HTTP 402 挑战机制，并通过 `X-Payment` 头部字段进行重试处理。
- 如果端点无法访问或支付失败，脚本会原样显示错误信息。
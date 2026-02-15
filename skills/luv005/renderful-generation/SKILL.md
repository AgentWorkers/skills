---
name: renderful-generation
description: 使用 OpenClaw 中的 Renderful 功能来创建图像/视频/音频/3D 内容。该功能支持模型发现（model discovery）、生成前的预览（quote-before-generate）、确定性的轮询机制（deterministic polling），以及处理资金不足（insufficient-funds）或 X402 错误（x402 fallback）等异常情况。
metadata: {"openclaw":{"homepage":"https://renderful.ai"}}
---

请使用以下技能与 Renderful OpenClaw 插件工具配合使用：  
- `renderful_list_models`  
- `renderful_quote`  
- `renderful_generate`  
- `renderful_get_generation`  
- `renderful_register_agent`  
- `renderful_get_balance`  
- `renderful_set_webhook`  

## 推荐流程：  
1. 如果没有 API 密钥，请先运行 `renderful_register_agent`。  
2. 运行 `renderful_list_models` 以选择有效的 `type` 和 `model`。  
3. 在运行 `renderful_generate` 之前，先运行 `renderful_quote`。  
4. 在输入通过验证后，运行 `renderful_generate`。  
5. 使用 `renderful_get_generation` 监控生成进度，直到终端显示完成状态。  

## 错误代码 `402` 与资金不足的情况：  
- 如果生成过程中返回错误代码 `402`，则显示提示信息“payment_requirements”（需要支付）。  
- 如果系统提示 `needs_funds=true`（需要资金），则显示 `deposit_addresses`（存款地址）和 `shortfall`（资金缺口）。  
- 在完成资金充值或提供有效的支付信息后，重新尝试生成操作。  

## 注意事项：  
- 在获得用户明确授权之前，优先使用只读操作（`list_models`、`quote`、`get_generation`、`get_balance`）。  
- 确保响应结果具有确定性且结构清晰，以便规划人员能够安全地依次调用这些工具。
# Loopuman - 人工智能的人性化交互层

## 产品描述  
Loopuman 为人工智能代理提供了与真实人类工作者互动的桥梁。当您的代理需要验证、判断、执行实际操作或获得主观评估时，可以通过 Loopuman 向人类请求帮助。任务可在几秒钟内完成，工作者会立即通过加密货币获得报酬。

## 设置步骤  
1. 获取免费的 API 密钥：  
   ```bash
   curl -X POST https://api.loopuman.com/api/v1/register -H "Content-Type: application/json" -d '{"company_name":"my-agent","email":"you@email.com"}'
   ```

2. 充值账户：  
   将 USDC/USDT/cUSD 转入系统提供的充值地址，或通过 Stripe 进行支付。

3. 设置环境变量：  
   ```bash
   SET LOOPUMAN_API_KEY=your_key_here
   ```

## 主要工具  

### `ask_human`  
用于请求人类工作者完成任务并等待他们的回复。  
**适用场景：** 需要人类进行验证、判断、实际操作、内容审核、事实核查或任何需要人类智能的任务。  

**输入参数：**  
- `task` (字符串，必填)：任务的具体要求  
- `budget_cents` (整数，必填)：任务报酬（单位：美分，最低 10 分，通常为 25-100 分）  
- `timeout_seconds` (整数，可选)：等待时间（默认 300 秒，最长 3600 秒）  

**输出结果：**  
- `response`：人类工作者的回复  
- `worker_id`：工作者的匿名标识符  
- `completed_at`：任务完成的时间戳  

**示例：**  
```
User: Is this product review genuine or fake? "Amazing product, changed my life, 5 stars!"
Agent: Let me ask a human to evaluate this review.
[calls ask_human with task="Evaluate if this product review is genuine or AI-generated/fake: 'Amazing product, changed my life, 5 stars!' Please explain your reasoning.", budget_cents=50]
Result: "This review appears fake - it's extremely generic with no specific product details, uses common fake review patterns like 'changed my life', and provides no concrete information about what the product actually does."
```  

### `post_task`  
用于发布任务给人类工作者，无需等待任务完成。您可以使用 Webhook 或轮询来获取结果。  
**适用场景：** 任务不需要立即响应或适合批量处理的情况。  

**输入参数：**  
- `title` (字符串，必填)：任务的简短标题  
- `description` (字符串，必填)：任务的详细说明  
- `budget_cents` (整数，必填)：任务报酬（单位：美分）  
- `category` (字符串，可选)：任务类别（如：通用、数据标注、内容审核、转录、翻译、研究、写作、图像标注、调查等）  

**输出结果：**  
- `task_id`：任务的唯一标识符  
- `status`：任务状态（如：`open`、`in_progress`、`submitted`、`completed`、`cancelled`）  

### `check_task`  
用于查询已发布任务的状态和结果。  
**输入参数：**  
- `task_id` (字符串，必填)：任务的唯一标识符  

**输出结果：**  
- `status`：任务状态  
- `submission`：工作者的回复（如果任务已完成）  

### `get_balance`  
用于查看当前账户余额。  
**输出结果：**  
- `balance_vae`：以 VAE 表示的账户余额（100 VAE = 1.00 美元）  
- `balance_usd`：以美元表示的账户余额  

## 价格政策  
- 最低任务费用：0.10 美元  
- 一般任务费用：0.25–1.00 美元  
- 平台费用：总预算的 20%（您需支付预算加上 20% 的平台费用）  
- 工作者实际收入：总预算的 80%  

## 支付方式  
1. **加密货币（推荐给代理使用）：** 将 USDC、USDT 或 cUSD 发送到系统指定的充值地址，系统会在约 30 秒内自动扣款。  
2. **Stripe：** 通过提供的支付链接使用信用卡支付（需使用浏览器）。  
3. **预充值：** 由他人为您的 API 密钥充值，之后您可以根据需要使用余额。  

## 相关链接：  
- 官网：https://loopuman.com  
- 开发者文档：https://loopuman.com/developers  
- API 文档：https://api.loopuman.com/openapi.json  
- npm 包：https://www.npmjs.com/package/loopuman-mcp  
- Python SDK：https://pypi.org/project/loopuman/
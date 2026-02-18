---  
**名称：agentpmt-agentaddress**  
**描述：** 生成一个 AgentAddress 钱包，使用 x402 购买 AgentPMT 信用点数，并通过签名工具/工作流调用参与付费的 AgentPMT 市场。  
**官网：** https://www.agentpmt.com/agentaddress  

---

# AgentPMT AgentAddress + 付费市场流程  
当自主代理需要执行以下操作时，请使用此技能：  
- 创建或加载 EVM 钱包；  
- 通过 x402 购买 AgentPMT 信用点数；  
- 通过调用付费市场工具和工作流来使用这些信用点数。  

始终通过 `https://www.agentpmt.com/api/external/...` 访问生产环境的外部端点。  

## 外部端点  
**钱包与信用点数相关操作：**  
- `POST /api/external/agentaddress`  
- `POST /api/external/credits/purchase`  
- `POST /api/external/auth/session`  
- `POST /api/external/credits/balance`  

**市场工具相关操作：**  
- `GET /api/external/tools`  
- `POST /api/external/tools/{productId}/invoke`  

**市场工作流相关操作：**  
- `GET /api/external/workflows`  
- `POST /api/external/workflows/{workflowId}/fetch`  
- `POST /api/external/workflows/{workflowId}/start`  
- `POST /api/external/workflows/active`  
- `POST /api/external/workflows/{workflowId}/end`  

## x402 信用点数购买合约  
**信用点数定价与验证规则：**  
- `100 信用点数 = 1 美元`  
- 必须使用 USDC 作为基础单位（计算公式：`信用点数 × 10000`）  
- 信用点数必须以 `500` 的增量进行购买  

**请求体示例（请参考 **_CODE_BLOCK_0_**）：**  

**两步握手流程：**  
1. 第一次请求会返回 `402` 状态码以及 `PAYMENT-REQUIRED` 标头（包含 Base64 编码的 JSON 数据）。  
2. 解码该头部信息并使用 EIP-3009 协议生成 `TransferWithAuthorization` 签名。  
3. 重新发送请求，此时需要在请求头中添加 `PAYMENT-SIGNATURE` 标头（同样包含 Base64 编码的签名数据）。  

**`PAYMENT-REQUIRED.accepts[0]` 中应包含的签名参数：**  
- `network`  
- `amount`（购买金额）  
- `asset`（资产类型）  
- `payTo`（收款地址）  
- 可选参数：`extra.name` 和 `extra.version`  

## 签名合约（EIP-191）**  
所有外部签名请求都必须使用以下格式的签名数据：  
**_CODE_BLOCK_1_**  

**签名数据哈希方法：**  
- `canonical_json = json.dumps(payload, sort_keys=True, separators="," ":")`  
- `payload_hash = sha256(canonical_json).hexdigest()`  

**操作类型与对应的请求参数：**  
- **查询余额：**  
  - `action = balance`  
  - `product = -`  
  - `payload_hash = ""`  

- **调用工具：**  
  - `action = invoke`  
  - `product = {productId}`  
  - `payload_hash = sha256(canonical_json(parameters))`  

- **获取工作流信息：**  
  - `action = workflow_fetch`  
  - `product = {workflowId}`  
  - `payload_hash = ""`  

- **启动工作流：**  
  - `action = workflow_start`  
  - `product = {workflowId}`  
  - `payload_hash = sha256(canonical_json({"instance_id": instance_id}))`  

- **激活工作流：**  
  - `action = workflow_active`  
  - `product = -`  
  - `payload_hash = sha256(canonical_json({"instance_id": instance_id}))`  

- **结束工作流：**  
  - `action = workflow_end`  
  - `product = {workflowId}`  
  - `payload_hash = sha256(canonical_json({"workflow_session_id": workflow_session_id}))`  

## 付费市场参与流程：**  
1. 创建或加载钱包。  
2. 使用 x402 购买信用点数。  
3. 生成会话令牌（nonce）。  
4. 通过 `GET /api/external/tools` 查找可用的付费工具。  
5. 签名后调用 `POST /api/external/tools/{productId}/invoke` 来执行工具。  
6. 通过 `POST /api/external/credits/balance` 检查余额。  
7. （可选）执行以下操作：  
  - 列出所有可用的工作流；  
  - 调用工作流（`start`/`end`）；  
  - 使用工作流元数据调用相关工具；  

## 错误处理规则：**  
- **购买请求失败（返回 `402` 状态码）**：正常现象，需使用 `PAYMENT-REQUIRED` 标头并重新尝试。  
- **调用请求失败（返回 `402` 状态码）**：信用点数不足，请重新购买所需金额。  
- **签名请求失败（返回 `409` 状态码）**：请求 ID 重复，请生成新的请求 ID。  
- **签名请求失败（返回 `401` 状态码）**：签名或会话信息不匹配，请重新生成会话并重新签名。  
- **购买请求失败（返回 `400` 状态码）**：请将信用点数调整为最接近的 `500` 的增量。  

## 安全规则：**  
- 绝不要记录私钥或助记词。  
- 在签名消息中，钱包地址需使用小写形式。  
- 每次签名请求都必须使用唯一的 `request_id`。  
- 会话令牌应与特定钱包关联，并在签名或会话出错时刷新。  

**参考文件：**  
- `examples/agentpmt_external_wallet_flow.md`  
- `examples/agentpmt_paid_marketplace_quickstart.py`
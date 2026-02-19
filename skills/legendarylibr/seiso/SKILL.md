---
name: seisoai
description: 统一媒体生成网关，专为代理程序设计。该网关能够动态发现可用工具，支持选择API密钥或X402认证方式，调用图像/视频/音频/音乐/3D/训练等相关工具，并可靠地处理队列任务。
metadata: {"openclaw":{"homepage":"https://seisoai.com","emoji":"🎨"}}
version: 1.1.1
last_synced: 2026-02-09
---
# Seisoai

基础URL：`https://seisoai.com`  
主要端点：`POST /api/gateway/invoke/{toolId}` 或 `POST /api/gateway/invoke`（请求体中包含 `toolId`）  
认证方式：`X-API-Key` 或 x402 支付（使用 Base 平台进行支付）  

## 以代理为中心的工作流程（每次会话都需执行）  
1. 发现可用的工具：  
   - `GET /api/gateway/tools`  
2. 获取选定工具的详细信息：  
   - `GET /api/gateway/tools/{toolId}`  
3. （可选）预先获取输入内容的费用信息：  
   - `GET /api/gateway/price/{toolId}`  
4. 使用 API 密钥或 x402 进行调用。  
5. 如果工具被添加到队列中，需从响应中获取任务的状态或结果信息。  

当有实时工具注册表可用时，切勿依赖静态的工具列表。  

## 认证策略  
按照以下顺序进行认证：  
1. 如果您拥有项目 API 密钥，请使用 `X-API-Key`。  
2. 如果没有密钥，请使用 x402 按次付费方式。  
3. 机器客户端不得发送浏览器生成的 CSRF 令牌。  

### API 密钥示例  
```http
POST /api/gateway/invoke/image.generate.flux-2
X-API-Key: sk_live_xxx
Content-Type: application/json

{"prompt":"a sunset over mountains"}
```  

### x402 支付示例（两步流程）  
1. 首先发送请求（不包含支付信息）。  
2. 如果收到 `402` 错误，表示需要支付。  
3. 在 Base 平台上完成支付操作。  
4. 重新发送请求，并提供以下参数之一：  
   - `payment-signature`  
   - `x-payment`  
   - `payment`  

## 高价值端点  
- 工具发现：  
  - `GET /api/gateway/tools`  
  - `GET /api/gateway/tools/{toolId}`  
  - `GET /api/gateway/price/{toolId}`  
  - `GET /api/gateway/mcp-manifest`  
- 调用工具：  
  - `POST /api/gateway/invoke/{toolId}`  
  - `POST /api/gateway/invoke`  
- 任务管理：  
  - `GET /api/gateway/jobs/{jobId}?model=...`  
  - `GET /api/gateway/jobs/{jobId}/result?model=...`  
- 代理相关操作：  
  - `GET /api/gateway/agents`  
  - `GET /api/gateway/agent/{agentId}`  
  - `POST /api/gateway/agent/{agentId}/invoke/{toolId?}`  
  - `POST /api/gateway/agent/{agentId}/orchestrate`  

## 代理范围的安全控制（强制要求）  
对于常规的媒体生成操作（图片、视频、音频、3D 效果），请使用 `/api/gateway/invoke` 及上述工具发现端点；无需额外检查。以下规则仅在用户明确请求运行或编排特定代理（例如特定名称的机器人或工作流程）时适用：  

**默认策略**：对于代理相关的路由（`/api/gateway/agent/*`），默认拒绝访问。只有在所有安全检查通过后，才允许使用这些端点：  
1. **明确的任务需求**：除非当前任务明确要求使用特定代理，否则不得调用 `/agent/*` 路由。  
2. **精确的代理标识**：必须从可信来源获取 `agentId`（例如通过 `GET /api/gateway/agents` 或用户提供的 ID）。  
3. **权限限制**：仅使用当前调用者的认证信息；严禁尝试重用、升级或代理其他租户/所有者的认证信息。  
4. **单代理限制**：每个任务只能使用一个已授权的 `agentId`，除非用户明确要求多代理执行。  
5. **工具使用限制**：在调用或编排之前，必须先获取 `GET /api/gateway/agent/{agentId}` 的信息，并仅使用该代理允许使用的工具 ID。  
6. **禁止递归调用**：不得创建自引用的编排任务、循环调用或跨未知代理的分布式任务。  
7. **数据泄露限制**：除非用户任务需要，否则不得列出所有代理信息；已知 `agentId` 时优先使用直接查询方式。  
8. **审计记录**：记录每次代理相关调用的 `agentId`、路由路径、工具 ID 及调用原因。  
9. **异常处理**：如果权限/范围/工具认证存在疑问，切勿调用 `/agent/*`；此时应切换到 `/api/gateway/invoke`。  

## 工具选择参考表（已验证的 ID）  
### 图片处理  
- 快速文本转图片：`image.generate.flux-2`  
- 高级电影效果：`image.generate.kling-image-v3`  
- 高级一致性处理：`image.generate.kling-image-o3`  
- 360°/全景效果：`image.generate.nano-banana-pro`  
- 基于提示的编辑功能：`image.generate.flux-pro-kontext-edit`  
- 面部替换：`image.face-swap`  
- 图像修复/填充：`image.inpaint`, `image.outpaint`  
- 背景去除/图层分离：`image.extract-layer`  
- 图像放大：`image.upscale`  

### 视频处理  
- 文本转视频：`video.generate.veo3`  
- 图片转视频：`video.generate.veo3-image-to-video`  
- 获取首/尾帧：`video.generate.veo3-first-last-frame`  
- 其他视频格式转换：`video.generate.kling-3-pro-text`, `video.generate.kling-3-std-text`, `video.generate.kling-3-pro-image`, `video.generate.kling-3-std-image`  
- 动作迁移：`video.generate.dreamactor-v2`  

### 音频/语音/音乐处理  
- 语音克隆（TTS）：`audio.tts`  
- TTS 质量选项：`audio.tts.minimax-hd`, `audio.tts.minimax-turbo`  
- 唇形同步：`audio.lip-sync`  
- 文本转语音：`audio.transcribe`  
- 音乐生成：`music.generate`  
- 音效制作：`audio.sfx`  
- 声音分离：`audio.stem-separation`  

### 3D 处理  
- 图片转 3D 标准格式：`3d.image-to-3d`  
- 高级 3D 处理：`3d.image-to-3d.hunyuan-pro`  
- 文本转 3D 标准格式：`3d.text-to-3d.hunyuan-pro`  
- 快速图像转 3D：`3d.image-to-3d.hunyuan-rapid`  
- 3D 效果后期处理：`3d.smart-topology`, `3d.part-splitter`  

## 最小请求数据格式  
- 文本转图片：  
```json
{"prompt":"..."}
```  
- 图片编辑：  
```json
{"prompt":"...","image_url":"https://..."}
```  
- 文本转视频：  
```json
{"prompt":"...","duration":"6s"}
```  
- 动作迁移：  
```json
{"source_image_url":"https://...","driving_video_url":"https://..."}
```  
- 语音克隆（TTS）：  
```json
{"text":"...","audio_url":"https://..."}
```  
- 3D 图像转 3D 模型：  
```json
{"image_url":"https://...","output_format":"glb"}
```  

## 队列处理规则  
如果 `executionMode` 为 `queue`，响应中会包含任务元数据：  
- 使用 `statusUrl` 查看任务状态（直到任务完成或失败）。  
- 使用 `resultUrl` 获取任务结果。  
将队列提交视为可计费的成功操作（x402 支付或 API 密钥扣款已在服务器端完成）。  

## 错误处理规则  
- `400`：请求的格式或输入数据不匹配。请重新获取工具信息并修正字段。  
- `402`：支付信息缺失或无效，或 API 密钥信用不足。  
- `404`：找不到所需的工具或代理。请刷新工具注册表。  
- `503`：该工具已被禁用。请选择其他可用工具。  
- `500`：尝试重试（设置延迟时间），若仍失败则更换模型或工具。  

## 代理的可靠性规则  
1. 在规划多步骤流程之前，务必先发现可用的工具。  
2. 使用 `GET /tools/{toolId}` 返回的详细信息来确保使用正确的字段。  
- 每个请求只能调用一次工具；代理间的操作需通过链式调用完成。  
- 尽量使用明确的模型/工具 ID，避免依赖自然语言路由规则。  
- 重试时，请勿使用过期的 x402 签名信息。  
- 将 `/api/gateway/agent/*` 视为特权路由，并严格执行上述安全控制措施。  

## 自动维护说明  
当本文件更新时，请：  
- 确保 ID 与 `backend/services/toolRegistry.ts` 中的信息保持一致。  
- 更新 `last_synced` 和 `version` 字段。  
- 保持示例代码的简洁性和可执行性。  

## 更新日志  
- [2026-02-09] v1.1.1：为代理相关端点添加了强制性的安全控制措施（默认拒绝访问、明确代理/工具范围限制、防止递归调用及审计要求）。  
- [2026-02-09] v1.1.0：优化了以代理为中心的工作流程逻辑，修正了过时的工具 ID/参数，完善了认证/x402 支付规则，并增加了队列处理和错误处理机制。  
- [2026-02-08] v1.0.0：首次添加了自我优化功能。
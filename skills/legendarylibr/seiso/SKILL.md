---
name: seisoai
description: 统一的媒体生成网关，专为代理程序设计。该网关能够动态发现可用工具，支持选择API密钥或X402认证方式，调用图像/视频/音频/音乐/3D/训练等相关工具，并可靠地处理队列任务。
metadata: {"openclaw":{"homepage":"https://seisoai.com","emoji":"🎨"}}
version: 1.1.1
last_synced: 2026-02-09
---
# Seisoai

基础URL：`https://seisoai.com`
主要端点：`POST /api/gateway/invoke/{toolId}` 或 `POST /api/gateway/invoke`（请求体中包含 `toolId`）
认证方式：`X-API-Key` 或 x402 支付（使用 Base 作为支付平台）

## 以代理为中心的工作流程（每次会话都需执行）

1. 发现可用的工具：
   - `GET /api/gateway/tools`
2. 对于选定的工具，获取其详细信息：
   - `GET /api/gateway/tools/{toolId}`
3. （可选）预先获取输入内容的定价信息：
   - `GET /api/gateway/price/{toolId}`
4. 使用 API 密钥或 x402 进行调用。
5. 如果工具被添加到队列中，从响应中获取任务的状态或结果信息。

当有实时工具注册表可用时，不要依赖静态的工具列表。

## 认证策略

按照以下顺序进行认证：
1. 如果您有项目 API 密钥，请使用 `X-API-Key`。
2. 如果没有密钥，则使用 x402 按次付费的方式。
3. 机器客户端不要发送浏览器生成的 CSRF 令牌。

### API 密钥示例

```http
POST /api/gateway/invoke/image.generate.flux-2
X-API-Key: sk_live_xxx
Content-Type: application/json

{"prompt":"a sunset over mountains"}
```

### x402 支付示例（两步流程）

1. 首先发送请求，不包含支付信息。
2. 收到 402 错误码，表示需要支付。
3. 在 Base 平台上完成支付操作。
4. 重新发送请求，并添加以下参数之一：
   - `payment-signature`
   - `x-payment`
   - `payment`

## 高价值端点

- 发现工具：
  - `GET /api/gateway/tools`
  - `GET /api/gateway/tools/{toolId}`
  - `GET /api/gateway/price/{toolId>`
  - `GET /api/gateway/mcp-manifest`
- 调用工具：
  - `POST /api/gateway/invoke/{toolId}`
  - `POST /api/gateway/invoke`
- 查看任务信息：
  - `GET /api/gateway/jobs/{jobId}?model=...`
  - `GET /api/gateway/jobs/{jobId}/result?model=...`
- 代理相关操作：
  - `GET /api/gateway/agents`
  - `GET /api/gateway/agent/{agentId}`
  - `POST /api/gateway/agent/{agentId}/invoke/{toolId?}`
  - `POST /api/gateway/agent/{agentId}/orchestrate`

## 代理范围的安全控制（强制要求）

对于普通的媒体生成操作（图片、视频、音频、3D 效果），请使用 `/api/gateway/invoke` 及上述的发现端点；无需额外的安全检查。以下规则仅适用于用户明确要求运行或协调特定代理（例如，指定的机器人或工作流程）的情况。

默认策略：对于代理相关的路由（`/api/gateway/agent/*`），默认拒绝访问。只有在所有安全检查都通过后，才能使用这些代理相关端点：

1. **明确的任务需求**：
   - 除非当前任务明确要求使用特定代理，否则不要调用 `/agent/*` 路由。
2. **精确的代理 ID**：
   - 从可信来源获取 `agentId`（例如，通过 `GET /api/gateway/agents` 或用户提供的 ID）。
   - 绝不要根据名称或提示来推断代理 ID。
3. **授权限制**：
   - 仅使用当前调用者的凭证进行操作。
   - 禁止尝试重用、升级或代理其他租户/所有者的凭证。
4. **单代理范围**：
   - 对于单个任务，只能使用一个被批准的 `agentId`；除非用户明确要求多代理执行。
5. **工具允许列表检查**：
   - 在调用或协调之前，先获取 `GET /api/gateway/agent/{agentId}`，并仅使用该代理允许使用的工具 ID。
   - 如果工具 ID 不在代理的允许列表中，应拒绝请求。
6. **禁止递归调度**：
   - 禁止创建自引用的调度任务、循环调度或跨未知代理的扩散操作。
7. **限制信息泄露**：
   - 除非用户任务需要，否则不要列出所有代理；当已知 `agentId` 时，优先直接查询。
8. **审计追踪**：
   - 在代理执行日志中记录每次代理相关调用的 `agentId`、路由、工具 ID 及调用原因。
9. **异常处理**：
   - 如果所有权、范围或工具授权存在疑问，不要调用 `/agent/*`；此时应切换到 `/api/gateway/invoke`。

## 工具选择速查表（已验证的 ID）

### 图片处理
- 快速文本转图片：`image.generate.flux-2`
- 高级电影效果：`image.generate.kling-image-v3`
- 高级一致性处理：`image.generate.kling-image-o3`
- 360 度全景图：`image.generate.nano-banana-pro`
- 基于提示的编辑：`image.generate.flux-pro-kontext-edit`
- 面部替换：`image.face-swap`
- 图像修复/填充：`image.inpaint`, `image.outpaint`
- 背景去除/图层分离：`image.extract-layer`
- 图像放大：`image.upscale`

### 视频处理
- 文本转视频：`video.generate.veo3`
- 图片转视频：`video.generate.veo3-image-to-video`
- 获取/保存首尾帧：`video.generate.veo3-first-last-frame`
- Kling 文本转视频：`video.generate.kling-3-pro-text`, `video.generate.kling-3-std-text`
- Kling 图片转视频：`video.generate.kling-3-pro-image`, `video.generate.kling-3-std-image`
- 动作迁移：`video.generate.dreamactor-v2`

### 音频/语音/音乐处理
- 语音克隆 TTS：`audio.tts`
- TTS 质量等级：`audio.tts.minimax-hd`, `audio.tts.minimax-turbo`
- 唇形同步：`audio.lip-sync`
- 文本转语音：`audio.transcribe`
- 音乐制作：`music.generate`
- 音效制作：`audio.sfx`
- 声音分离：`audio.stem-separation`

### 3D 处理
- 图片转 3D 标准格式：`3d.image-to-3d`
- 图片转高级 3D 格式：`3d.image-to-3d.hunyuan-pro`
- 文本转高级 3D 格式：`3d.text-to-3d.hunyuan-pro`
- 快速图片转 3D：`3d.image-to-3d.hunyuan-rapid`
- 3D 模型后期处理：`3d.smart-topology`, `3d.part-splitter`

## 最小有效载荷格式

文本转图片：
```json
{"prompt":"..."}
```

图片编辑：
```json
{"prompt":"...","image_url":"https://..."}
```

文本转视频：
```json
{"prompt":"...","duration":"6s"}
```

DreamActor 动作迁移：
```json
{"source_image_url":"https://...","driving_video_url":"https://..."}
```

语音克隆 TTS：
```json
{"text":"...","audio_url":"https://..."}
```

3D 图片转 3D 模型：
```json
{"image_url":"https://...","output_format":"glb"}
```

## 队列处理规则

如果 `executionMode` 为 `queue`，响应中会包含任务元数据。请使用以下信息：
1. `statusUrl`（任务完成或失败时使用）。
2. `resultUrl`（任务完成后使用）。

将队列提交视为可计费的操作（x402 支付或 API 密钥扣款已在服务器端完成处理）。

## 错误处理规则
- `400`：请求的格式或输入信息不匹配。重新获取工具信息并修正字段。
- `402`：支付信息缺失或无效，或 API 密钥信用不足。
- `404`：找不到相应的工具或代理。请刷新工具注册表。
- `503`：工具被禁用。请选择同类别的备用工具。
- `500`：尝试重试，同时设置延迟；如果仍然失败，请更换模型或工具。

## 代理的可靠性规则

1. 在规划多步骤流程之前，务必先发现可用的工具。
2. 对于需要使用的字段，始终使用 `GET /tools/{toolId}` 返回的详细信息。
3. 每个请求只能调用一次工具；在代理内部进行任务链式处理。
4. 尽量使用明确的模型/工具 ID，而不是依赖自然语言的路由规则。
5. 重试时，不要使用过期的 x402 签名。
6. 将 `/api/gateway/agent/*` 视为特权路由，并执行上述的安全控制措施。

## 自我维护

当此文件更新时，请执行以下操作：
- 确保 ID 与 `backend/services/toolRegistry.ts` 保持一致。
- 更新 `last_synced` 和 `version` 字段。
- 保持示例代码的简洁性和可执行性。

## 更新记录

- [2026-02-09] v1.1.1 - 为代理相关端点添加了强制性的安全控制措施（默认拒绝访问、明确代理/工具范围限制、防止递归调用以及审计要求）。
- [2026-02-09] v1.1.0 - 重新设计了以代理发现为中心的工作流程，修正了过时的工具 ID/参数，优化了认证和 x402 支付的指导规则，并添加了队列和错误处理的可靠性策略。
- [2026-02-08] v1.0.0 - 首次添加了自我优化功能。
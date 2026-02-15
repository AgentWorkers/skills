---
name: saa-agent
description: 该功能允许AI代理通过命令行接口，使用“Character Select Stand Alone App (SAA)”的图像生成后端来生成图像。
license: MIT
---

# SAA CLI 工具

这是一个命令行接口，用于通过 WebSocket 连接与 Character Select Stand Alone App (SAA) 进行交互。该工具支持 ComfyUI 和 WebUI 两种后端，用于 AI 图像生成。

## 前提条件

**重要提示：** 在使用此工具之前，请务必确认以下内容：
1. SAA 后端正在运行，并且版本高于 2.4.0。
2. SAAC (SAA 客户端) 功能已启用。
3. WebSocket 地址已获取。
4. 部分 Mac 用户使用 `python3` 而不是 `python` 来运行 Python 3.x。

有关 SAA 的设置详情，请访问 [项目仓库](https://github.com/mirabarukaso/character_select_stand_alone_app)。

## 基本用法

该工具只需要最少的参数即可正常使用。以下示例展示了标准的使用方式：

### 带有模型选择的简单命令（适用于大多数情况）

```bash
python saa-agent.py \
  --ws-address "user_provided_ws_address" \
  --model "waiIllustriousSDXL_v160.safetensors" \
  --positive "your detailed prompt here" \
  --negative "low quality, blurry, bad anatomy"
```

### 地区化提示（分割组合）

```bash
python saa-agent.py \
  --ws-address "user_provided_ws_address" \
  --model "waiIllustriousSDXL_v160.safetensors" \
  --regional \
  --positive-left "1girl, warrior, red armor" \
  --positive-right "1boy, mage, blue robes"
```

### 更多示例
更多使用示例和参数说明请参见：

```bash
python saa-agent.py
python saa-agent.py --help
```

## 关键参数

### 必需参数
- `--ws-address`：WebSocket 地址（从用户处获取）
- `--positive`：主提示选项；或结合 `--positive-left` 和 `--positive-right` 使用 `--regional` 模式

### 常见可修改参数
- `--model`：更改检查点模型（默认值：`waiIllustriousSDXL_v160.safetensors`）
- `--negative`：指定不需要的元素
- `--width` / `--height`：图像尺寸（默认值：1024x1360）
- `--steps`：采样步数（默认值：28）
- `--seed`：设置特定种子值；或使用 -1 表示随机生成

### 高级参数（谨慎使用）
- `--cfg`：CFG 缩放比例（默认值：7.0）
- `--sampler`：采样算法（默认值：`euler_ancestral`）
- `--scheduler`：调度器类型（默认值：`normal`）

## 重要提示

### HiResFix 警告

**除非用户明确要求，否则** **不要使用 `--hifix`。**

`--hifix` 会显著增加生成时间，并消耗大量 GPU 资源。仅在以下情况下启用：
- 用户明确请求高分辨率放大。
- 用户确认其 GPU 能够承受额外的负载。

## 后端繁忙状态

如果生成过程中出现以下错误之一：

```
Error: WebUI is busy, cannot run new generation, please try again later.
Error: ComfyUI is busy, cannot run new generation, please try again later.
```

**应对措施：**
1. **不要** 自动重试生成。
2. 通知用户：“SAA 后端当前繁忙。这可能是另一个进程正在生成图像，或者后端因之前的错误而被锁定。”
3. 建议用户：“请等待 20-60 秒后再尝试。”
4. 允许用户手动重试。

**不要** 连续多次重试，因为这可能会加重后端的负担。

### Skeleton Key 的使用

`--skeleton-key` 参数可以强制解锁后端的原子锁。

**使用场景：**
- 用户确认没有其他进程正在使用后端。
- 尽管等待后端仍未响应。
- 用户明确要求解锁。

**使用方法：**

```bash
python saa-agent.py \
  --ws-address "user_provided_ws_address" \
  --skeleton-key \
  --positive "test prompt"
```

**注意事项：**
1. **在使用 `--skeleton-key` 之前** **务必** 获得用户确认。
2. **每个用户请求** **仅使用一次**。
3. 向用户说明该参数会强制终止所有锁定。

示例对话：
```
AI: "The backend appears to be locked. Would you like me to use the skeleton key to force unlock it? This will terminate any existing locks."
User: "Yes, please unlock it."
AI: [proceeds to run command with --skeleton-key]
```

## 参数默认值

如有疑问，请使用以下默认值，它们适用于大多数情况：
- 模型：`waiIllustriousSDXL_v160.safetensors`
- 尺寸：1024x1360
- CFG：7.0
- 采样步数：28
- 采样算法：`euler_ancestral`
- 调度器：`normal`
- 种子值：-1（随机生成）

## 输出处理

默认情况下，图像会被保存为 `generated_image.png`。您也可以指定自定义的输出路径：

```bash
--output "custom_filename.png"
```

对于程序化处理，可以使用 base64 格式输出：

```bash
--base64
```

这种方式会将 base64 编码的图像数据直接输出到标准输出（stdout），而不是保存到文件中。

## 示例工作流程

1. 用户请求：“生成一个蓝色长发的动漫女孩。”
2. AI 执行生成任务：
```bash
python saa-agent.py \
  --ws-address "user_ws_address" \
  --positive "1girl, long hair, blue hair, anime style, detailed" \
  --negative "low quality, blurry, bad anatomy"
```

3. 如果出现后端繁忙错误：
   - 通知用户。
   - 等待用户重新尝试。
4. 如果生成成功：
   - 确认图像已生成。
   - 提供图像文件路径（如适用）。

## 常见错误及避免方法

1. **除非用户明确要求，否则不要使用 `--hifix`**。
2. **后端繁忙时不要自动重试**。
3. **未经用户许可，不要使用 `--skeleton-key`**。
4. **不要添加过多的参数**——除非用户特别要求，否则默认值已经调优得很好。
5. **不要假设后端已准备好**——使用前务必先确认。

## 错误代码

- 出口代码 0：成功
- 出口代码 1：连接错误（检查后端是否正在运行）
- 出口代码 2：认证错误（检查凭据）
- 出口代码 3：生成错误（检查参数）
- 出口代码 4：超时（后端可能过载）
- 出口代码 5：参数无效（检查命令语法）

## 最佳实践

1. 如果需要，从带有模型选择的简单参数开始使用。
2. 首次使用时询问用户的 WebSocket 地址。
3. 灵活处理后端繁忙的情况——不要频繁重试。
4. 调试问题时使用 `--verbose` 标志。
5. 尊重 `skeleton key` 的作用——它是一个强大的强制解锁工具。

## 本技能的 AI 代理指南

这些规则有助于保持生成的透明度和用户的控制权：

1. **命令执行与用户通知**  
   默认情况下，直接执行命令，无需用户确认。  
   仅在以下情况下显示完整命令并请求用户批准：  
   - 用户明确要求先查看命令内容。  
   - 操作涉及敏感或高影响的参数。  
   - 代理认为显示命令是必要的。  

   示例（需要披露命令内容时）：  
    ```
    python3 saa-agent.py --ws-address "wss://..." --username "..." --password "..." --positive "[prompt]" --negative "[prompt]" --output "[path]" [--verbose]
    ```

2. **--verbose 标志**  
   默认情况下不使用。  
   在以下情况下自动启用或推荐使用：  
   - 任务失败且需要调试时。  
   - 用户特别请求详细日志或种子值。  

3. **结果报告**  
   完成后，向用户提供简短的结果总结，包括：  
   - 成功/失败状态。  
   - 正面/负面提示内容（或相关总结）。  
   - 种子值（如果有的话）。  
   - 输出路径。  

   示例：  
    ```
    Generation completed
    • Positive: [...]
    • Negative: [...]
    • Seed: 123456789
    • Output: [path]
    ```  
   除非用户明确要求静默或简化的反馈，否则始终报告详细结果。  
   即使在静默模式下，也必须报告错误。

4. **错误处理**  
   - 失败时：尝试使用 `--verbose` 重试一次以收集诊断信息。  
   清晰地传达主要错误原因。  
   不要无限次重试；如果需要，尝试一次后等待用户决定。
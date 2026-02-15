---
name: doubleword-batches
description: 使用 Doubleword API (api.doubleword.ai) 创建和管理批量推理任务。适用于以下场景：  
(1) 批量处理多个 AI 请求；  
(2) 提交 JSONL 格式的文件以进行异步推理；  
(3) 监控批量任务的进度并获取结果；  
(4) 与 OpenAI 兼容的批量接口进行交互；  
(5) 处理不需要立即响应的大规模推理任务；  
(6) 批量调用工具或使用结构化输出；  
(7) 使用自动批处理工具（autobatcher）自动执行 API 调用。
---

# 双词批量推理

使用Doubleword的批量API异步处理多个AI推理请求，具有高吞吐量和低成本的特点。

## 先决条件

在提交批量请求之前，您需要：
1. **Doubleword账户** - 在https://app.doubleword.ai/注册
2. **API密钥** - 在仪表板的API密钥部分创建一个
3. **账户信用额度** - 添加信用额度以处理请求（请参见下面的价格信息）

## 何时使用批量处理

批量处理适用于以下情况：
- 可以同时运行的多个独立请求
- 不需要立即响应的工作负载
- 如果单独发送会超出速率限制的大量请求
- 对成本敏感的工作负载（24小时窗口比实时请求便宜50-60%）
- 大规模工具调用和结构化输出生成

## 可用模型及定价

定价按每100万个令牌（输入/输出）计算：

**Qwen3-VL-30B-A3B-Instruct-FP8**（中型模型）：
- 实时SLA：$0.16 / $0.80
- 1小时SLA：$0.07 / $0.30（便宜56%）
- 24小时SLA：$0.05 / $0.20（便宜69%）

**Qwen3-VL-235B-A22B-Instruct-FP8**（旗舰模型）：
- 实时SLA：$0.60 / $1.20
- 1小时SLA：$0.15 / $0.55（便宜75%）
- 24小时SLA：$0.10 / $0.40（便宜83%）
- 支持最多262K个令牌，每次请求最多16K个新令牌

**成本估算：** 在提交之前，将文件上传到Doubleword控制台以预览费用。

## 快速入门

有两种方式提交批量请求：

**通过API：**
1. 创建一个包含请求的JSONL文件
2. 上传文件以获取文件ID
3. 使用文件ID创建批次
4. 轮询状态直到完成
5. 从output_file_id下载结果

**通过Web控制台：**
1. 访问https://app.doubleword.ai/的Batches部分
2. 上传JSONL文件
3. 配置批次设置（模型、完成时间窗口）
4. 在实时仪表板中监控进度
5. 等待结果准备好后下载

## 工作流程

### 第1步：创建批次请求文件

创建一个`.jsonl`文件，其中每一行都包含一个完整的、有效的JSON对象，并且对象内部没有换行符：

```json
{"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "anthropic/claude-3-5-sonnet", "messages": [{"role": "user", "content": "What is 2+2?"}]}}
{"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "anthropic/claude-3-5-sonnet", "messages": [{"role": "user", "content": "What is the capital of France?"}]}}
```

**每行所需的字段：**
- `custom_id`：唯一标识符（最多64个字符） - 使用描述性ID，如`"user-123-question-5"`以便于结果映射
- `method`：始终为`"POST"`
- `url`：API端点 - `"/v1/chat/completions"`或`"/v1/embeddings"`
- `body`：包含`model`和`messages`的标准API请求

**可选的body参数：**
- `temperature`：0-2（默认值：1.0）
- `max_tokens`：最大响应令牌数
- `top_p`：Nucleus采样参数
- `stop`：停止序列
- `tools`：工具调用定义（请参见工具调用部分）
- `response_format`：结构化输出的JSON格式（请参见结构化输出部分）

**文件要求：**
- 最大大小：200MB
- 格式：仅支持JSONL（JSON行 - 以换行符分隔的JSON）
- 每一行都必须是有效的JSON，内部不能有换行符
- 不允许重复的`custom_id`值
- 如有必要，可以将大型批次拆分为多个文件

**常见错误：**
- JSON对象内部有换行符（会导致解析错误）
- JSON语法无效
- `custom_id`值重复

**辅助脚本：**
使用`scripts/create_batch_file.py`来程序化生成JSONL文件：

```bash
python scripts/create_batch_file.py output.jsonl
```

修改脚本中的`requests`列表以生成您的特定批次请求。

### 第2步：上传文件

**通过API：**
```bash
curl https://api.doubleword.ai/v1/files \
  -H "Authorization: Bearer $DOUBLEWORD_API_KEY" \
  -F purpose="batch" \
  -F file="@batch_requests.jsonl"
```

**通过控制台：**
通过https://app.doubleword.ai/的Batches部分上传文件

响应中包含`id`字段 - 保存此文件ID以用于后续步骤。

### 第3步：创建批次

**通过API：**
```bash
curl https://api.doubleword.ai/v1/batches \
  -H "Authorization: Bearer $DOUBLEWORD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input_file_id": "file-abc123",
    "endpoint": "/v1/chat/completions",
    "completion_window": "24h"
  }'
```

**通过控制台：**
在Web界面中配置批次设置。

**参数：**
- `input_file_id`：上传步骤中的文件ID
- `endpoint`：API端点（`"/v1/chat/completions"`或`"/v1/embeddings"`)
- `completion_window`：根据紧急程度和预算选择：
  - `"24h"`：最佳价格，24小时内完成结果（通常更快）
  - `"1h"`：价格贵50%，1小时内完成结果（通常更快）
  - 实时：容量有限，成本最高（批量服务适用于异步处理）

响应中包含批次`id` - 保存此ID以用于状态轮询。

**提交之前，请验证：**
- 您有权访问指定的模型
- 您的API密钥是有效的
- 您有足够的账户信用额度

### 第4步：轮询状态

**通过API：**
```bash
curl https://api.doubleword.ai/v1/batches/batch-xyz789 \
  -H "Authorization: Bearer $DOUBLEWORD_API_KEY"
```

**通过控制台：**
在Batches仪表板中实时监控进度。

**状态进展：**
1. `validating` - 检查输入文件格式
2. `in_progress` - 处理请求中
3. `completed` - 所有请求已完成

**其他状态：**
- `failed` - 批次失败（请查看`error_file_id`）
- `expired` - 批次超时
- `cancelling`/`cancelled` - 批次已取消

**响应包括：**
- `output_file_id` - 在此处下载结果
- `error_file_id` - 失败的请求（如果有）
- `request_counts` - 总计/已完成/失败的请求数量

**轮询频率：** 在处理过程中每30-60秒检查一次。

**提前获取结果：** 在批次完全完成之前，可以通过`output_file_id`获取部分结果 - 请查看`X-Incomplete`头部。

### 第5步：下载结果

**通过API：**
```bash
curl https://api.doubleword.ai/v1/files/file-output123/content \
  -H "Authorization: Bearer $DOUBLEWORD_API_KEY" \
  > results.jsonl
```

**通过控制台：**
直接从Batches仪表板下载结果。

**响应头部：**
- `X-Incomplete`：批次仍在处理中，更多结果即将发送
- `X-Last-Line: 45` - 部分下载的继续点

**输出格式（每行）：**
```json
{
  "id": "batch-req-abc",
  "custom_id": "request-1",
  "response": {
    "status_code": 200,
    "body": {
      "id": "chatcmpl-xyz",
      "choices": [{
        "message": {
          "role": "assistant",
          "content": "The answer is 4."
        }
      }]
    }
  }
}
```

**下载错误（如果有）：**
```bash
curl https://api.doubleword.ai/v1/files/file-error123/content \
  -H "Authorization: Bearer $DOUBLEWORD_API_KEY" \
  > errors.jsonl
```

**错误格式（每行）：**
```json
{
  "id": "batch-req-def",
  "custom_id": "request-2",
  "error": {
    "code": "invalid_request",
    "message": "Missing required parameter"
  }
}
```

## 批量中的工具调用

工具调用（函数调用）使模型能够智能地选择和使用外部工具。Doubleword完全兼容OpenAI。

**包含工具的示例批次请求：**
```json
{
  "custom_id": "tool-req-1",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "anthropic/claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "What's the weather in Paris?"}],
    "tools": [{
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string"}
          },
          "required": ["location"]
        }
      }
    }]
  }
}
```

**使用场景：**
- 大规模与API交互的代理
- 为多个查询获取实时信息
- 通过标准化的工具定义执行操作

## 批量中的结构化输出

结构化输出确保模型响应符合您的JSON格式，避免字段缺失或枚举值无效的问题。

**包含结构化输出的示例批次请求：**
```json
{
  "custom_id": "structured-req-1",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "anthropic/claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "Extract key info from: John Doe, 30 years old, lives in NYC"}],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "person_info",
        "schema": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "city": {"type": "string"}
          },
          "required": ["name", "age", "city"]
        }
      }
    }
  }
}
```

**优势：**
- 保证符合格式规范
- 没有缺失的必需字段
- 没有错误的枚举值
- 与OpenAI完美兼容

## autobatcher：自动批量处理

autobatcher是一个Python客户端，它可以自动将单个API调用转换为批量请求，无需修改代码即可降低成本。

**安装：**
```bash
pip install autobatcher
```

**工作原理：**
1. **收集阶段**：在一段时间内（默认：1秒）或达到批次大小阈值时累积请求
2. **批量提交**：收集到的请求一起提交
3. **结果轮询**：系统监控已完成的响应
4. **透明响应**：您的代码接收标准的ChatCompletion响应

**主要优势：** 通过自动批量处理，在使用熟悉的OpenAI接口编写正常异步代码时显著降低成本。

**文档：** https://github.com/doublewordai/autobatcher

## 其他操作

### 列出所有批次

**通过API：**
```bash
curl https://api.doubleword.ai/v1/batches?limit=10 \
  -H "Authorization: Bearer $DOUBLEWORD_API_KEY"
```

**通过控制台：**
在仪表板中查看所有批次。

### 取消批次

**通过API：**
```bash
curl https://api.doubleword.ai/v1/batches/batch-xyz789/cancel \
  -X POST \
  -H "Authorization: Bearer $DOUBLEWORD_API_KEY"
```

**通过控制台：**
在批次详情页面点击取消。

**注意：**
- 未处理的请求将被取消
- 已处理的结果仍然可以下载
- 仅对已完成的工作收费
- 无法取消已完成的批次

## 常见模式

### 处理结果

逐行解析JSONL输出：

```python
import json

with open('results.jsonl') as f:
    for line in f:
        result = json.loads(line)
        custom_id = result['custom_id']
        content = result['response']['body']['choices'][0]['message']['content']
        print(f"{custom_id}: {content}")
```

### 处理部分结果

检查未完成的批次并继续处理：

```python
import requests

response = requests.get(
    'https://api.doubleword.ai/v1/files/file-output123/content',
    headers={'Authorization': f'Bearer {api_key}'}
)

if response.headers.get('X-Incomplete') == 'true':
    last_line = int(response.headers.get('X-Last-Line', 0))
    print(f"Batch incomplete. Processed {last_line} requests so far.")
    # Continue polling and download again later
```

### 重试失败请求

从错误文件中提取失败请求并重新提交：

```python
import json

failed_ids = []
with open('errors.jsonl') as f:
    for line in f:
        error = json.loads(line)
        failed_ids.append(error['custom_id'])

print(f"Failed requests: {failed_ids}")
# Create new batch with only failed requests
```

### 处理工具调用

处理工具调用响应：

```python
import json

with open('results.jsonl') as f:
    for line in f:
        result = json.loads(line)
        message = result['response']['body']['choices'][0]['message']

        if message.get('tool_calls'):
            for tool_call in message['tool_calls']:
                print(f"Tool: {tool_call['function']['name']}")
                print(f"Args: {tool_call['function']['arguments']}")
```

## 最佳实践**

1. **使用描述性`custom_id`：** 在ID中包含上下文信息，以便于结果映射
   - 示例：`"user-123-question-5"`，`dataset-A-row-42`
   - 不建议的ID：`1`，`req1`
2. **在本地验证JSONL**：在上传之前确保每一行都是有效的JSON，并且没有内部换行符
3. **避免重复ID**：每个`custom_id`在批次中必须是唯一的
4. **分割大文件**：如果需要，将文件分割成多个文件，以保持200MB的限制
5. **选择合适的窗口**：选择`24h`以节省成本（便宜50-83%），仅在时间敏感时选择`1h`
6. **优雅地处理错误**：始终检查`error_file_id`并重试失败的请求
7. **监控请求计数**：通过`completed`/`total`比率跟踪进度
8. **保存文件ID**：存储batch_id、input_file_id、output_file_id以便后续查询
9. **使用成本估算器**：在提交大型批次之前，在控制台预览费用
10. **考虑使用autobatcher**：对于持续的工作负载，使用autobatcher自动将单个API调用批量处理

## 参考文档

有关完整的API详细信息，请参阅：
- **API参考**：`references/api_reference.md` - 完整的端点文档和格式
- **入门指南**：`references/getting_started.md` - 详细的设置和账户管理
- **定价详情**：`references/pricing.md` - 模型成本和SLA比较
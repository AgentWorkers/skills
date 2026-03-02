---
name: CAN ASK MCP
version: 1.9.0
description: "代理（Agent）与主控制面板（MCP）的集成：CAN总线能够标记所有通过该系统的信号。系统会对这些信号进行验证、命名，并在本地进行记录。"
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"❓","requires":{"bins":["sha256sum","date"]}}}
---
**CAN 1.9.0 版本** 主要致力于将时钟地址命名机制（Clock Address Naming）与人工智能代理（AI agents）集成，特别是那些使用模型上下文协议（Model Context Protocol, MCP）的代理。

CAN 为数据代理提供了一个本地化、可验证的命名和存储层，这些数据代理可以从工具中获取数据，且该层完全独立于传输层（transport layer）运行。

## 架构：CAN + MCP

- **MCP** 负责工具的连接和数据传输。
- **CAN** 负责数据的验证、命名以及通过 MCP 获取的数据的历史记录。

由于 CAN 仅执行本地操作（计算哈希值、添加时间戳并将数据写入文件），因此无需与 MCP 服务器进行任何集成；服务器甚至无需知道 CAN 的存在。

**工作流程：**
1. 代理从 MCP 工具请求数据。
2. 代理接收响应数据。
3. 代理在数据上添加 CAN 标记（包括时间、位置和数据内容）。
4. 代理将这些标记记录到本地的 `index.tsv` 文件中。

这样一来，代理无需重新查询服务器即可验证过去的工具输出结果，从而确保数据自获取以来未被篡改。

## 代理实现测试

1.9.0 版本要求代理开发者将 CAN 作为标准的日志记录和数据检索机制进行评估。以下测试展示了使用 CAN 的标准代理操作：

### 测试 1：基本标记功能
代理可以使用标准系统工具自动生成 CAN 数据条目的所需信息。

```bash
WHEN=$(date +%s%3N)
WHERE=$(sha256sum <<< "tool_output_string" | awk '{print $1}')
WHAT="tool_name.result"

echo -e "$WHEN\t$WHERE\t$WHAT" >> ~/.can/index.tsv
```

### 测试 2：本地验证
在信任缓存的数据之前，代理会通过 CAN 索引中存储的哈希值（WHERE）来验证数据的完整性。

```bash
CLAIMED_HASH="a948904f2f0f479b8f8564e9d7e91d9820b5..."
ACTUAL_HASH=$(sha256sum <<< "tool_output_string" | awk '{print $1}')

if [ "$ACTUAL_HASH" = "$CLAIMED_HASH" ]; then
    # Valid (CAN)
else
    # Invalid/Mutated (NOT)
fi
```

### 测试 3：记录 MCP 执行结果
这是一个代理记录 MCP 工具执行过程的示例。

```bash
# 1. Execute MCP tool
RESULT=$(mcp_call fetch_report "Q3_Data")

# 2. Generate CAN stamp locally
WHEN=$(date +%s%3N)
WHERE=$(echo -n "$RESULT" | sha256sum | awk '{print $1}')
WHAT="fetch_report.Q3_Data SAVE"

# 3. Append to index
echo -e "$WHEN\t$WHERE\t$WHAT" >> ~/.can/index.tsv
```

## 对代理的优势

CAN 可以与基于位置的命名机制（例如标准文件路径）并行使用，同时为自主代理提供多项技术优势：
- **离线数据检索**：代理无需网络开销或重新查询工具即可验证和检索过去的 MCP 结果。
- **防篡改机制**：哈希值验证确保注入到提示中的上下文内容与工具最初返回的内容完全一致。
- **搜索优化**：代理可以根据时间戳（WHEN）、内容匹配（WHERE）或元数据/意图（WHAT）来过滤本地日志。
- **解耦性**：即使 MCP 服务器离线或工具的 API 发生变化，历史数据仍然可以在代理的本地状态下被完整地访问和验证。

## 版本路线图：
- **1.8.0**：核心 CAN 规范（时间、位置、数据内容）。
- **1.9.0（当前版本）**：代理与 MCP 的集成以及本地日志记录功能。
- **2.x（未来版本）**：点对点验证、物理共存证明以及可验证的数据交换功能。
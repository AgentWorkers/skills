---
name: Golden Master
description: 跟踪文件之间的“来源-真实性”关系（即确定内容是从何处获取的），以便了解派生内容何时会过时或不再准确。
homepage: https://github.com/Obviously-Not/patent-skills/tree/main/golden-master
user-invocable: true
emoji: 🏆
tags:
  - golden-master
  - source-tracking
  - staleness-detection
  - documentation-tools
  - checksum-validation
  - file-relationships
---

# Golden Master

## 代理身份（Agent Identity）

**角色**：帮助用户建立并验证文件之间的来源关系（即确定哪些文件是从哪个文件派生而来的）。
**理解能力**：过时的文档会引发实际问题——错误的指令、失效的示例、困惑的用户。
**处理方式**：使用加密哈希值来创建可验证的链接；验证过程成本低廉，而处理过时文件的成本较高。
**工作边界**：仅识别文件之间的关系以及文件的更新状态，绝不会在未经明确请求的情况下自动修改文件。
**沟通风格**：精确、系统化，专注于验证工作。
**开场白**：“您有一些文件依赖于其他文件——让我们明确这些关系，这样当文件出现不一致时，您就能及时发现。”

## 使用场景

当用户提出以下请求时，可激活此技能：
- “我想追踪哪些文件是从这个源文件派生出来的。”
- “我的 README 文件与其源文件是否保持同步？”
- “为我的文档设置过期检测功能。”
- “哪些文件依赖于 ARCHITECTURE.md 文件？”
- “检查派生文件是否是最新的。”

## 重要限制

- 仅能识别文件之间的关系及文件的更新状态，不会自动修改文件。
- 仅支持单个仓库范围内的文件（版本 1.0.0；未来将支持跨仓库功能）。
- 文件关系的确认需要人工确认。
- 哈希值用于追踪文件内容，而非文件的语义含义。

---

## 核心操作

### 1. 分析文件关系（Analyze Relationships）

扫描文件，根据内容重叠情况建议文件之间的来源/派生关系。

**输入**：文件路径或目录路径
**输出**：包含置信度的文件关系列表

```json
{
  "operation": "analyze",
  "metadata": {
    "timestamp": "2026-02-04T12:00:00Z",
    "files_scanned": 12,
    "relationships_tracked": 0
  },
  "result": {
    "relationships": [
      {
        "source": "docs/ARCHITECTURE.md",
        "derived": ["README.md", "docs/guides/QUICKSTART.md"],
        "confidence": "high",
        "evidence": "Section headers match, content overlap 73%"
      }
    ]
  },
  "next_steps": [
    "Review suggested relationships — some may be coincidental similarity",
    "Run 'establish' to create tracking metadata for confirmed relationships"
  ]
}
```

### 2. 建立追踪机制（Establish Tracking）

为源文件和派生文件创建元数据。

**输入**：源文件路径、派生文件路径
**输出**：需要添加到文件中的元数据注释

```json
{
  "operation": "establish",
  "metadata": {
    "timestamp": "2026-02-04T12:00:00Z",
    "files_scanned": 0,
    "relationships_tracked": 2
  },
  "result": {
    "source_metadata": {
      "file": "docs/ARCHITECTURE.md",
      "comment": "<!-- golden-master:source checksum:a1b2c3d4 derived:[README.md,docs/guides/QUICKSTART.md] -->",
      "placement": "After title, before first section"
    },
    "derived_metadata": [
      {
        "file": "README.md",
        "comment": "<!-- golden-master:derived source:docs/ARCHITECTURE.md source_checksum:a1b2c3d4 derived_at:2026-02-04 -->",
        "placement": "After title"
      }
    ]
  },
  "next_steps": [
    "Add metadata comments to listed files",
    "Commit together to establish baseline"
  ]
}
```

### 3. 验证文件更新状态（Validate Freshness）

检查派生文件是否与其源文件保持同步。

**输入**：包含 Golden Master 元数据的文件路径或目录路径
**输出**：文件过期报告

```json
{
  "operation": "validate",
  "metadata": {
    "timestamp": "2026-02-04T12:00:00Z",
    "files_scanned": 4,
    "relationships_tracked": 2
  },
  "result": {
    "fresh": [
      {
        "derived": "docs/guides/QUICKSTART.md",
        "source": "docs/ARCHITECTURE.md",
        "status": "Current (checksums match)"
      }
    ],
    "stale": [
      {
        "derived": "README.md",
        "source": "docs/ARCHITECTURE.md",
        "source_checksum_stored": "a1b2c3d4",
        "source_checksum_current": "e5f6g7h8",
        "days_stale": 12,
        "source_changes": [
          "Line 45: Added new 'Caching' section",
          "Line 78: Updated database diagram"
        ]
      }
    ]
  },
  "next_steps": [
    "Review stale items — README.md needs attention (12 days behind)",
    "After updating derived files, run 'refresh' to sync checksums"
  ]
}
```

### 4. 更新哈希值（Refresh Checksums）

在手动同步派生文件内容后，更新元数据。

**输入**：手动更新后的派生文件路径
**输出**：更新后的元数据注释

```json
{
  "operation": "refresh",
  "metadata": {
    "timestamp": "2026-02-04T12:00:00Z",
    "files_scanned": 1,
    "relationships_tracked": 1
  },
  "result": {
    "file": "README.md",
    "old_source_checksum": "a1b2c3d4",
    "new_source_checksum": "e5f6g7h8",
    "updated_comment": "<!-- golden-master:derived source:docs/ARCHITECTURE.md source_checksum:e5f6g7h8 derived_at:2026-02-04 -->"
  },
  "next_steps": [
    "Replace the golden-master comment in README.md with the updated version",
    "Commit with message describing what was synchronized"
  ]
}
```

---

## 元数据格式

### 文件内注释（推荐使用）

**源文件**：
```markdown
<!-- golden-master:source checksum:a1b2c3d4 derived:[file1.md,file2.md] -->
```

**派生文件**：
```markdown
<!-- golden-master:derived source:path/to/source.md source_checksum:a1b2c3d4 derived_at:2026-02-04 -->
```

### 独立清单（备用方案）

适用于集中式追踪：

```yaml
# .golden-master.yaml
version: 1
relationships:
  - source: docs/ARCHITECTURE.md
    checksum: a1b2c3d4
    derived:
      - path: README.md
        source_checksum: a1b2c3d4
        derived_at: 2026-02-04
```

---

## 哈希值规范

**算法**：使用 SHA256 进行哈希计算，并对文件内容进行规范化处理。

**规范化步骤**（在哈希之前必须执行）：
1. 将行尾格式统一为 LF（Unix 标准）。
2. 删除每行末尾的空白字符。
3. 过滤掉与 Golden Master 元数据相关的注释（格式为 `<!--\s*golden-master:.*?-->`）。

**显示方式**：显示哈希值的前 8 个字符（完整哈希值存储在内部）。

**实现说明**：需要自定义代码来实现这些规范化步骤。标准库中的 `sha256sum` 函数无法完成这些操作。示例处理流程如下：

```bash
# Normalize and hash (requires sed + shasum)
cat FILE | \
  sed 's/\r$//' | \                    # CRLF → LF
  sed 's/[[:space:]]*$//' | \          # Trim trailing whitespace
  sed 's/<!--[[:space:]]*golden-master:[^>]*-->//g' | \  # Strip metadata
  shasum -a 256 | \
  cut -c1-8                            # First 8 chars for display
```

**注意**：实现此功能的 AI 代理应通过编程方式完成规范化处理，而非使用 shell 命令。上述流程仅用于手动验证。

---

## 输出格式

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["operation", "metadata", "result", "next_steps"],
  "properties": {
    "operation": {
      "type": "string",
      "enum": ["analyze", "establish", "validate", "refresh"]
    },
    "metadata": {
      "type": "object",
      "required": ["timestamp", "files_scanned", "relationships_tracked"],
      "properties": {
        "timestamp": { "type": "string", "format": "date-time" },
        "files_scanned": { "type": "integer", "minimum": 0 },
        "relationships_tracked": { "type": "integer", "minimum": 0 }
      }
    },
    "result": {
      "type": "object",
      "description": "Operation-specific result (see Core Operations for each operation's result structure)"
    },
    "next_steps": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1,
      "maxItems": 2
    },
    "error": {
      "type": "object",
      "required": ["code", "message"],
      "properties": {
        "code": { "type": "string", "enum": ["NO_FILES", "NO_METADATA", "INVALID_PATH", "CHECKSUM_MISMATCH"] },
        "message": { "type": "string" },
        "suggestion": { "type": "string" }
      }
    }
  }
}
```

**说明**：`result` 对象的结构因操作类型而异。具体每个操作的输出字段请参见“核心操作”部分（例如，`analyze` 操作返回 `relationships[]`，`validate` 操作返回 `fresh[]` 和 `stale[]`）。

---

## 错误处理

| 错误代码 | 触发条件 | 错误信息 | 建议措施 |
|------------|----------------|-----------------|---------------------------|
| `NO FILES` | 指定路径下找不到文件 | “该路径下没有文件。” | “请确认路径存在且包含可读取的文件。” |
| `NO_METADATA` | 未找到 Golden Master 元数据 | “未检测到 Golden Master 的追踪元数据。” | “请先运行 ‘establish’ 操作来建立文件关系。” |
| `INVALID_PATH` | 路径格式不正确或包含无效字符 | “路径格式有误。” | “请使用项目根目录下的相对路径，不允许使用 ‘..’。” |
| `CHECKSUM_MISMATCH` | 存储的哈希值格式不正确 | “元数据中的哈希值与预期格式不符。” | “哈希值应为 8 个以上的十六进制字符。文件是否被手动修改过？” |

---

## 术语说明

| 术语 | 适用场景 | 禁用场景 |
|------|----------------|-------------------------|
| **Source** | 其他文件依赖的基准文件 | 派生文件 |
| **Derived** | 基于源文件内容生成的文件 | 源文件 |
| **Stale** | 源文件的哈希值发生变化的派生文件 | 未进行追踪的文件 |
| **Fresh** | 哈希值与源文件一致的派生文件 | 新生成的文件 |
| **Tracking** | 已建立的元数据关系 | 非正式的文件引用方式 |

---

## 相关技能

- **principle-synthesizer**：从多个来源中识别出可能的 Golden Master 文件。
- **core-refinery**：通过对话式交互生成 Golden Master 文件的候选列表。
- **pbe-extractor**：提取可能成为 Golden Master 的文件内容。

---

## 必需的免责声明

此技能仅用于识别文件之间的关系和检测文件是否过期，并不保证派生文件的内容完全准确反映了源文件的内容。在检测到文件过期后，请用户自行审查源文件的更改并相应地更新派生文件。该技能仅负责追踪文件的结构，不负责验证内容的语义正确性。

---

*由 Obviously Not 开发——这是一款用于辅助思考的工具，而非用于得出结论的工具。*
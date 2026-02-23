---
name: doc-accurate-codegen
version: "1.0.0"
description: "生成代码时，必须引用实际的文档内容，以防止出现“幻觉错误”（即代码因误解文档而产生错误）。在生成代码之前，务必先加载相关文档，验证代码与 API 签名的匹配性，并确认代码的正确性。此方法适用于任何代码生成、API 使用或配置创建的场景。"
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: ["curl", "jq", "git"]
      env: ["BRAVE_API_KEY"]
    install:
      - id: npm
        kind: node
        package: axios
        bins: ["axios"]
---
# 精确的代码生成（Documentation-Accurate Code Generation）

**关键性**：该技能通过强制使用文档作为参考，有效防止了大型语言模型（LLMs）生成错误或虚构的代码。

## 使用场景
- **在生成代码时** **务必** 使用该技能。
- **在使用API时** **务必** 使用该技能。
- **在创建配置文件时** **务必** 使用该技能。
- **在实现新功能时** **务必** 使用该技能。

## 核心理念
**永远不要仅凭记忆生成代码，必须始终参考文档。**

### 问题所在
- 大型语言模型可能会生成不存在的API。
- 方法的名称可能会被更改或删除。
- 参数的类型或用途可能会发生变化。
- 返回值的类型可能会出乎意料地改变。
- 配置文件的格式也可能会更新。

### 解决方案
1. **首先加载文档** — 在编写任何代码之前，先读取相关文档。
2. **提取API签名** — 获取实际的API方法签名。
3. **根据文档生成代码** — 使用文档中的信息来生成代码。
4. **与文档进行验证** — 确保生成的代码与文档内容一致。
5. **记录引用来源** — 记录生成代码时所参考的文档。

## 工作流程
```
1. IDENTIFY → What code/API/tool is needed?
2. LOCATE → Find documentation source
3. LOAD → Fetch and parse documentation
4. EXTRACT → Pull API signatures, parameters, examples
5. GENERATE → Create code using actual docs
6. VALIDATE → Check code matches documentation
7. REFERENCE → Track what docs were used
```

## 文档来源
### 1. OpenClaw内部文档
- 位置：`C:\Users\clipp\AppData\Roaming\npm\node_modules\openclaw\docs`
- 访问方式：使用`read`工具
- 用途：用于OpenClaw特有的API、工具和功能的文档。

### 2. 工具文档
- 工具帮助信息：通过`--help`命令获取。
- 手册页：使用`man <command>`查看。
- 官方文档：使用`web_fetch`工具下载。

### 3. API文档
- 官方文档：使用`web_fetch`工具获取。
- OpenAPI规范：解析并引用这些规范。
- 包的文档：包括npm、pip、cargo等包的官方文档。

### 4. 代码示例
- 查阅现有的代码实现。
- 测试代码：检查测试文件中的用法示例。
- 寻找可运行的代码示例。

## 代码生成流程
### 第一步：文档查找
```bash
# For OpenClaw tools
read("openclaw-docs-path/tool-name.md")

# For external tools
web_fetch("https://docs.tool.com/api")

# For local tools
exec("tool --help")
```

### 第二步：提取API签名
```markdown
# Extract:
- Method names
- Parameters (names, types, required/optional)
- Return types
- Error handling
- Examples
- Version information
```

### 第三步：代码生成
```python
# Generate code using actual API data
def generate_from_docs(api_docs):
    # Use real method names
    # Use real parameter names
    # Use real return types
    # Include error handling from docs
    # Add docstrings from docs
    pass
```

### 第四步：代码验证
```python
def validate_against_docs(code, api_docs):
    # Check method names match
    # Check parameter names match
    # Check types match
    # Check return types match
    # Verify no hallucinated methods
    pass
```

## 常用命令
- `codegen <api>` — 根据文档生成代码。
- `validate <code>` — 检查代码是否与文档一致。
- `doc-lookup <api>` — 加载并显示文档内容。
- `api-extract <tool>` — 提取指定工具的API签名。

## 使用示例
```
"Generate code to use the OpenClaw sessions_spawn tool"
# Process: Load docs → Extract API → Generate → Validate

"Create a Python script using the requests library"
# Process: Fetch requests docs → Extract API → Generate → Validate

"Write configuration for OpenClaw channels"
# Process: Load config docs → Extract format → Generate → Validate
```

## 验证规则
### 1. 方法名称验证
- 确认方法在文档中存在。
- 名称拼写必须完全一致。
- 确认方法未被弃用。

### 2. 参数验证
- 所有必需的参数都必须存在。
- 参数名称必须与文档中的描述完全匹配。
- 参数类型必须与文档中的描述一致。
- 可选参数的标记必须正确。

### 3. 返回类型验证
- 返回类型必须与文档中的描述一致。
- 错误类型必须与文档中的描述一致。
- 边缘情况必须得到妥善处理。

### 4. 配置验证
- 键值对必须与文档中的描述一致。
- 值的类型必须符合文档中的规范。
- 必需的字段必须存在。
- 格式必须符合文档中的要求。

## 错误预防措施
### 常见的问题
1. **不存在的方法**：生成了实际上并不存在的方法。
2. **错误的参数名称**：生成了错误的参数名称。
3. **错误的类型**：生成了错误的参数或返回类型。
4. **忽略文档中的错误处理**：未处理文档中规定的错误。
5. **错误的配置格式**：配置文件的格式不正确。

### 预防策略
1. **始终先加载文档**：绝不依赖记忆生成代码。
2. **提取准确的API签名**：不要猜测API的接口结构。
3. **全面验证**：所有内容都必须与文档进行比对。
4. **记录引用来源**：明确记录生成代码时所参考的文档。
5. **使用真实的API进行测试**：确保代码能够正常运行。

## 与其他技能的集成
- **编码技能**：结合该技能生成基于文档的代码。
- **自我优化**：通过文档验证来持续改进代码生成能力。
- **内容生成**：生成准确的代码示例。
- **资料研究**：从官方文档中查找API相关信息。

## 与OpenClaw工具的集成
- `read`：用于加载OpenClaw的内部文档。
- `web_fetch`：用于下载外部文档。
- `exec`：通过`--help`参数执行工具并查看文档。
- `edit/write`：根据文档生成经过验证的代码。

## 文档引用记录
### 文档格式规范
```markdown
# Code Generation Reference

## Generated Code
- File: path/to/file.py
- Generated: 2026-02-23
- Tool: doc-accurate-codegen

## Documentation Sources
1. OpenClaw Tool Docs: /docs/tools/exec.md
2. API Reference: https://docs.example.com/api
3. Examples: /examples/exec-usage.py

## Validation
- ✅ Method names validated
- ✅ Parameters validated
- ✅ Return types validated
- ✅ Error handling validated

## Notes
- Using exec tool with sandbox mode
- All parameters from official docs
- Error handling from API reference
```

## 代码生成输出格式
在生成代码时，务必包含以下内容：
```python
# Code generated with documentation reference
# Source: [documentation URL or path]
# Validated: [timestamp]
# API Version: [version if available]

def function_name():
    """
    [Docstring from actual documentation]
    
    Source: [link to docs]
    Parameters: [from docs]
    Returns: [from docs]
    """
    # Implementation using actual API
    pass
```

## 最佳实践
1. **始终优先参考文档**：生成代码前必须先加载文档。
2. **确保完全一致**：使用文档中的准确名称、类型和格式。
3. **全面验证**：对生成的代码进行彻底检查。
4. **记录引用来源**：明确记录生成代码时所参考的文档。
5. **使用真实API进行测试**：确保代码能够正常运行。
6. **定期更新**：随着API的更新，及时重新检查文档内容。
7. **处理错误**：包含文档中规定的所有错误信息。
8. **提供示例**：引用文档中的有效代码示例。

## 常见误区
1. **假设API的稳定性**：API可能会发生变化，因此必须定期重新检查文档。
2. **依赖记忆而非文档**：始终信任文档内容，而非记忆中的信息。
3. **部分加载文档**：必须加载完整的文档内容。
4. **不进行验证**：生成代码后必须进行验证。
5. **忽略引用记录**：必须记录生成代码时所参考的文档来源。

## 成功指标
- **错误生成率**：0%（所有代码都引用实际存在的文档）。
- **验证通过率**：100%（所有代码都经过验证）。
- **引用记录率**：100%（所有代码都记录了文档来源）。
- **错误率**：0%（没有错误的使用API的情况）。
- **测试通过率**：100%（所有生成的代码都能正常运行）。

## 高级功能
### 1. 自动文档加载
- 自动识别所需的API。
- 自动下载相关文档并缓存以供后续使用。
### 2. API变更检测
- 监测文档的更新情况。
- 在API发生变化时发出警报。
- 提供代码更新的提示。

### 3. 多源验证
- 跨多个文档来源进行验证。
- 检测不同来源之间的冲突。
- 选择最权威的文档作为参考。

### 4. 示例提取
- 从文档中提取可运行的代码示例。
- 根据具体需求调整示例代码。
- 在使用示例代码之前进行测试。

## 与OpenClaw工具的集成细节
- **工具文档**：如何使用`read`工具加载OpenClaw的内部文档。
- **web_fetch**：如何使用`web_fetch`工具下载外部文档。
- **exec**：如何使用`exec`命令查看工具的帮助信息。
- **edit/write**：如何根据文档生成经过验证的代码。

## 文档引用记录的格式规范
```markdown
# Code Generation Reference

## Generated Code
- File: path/to/file.py
- Generated: 2026-02-23
- Tool: doc-accurate-codegen

## Documentation Sources
1. OpenClaw Tool Docs: /docs/tools/exec.md
2. API Reference: https://docs.example.com/api
3. Examples: /examples/exec-usage.py

## Validation
- ✅ Method names validated
- ✅ Parameters validated
- ✅ Return types validated
- ✅ Error handling validated

## Notes
- Using exec tool with sandbox mode
- All parameters from official docs
- Error handling from API reference
```

## 代码生成时的输出格式要求
在生成代码时，务必包含以下内容：
```python
# Code generated with documentation reference
# Source: [documentation URL or path]
# Validated: [timestamp]
# API Version: [version if available]

def function_name():
    """
    [Docstring from actual documentation]
    
    Source: [link to docs]
    Parameters: [from docs]
    Returns: [from docs]
    """
    # Implementation using actual API
    pass
```

## 总结
该技能的存在是为了防止大型语言模型生成错误代码。在生成代码时，务必始终使用该技能。只有通过引用官方文档，才能确保代码的准确性和可靠性。
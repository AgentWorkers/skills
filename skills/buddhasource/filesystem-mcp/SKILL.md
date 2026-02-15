---
name: filesystem-mcp
description: 官方文件系统MCP服务器，支持安全的文件操作并具备可配置的访问控制功能。用户可以执行读、写、创建、删除、移动文件和目录等操作，还可以搜索文件和目录、查看目录内容、编辑文本文件以及管理文件权限。内置的安全沙箱机制可有效防止未经授权的访问。该服务器对于需要处理本地文件的代理程序、项目管理工作、日志分析、内容生成以及文件组织等场景至关重要。当代理程序需要访问文件系统、进行文件操作、导航目录或管理文件内容时，强烈推荐使用该服务器。
---

# 文件系统 MCP 服务器

> **为 AI 代理提供安全的文件操作功能**

这是 ModelContextProtocol (MCP) 的官方实现，提供了安全、沙箱化的文件系统访问功能，并具备细粒度的权限控制。

## 为什么选择 Filesystem MCP？

### 🔒 以安全为核心的设计
- **沙箱化访问**：代理只能访问明确允许的目录。
- **权限控制**：针对每个目录支持只读、写入或完全访问权限。
- **路径验证**：防止目录遍历和未经授权的访问。
- **审计追踪**：所有操作都会被记录下来，以便进行安全审查。

### 🤖 对代理工作流程至关重要
大多数代理任务都涉及文件操作：
- 阅读文档
- 编写代码文件
- 分析日志
- 生成报告
- 管理项目文件
- 组织内容

### 📦 完全不依赖外部组件
该实现完全使用 Node.js 的内置模块，无需依赖任何外部 API 或设置速率限制。

## 安装

```bash
# Official reference implementation
npm install -g @modelcontextprotocol/server-filesystem

# Or build from source
git clone https://github.com/modelcontextprotocol/servers
cd servers/src/filesystem
npm install
npm run build
```

## 配置

将以下配置添加到您的 MCP 客户端配置中：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/Documents",
        "/Users/yourname/Projects"
      ]
    }
  }
}
```

**参数** = 允许的目录（一个或多个路径）

### 权限模式

**只读访问：**
```json
"args": ["--read-only", "/path/to/docs"]
```

**完全访问（默认）：**
```json
"args": ["/path/to/workspace"]
```

### 示例配置

#### 开发工作区
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/dev/projects",
        "/Users/dev/workspace"
      ]
    }
  }
}
```

#### 文档访问（只读）
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "--read-only",
        "/Users/docs/knowledge-base"
      ]
    }
  }
}
```

## 可用的工具

### 目录操作

#### 1. **列出目录** (`list_directory`)
```
Agent: "What files are in my Projects folder?"
Agent: "Show contents of /workspace/src"
```

**返回内容：**
- 文件名
- 文件类型（文件、目录、符号链接）
- 文件大小
- 最后修改时间

#### 2. **创建目录** (`create_directory`)
```
Agent: "Create a new folder called 'components'"
Agent: "Make directory /workspace/tests"
```

#### 3. **移动/重命名** (`move_file`)
```
Agent: "Rename old-name.txt to new-name.txt"
Agent: "Move report.pdf to /Documents/Reports/"
```

### 文件操作

#### 4. **读取文件** (`read_file`)
```
Agent: "Read the contents of config.json"
Agent: "Show me the README.md file"
```

**支持格式：**
- 文本文件（UTF-8）
- JSON、YAML、XML
- Markdown 文件
- 大文件（支持流式读取）

#### 5. **写入文件** (`write_file`)
```
Agent: "Create a file called notes.txt with meeting notes"
Agent: "Write the generated code to src/index.ts"
```

#### 6. **编辑文件** (`edit_file`)
```
Agent: "Replace 'version: 1.0' with 'version: 2.0' in package.json"
Agent: "Add a new function to utils.js"
```

#### 7. **获取文件信息** (`get_file_info`)
```
Agent: "When was report.pdf last modified?"
Agent: "What's the size of data.csv?"
```

**返回信息：**
- 文件大小（字节）
- 创建时间
- 最后修改时间
- 权限
- 文件类型

### 高级操作

#### 8. **搜索文件** (`search_files`)
```
Agent: "Find all Python files in the project"
Agent: "Search for files containing 'API_KEY'"
```

**搜索条件：**
- 文件名模式（glob）
- 文件内容（正则表达式）
- 文件类型
- 修改日期

#### 9. **删除文件** (`delete_file`)
```
Agent: "Delete the temporary log files"
Agent: "Remove old-backup.zip"
```

**安全措施：**
- 大文件删除前需要确认
- 不能删除不允许的目录中的文件
- 所有操作都会被记录以供审计。

## 代理工作流程示例

### 代码生成
```
Human: "Create a React component for a login form"

Agent:
1. create_directory("/workspace/components")
2. write_file("/workspace/components/LoginForm.tsx", generated_code)
3. write_file("/workspace/components/LoginForm.test.tsx", test_code)
4. "Created LoginForm component at components/LoginForm.tsx"
```

### 日志分析
```
Human: "Analyze error logs and summarize issues"

Agent:
1. list_directory("/var/log/app")
2. read_file("/var/log/app/error.log")
3. search_files(pattern="ERROR", path="/var/log/app")
4. generate_summary()
5. write_file("/reports/error-summary.md", summary)
```

### 项目组织
```
Human: "Organize my documents by type"

Agent:
1. list_directory("/Documents")
2. For each file:
   - get_file_info(file)
   - Determine file type
   - create_directory("/Documents/[type]")
   - move_file(file, destination_folder)
```

### 文档生成
```
Human: "Generate API documentation from code comments"

Agent:
1. search_files(pattern="*.ts", path="/src")
2. For each file:
   - read_file(file)
   - extract_doc_comments()
3. Generate markdown docs
4. write_file("/docs/API.md", generated_docs)
```

## 安全模型

### 沙箱机制的强制执行

**代理可以执行的操作：**
- ✅ 访问明确允许的目录
- ✅ 在允许的路径内创建/读取/写入文件
- ✅ 列出目录内容
- ✅ 在允许的路径内搜索文件

**代理不能执行的操作：**
- ❌ 访问上级目录（`../`）
- ❌ 访问系统文件（`/etc/`, `/sys/`）
- ❌ 跟随不允许路径中的符号链接
- ❌ 执行二进制文件或脚本
- ❌ 修改文件权限

### 路径验证
```
Allowed: /Users/dev/projects
Agent tries: /Users/dev/projects/src/index.ts → ✅ Allowed
Agent tries: /Users/dev/projects/../secret → ❌ Blocked
Agent tries: /etc/passwd → ❌ Blocked
```

### 最佳实践

1. **最小权限原则**：
   - 仅授予必要的目录访问权限。
   - 如果不需要写入权限，使用 `--read-only` 参数。

2. **禁止 root 权限**：
   - 不允许访问 `/` 或系统目录。
   - 将代理限制在用户的工作区内。

3. **审计代理行为**：
   - 定期审查 MCP 服务器日志。
   - 监控异常的文件访问行为。

4. **分离敏感数据**：
   - 将凭证和密钥存储在单独的目录中。
   - 确保这些目录不在允许的访问路径范围内。

## 使用场景

### 📝 内容管理
代理生成博客文章、报告和文档，并将它们保存到有序的文件夹中。

### 🤖 代码辅助工具
代理可以读取项目文件、生成代码、创建测试用例以及更新配置。

### 📊 数据分析
代理可以读取 CSV/JSON 数据文件，进行分析并生成报告和可视化结果。

### 🗂️ 文件组织
代理可以扫描目录、对文件进行分类、移动到适当的文件夹中，并删除重复文件。

### 📚 知识库
代理可以索引 Markdown 文件、搜索文档、提取信息并更新维基页面。

### 🔍 日志分析
代理可以解析日志文件、识别错误、生成摘要并触发警报。

## 性能

### 大文件处理
- 支持大于 10MB 的文件流式读取。
- 支持增量读取。
- 处理过程高效且节省内存。

### 目录扫描
- 优化了递归搜索功能。
- 支持全局模式匹配（glob）。
- 可忽略某些目录（例如 `node_modules/`）。

### 并发操作
- 支持安全的并行文件访问。
- 执行原子性的写入操作。
- 在需要时会对文件进行锁定。

## 故障排除

### “权限被拒绝”错误
- 确认路径是否在允许的目录范围内。
- 检查文件系统的权限设置。
- 确保 MCP 服务器具有读写权限。

### “路径未找到”错误
- 确认目录是否存在。
- 检查路径中是否有拼写错误。
- 核对路径格式（绝对路径 vs 相对路径）。

### 只读模式下的问题
- 在只读模式下无法写入文件。
- 如有需要，可以重新配置服务器以允许写入权限。

## 与其他文件访问方法的比较

| 方法 | 安全性 | 代理集成程度 | 设置复杂性 |
|--------|----------|-------------------|-------|
| **Filesystem MCP** | ✅ 沙箱化保护 | ✅ 自动识别代理 | 配置简单 |
| **直接文件系统访问** | ❌ 全系统访问权限 | ❌ 需手动配置 | 配置复杂 |
| **文件上传/下载** | ✅ 需手动控制 | ⚠️ 有限的功能 | 配置复杂 |
| **云存储 API** | ✅ 基于 API 的访问 | ⚠️ 需要 SDK | 配置复杂 |

## 资源

- **GitHub**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- **MCP 文档**: https://modelcontextprotocol.io/
- **安全最佳实践**: https://modelcontextprotocol.io/docs/concepts/security

## 高级配置

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": [
        "/path/to/filesystem-server/build/index.js",
        "/workspace",
        "/documents"
      ],
      "env": {
        "MAX_FILE_SIZE": "10485760",
        "ENABLE_LOGGING": "true",
        "LOG_PATH": "/var/log/mcp-filesystem.log"
      }
    }
  }
}
```

---

**Filesystem MCP 为代理提供了安全、可靠的文件系统访问功能**：从代码生成到日志分析，它是代理执行文件操作的基础。
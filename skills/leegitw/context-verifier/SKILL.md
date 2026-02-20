---
name: context-verifier
version: 1.3.0
description: 请确保您正在编辑的文件确实是您想要修改的文件。在采取任何操作之前，请先验证该文件的完整性。
author: Live Neon <contact@liveneon.dev>
homepage: https://github.com/live-neon/skills/tree/main/agentic/context-verifier
repository: leegitw/context-verifier
license: MIT
tags: [agentic, verification, hash, integrity, context]
layer: foundation
status: active
alias: cv
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      config:
        - .openclaw/context-verifier.yaml
        - .claude/context-verifier.yaml
      workspace:
        - output/context-packets/
---
# context-verifier（验证工具）

这是一个集成了文件哈希计算、完整性验证、严重性标记以及上下文数据包生成功能的统一工具。它将原本独立的三个功能整合到了一个验证系统中。

**触发方式**：需要显式调用该工具。

**依赖技能**：context-packet、file-verifier、severity-tagger

## 安装

```bash
openclaw install leegitw/context-verifier
```

**注意事项**：该工具为基础功能模块，无需额外依赖其他组件。

**独立使用**：该工具可独立运行，提供文件完整性验证服务，是Neon Agentic Suite中其他工具依赖的核心组件。在开始使用Neon Agentic Suite时，请先安装此工具。

**数据处理方式**：该工具仅用于执行指令（`disable-model-invocation: true`），它会计算文件哈希并生成上下文数据包，但不会直接调用AI模型。不会使用任何外部API或第三方服务。验证结果会保存在工作区的`output/context-packets/`目录下。

**文件访问权限**：该工具会读取用户指定的文件以计算哈希值。虽然元数据中仅声明了配置和输出路径，但该工具会读取你通过`/cv hash`、`/cv verify`或`/cv packet`提供的任何文件路径。请谨慎处理敏感文件。

## 功能说明**

AI代理有时可能会使用过时的数据（例如，修改了但在读取后被再次使用的文件，或者依赖已失效的缓存内容）。context-verifier通过以下方式防止此类问题：
1. 在操作前后计算文件的哈希值。
2. 检测文件在读取和写入之间的变化。
3. 生成包含可验证校验和的上下文数据包，以便后续进行审核。

**使用建议**：虽然可以信任AI的结果，但务必进行验证——你读取的文件可能与即将编辑的文件不一致，请先进行确认。

## 命令用法

```
/cv <sub-command> [arguments]
```

## 子命令

| 命令            | 功能                | 触发方式       |
|------------------|------------------|-------------|
| `/cv hash`         | 计算文件哈希（SHA256）        | 显式调用       |
| `/cv verify`        | 验证文件完整性          | 显式调用       |
| `/cv tag`         | 为文件分配严重性等级（critical/important/minor）| 显式调用       |
| `/cv packet`        | 生成包含文件信息的JSON数据包       | 显式调用       |

## 参数说明

### /cv hash

| 参数            | 是否必填 | 说明                          |
|------------------|------------------|-------------------------|
| file            | 是                | 需要验证的文件路径                |
| --algorithm       | 否                | 哈希算法（仅支持sha256，MD5/SHA-1已被弃用）         |

### /cv verify

| 参数            | 是否必填 | 说明                          |
| file            | 是                | 需要验证的文件路径                |
| hash            | 是                | 预期的哈希值                    |
| --algorithm       | 否                | 哈希算法（仅支持sha256）                 |

### /cv tag

| 参数            | 是否必填 | 说明                          |
| file            | 是                | 需要标记的文件路径                |
| severity         | 是                | 文件的严重性等级（critical/important/minor）     |

### /cv packet

| 参数            | 是否必填 | 说明                          |
| files            | 是                | 以逗号分隔的文件路径或通配符模式            |
| --name          | 否                | 数据包名称（默认自动生成）              |
| --include-content    | 否                | 是否包含文件内容（默认不包含）           |

> **安全警告**：`--include-content`选项会将文件内容保存到磁盘。请勿对敏感文件（如`.env`、凭据、密钥文件）使用此选项。请参阅下面的[安全注意事项]。

## 配置设置

配置信息按优先级顺序从以下文件加载：
1. `.openclaw/context-verifier.yaml`（OpenClaw标准配置）
2. `.claude/context-verifier.yaml`（Claude代码兼容性配置）
3. 系统默认配置

## 安全注意事项

- **该工具不会执行以下操作**：
  - 调用AI模型
  - 使用外部API或第三方服务
  - 将数据发送到外部服务
  - 修改源文件（仅将结果写入`output/context-packets/`）

- **该工具访问的内容**：
  - `.openclaw/context-verifier.yaml`和`.claude/context-verifier.yaml`中的配置文件
  - 用户指定的文件（仅用于哈希计算，读-only）
  - 自定义的输出目录`output/context-packets/`

**重要提示**：与其他工具不同，context-verifier会读取用户指定的任意文件。元数据中仅声明了配置和输出路径。例如，当你运行`/cv hash myfile.go`时，即使该文件未在元数据中列出，工具也会读取该文件。这是为了确保能够验证用户希望检查的文件。

**敏感文件处理**：
- `critical_patterns`（如`.env`、`*credentials`、`*secret`）用于：
  - 识别需要触发警告的文件
  - 标记这些文件为关键文件，以防止其被修改

默认情况下，`/cv hash`和`/cv packet`在计算哈希时不会读取文件内容。

**--include-content选项**：
- 该选项会将文件内容保存到磁盘。请注意：
  - **切勿对`.env`、凭据或密钥文件使用此选项**。
  - 如果使用，请将`output/context-packets/`添加到`.gitignore`文件中。
  - 数据会永久保存，需手动删除不再需要的数据包。

**推荐使用方法**：
```bash
# Safe: Hash only (default) - no content stored
/cv packet src/*.go --name "pre-refactor"

# Risky: Content included - ensure no sensitive files in glob
/cv packet docs/*.md --name "docs-backup" --include-content

# NEVER do this:
/cv packet .env --include-content  # Stores secrets to disk!
```

### .gitignore配置

请在`.gitignore`文件中添加以下内容，以防意外提交敏感文件：

```gitignore
# Context verification packets (may contain sensitive data)
output/context-packets/
```

## 数据存储与保留策略

- **存储位置**：数据包保存在工作区的`output/context-packets/`目录中。
- **格式**：未加密的JSON格式。
- **保留策略**：数据包不会自动删除，需手动清理。
- **访问权限**：使用标准文件系统权限。

对于敏感环境，建议采取以下措施：
- 限制`output/`目录的访问权限。
- 使用加密文件系统。
- 定期清理旧数据包。

## 开发者信息

该工具由Live Neon（https://github.com/live-neon/skills）开发，并通过`leegitw`账户发布在ClawHub上。开发者为同一人。

## 核心逻辑

- **哈希计算**：默认使用SHA-256算法。

```
hash(file) = SHA256(file.content)
```

## 严重性分类

文件会根据可配置的规则自动分类：

| 严重性等级 | 规则匹配条件 | 处理方式         |
|------------|------------------|-------------------------|
| critical     | `*.env`、`*credentials`、`*secret`、项目配置文件 | 禁止操作                |
| important    | `*.go`、`*.ts`、`*.md`（文档文件） | 提示用户注意             |
| minor      | `*.log`、`*.tmp`、`output/*`     | 仅记录日志                |

**重要文件的配置规则**可在`.openclaw/context-verifier.yaml`中调整：

```yaml
# .openclaw/context-verifier.yaml
critical_patterns:
  - "*.env"
  - "*credentials*"
  - "*secret*"
  - "CLAUDE.md"     # Claude Code projects
  - "AGENTS.md"     # OpenClaw projects
  - "pyproject.toml" # Python projects
  - "Cargo.toml"    # Rust projects
```

## 上下文数据包结构

```json
{
  "id": "PKT-20260215-001",
  "created": "2026-02-15T10:30:00Z",
  "files": [
    {
      "path": "src/main.go",
      "hash": "abc123...",
      "severity": "important",
      "size": 1234,
      "modified": "2026-02-15T10:00:00Z"
    }
  ],
  "metadata": {
    "purpose": "pre-refactor snapshot",
    "creator": "context-verifier"
  }
}
```

## 输出结果

- `/cv hash`的输出格式
```
[HASH] src/main.go
Algorithm: SHA-256
Hash: a1b2c3d4e5f6...
Size: 1,234 bytes
Modified: 2026-02-15 10:00:00
```

- `/cv verify`（匹配结果）的输出格式
```
[VERIFY] src/main.go
Status: ✓ MATCH
Expected: a1b2c3d4e5f6...
Actual:   a1b2c3d4e5f6...
```

- `/cv verify`（不匹配结果）的输出格式
```
[VERIFY] src/main.go
Status: ✗ MISMATCH
Expected: a1b2c3d4e5f6...
Actual:   x9y8z7w6v5u4...

WARNING: File has changed since last read.
Action: Re-read file before making changes.
```

- `/cv tag`的输出格式
```
[TAG] src/main.go
Severity: important
Reason: Go source file
Behavior: Warn on unexpected change
```

- `/cv packet`的输出格式
```
[PACKET CREATED]
ID: PKT-20260215-001
Files: 4
Total size: 10,234 bytes

Files included:
- src/main.go (important) - a1b2c3...
- src/handler.go (important) - d4e5f6...
- docs/README.md (important) - j0k1l2...
- config/settings.yaml (important) - m3n4o5...

Stored: output/context-packets/PKT-20260215-001.json
```

**注意事项**：
- 请避免在数据包中包含敏感文件（如`.env`、凭据文件）。使用特定的通配符（如`src/*.go`）来排除敏感文件。

## 集成方式**

- **所属层级**：基础功能模块（无依赖关系）。
- **依赖关系**：无（作为基础验证系统）。
- **使用场景**：
  - failure-memory（用于检测文件变更）
  - constraint-engine（用于操作前的验证）

## 错误处理情况

| 错误条件 | 处理方式                |
|------------|------------------|-------------------------|
| 文件未找到       | 报错：“文件未找到：{path}”         |
| 权限不足       | 报错：“无法读取文件：{path}”         |
| 哈希格式无效     | 报错：“哈希格式无效。预期格式：{algorithm}”     |
| 通配符匹配不到文件   | 警告：“无文件匹配指定模式”         |

## 使用后的后续步骤

- 如果哈希值不匹配，提示用户重新读取文件。
- 如果检测到关键文件被修改，禁止操作并要求重新验证。
- 生成的数据包会被保存在`output/context-packets/`目录中，以供审计使用。

## 工作区文件影响

该工具会读取和写入以下文件：

```
output/
└── context-packets/
    └── PKT-YYYYMMDD-XXX.json
```

## 示例用法

- **编辑文件前进行验证**（示例代码）
```
/cv hash src/main.go
# Save hash: a1b2c3d4e5f6...

# ... later, before editing ...

/cv verify src/main.go a1b2c3d4e5f6
# ✓ MATCH - safe to edit
```

- **为代码重构创建上下文数据包**（示例代码）
```
/cv packet src/*.go,internal/**/*.go --name "pre-refactor"
# Creates packet with all Go files

# ... after refactoring ...

# Can compare against packet to see what changed
```

- **为敏感文件标记严重性等级**（示例代码）
```
/cv tag .env
# Severity: critical

/cv tag src/handler.go
# Severity: important
```

- **部署前验证数据库迁移**（示例代码）
```
/cv packet db/migrations/*.sql --name "pre-deploy-migrations"
# Creates packet with all migration files

# After staging deployment...
/cv verify db/migrations/001_users.sql abc123...
# ✓ MATCH - migration file unchanged, safe to deploy to production
```

- **生成API架构验证数据包**（示例代码）
```
/cv packet api/schemas/*.json,api/openapi.yaml --name "api-schema-v2"
# Creates packet with all API schema files for version control
```

## 验收标准：
- `/cv hash`能正确计算文件的SHA-256哈希值。
- `/cv verify`能将文件哈希与预期值进行比对。
- `/cv tag`能根据规则自动分配文件严重性等级。
- `/cv tag`支持手动修改文件的严重性等级。
- `/cv packet`能生成包含文件元数据的JSON数据包。
- `/cv packet`支持通配符模式。
- 关键文件变更会触发相应的处理机制。
- 工作区文件会被保存在指定的位置。

---

*该工具整合自三个独立功能，发布日期：2026-02-15.*
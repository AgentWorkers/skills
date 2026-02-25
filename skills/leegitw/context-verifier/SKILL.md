---
name: context-verifier
version: 1.5.1
description: 请确保您正在编辑的文件确实是您想要修改的文件。在采取任何操作之前，先验证该文件的完整性。
author: Live Neon <contact@liveneon.dev>
homepage: https://github.com/live-neon/skills/tree/main/agentic/context-verifier
repository: leegitw/context-verifier
license: MIT
tags: [agentic, verification, integrity, validation, checksums, drift-detection, state, file-verification]
layer: foundation
status: active
alias: cv
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

**注意事项**：该工具为独立使用的基礎技能，无需额外依赖其他组件。在部署Neon Agentic Suite时，请先安装此工具，因为它提供了其他工具所需的文件完整性验证功能。

**数据处理方式**：该工具仅执行本地操作。哈希计算使用标准的SHA256算法，不会将文件内容发送到任何模型、API或外部服务。验证结果会被保存在工作区的`output/context-packets/`目录下。工具的配置信息来自`.openclaw/context-verifier.yaml`或`.claude/context-verifier.yaml`文件。

**文件访问权限**：该工具会读取用户指定的文件以进行哈希计算。配置文件中仅声明了配置路径和输出路径；工具会读取你通过`/cv hash`、`/cv verify`或`/cv packet`提供的任何文件路径。请注意处理敏感文件时的安全性。

## 功能说明**

AI代理有时会使用过时的数据（例如，修改了但在读取后被更改的文件，或者依赖已失效的缓存内容）。该工具通过以下方式防止这些问题：
1. 在操作前后计算文件的哈希值。
2. 检测文件在读取和写入之间的变化。
3. 生成包含可验证校验和的上下文数据包，以便后续审核。

**使用建议**：虽然可以信任系统，但仍需进行验证——因为你读取的文件可能与即将编辑的文件不同，请务必先进行检查。

## 命令列表

| 命令          | 功能                | 触发方式            |
|------------------|------------------|-------------------|
| /cv hash       | 计算文件的SHA256哈希值       | 显式调用            |
| /cv verify       | 验证文件的哈希值是否与预期匹配    | 显式调用            |
| /cv tag        | 为文件分配严重性等级（critical, important, minor） | 显式调用            |
| /cv packet      | 创建包含文件元数据的JSON数据包    | 显式调用            |

## 参数说明

### /cv hash

| 参数          | 是否必填 | 说明                |
|------------------|------------------|-------------------|
| file          | 是                | 需要验证的文件路径          |
| --algorithm     | 否                | 哈希算法（仅支持sha256，MD5/SHA-1已被弃用） |

### /cv verify

| 参数          | 是否必填 | 说明                |
| file          | 需要验证的文件路径          |
| hash          | 预期的哈希值            |
| --algorithm     | 否                | 哈希算法（仅支持sha256）         |

### /cv tag

| 参数          | 是否必填 | 说明                |
| file          | 需要标记的文件路径          |
| severity       | 文件的严重性等级（critical, important, minor） | 可选                |

### /cv packet

| 参数          | 是否必填 | 说明                |
| files         | 需要处理的文件路径（逗号分隔）     |
| --name        | 数据包名称（可选）         | 默认自动生成          |
| --include-content | 是否包含文件内容       | 默认不包含文件内容     | （详见安全注意事项）       |

> **⚠️ 安全警告**：`--include-content`选项会将文件内容保存到磁盘。切勿对敏感文件（如`.env`、凭据、密钥文件）使用此选项。请参阅下面的[安全注意事项]。**

## 配置设置

配置信息按优先级顺序从以下文件加载：
1. `.openclaw/context-verifier.yaml`（OpenClaw标准配置）
2. `.claude/context-verifier.yaml`（Claude代码兼容性配置）
3. 系统默认配置（内置模式）

## 安全注意事项

- 所有哈希计算都在本地使用标准的SHA256算法完成，不会将文件内容发送到任何大型语言模型（LLM）、API或外部服务。
- 该工具仅用于解析命令，不会处理文件内容。
- 该工具不会将文件内容发送到任何模型或API，也不会调用外部服务。
- 该工具仅写入`output/context-packets/`目录。

**重要提示**：与其他工具不同，`context-verifier`会读取用户指定的任意文件。配置文件中仅声明了配置和输出路径。例如，当你运行`/cv hash myfile.go`时，即使该文件未在配置文件中列出，工具也会读取它。这是为了确保能够验证用户实际需要验证的文件。

**安全使用建议**：
- 对于敏感文件（如`.env`、凭据文件），请勿使用`--include-content`选项，因为这会导致文件内容被保存到磁盘。
- 请将`output/context-packets/`目录添加到`.gitignore`文件中，以防止意外提交敏感文件。

## 存储与数据保留策略

- 数据包保存在工作区的`output/context-packets/`目录中（仅限本地访问）。
- 数据包采用未加密的JSON格式保存。
- 数据包不会自动删除，需要手动清理。
- 在敏感环境中，建议限制`output/`目录的访问权限，或使用加密文件系统，并定期清理旧数据包。

## 开发者信息

该工具由Live Neon（https://github.com/live-neon/skills）开发，并通过leegitw账户发布在ClawHub平台上。开发者为同一人。

## 核心逻辑

- **哈希计算**：使用默认的SHA-256算法。

### 严重性分类

文件会根据可配置的模式自动分类：

| 严重性等级 | 对应的模式                | 处理方式                |
|-----------|------------------|-------------------|
| critical    | `*.env`, `*credentials*`, `*secret*`     | 禁止操作                |
| important   | `*.go`, `*.ts`, `*.md`（文档相关文件） | 提示用户注意             |
| minor     | `*.log`, `*.tmp`, `output/*`       | 仅记录日志               |

**重要文件的模式可以通过`.openclaw/context-verifier.yaml`进行配置。**

## 数据包结构

## 输出结果

- `/cv hash`的输出结果
- `/cv verify`的匹配结果
- `/cv verify`的不一致结果
- `/cv tag`的标记结果
- `/cv packet`的数据包内容

## 集成方式

- 该工具属于基础层技能，无需依赖其他组件。
- 被`failure-memory`（用于检测文件变化）和`constraint-engine`（用于预操作检查）等工具所使用。

## 错误处理方式

- 如果文件未找到，会显示错误信息：“文件未找到：{path}”。
- 如果权限不足，会显示错误信息：“无法读取文件：{path}”。
- 如果哈希格式无效，会显示错误信息：“哈希格式无效。预期格式：{algorithm}”。
- 如果匹配到的文件不存在，会显示警告信息：“没有文件符合模式：{glob}”。

## 使用建议

- 使用后，请根据实际情况采取相应操作（例如，提示用户重新读取文件、阻止操作或进行验证）。

## 工作区文件

该工具会读取和写入以下文件：

## 示例用法

- 在编辑文件前验证文件内容。
- 为代码重构创建上下文数据包。
- 为敏感文件分配严重性等级。
- 在部署数据库迁移前进行验证。
- 生成API架构的验证数据包。

## 验收标准

- 能够计算文件的SHA-256哈希值。
- 能够将文件哈希值与预期值进行比较。
- 能够清晰地显示匹配或不一致的情况。
- 能够根据模式自动分配文件的严重性等级。
- 能够生成包含文件元数据的JSON数据包。
- 支持使用通配符来指定文件路径。
- 严重文件的变化会触发相应的处理机制。
- 工作区的文件会被保存在指定的位置。

---

*该工具于2026年2月15日通过整合三个独立技能而开发完成。*
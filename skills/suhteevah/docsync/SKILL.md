---
name: docsync
description: 通过 Git 钩子从代码自动生成文档，并检测文档内容的变更。提供免费的 README 文件生成服务以及付费的实时文档更新服务。
homepage: https://docsync.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "📖",
      "primaryEnv": "DOCSYNC_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash"]
      },
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        },
        {
          "id": "tree-sitter",
          "kind": "brew",
          "formula": "tree-sitter",
          "bins": ["tree-sitter"],
          "label": "Install tree-sitter (code parser)"
        },
        {
          "id": "difftastic",
          "kind": "brew",
          "formula": "difftastic",
          "bins": ["difft"],
          "label": "Install difftastic (semantic diff)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# DocSync — 为您的代码库提供实时更新的文档

DocSync 会根据您的代码自动生成文档，并保持文档的同步。它使用 `tree-sitter` 进行多语言的抽象语法树（AST）解析，通过 `lefthook` 集成到 Git 钩子中，以及使用 `difftastic` 来检测代码的语义变化。

## 命令

### 免费 tier（无需许可证）

#### `docsync generate <文件或目录>`
为单个文件或目录生成一次性的 README 或 API 文档。

**执行方式：**
```bash
bash "<SKILL_DIR>/scripts/docsync.sh" generate <target>
```

**功能：**
1. 使用 `tree-sitter` 解析目标文件，提取符号（函数、类、导出项、类型、接口等）
2. 从 `<SKILL_DIR>/templates/` 中选择相应的模板
3. 在源代码旁边生成 Markdown 格式的文档文件

**示例用法：**
- “为 `src/utils/auth.ts` 生成文档” → 运行 `docsync generate src/utils/auth.ts`
- “为整个目录生成文档” → 运行 `docsync generate src/api/`
- “为这个项目创建 README” → 运行 `docsync generate .`

### Pro tier（29 美元/用户/月 — 需要 DOCSYNC_LICENSE_KEY）

#### `docsync drift [目录]`
检测文档的更新滞后情况——找出代码已更改但文档尚未更新的部分。

**执行方式：**
```bash
bash "<SKILL_DIR>/scripts/docsync.sh" drift [directory]
```

**功能：**
1. 从配置文件中验证许可证密钥
2. 使用 `tree-sitter` 解析所有源文件
3. 将提取的符号与现有文档进行比较
4. 报告：新出现的未记录的符号、文档中签名已更改但未更新的符号、以及文档中仍然存在的已删除的符号
5. 输出包含严重程度（严重/警告/信息）的差异报告

#### `docsync hooks install`
安装 Git 钩子，以便在每次提交时自动检查文档的更新滞后情况。

**执行方式：**
```bash
bash "<SKILL_DIR>/scripts/docsync.sh" hooks install
```

**功能：**
1. 验证 Pro+ 许可证
2. 将 `lefthook` 的配置文件复制到项目根目录
3. 安装 `lefthook` 的提交前钩子
4. 在每次提交时：分析待提交的文件；如果检测到严重差异，则阻止提交，并提供自动重新生成文档的选项

#### `docsync hooks uninstall`
移除 DocSync 的 Git 钩子。

```bash
bash "<SKILL_DIR>/scripts/docsync.sh" hooks uninstall
```

#### `docsync auto-fix [目录]`
自动为检测到文档滞后的文件重新生成文档。

```bash
bash "<SKILL_DIR>/scripts/docsync.sh" auto-fix [directory]
```

### Team tier（49 美元/用户/月 — 需要 DOCSYNC_LICENSE_KEY 和团队许可）

#### `docsync onboarding [目录]`
为新开发者生成全面的入职指南。

```bash
bash "<SKILL_DIR>/scripts/docsync.sh" onboarding [directory]
```

#### `docsync architecture [目录]`
生成展示模块关系和数据流的架构文档。

```bash
bash "<SKILL_DIR>/scripts/docsync.sh" architecture [directory]
```

## 支持的语言

DocSync 使用 `tree-sitter` 的语法解析器，支持以下语言：
- JavaScript / TypeScript（包括 JSX/TSX）
- Python
- Rust
- Go
- Java
- C / C++
- Ruby
- PHP
- C#
- Swift
- Kotlin

## 配置

用户可以在 `~/.openclaw/openclaw.json` 中配置 DocSync：

```json
{
  "skills": {
    "entries": {
      "docsync": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "outputDir": "docs",
          "templateOverrides": {},
          "excludePatterns": ["**/node_modules/**", "**/dist/**", "**/.git/**"],
          "languages": ["typescript", "python", "go"],
          "driftThreshold": "warning",
          "autoFix": false
        }
      }
    }
  }
}
```

## 重要说明

- **免费 tier** 可立即使用，无需任何配置
- **Pro/Team tier** 需要从 https://docsync.pages.dev 获取许可证密钥
- 所有处理都在 **本地** 完成——不会将任何代码发送到外部服务器
- 许可证验证是 **离线的**——无需网络请求
- Git 钩子使用 `lefthook`，请确保已安装该工具（详见上面的安装说明）
- `tree-sitter` 和 `difftastic` 是可选的，但推荐使用以获得最佳效果；如果这些工具不可用，系统会回退到基于正则表达式的解析方式

## 错误处理

- 如果未安装 `tree-sitter`，系统会回退到基于正则表达式的符号提取方式（虽然准确性较低，但仍然可用）
- 如果未安装 `lefthook` 且用户尝试使用 `hooks install`，系统会提示安装该工具
- 如果许可证密钥无效或过期，系统会显示明确的信息，并提供前往 https://docsync.pages.dev/renew 的链接
- 如果某种语言的语法解析器不可用，系统会跳过该文件并显示警告

## 何时使用 DocSync

用户可能会提出以下需求：
- “为这个文件/项目生成文档”
- “我的文档是否是最新的？”
- “检查文档的更新滞后情况”
- “为我的提交设置自动文档生成功能”
- “生成入职指南”
- “记录代码库中的未记录内容”
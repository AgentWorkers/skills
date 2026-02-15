---
name: depguard
description: 依赖项审计、漏洞扫描以及许可证合规性检查。提供免费的漏洞检测服务，同时支持通过 Git 钩子（git hooks）实现付费的持续监控功能。
homepage: https://depguard.dev
metadata:
  {
    "openclaw": {
      "emoji": "🛡️",
      "primaryEnv": "DEPGUARD_LICENSE_KEY",
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
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# DepGuard — 依赖项审计与许可证合规性检查

DepGuard 会扫描您项目中的依赖项，以检测已知的漏洞、许可证违规以及过时的包。它使用原生包管理器审计工具（如 npm audit、pip-audit、cargo-audit 等），并通过许可证分析和风险评分来丰富审计结果。

## 命令

### 免费 tier（无需许可证）

#### `depguard scan [目录]`
对您项目中的依赖项进行一次性漏洞和许可证审计。

**执行方式：**
```bash
bash "<SKILL_DIR>/scripts/depguard.sh" scan [directory]
```

**功能：**
1. 检测包管理器（npm、yarn、pnpm、pip、cargo、go、composer、bundler、maven、gradle）的依赖项。
2. 运行原生审计命令（npm audit、pip-audit、cargo audit 等）。
3. 解析依赖项清单以获取许可证信息。
4. 生成包含风险级别的安全报告。
5. 列出存在问题或许可证未知的包。

**示例用法：**
- “扫描我的依赖项中的漏洞” → 运行 `depguard scan .`
- “检查我的 Node.js 模块的许可证” → 运行 `depguard scan . --licenses-only`
- “我的某些包是否不安全？” → 运行 `depguard scan`

#### `depguard report [目录]`
生成格式化的依赖项健康报告（markdown 格式）。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" report [directory]
```

### Pro tier（费用：19 美元/用户/月 — 需要 DEPGUARD_LICENSE_KEY）

#### `depguard hooks install`
安装 Git 钩子，在每次修改 lockfile 的提交时自动扫描依赖项。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" hooks install
```

**功能：**
1. 验证 Pro+ 许可证。
2. 安装 pre-commit 钩子，用于监控 lockfile 的变化。
3. 每当修改 package-lock.json、yarn.lock、Cargo.lock 等文件时，运行漏洞扫描；如果发现严重或高风险的漏洞，则阻止提交。

#### `depguard hooks uninstall`
卸载 DepGuard 的 Git 钩子。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" hooks uninstall
```

#### `depguard watch [目录]`
持续监控——在 lockfile 发生任何变化时自动重新扫描。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" watch [directory]
```

#### `depguard fix [目录]`
自动修复漏洞，将依赖项升级到已修复的版本（如果可用的话）。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" fix [directory]
```

### Team tier（费用：39 美元/用户/月 — 需要 DEPGUARD_license_KEY 并启用团队功能）

#### `depguard policy [目录]`
强制执行依赖项策略：禁止特定许可证，要求最低版本，拒绝特定包的安装。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" policy [directory]
```

#### `depguard sbom [目录]`
生成 CycloneDX 或 SPDX 格式的软件物料清单（Software Bill of Materials, SBOM）。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" sbom [directory]
```

#### `depguard compliance [目录]`
为审计人员生成合规性报告——将许可证分类为允许使用、copyleft、专有许可证或未知许可证。

```bash
bash "<SKILL_DIR>/scripts/depguard.sh" compliance [directory]
```

## 支持的包管理器

| 包管理器 | Lockfile | 审计工具 |
|---------|----------|------------|
| npm | package-lock.json | npm audit |
| yarn | yarn.lock | yarn audit |
| pnpm | pnpm-lock.yaml | pnpm audit |
| pip | requirements.txt / Pipfile.lock | pip-audit / safety |
| cargo | Cargo.lock | cargo audit |
| go | go.sum | govulncheck |
| composer | composer.lock | composer audit |
| bundler | Gemfile.lock | bundle audit |
| maven | pom.xml | mvn dependency-check |
| gradle | build.gradle | gradle dependencyCheck |

## 配置

将以下配置添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "depguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "blockedLicenses": ["GPL-3.0", "AGPL-3.0"],
          "allowedLicenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"],
          "ignoredVulnerabilities": [],
          "autoFix": false,
          "sbomFormat": "cyclonedx"
        }
      }
    }
  }
}
```

## 重要说明

- **免费 tier** 可立即使用，无需配置。
- 所有扫描都在本地进行，使用原生包管理器审计工具。
- 许可证验证是离线的，不会发送任何数据到外部服务器。
- 如果原生审计工具不可用，系统会转而使用依赖项清单进行解析。
- 支持单仓库（monorepo）——扫描所有工作区/包。

## 何时使用 DepGuard

用户可能会使用以下命令：
- “扫描我的依赖项中的漏洞”
- “检查我的包的许可证”
- “我的某些 npm 包是否不安全？”
- “生成安全审计报告”
- “设置依赖项监控”
- “禁止项目中使用 GPL 许可证的包”
- “生成软件物料清单（SBOM）”
- “检查我们的项目是否符合许可证政策”
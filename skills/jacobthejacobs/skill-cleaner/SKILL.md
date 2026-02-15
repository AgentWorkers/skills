---
name: skill-cleaner
version: 2.4.0
description: 通过 VirusTotal 自动验证“可疑”技能，并通过 Bridge 将它们添加到安全允许列表中。
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🧹",
        "requires": { "env": ["VIRUSTOTAL_API_KEY"], "bin": ["openclaw"] },
        "category": "security",
      },
  }
command-dispatch: tool
command_tool: exec
command_template: "node --import tsx skills/skill-cleaner/scripts/clean.ts {args}"
tags: [security, trust, virus-total, scanner]
---
# Skill Cleaner

该工具会扫描您已安装的技能（programs），检测其中是否存在可疑的模式，并通过将疑似问题文件添加到安全允许列表（safety allowlist）中来修复这些误报（false positives）。

## 使用方法

运行该工具即可自动验证这些技能，并将疑似问题文件添加到安全允许列表中：

```bash
# Dry run (safe, just shows what would happen)
npx tsx ./skills/skill-cleaner/scripts/clean.ts

# Commit trust to safety allowlist for clean files
npx tsx ./skills/skill-cleaner/scripts/clean.ts --commit

# Full Security Fix: Trust clean files AND quarantine malicious ones
npx tsx ./skills/skill-cleaner/scripts/clean.ts --fix
```

## 主要功能

- **启发式扫描（Heuristic Scanning）**：使用 OpenClaw Core 扫描器来检测可疑的代码模式。
- **与 VirusTotal 集成（Integration with VirusTotal）**：将检测到的文件哈希值与 VirusTotal 的数据库进行比对，以评估文件的安全性。
- **自动允许列表机制（Automatic Allowlisting）**：通过安全网关（Gateway）自动将误报文件添加到允许列表中。
- **隔离机制（Quarantine）**：将病毒文件（VirusTotal 检测结果为“阳性”的文件）移动到 `.quarantine/` 文件夹中，以确保系统安全。

## 安全性说明

由于该工具需要高权限才能正常运行（作为安全工具使用），因此请注意以下安全细节：

- **安全网关（Safe Gateway）**：使用加固版的非外壳式网关（Gateway RPC）来验证文件的安全性，避免直接修改文件系统。
- **隐私保护（Privacy Protection）**：仅从您的 `.env` 文件中读取 `VIRUSTOTAL_API_KEY`，不会访问或泄露其他敏感信息。
- **验证过程（Verification Process）**：使用 OpenClaw 的内部安全模块对 `skills/` 目录进行实时扫描，并计算文件的哈希值以验证其安全性。

**审计建议（Audit Guidance）**：如果在 ClawHub 上看到“高权限”（High Privilege）提示，这是正常现象——因为该工具需要与系统安全核心模块进行交互。在正式应用任何更改之前，请务必先在测试模式下运行该工具以进行检查。
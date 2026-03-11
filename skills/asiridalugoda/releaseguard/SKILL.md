---
name: releaseguard
description: 使用 ReleaseGuard 对发布工件（release artifacts）进行扫描、加固、签名和验证——ReleaseGuard 是专为 dist/ 和 release/ 输出路径设计的工件策略管理工具。
homepage: https://github.com/Helixar-AI/ReleaseGuard
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["releaseguard"],"env":[]}}}
---
# ReleaseGuard 技能

ReleaseGuard 是一个用于管理软件构建产出的工具，它可以扫描构建结果中的敏感信息、配置错误以及供应链风险，对这些问题进行修复；生成软件物料清单（SBOM），对工件进行签名，并验证发布的完整性。

## 安装 ReleaseGuard

**推荐方式 — 使用 Homebrew（适用于 macOS/Linux，不支持远程脚本执行）：**

```bash
brew install Helixar-AI/tap/releaseguard
```

**替代方式 — 从 GitHub Releases 手动下载（使用前请先查看说明）：**

```bash
# 1. Review the install script before executing:
curl -sSfL https://raw.githubusercontent.com/Helixar-AI/ReleaseGuard/main/scripts/install.sh | less

# 2. If satisfied, run it:
curl -sSfL https://raw.githubusercontent.com/Helixar-AI/ReleaseGuard/main/scripts/install.sh | sh
```

**替代方式 — 直接下载二进制文件（无需使用 shell 脚本）：**

```bash
# Replace VERSION, OS, and ARCH as appropriate (linux/darwin, amd64/arm64)
curl -sSfL https://github.com/Helixar-AI/ReleaseGuard/releases/latest/download/releaseguard-VERSION-OS-ARCH.tar.gz \
  | tar -xz releaseguard
sudo mv releaseguard /usr/local/bin/releaseguard
```

> **注意：** 安装脚本遵循 MIT 许可协议，代码开源，可访问：
> https://github.com/Helixar-AI/ReleaseGuard/blob/main/scripts/install.sh
> 在敏感环境中执行前请务必仔细阅读并理解其工作原理。

---

## 外部服务

部分命令会与外部服务进行交互。具体交互方式会在每个命令的文档中详细说明。除非明确指定了相关选项，否则不会向外部发送任何数据：

| 功能 | 外部服务 | 触发条件 |
|---|---|---|
| CVE 信息补充 | OSV.dev（仅读，无需认证） | `sbom --enrich-cve` 或 `vex` |
| 无密钥签名 | Sigstore / Fulcio（需要 OIDC 令牌） | `sign --mode keyless` |
| 云混淆处理 | ReleaseGuard Cloud API | `obfuscate --level medium/aggressive` |
| SLSA 来源证明（L3 级别） | ReleaseGuard Cloud API | 仅适用于云环境 |

**凭证要求：** 无密钥签名功能需要 OIDC 令牌（可在 GitHub Actions、GitLab CI 等平台获取）。本地签名需要提供私钥文件（使用 `--key` 参数）。云相关功能需要 `RELEASEGUARD_CLOUD_TOKEN`。`check`、`fix`、`sbom`、`pack`、`report` 和 `verify` 命令默认不使用任何凭证。

---

## 命令说明

### Check / Scan — `releaseguard check <path>`

扫描指定路径下的工件并评估发布策略。**不进行任何外部网络调用。**

**常用命令：** "scan"、"check"、"audit"、"analyze release"、"inspect dist"、"any secrets"、"find vulnerabilities"

```bash
releaseguard check <path>
releaseguard check <path> --format json
releaseguard check <path> --format sarif --out results.sarif
releaseguard check <path> --format markdown --out report.md
```

- 默认输出格式：`cli`（人类可读格式）
- 其他支持格式：`json`、`sarif`、`markdown`、`html`
- 成功返回代码：0；失败返回非零代码

---

### Fix — `releaseguard fix <path>`

对工件应用安全的、可预测的加固处理。**不进行任何外部网络调用。**

**常用命令：** "fix"、"harden"、"apply fixes"、"remediate"、"auto-fix release"

```bash
releaseguard fix <path>
releaseguard fix <path> --dry-run   # preview without applying
```

---

### SBOM — `releaseguard sbom <path>`

生成软件物料清单（SBOM）。

**常用命令：** "sbom"、"software bill of materials"、"dependencies"、"generate bom"

**输出格式：** `cyclonedx`
- 使用 `--enrich-cve` 时，会向 OSV.dev 发送仅读请求；无需提供凭证

---

### Obfuscate — `releaseguard obfuscate <path>`

对工件进行混淆处理，以保护其中的信息。

**常用命令：** "obfuscate"、"strip symbols"、"protect binary"

**混淆级别：**
- `none` / `light`：仅在本地执行，不进行外部调用（适用于开源软件）
- `medium` / `aggressive`：会调用 ReleaseGuard Cloud API；需要 `RELEASEGUARD_CLOUD_TOKEN`

---

### Harden — `releaseguard harden <path>`

执行完整的加固流程：包括修复漏洞、混淆处理以及添加数字版权管理（DRM）保护。

**常用命令：** "full harden"、"harden release"、"full hardening pipeline"

---

### Pack — `releaseguard pack <path>`

将工件打包成标准格式的归档文件。

**常用命令：** "pack"、"package artifact"、"create archive"

---

### Sign — `releaseguard sign <artifact>`

对工件及其相关证据进行签名。

**常用命令：** "sign"、"cosign"、"keyless sign"、"sign artifact"

- **无密钥签名（`keyless`）** 会通过 Sigstore 的 Fulcio CA 和 Rekor 服务完成签名；签名过程完全离线进行
- **本地签名（`local`）**：密钥保存在本地

---

### Attest — `releaseguard attest <artifact>**

生成工件来源证明文件（符合 SLSA 标准）。

**常用命令：** "attest"、"provenance"、"slsa"、"in-toto"

---

### Verify — `releaseguard verify <artifact>**

验证工件的签名及发布策略的合规性。**验证过程无需任何凭证。**

**常用命令：** "verify"、"check signature"、"validate artifact"

---

### Report — `releaseguard report <path>**

导出扫描报告。**不进行任何外部网络调用。**

**常用命令：** "report"、"export report"、"compliance report"

---

### VEX — `releaseguard vex <path>`

使用 VEX 数据丰富软件物料清单（SBOM）。**仅向 OSV.dev 发送仅读请求。**

**常用命令：** "vex"、"vulnerability data"、"enrich sbom"

---

## 典型工作流程

### 快速扫描（无需网络连接，无需凭证）  
```bash
releaseguard check ./dist
```

### 完整的自动化流程（包含无密钥签名）  
```bash
releaseguard check ./dist
releaseguard fix ./dist
releaseguard sbom ./dist
releaseguard pack ./dist --out release.tar.gz
releaseguard sign release.tar.gz --mode keyless   # OIDC token required
releaseguard attest release.tar.gz
releaseguard verify release.tar.gz
```

### 离线流程（无需网络连接，使用本地密钥）  
```bash
releaseguard check ./dist
releaseguard fix ./dist
releaseguard sbom ./dist
releaseguard pack ./dist --out release.tar.gz
releaseguard sign release.tar.gz --mode local --key signing.key
```

---

## 配置设置  
```bash
releaseguard init   # creates .releaseguard.yml
```  
```yaml
# .releaseguard.yml
version: 2
scanning:
  exclude_paths:
    - test/fixtures
policy:
  fail_on: [critical, high]
```
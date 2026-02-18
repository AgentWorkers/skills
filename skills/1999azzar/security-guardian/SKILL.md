---
name: security-guardian
description: OpenClaw项目的自动化安全审计功能：使用Trivy工具扫描代码中硬编码的敏感信息（如API密钥、令牌）以及容器中的安全漏洞（CVE）。系统会生成结构化的报告，以帮助维护代码库的整洁性和安全性。
metadata: {"openclaw":{"requires":{"skills":["mema-vault"]}}}
---
# 安全守护者（Security Guardian）

一个用于自动化安全审计和凭证保护的系统。

## 核心工作流程

### 1. 秘密信息扫描（Secret Scanning）
扫描特定项目目录中是否存在硬编码的凭证。
- **工具**：`scripts/scan_secrets.py`
- **使用方法**：`python3 $WORKSPACE/skills/security-guardian/scripts/scan_secrets.py <项目路径>`
- **工作流程**：
    1. 对指定的项目或目录执行扫描。
    2. 如果发现敏感信息（退出代码为1）：
        - 查看相关文件及其行号。
        - **处理方式**：将敏感信息移至安全的存储库（例如使用 `mema-vault`）。
        - **替换方式**：用环境变量或存储库查询来替换源代码中的明文凭证。

### 2. 容器漏洞扫描（Container Vulnerability Scan）
在部署前分析 Docker 镜像中的漏洞。
- **工具**：`scripts/scan_container.sh`
- **使用方法**：`bash $WORKSPACE/skills/security-guardian/scripts/scan_container.sh <镜像名称>`
- **逻辑**：识别严重性为 “高”（HIGH）和 “危急”（CRITICAL）的漏洞，并建议更新基础镜像或应用安全补丁。

## 安全防护措施（Security Guardrails）
- **范围限制**：避免扫描系统级别的目录，仅针对相关的项目工作区进行扫描。
- **凭证隔离**：硬编码的凭证被视为高严重性的安全风险。
- **依赖项**：容器扫描需要在主机系统上安装 `trivy` 工具。

## 集成（Integration）
- **凭证管理**：该系统能够检测凭证泄露情况，应使用专门的凭证管理工具（如 `mema-vault`）进行修复。
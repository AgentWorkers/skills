---
name: sev-attestation
description: 执行 AMD SEV-SNP 远程认证，以加密方式验证虚拟机（VM）的身份和完整性。该功能可用于证明虚拟机正在真实的 AMD SEV-SNP 保密计算环境中运行；在将机密信息委托给虚拟机之前验证其完整性；检查 SEV-SNP 的可用性；生成认证报告；验证 AMD 证书链（ARK/ASK/VCEK）；以及调试认证过程中的故障。
---

# sev-attestation

AMD SEV-SNP（安全加密虚拟化 - 安全嵌套分页）用于对虚拟机（VM）的身份进行加密验证。

## 描述

使用 AMD SEV-SNP 进行远程验证，以加密方式确认虚拟机的身份和完整性。在以下情况下可以使用此功能：

- 证明虚拟机运行在真实的 AMD SEV-SNP 保密计算环境中
- 在将机密信息委托给虚拟机之前验证其完整性
- 检查 SEV-SNP 是否可用以及配置是否正确
- 生成用于远程验证的证明报告
- 验证 AMD 证书链（ARK → ASK → VCEK）
- 调试验证失败或证书相关的问题

**关键词**：SEV-SNP、验证、保密计算、AMD、VCEK、证书链、远程验证、虚拟机身份、TCB（可信计算基础）、测量

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEV-SNP Attestation Flow                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  1. Detection    │
                    │  Is SEV-SNP      │
                    │  available?      │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
        ┌─────────┐                   ┌─────────┐
        │   YES   │                   │   NO    │
        └────┬────┘                   └────┬────┘
             │                              │
             ▼                              ▼
    ┌─────────────────┐             ┌─────────────────┐
    │ 2. Generate     │             │ Exit with       │
    │    Report       │             │ helpful error   │
    └────────┬────────┘             └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. Display      │
    │    Report Info  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 4. Fetch AMD    │
    │    Certificates │
    │ (ARK, ASK, VCEK)│
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. Verify       │
    │    Cert Chain   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 6. Verify       │
    │    Report Sig   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   PASSED or     │
    │   FAILED        │
    └─────────────────┘
```

## 快速入门

### 检查 SEV-SNP 是否可用

```bash
./scripts/detect-sev-snp.sh
```

### 运行完整验证流程

```bash
./scripts/full-attestation.sh [output_dir]
```

该流程会执行完整的 6 个步骤，并输出“PASSED”或“FAILED”的结果。

## 单个步骤

每个步骤都可以独立运行，以便进行调试或自定义工作流程：

| 脚本 | 用途 |
|--------|---------|
| `scripts/detect-sev-snp.sh` | 检查 SEV-SNP 是否可用 |
| `scripts/generate-report.sh <output_dir>` | 生成包含随机数（nonce）的验证报告 |
| `scripts/fetch-certificates.sh <report_file> <output_dir>` | 从 AMD KDS 获取证书 |
| `scripts/verify-chain.sh <certs_dir>` | 验证证书链 |
| `scripts/verify-report.sh <report_file> <certs_dir>` | 验证报告签名 |

## 先决条件

- **snpguest**：来自 [virtee/snpguest](https://github.com/virtee/snpguest) 的 Rust 命令行工具
- **openssl**：用于证书操作
- **curl**：用于从 AMD KDS 获取证书
- **root 权限**：需要具有 `/dev/sev-guest` 的访问权限

安装 snpguest：
```bash
cargo install snpguest
```

## 参考文档

- [报告字段](references/report-fields.md) - 验证报告的字段说明
- [错误代码](references/error-codes.md) - 常见错误及故障排除方法
- [手动验证](references/manual-verification.md) - 不使用 snpguest 的 OpenSSL 基础验证方法

## 技术细节

- **AMD KDS URL**：`https://kdsintf.amd.com`
- **证书链**：ARK（自签名）→ ASK → VCEK
- **报告签名**：ECDSA P-384
- **设备**：`/dev/sev-guest`（需要 root 权限或属于 sev 组）
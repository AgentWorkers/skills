---
name: gog-safety
description: 构建并部署经过安全配置的 `gogcli` 二进制文件，这些文件会在编译时自动移除某些敏感命令。此方法适用于为权限受限的 AI 代理设置 `gog` 工具：用户可以选择 L1（仅草稿模式）、L2（协作模式）或 L3（标准写入模式）。文档内容涵盖了如何通过 Pull Request（PR）来构建这些安全配置的 `gogcli` 二进制文件。
---
# gog 安全配置文件

在构建和部署 `gog` 二进制文件时，会通过编译时配置来禁用某些命令。被禁用的命令将不会被包含在最终生成的二进制文件中，因此无法在运行时被重新启用。

## 快速入门

### 1. 选择安全级别

| 安全级别 | 适用场景 | 是否支持发送邮件/聊天？ |
|-------|----------|---------------------|
| **L1** | 邮件分类、草稿处理、收件箱整理 | 不支持 |
| **L2** | L1 的功能 + 评论、回复、协作工作 | 不支持 |
| **L3** | 全部写入权限，无危险的管理操作 | 支持 |

详细信息请参阅：`references/levels.md`

### 2. 构建

```bash
# Build for current platform
./scripts/build-gog-safe.sh L1

# Cross-compile for Linux ARM64 (e.g., AWS Graviton)
./scripts/build-gog-safe.sh L1 --arch arm64 --os linux

# Custom output
./scripts/build-gog-safe.sh L2 --output /tmp/gog-l2
```

**要求：** Go 1.22+ 和 git。首先克隆 PR #366 分支（大约需要 30 秒）。

### 3. 部署

```bash
# Deploy to a remote host via SSH
./scripts/deploy-gog-safe.sh spock /tmp/gogcli-safety-build/bin/gog-l1-safe

# Deploy with verification (tests blocked + allowed commands)
./scripts/deploy-gog-safe.sh spock /tmp/gogcli-safety-build/bin/gog-l1-safe --verify
```

部署脚本会执行以下操作：
- 备份现有的 `gog` 二进制文件到 `gog-backup`；
- 安装新的二进制文件；
- 验证版本信息；
- 可选地测试被禁用的命令是否已被移除，以及允许使用的命令是否能正常工作。

### 4. 回滚

```bash
ssh <host> 'sudo mv /usr/local/bin/gog-backup /usr/local/bin/gog'
```

## 工作原理

该系统利用了 `gogcli` 的编译时安全配置功能（PR #366，由 steipete/gogcli 提出）。通过一个 YAML 文件来指定哪些命令应该被启用（`true`），哪些命令应该被禁用（`false`）。构建系统会生成仅包含启用命令的 Go 源代码，然后进行编译。最终生成的二进制文件会带有 `-safe` 标签，以表明其安全性设置。

## YAML 配置文件

在 `references/` 目录下有以下配置文件：
- `l1-draft.yaml`：用于草稿处理和收件箱整理
- `l2-collaborate.yaml`：用于草稿处理和协作工作
- `l3-standard.yaml`：提供全部写入权限，但不支持管理操作

**自定义配置：** 可以复制任何 YAML 文件，修改其中的 `true`/`false` 标志，然后通过 `build-gog-safe.sh` 脚本进行构建。

## 验证

部署完成后，需要使用以下命令进行验证：
```bash
ssh <host> "gog --version"                     # Should show -safe suffix
ssh <host> "gog gmail send --help 2>&1"        # Should fail (L1/L2)
ssh <host> "gog gmail drafts create --help"    # Should work (all levels)
```

## 已知的边缘情况

- **邮件转发：** 在 L1+ 级别中，允许使用 `gmail settings filters create` 功能来管理邮件转发。带有转发功能的过滤器可能会自动转发邮件。这在 v1 版本中是被接受的风险。
- **驱动器共享：** 在 L1+ 级别中，允许使用 `drive share` 功能进行文件共享。因为共享操作不会发送通知邮件，所以共享用户可以在“与我共享”列表中看到共享内容，但不会收到通知邮件。
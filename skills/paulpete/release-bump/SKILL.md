---
name: release-bump
description: **使用说明：**  
在修复问题并准备好发布新版本后，若需要更新 `ralph-orchestrator` 的版本号（即进行版本升级），请按照以下步骤操作：  

1. 首先，确保所有相关的修复代码已被提交到版本控制系统（如 Git）。  
2. 接着，使用以下命令来更新 `ralph-orchestrator` 的版本号：  
   ```bash
   git tag ralph-orchestrator new_version_number
   ```
   其中 `new_version_number` 是你想要设置的新的版本号。  
3. 最后，使用以下命令将新的标签推送到远程仓库：  
   ```bash
   git push origin ralph-orchestrator:new_version_number
   ```
   这将使远程仓库中的 `ralph-orchestrator` 分支更新为新的版本号。  

**注意：**  
- 在执行上述操作之前，请确保你的团队成员已经了解了版本升级的详细信息，并且所有必要的测试和验证工作已经完成。  
- 如果版本升级可能会影响现有系统的稳定性，请在升级前进行充分的测试和备份。
---

# 版本升级（Version Bump）

## 概述

本流程用于升级 `ralph-orchestrator` 的版本并触发发布。所有版本信息都存储在 `Cargo.toml` 文件中，各个独立的库（crates）通过 `version_workspace = true` 来继承这些版本信息。

在升级版本之前，需要先与用户确认新版本的细节。一旦版本升级的提交（bump commit）被推送成功，系统会开始跟踪发布的进度。

## 快速参考

| 步骤 | 命令/操作 |
|------|----------------|
| 1. 升级版本 | 修改 `Cargo.toml` 文件：将所有 `version = "X.Y.Z"` 的值替换为新的版本号（共7处） |
| 2. 构建二进制文件 | 执行 `cargo build`（更新 `Cargo.lock` 文件） |
| 3. 运行测试 | 执行 `cargo test` |
| 4. 提交更改 | 使用 `git add Cargo.toml Cargo.lock` 后执行 `git commit -m "chore: bump to vX.Y.Z"` |
| 5. 推送代码到仓库 | 使用 `git push origin main` |
| 6. 创建版本标签 | 使用 `git tag vX.Y.Z` 并执行 `git push origin vX.Y.Z` |

## 版本信息的位置（全部在 `Cargo.toml` 中）

```toml
# Line ~17 - workspace version
[workspace.package]
version = "X.Y.Z"

# Lines ~113-118 - internal crate dependencies
ralph-proto = { version = "X.Y.Z", path = "crates/ralph-proto" }
ralph-core = { version = "X.Y.Z", path = "crates/ralph-core" }
ralph-adapters = { version = "X.Y.Z", path = "crates/ralph-adapters" }
ralph-tui = { version = "X.Y.Z", path = "crates/ralph-tui" }
ralph-cli = { version = "X.Y.Z", path = "crates/ralph-cli" }
ralph-bench = { version = "X.Y.Z", path = "crates/ralph-bench" }
```

**提示：** 可以使用文本编辑工具，并设置 `replace_all: true` 选项，将所有 `version = "OLD"` 替换为 `version = "NEW`，从而一次性更新所有7处版本信息。

## 持续集成（CI）的自动处理流程

当你推送版本标签后，`.github/workflows/release.yml` 脚本会自动执行以下操作：

1. 在 GitHub 上创建一个新的版本发布记录，并自动生成相关说明。
2. 为 macOS（arm64, x64）和 Linux（arm64, x64）平台构建二进制文件。
3. 将构建好的文件上传到 GitHub 的版本发布页面。
4. 按依赖关系顺序将二进制文件发布到 crates.io 平台。
5. 在 npm 上以 `@ralph-orchestrator/ralph` 的名称发布该软件包。

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| 只更新了 `workspace.package.version`，而忽略了其他地方 | 需要更新 `Cargo.toml` 中的所有版本信息，包括所有内部依赖的版本号。 |
| 忘记运行测试 | 提交代码之前务必执行 `cargo test`。 |
| 试图手动使用 `gh release create` 创建版本发布 | 只需推送版本标签即可，持续集成系统会自动完成发布流程。 |
| 先推送了标签再推送主分支（`main`） | 应先推送主分支（`main`），然后再推送版本标签。 |
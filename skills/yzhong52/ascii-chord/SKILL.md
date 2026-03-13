---
name: ascii-chord
description: 使用 `ascii_chord` CLI 工具显示 ASCII 格式的吉他和弦图。当有人询问如何弹奏某个吉他和弦时，或者需要查看任意和弦名称（例如 E、B7、Am、C、G、Dm 等）的和弦图时，可以使用该工具。安装此工具需要先安装 Git 和 Cargo（Rust 开发工具链）。首先，将 https://github.com/yzhong52/ascii_chord 仓库克隆到 `/tmp` 目录中，然后使用 Cargo 进行构建；如果需要，可以在运行之前查看源代码。
metadata:
  openclaw:
    requires:
      bins:
        - git
        - cargo
    sideEffects:
      note: >
        If the Rust toolchain is not installed, the SKILL.md suggests installing rustup — this modifies
        the user's home directory (~/.cargo, ~/.rustup) and may update PATH. cargo build also creates
        a target/ directory under /tmp/ascii_chord. These are normal Rust toolchain side effects
        and persist beyond a single invocation.
    thirdPartyCode:
      note: >
        This skill clones https://github.com/yzhong52/ascii_chord (MIT, authored by the same person as
        this skill) and builds it locally with `cargo run`. You are compiling and executing code fetched
        from GitHub. Review the repository before building if you have concerns. The repo is open-source
        and MIT licensed.
---
# ascii-chord

使用 [ascii_chord](https://github.com/yzhong52/ascii_chord) 显示 ASCII 格式的吉他和弦图谱——这是一个开源的 Rust 命令行工具（CLI），由与本技能相同的作者开发，采用 MIT 许可证。

## 所需工具

| 工具 | 用途 | 检查方法 |
|---|---|---|
| **git** | 克隆源代码仓库 | `git --version` |
| **cargo / Rust** | 构建并运行 CLI | `cargo --version` |

## 首次使用前的准备

本技能会将 `https://github.com/yzhong52/ascii_chord` 克隆到 `/tmp` 目录中，并使用 `cargo run` 进行构建。该工具会在您的机器上执行第三方代码。该仓库是开源的（MIT 许可证），由与本技能相同的作者开发，您可以在 [https://github.com/yzhong52/ascii_chord](https://github.com/yzhong52/ascii_chord) 查看其源代码。

### 安装 Rust（如果尚未安装）

```bash
# macOS (Homebrew — recommended)
brew install rustup-init && rustup-init
```

或者从 [rustup.rs](https://rustup.rs) 下载安装程序并按照说明进行安装。

> **注意：** 通过 rustup 安装 Rust 会在您的主目录下创建 `~/.cargo` 和 `~/.rustup` 文件，并可能修改您的 shell `PATH` 环境变量。这是 Rust 工具链的默认行为，在技能运行结束后这些设置也会保留。

### 克隆仓库

检查是否已经克隆了仓库；如果没有，请执行克隆操作：

```bash
[ -d /tmp/ascii_chord ] || git clone https://github.com/yzhong52/ascii_chord /tmp/ascii_chord
```

后续无需再进行任何安装步骤——`cargo run` 会一次性完成构建和运行。编译后的二进制文件会被缓存到 `/tmp/ascii_chord/target/` 目录中，后续运行时会重用这些文件。

## 使用方法

- **显示单个和弦：**
```bash
cd /tmp/ascii_chord && cargo run -- get <CHORD> 2>/dev/null
```

- **并排显示多个和弦：**
```bash
cd /tmp/ascii_chord && cargo run -- list <CHORD1> <CHORD2> ... 2>/dev/null
```

- **列出所有支持的和弦：**
```bash
cd /tmp/ascii_chord && cargo run -- all 2>/dev/null
```

## 示例

```bash
# Single chord
cd /tmp/ascii_chord && cargo run -- get Am 2>/dev/null

# Multiple side by side (great for progressions)
cd /tmp/ascii_chord && cargo run -- list C G Am F 2>/dev/null

# Full list of supported chord names
cd /tmp/ascii_chord && cargo run -- all 2>/dev/null
```

## 注意事项：

- 使用 `2>/dev/null` 可以抑制构建过程中的警告信息。
- 和弦名称区分大小写（例如 `Am` 和 `am` 是不同的，`B7` 和 `b7` 也是不同的）。
- 首次构建完成后，后续运行会更快（因为二进制文件会被缓存到 `/tmp/ascii_chord/target/`）。
- 源代码仓库：[https://github.com/yzhong52/ascii_chord](https://github.com/yzhong52/ascii_chord)（MIT 许可证）
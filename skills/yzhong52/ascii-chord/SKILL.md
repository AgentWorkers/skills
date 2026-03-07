---
name: ascii-chord
description: 使用 `ascii_chord` CLI 工具（来自 Yz 的 Rust 仓库）来显示 ASCII 格式的吉他和弦图。当有人询问如何弹奏某个吉他和弦时，或者需要查看任意和弦名称（例如 E、B7、Am、C、G、Dm 等）的和弦图时，可以使用这个工具。
---
# ascii-chord

该工具使用 https://github.com/yzhong52/ascii_chord 生成 ASCII 格式的吉他和弦图。

## 设置

项目仓库已克隆到 `/tmp/ascii_chord` 目录。如果该目录不存在，请先克隆它：

```bash
git clone https://github.com/yzhong52/ascii_chord /tmp/ascii_chord
```

## 使用方法

**显示单个和弦：**
```bash
cd /tmp/ascii_chord && cargo run -- get <CHORD> 2>/dev/null
```

**并排显示多个和弦：**
```bash
cd /tmp/ascii_chord && cargo run -- list <CHORD1> <CHORD2> ... 2>/dev/null
```

**列出所有支持的和弦：**
```bash
cd /tmp/ascii_chord && cargo run -- all 2>/dev/null
```

## 示例

```bash
cargo run -- get E
cargo run -- get B7
cargo run -- list C G Am F
```

## 注意事项：

- 使用 `2>/dev/null` 命令可以抑制编译器的警告信息。
- 和弦名称区分大小写（例如，`Am` 和 `am` 是不同的）。
- 有关所有支持的和弦的完整列表，请参阅仓库中的 `all_supported_chords.md` 文件。
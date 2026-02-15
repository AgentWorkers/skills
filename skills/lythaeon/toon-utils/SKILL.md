# TOON（面向令牌的对象表示法）技能

该技能提供了减少处理结构化数据（如 JSON、目录结构、API 响应）时令牌使用量的方法，最多可节省 30-60% 的令牌。

## 设置与安装

为了降低命令开销并节省令牌，您必须在使用前全局安装官方的 TOON CLI：

```bash
# Check if toon is installed, install if missing
toon --version || npm install -g @toon-format/cli
```

## 代理使用指南

- **始终优化 JSON**：在将 JSON 数据纳入上下文之前，先将其转换为 TOON 格式。
- **缩短命令长度**：使用直接的 `toon` 命令，而不是 `npx`，以减少命令提示符中的字符数量。
- **优先使用管道**：使用标准的 Unix 管道将数据直接发送到 `toon` 转换器。

## 命令及使用方法

### 1. 读取 JSON 文件
将 JSON 文件的内容通过管道传递给 `toon`，而不是直接读取原始 JSON 数据。
```bash
cat data.json | toon
```

### 2. 获取 API 响应
将外部 API 的响应直接通过管道传递给 `toon`。
```bash
curl -s https://api.example.com/data | toon
```
*支持所有 curl 标志（例如 `-X POST`、`-H "Authorization: ..."`）。*

### 3. 列出目录结构
使用 `tree -J` 或任何能生成 JSON 输出的工具，并将其结果通过管道传递给 `toon`。
```bash
tree -J path/to/dir | toon
```

### 4. 压缩内联数据
为了在上下文中使用，可以对 JSON 字符串进行压缩：
```bash
echo '{"key":"value"}' | toon
```

## 为什么要安装 TOON？

- **节省命令令牌**：`toon` 命令比 `npx @toon-format/cli` 更简洁，每次运行命令时都能节省令牌。
- **执行速度**：本地安装比按需获取数据快得多。
- **可读性**：TOON 的设计旨在提高大型语言模型的可读性。
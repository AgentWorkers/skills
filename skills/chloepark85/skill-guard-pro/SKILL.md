---
name: clawguard
description: "用于ClawHub技能的安全扫描工具。在安装之前，请先进行安全分析。"
license: "MIT"
metadata:
  { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["uv"] } } }
---
# ClawGuard 🛡️

**在安装前扫描 ClawHub 中的技能以检测安全风险。**

ClawGuard 会对 ClawHub 中的技能进行静态代码分析，以检测以下安全问题：
- 🌐 网络数据泄露（通过 HTTP POST 请求发送到外部 URL）
- 🔑 凭据访问（API 密钥、令牌、密码）
- ⚡ Shell 命令执行
- 💥 文件删除（如 `rm -rf`、`unlink`）
- 🎭 代码混淆（如 `eval()`、`base64` 解码）
- 👻 隐藏文件和目录

## 使用方法

### 按技能名称扫描
从 ClawHub 下载并扫描某个技能：
```bash
uv run {baseDir}/scripts/scan.py --skill <skill-name>
```

### 扫描本地目录
扫描您本地文件系统中的某个技能目录：
```bash
uv run {baseDir}/scripts/scan.py --path /path/to/skill
```

### JSON 输出
以 JSON 格式获取扫描结果：
```bash
uv run {baseDir}/scripts/scan.py --skill <skill-name> --json
```

## 示例

扫描 GitHub 上的技能：
```bash
uv run {baseDir}/scripts/scan.py --skill github
```

扫描本地的技能：
```bash
uv run {baseDir}/scripts/scan.py --path ~/.openclaw/skills/my-skill
```

## 风险等级

- 🟢 **安全** (0-30): 未检测到显著风险
- 🟡 **警告** (31-60): 安装前请仔细检查标记的项目
- 🔴 **危险** (61-100): 检测到高风险行为 — **切勿安装**

## 输出代码

- `0`: 安全
- `1`: 警告
- `2`: 危险

## 系统要求

- Python 3.11 或更高版本
- `uv`（Python 包管理工具）
- `clawhub` CLI（可选，用于下载技能）

## 工作原理

1. **模式匹配**：基于正则表达式检测危险代码模式
2. **AST 分析**：解析 Python 代码以检测 `eval()` 或 `exec()` 等操作
3. **URL 提取**：识别所有网络请求的终点地址
4. **风险评分**：根据风险程度进行评分（0-100）

## 检测内容

| 类别 | 分值 | 例子 |
|----------|--------|---------|
| 网络数据泄露 | 25 | 向未知 URL 发送 POST 请求 |
| 凭据访问 | 20 | 读取 API 密钥、令牌 |
| Shell 命令执行 | 15 | `exec()`、`subprocess`、`system()` 等函数 |
| 文件删除 | 15 | `rm -rf`、`unlink`、`rmdir` 等命令 |
| 代码混淆 | 15 | `eval()`、`atob()`、`Buffer.from` 等操作 |
| 隐藏文件 | 10 | 使用点文件（`.dot` 文件）或隐藏目录 |

## 限制

- **仅支持静态分析**：无法检测运行时行为
- **基于正则表达式**：可能存在误报或漏报
- **JavaScript/TypeScript**：仅支持基本模式匹配（不进行完整的 AST 分析）
- **加密/压缩的代码**：无法分析被混淆的代码

## 最佳实践

1. **在安装任何不受信任的技能之前务必进行扫描**
2. **手动检查被标记为“警告”级别的风险**
3. **检查网络请求的终点地址是否为已知域名**
4. **未经验证切勿安装被标记为“危险”的技能**
5. **向 ClawHub 的管理员报告可疑技能**

## 许可证

MIT 许可证
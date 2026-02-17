---
name: skill-scanner
description: 在安装 OpenClaw 的技能之前，请先扫描这些技能是否存在安全漏洞。此步骤适用于从 ClawHub 或任何第三方来源评估新技能时。该扫描能够检测到窃取凭证的工具、数据泄露行为、恶意 URL、混淆代码以及供应链攻击。
user-invocable: true
metadata: {"openclaw": {"emoji": "🔒", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 技能扫描器

在安装 OpenClaw 的技能之前，先扫描其中是否存在安全问题。在 ClawHub 上发现了 341 个恶意技能——不要成为下一个受害者。

## 该工具存在的必要性

ClawHub 市场上有 22% 至 26% 的技能被标记为包含漏洞。常见的攻击方式包括：
- 伪装成良性插件的密码窃取器
- **域名抢注**（使用与热门技能相似的虚假名称）
- 通过隐藏的 HTTP 请求进行数据泄露
- 用混淆代码隐藏恶意负载
- 通过 SKILL.md 文件内容进行提示注入（prompt injection）

## 命令

### 扫描本地技能目录
```bash
python3 {baseDir}/scripts/scanner.py scan --path ~/.openclaw/skills/some-skill/
```

### 直接扫描 SKILL.md 文件
```bash
python3 {baseDir}/scripts/scanner.py scan --file ./SKILL.md
```

### 以详细输出方式扫描
```bash
python3 {baseDir}/scripts/scanner.py scan --path ~/.openclaw/skills/some-skill/ --verbose
```

### 扫描所有已安装的技能
```bash
python3 {baseDir}/scripts/scanner.py scan-all
```

### 带有二进制校验和验证的扫描
```bash
python3 {baseDir}/scripts/scanner.py scan --path ~/.openclaw/skills/some-skill/ --checksum checksums.json
```

### 为二进制资产生成校验和
```bash
python3 {baseDir}/scripts/scanner.py checksum --path ~/.openclaw/skills/some-skill/ -o checksums.json
```

### 校验二进制文件的校验和与清单（manifest）是否一致
```bash
python3 {baseDir}/scripts/scanner.py checksum --path ~/.openclaw/skills/some-skill/ --verify checksums.json
```

### 以 JSON 格式输出结果
```bash
python3 {baseDir}/scripts/scanner.py scan --path ./skill-dir/ --json
```

## 扫描内容

### SKILL.md 文件分析：
- 可疑的 URL（非 HTTPS、IP 地址、URL 缩写工具）
- 提示注入模式（隐藏的指令、尝试覆盖系统设置）
- 请求密码、API 密钥或令牌
- 混淆或编码的内容（Base64、十六进制、Unicode 转义）

### 脚本分析：
- 网络调用（curl、wget、requests、urllib、fetch）
- 在预期路径之外的文件系统写入操作
- 访问环境变量（用于收集密码）
- 执行 Shell 命令（os.system、subprocess、exec）
- 混淆的字符串（Base64 解码、eval、exec）
- 数据泄露模式（将数据发送到外部 URL）
- 加密货币钱包相关代码
- 动态指令下载（远程 .md/.yaml/.json 文件）
- 远程代码执行模式
- 遥测数据泄露（将环境变量/配置/秘密信息输出到标准输出）
- 二进制/资产风险（预构建的可执行文件、编译后的代码、库注入）
- 在 subprocess 调用中使用 Shell（远程代码执行风险）
- 路径遍历漏洞（通过../ 序列进行目录遍历）

### 名称分析：
- 域名抢注检测（与已知的热门技能进行比较）
- 计算编辑距离以检测拼写错误和字符替换

### 二进制/资产校验和验证：
- 所有二进制文件（.exe、.dll、.so、.wasm、.pyc 等）的 SHA-256 校验和
- 为可信的技能版本生成校验和清单
- 在更新时验证二进制文件的校验和是否与预期一致
- 标记未经验证的文件或校验和不匹配的情况（检测篡改）

### 元数据分析：
- 过度的权限要求
- 可疑的安装脚本
- 似乎不必要的环境变量要求

## 风险等级：
- **CRITICAL** — 几乎可以肯定是恶意的。切勿安装。
- **HIGH** — 很可能是恶意的或风险极高。需要手动审核。
- **MEDIUM** — 发现可疑的模式。安装前请进行审核。
- **LOW** — 仅有轻微问题。可能安全，但仍需检查。
- **CLEAN** — 未检测到问题。可以安全安装。

## 提示：
- 在安装任何第三方技能之前，务必进行扫描。
- 即使结果是 “CLEAN”，也不能保证完全安全——该工具能检测到已知的恶意模式。
- 如果某个技能需要网络访问，请验证它所连接的域名。
- 将技能名称与已知的域名抢注情况进行交叉比对。
- 如果有疑问，请自行阅读源代码。
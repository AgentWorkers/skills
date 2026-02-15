---
name: skill-scanner
description: 在安装 OpenClaw 的技能之前，请先扫描这些技能以检测是否存在安全漏洞。此步骤适用于从 ClawHub 或任何第三方来源评估新技能时。该扫描能够识别出窃取凭证的工具、数据泄露行为、恶意 URL、混淆代码以及供应链攻击等安全风险。
user-invocable: true
metadata: {"openclaw": {"emoji": "🔒", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 技能扫描器

在安装 OpenClaw 技能之前，先扫描其中是否存在安全问题。在 ClawHub 上发现了 341 个恶意技能——别成为下一个受害者。

## 该工具的用途

ClawHub 市场上有 22% 至 26% 的技能被标记为含有漏洞。常见的攻击方式包括：
- 伪装成良性插件的密码窃取工具
- **域名抢注**（使用与热门技能相似的虚假名称）
- 通过隐藏的 HTTP 请求进行数据窃取
- 用混淆代码隐藏恶意负载
- 通过 SKILL.md 文件内容进行提示注入（即向用户显示虚假信息以窃取信息）

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

### 以 JSON 格式输出结果
```bash
python3 {baseDir}/scripts/scanner.py scan --path ./skill-dir/ --json
```

## 扫描内容

### SKILL.md 文件分析：
- 可疑的 URL（非 HTTPS、IP 地址、URL 缩短服务）
- 提示注入模式（隐藏的指令、尝试覆盖用户输入）
- 请求用户输入凭证、API 密钥或令牌
- 混淆或编码的内容（Base64、十六进制编码、Unicode 转义）

### 脚本分析：
- 网络调用（curl、wget、requests、urllib、fetch）
- 在非预期路径下的文件系统写操作
- 访问环境变量（用于收集用户凭证）
- 执行 Shell 命令（os.system、subprocess、exec）
- 混淆的字符串（Base64 解码、eval、exec）
- 数据窃取行为（将数据发送到外部 URL）
- 与加密货币钱包相关的代码
- 动态加载恶意代码（远程下载 .md/.yaml/.json 文件）
- 远程代码执行（远程代码执行）
- 数据泄露行为（将环境变量/配置信息输出到标准输出）
- 二进制文件/资产的安全风险（预编译的可执行文件、注入的库）
- 在 subprocess 调用中使用 `Shell=True`（存在远程代码执行风险）
- 路径遍历漏洞（通过 `../` 序列进行路径遍历）

### 名称分析：
- 检测域名抢注行为（与已知的热门技能进行比较）
- 通过计算编辑距离来识别拼写错误和字符替换

### 元数据分析：
- 过度的权限要求
- 可疑的安装脚本
- 显得不必要的环境变量需求

## 风险等级：
- **CRITICAL** — 几乎可以肯定属于恶意软件。请勿安装。
- **HIGH** — 很可能是恶意软件或风险极高。需要手动审核。
- **MEDIUM** — 发现了可疑的代码模式。安装前请进行审核。
- **LOW** — 仅有轻微问题。虽然可能安全，但仍需检查。
- **CLEAN** — 未检测到问题。可以安全安装。

## 使用提示：
- 在安装任何第三方技能之前，务必进行扫描。
- 即使结果显示为 “CLEAN”，也不能完全保证安全——该工具能检测到已知的恶意模式。
- 如果某个技能需要网络访问，请验证它所连接的域名。
- 将技能名称与已知的域名抢注情况进行比对。
- 如果有疑问，请自行阅读源代码。
---
name: skill-sandbox
description: 在安装之前，请在隔离环境中测试未经验证的技能（untrusted skills）。监控网络访问、文件系统写操作、环境变量读取以及子进程（subprocess）的调用。确保以安全的方式运行这些技能，避免危及你的代理（agent）的数据或凭据安全。
user-invocable: true
metadata: {"openclaw": {"emoji": "🏖️", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 技能沙箱（Skill Sandbox）

在受监控的环境中运行不可信的技能。在允许这些技能访问您的真实系统之前，您可以准确了解它们的行为。

## 为何需要这个功能

ClawHub 拥有数百种技能，其中一些可能是恶意的。即使使用 `arc-skill-scanner` 进行扫描，静态分析也无法检测到所有恶意行为。沙箱允许您运行技能的脚本，并观察它们在运行时的行为——例如：它们会发起哪些网络请求、访问哪些文件、读取哪些环境变量。

## 命令

### 将技能目录放入沙箱
```bash
python3 {baseDir}/scripts/sandbox.py run --path ~/.openclaw/skills/some-skill/
```

### 在沙箱中运行特定脚本
```bash
python3 {baseDir}/scripts/sandbox.py run --script ~/.openclaw/skills/some-skill/scripts/main.py
```

### 带网络监控运行
```bash
python3 {baseDir}/scripts/sandbox.py run --path ~/.openclaw/skills/some-skill/ --monitor-network
```

### 使用虚拟环境变量运行
```bash
python3 {baseDir}/scripts/sandbox.py run --path ~/.openclaw/skills/some-skill/ --fake-env
```

### 设置运行时间限制
```bash
python3 {baseDir}/scripts/sandbox.py run --path ~/.openclaw/skills/some-skill/ --timeout 30
```

### 生成安全报告
```bash
python3 {baseDir}/scripts/sandbox.py report --path ~/.openclaw/skills/some-skill/
```

## 监控内容

### 文件系统操作
- 打开的文件（读取/写入）
- 创建的目录
- 文件删除
- 权限更改

### 环境变量
- 被读取的环境变量
- 是否访问了敏感信息（如 API 密钥、令牌、密码）
- 可以注入虚拟值以观察技能对这些信息的处理方式

### 网络活动
- 出站 HTTP/HTTPS 请求（URL、方法、数据包）
- DNS 查询
- 套接字连接
- FTP、SMTP 等协议

### 进程执行
- 子进程调用
- Shell 命令
- 动态导入

## 安全模式

- **观察模式**（默认）：运行技能并记录所有操作，无任何限制。
- **限制模式**：阻止网络访问和文件系统写操作（仅允许在临时目录内进行）。
- **蜜罐模式**：提供虚拟凭据和端点，以检测技能是否尝试窃取数据。

## 输出结果

沙箱会生成一个 JSON 报告，其中包含：
- 所有的文件系统操作（读取、写入、删除）
- 所有访问的环境变量
- 所有的网络连接尝试
- 所有的子进程调用
- 对可疑行为的警告
- 安全评估结果（安全 / 可疑 / 危险）

## 集成方式

可以与工作流编排器结合使用，实现自动化的预安装检查：
```
scan skill → sandbox run → review report → install if safe → audit log
```

## 限制事项

- 仅支持 Python 技能（JavaScript 和 Shell 的支持正在规划中）
- 无法检测所有规避技术（如混淆代码或延迟执行）
- 网络监控要求技能使用标准的 Python 库
- 这不是一个真正的操作系统级沙箱（需要使用 Docker 来实现更高程度的隔离）
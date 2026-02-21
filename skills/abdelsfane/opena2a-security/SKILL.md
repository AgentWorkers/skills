---
name: opena2a-security
description: OpenClaw的安全加固功能：审核您的配置，扫描已安装的组件以检测恶意软件，识别CVE-2026-25253漏洞，检查凭据是否被泄露，并提供可操作的修复建议。该工具可在本地运行，无需调用任何外部API。
version: 1.0.0
requires:
  bins: [node, npx]
  env: []
  config: []
permissions:
  filesystem:
    - "~/.openclaw"
  network: []
  exec:
    - npx hackmyagent
tags: [security, audit, hardening, vulnerability-scanner, cve-detection, credential-protection, supply-chain]
---
# OpenA2A OpenClaw安全检查工具

该工具用于对OpenClaw安装环境进行安全审计和加固。它可以扫描配置文件、检测已知漏洞、检查已安装的技能模块中是否存在恶意代码，并提供具体的修复建议。

该工具完全在本地运行，不会将任何数据传输到外部服务器，也不需要使用API密钥。

## 可用的功能

### 快速安全检查

获取您当前安全状况的概览：

```
"Run a security audit on my OpenClaw setup"
```

```
"Is my OpenClaw configuration secure?"
```

```
"Check my OpenClaw for known vulnerabilities"
```

### CVE-2026-25253漏洞检测

检查您的OpenClaw实例是否容易受到WebSocket劫持（RCE）攻击（CVSS评分8.8）：

```
"Am I vulnerable to CVE-2026-25253?"
```

```
"Check for the OpenClaw WebSocket vulnerability"
```

### 模块扫描

扫描已安装的技能模块，查找恶意代码（如命令注入、数据泄露、混淆后的载荷、加密挖矿等行为）：

```
"Scan my installed skills for malware"
```

```
"Is the weather-bot skill safe?"
```

```
"Check all my skills for security issues"
```

### 凭据审计

检查是否存在暴露的凭据、过弱的文件权限以及明文存储的凭据：

```
"Are my API keys and tokens stored securely?"
```

```
"Check my credential file permissions"
```

### 配置加固

获取针对OpenClaw配置的具体加固建议：

```
"How do I harden my OpenClaw configuration?"
```

```
"What security settings should I change?"
```

## 工作原理

该工具使用了开源的安全扫描工具**HackMyAgent**，该工具针对OpenClaw提供了47项专门的安全检查项：

### 模块安全检查（6项）

| 检查项 | 检测内容 |
|-------|-----------------|
| SKILL-001 | 通过shell执行进行的命令注入 |
| SKILL-002 | 动态代码执行（eval、Function、vm） |
| SKILL-003 | 数据泄露至外部端点 |
| SKILL-004 | 混淆后的代码（base64、hex、charcode格式） |
| SKILL-005 | 加密挖矿的迹象 |
| SKILL-006 | 超出模块目录的路径遍历行为 |

### 凭据安全检查（4项）

| 检查项 | 检测内容 |
|-------|-----------------|
| CRED-001 | 通过网关API暴露的凭据 |
| CRED-002 | 具有全局可读权限的凭据文件 |
| CRED-003 | 未加密的明文凭据存储 |
| CRED-004 | 认证过程中的时间戳侧信道攻击 |

### 网关安全检查（4项）

| 检查项 | 检测内容 |
|-------|-----------------|
| GW-001 | 端点上缺少速率限制机制 |
| GW-002 | 易受SSRF攻击的URL请求处理函数 |
| GW-003 | 缺少或不完整的安全头部信息 |
| GW-004 | CVE-2026-25253 WebSocket劫持漏洞 |

### 供应链安全检查（4项）

| 检查项 | 检测内容 |
|-------|-----------------|
| SC-001 | 安装npm包时未使用`--ignore-scripts`选项 |
| SC-002 | 未签名的或预发布的依赖项 |
| SC-003 | 缺少技能模块的签名或哈希验证 |
| SC-004 | 存在已知危险的ClawHavoc恶意模块 |

## 执行扫描

当需要执行扫描时，请运行以下命令：

### 全面安全审计
```bash
npx hackmyagent secure ~/.openclaw
```

### 扫描特定模块
```bash
npx hackmyagent scan --skill <skill-name>
```

### 仅检测CVE漏洞
```bash
npx hackmyagent scan --cve ~/.openclaw
```

### 配置审计
```bash
npx hackmyagent audit ~/.openclaw/config.json5
```

### 生成安全报告

报告格式：text、json、sarif、html、asp

## 安全建议

在提供建议时，请参考以下优先级：

### 立即执行

1. **更新OpenClaw**至最新版本（修复CVE-2026-25253漏洞，保护凭据安全，采用时间戳安全的认证机制，阻止生命周期脚本的执行）。
2. **运行`npx hackmyagent secure`以识别当前的安全风险**。
3. **审查已安装的技能模块**——移除不再使用的模块。
4. **检查文件权限**——凭据文件应设置为0600权限（仅允许所有者读取）。

### 配置调整

根据需要修改`config.json`文件：

- 将`gateway.auth`设置为强密码（至少32个字符，随机生成）。
- 将`gateway.host`设置为`127.0.0.1`（仅限本地访问）。
- 禁用未使用的通道集成。
- 将`plugins.allowUnsafe`设置为`false`。
- 如果支持，启用Docker沙箱模式。

### 对于技能模块开发者

- 不要在技能模块代码中硬编码API密钥，应使用环境变量。
- 在`SKILL.md`文件的首页中明确声明所需的最低权限。
- 不要在处理用户输入时使用`eval()`、`Function()`或`child_process.exec()`函数。
- 安装过程中不要访问外部URL。

## 解读扫描结果

在向用户展示扫描结果时：

- **严重风险**需要立即处理——详细说明风险内容并提供修复命令。
- **高风险**建议在部署到生产环境之前解决。
- **中等风险**建议采取深度防御措施进行改进。
- **低风险**建议遵循最佳实践进行优化。

请始终用通俗的语言解释扫描结果。并非所有用户都是安全专家，请明确说明风险所在、可能被攻击的对象以及具体的修复方法。

## 背景信息

该工具由OpenA2A（opena2a.org）团队开发，他们为OpenClaw提交了6项安全修复补丁：

| PR编号 | 修复内容 |
|----|-----|
| #9806 | 模块代码安全扫描工具（19项检测规则，共1,721行代码） |
| #9858 | 保护网关WebSocket响应中的凭据安全 |
| #10525 | 修复A2UI文件服务中的路径遍历问题 |
| #10527 | 采用时间戳安全的认证机制 |
| #10528 | 在安装插件时阻止生命周期脚本的执行 |
| #10529 | 强制执行WhatsApp凭据的文件权限设置 |

扫描工具：https://www.npmjs.com/package/hackmyagent
来源代码：https://github.com/opena2a-org/hackmyagent
威胁模型：https://github.com/openclaw/trust/pull/7
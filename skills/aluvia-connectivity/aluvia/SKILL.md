---
name: aluvia
description: "防止你的AI代理被屏蔽。Aluvia通过真实的美国移动运营商IP（AT&T、T-Mobile、Verizon）来路由流量，从而使网站将你的代理视为人类用户。它可以自动绕过Cloudflare、DataDome、PerimeterX、Akamai Bot Manager等反机器人系统。当你的代理遇到403 Forbidden错误、Cloudflare的验证请求、CAPTCHA验证码、速率限制（429）、IP封禁、空响应或WAF（Web Application Firewall）的拦截时，可以使用该工具。该工具具备自动检测和绕过屏蔽功能、一键式IP轮换机制、美国地理定位功能、动态代理路由规则，以及通过Playwright管理的无头Chromium浏览器——所有这些功能都通过专为AI代理设计的基于JSON的命令行界面（CLI）来实现。"
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["aluvia"], "env": ["ALUVIA_API_KEY"] },
        "primaryEnv": "ALUVIA_API_KEY",
        "emoji": "🌐",
      },
  }
---
# Aluvia Proxy：通过代理和Playwright解除代理对代理浏览器的限制

## 问题

您的OpenClaw代理会被阻止，因为反机器人系统旨在阻止来自数据中心IP地址的代理/机器人流量。您可能会遇到403 Forbidden错误、CAPTCHAs、429速率限制、IP封禁或空响应等问题。

## 解决方案

Aluvia将您的代理流量路由到**真实的美国移动运营商IP地址**——这些IP地址被数百万真实用户在其手机上使用。网站无法区分您的代理和通过移动设备浏览的合法用户。

Aluvia结合了代理、Playwright和Chrome技术栈：能够检测到网站对代理的封锁，并在必要时将代理流量重新路由到合法的移动IP地址。所有操作都是自动完成的，无需配置代理或编写自定义路由规则。

## 主要特性

- **移动运营商的住宅IP地址**：使用的是真实的移动运营商IP地址，而非数据中心或共享的IP地址。这些IP地址受到网站的信任，属于最高质量的代理服务。
- **自动检测和绕过封锁**：每个页面加载的评分范围为0.0–1.0。能够检测到Cloudflare的封锁机制、CAPTCHAs、403/429错误、软封锁以及空页面。通过`--auto-unblock`选项，系统会自动通过代理重新路由并重新加载页面来解除封锁。
- **单命令IP轮换**：在会话过程中无需重启浏览器即可切换到新的移动IP地址，从而立即突破持续的封锁和速率限制。
- **美国地理位置定位**：可以将您的退出IP地址设置为特定的美国州（如加利福尼亚州、纽约州、德克萨斯州等），以便进行位置敏感的爬取和内容访问。
- **动态代理路由规则**：仅对需要代理的域名进行代理处理。当代理访问新网站时，可以动态添加或删除主机名。
- **使用Playwright管理的无头Chrome浏览器**：支持完整的浏览器会话，并提供Chrome DevTools Protocol (CDP)接口。无需进行任何浏览器设置或安装隐藏插件。
- **专为代理设计的JSON格式CLI**：所有命令都会以结构化的JSON格式返回结果，适用于AI代理的程序化调用，而非人类在终端中手动输入命令。

## 安装

```bash
npm install -g @aluvia/mcp
```

或者直接使用`npx`（无需安装）：

```bash
npx aluvia help
```

## CLI接口

- 每条命令都会将结果以JSON对象的形式输出到标准输出（stdout）。
- 成功返回退出代码`0`，失败返回`1`。错误时返回`{"error": "message"}`。
- CLI可以管理长时间运行的浏览器进程：启动会话、通过`exec`工具进行交互，并在会话结束后关闭进程。
- 页面加载的封锁评分范围为0.0–1.0：`blocked` >= 0.7表示被封锁，`suspected` >= 0.4表示疑似被封锁，`clear` < 0.4表示未被封锁。
- `--auto-unblock`选项会自动将需要绕过的域名添加到代理规则中并重新加载页面。

## 使用前的准备工作

在使用任何命令之前，请检查以下环境：

```bash
# 1. 确保API密钥已设置（切勿记录API密钥的完整值）
echo "${ALUVIA_API_KEY:0:8}..."

# 2. 确保CLI二进制文件可用
aluvia help --json

# 3. 确保已安装Playwright（用于浏览器会话）
node -e "require('playwright'"
```

如果API密钥缺失，请引导用户前往[Aluvia控制台](https://dashboard.aluvia.io)创建密钥，并设置`ALUVIA_API_KEY`。如果未找到`aluvia`模块，请运行`npm install @aluvia/mcp`；如果未安装Playwright，请运行`npm install playwright`。

## 核心命令快速参考

| 命令                          | 功能                                                                 | 常见用法                                                                 |
| --------------------------- | ---------------                                                                 | ----------------------------------------------------------------------------------- |
| `session start <url>`       | 启动一个无头浏览器会话                                                                 | `aluvia session start https://example.com --auto-unblock --browser-session my-task` |
| `session close`             | 关闭正在运行的会话                                                                 | `aluvia session close --browser-session my-task`                                                                 |
| `session list`              | 列出所有活跃的会话                                                                 | `aluvia session list`                                                                 |
| `session get`               | 获取会话详情、封锁检测结果和连接信息                                                                 | `aluvia session get --browser-session my-task`                                                                 |
| `session rotate-ip`         | 切换到新的上游IP地址                                                                 | `aluvia session rotate-ip --browser-session my-task`                                                                 |
| `session set-geo <geo>`     | 设置会话的地理位置                                                                 | `aluvia session set-geo us_ca --browser-session my-task`                                                                 |
| `session set-rules <rules>` | 向代理路由规则中添加域名                                                                 | `aluvia session set-rules "example.com,api.example.com" --browser-session my-task`                                                                 |
| `account`                   | 显示账户信息和余额                                                                 | `aluvia account`                                                                 |
| `account usage`             | 显示带宽使用情况                                                                 | `aluvia account usage`                                                                 |
| `geos`                      | 列出可用的地理位置目标                                                                 | `aluvia geos`                                                                 |
| `help`                      | 显示帮助信息（使用`--json`可获取结构化输出）                                                                 | `aluvia help --json`                                                                 |

## 标准工作流程

### 1. 启动会话

始终使用`--browser-session`参数为会话命名。除非需要手动控制封锁机制，否则请使用`--auto-unblock`选项：

```bash
aluvia session start https://example.com --auto-unblock --browser-session my-task
```

### 2. 解析JSON输出

启动命令会返回以下JSON格式的结果：

```json
{
  "browserSession": "my-task",
  "pid": 12345,
  "startUrl": "https://example.com",
  "cdpUrl": "http://127.0.0.1:38209",
  "connectionId": 3449,
  "blockDetection": true,
  "autoUnblock": true
}
```

请保存`browserSession`变量，后续命令都需要使用它。

**如果代理使用OpenClaw浏览器工具**：使用该会话的`cdpUrl`创建一个远程CDP配置文件，并在所有浏览器操作中使用该配置文件。详情请参阅[OpenClaw浏览器集成文档](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/integrations/openclaw-browser.md)。

### 3. 监控封锁情况

检查会话状态及最新的封锁检测结果：

```bash
aluvia session get --browser-session my-task
```

查看响应中的`lastDetection`对象。如果`blockStatus`为`"blocked"`且`--auto-unblock`选项处于启用状态，说明SDK已自动处理了封锁。如果封锁仍然存在，请采取进一步措施。

### 4. 在被封锁时切换IP地址

```bash
aluvia session rotate-ip --browser-session my-task
```

此命令会返回一个新的`sessionId`（UUID）。后续的请求将使用新的IP地址进行。

### 5. 设置地理位置目标（如需）

某些网站会根据地理位置提供不同的内容或采取不同的封锁措施：

```bash
aluvia session set-geo us_ca --browser-session my-task
```

### 6. 动态扩展代理规则

如果代理访问的新域名需要代理支持，请动态添加相应的规则：

```bash
aluvia session set-rules "newsite.com,api.newsite.com" --browser-session my-task
```

新规则会添加到现有规则中（而不会替换原有规则）。

### 7. 完成后关闭会话

**务必关闭会话**。会话会持续消耗系统资源，除非明确关闭：

```bash
aluvia session close --browser-session my-task
```

## 安全注意事项

在每次使用Aluvia时，请遵循以下规则：

1. **始终关闭会话**：无论任务是否完成，都应运行`session close`命令。如果不确定会话是否存在，请先使用`session list`查询。
2. **切勿泄露API密钥**：仅以名称形式引用`ALUVIA_API_KEY`，切勿记录、打印或将其值包含在输出中。
3. **在高成本操作前检查余额**：在进行长时间爬取任务前，请使用`aluvia account`查看余额。
4. **限制IP轮换尝试次数**：如果尝试三次切换IP地址仍无法解除封锁，请停止操作并报告问题（某些网站可能使用其他方式识别用户）。
5. **优先使用自动解除封锁功能**：让SDK自动处理封锁检测和解除措施。仅在需要手动控制路由决策时才禁用该功能。
6. **优先使用无头模式**：除非需要调试，否则始终使用无头模式（headless mode）。无头模式更快且更节省资源。
7. **解析退出代码**：务必检查退出代码。如果退出代码为1，请解析`error`字段并相应处理错误，切勿盲目重试。
8. **使用有名称的会话**：为每个会话指定名称（如`--browser-session my-task`），以避免混淆。
9. **失败后进行清理**：如果任何步骤失败，请先关闭会话后再尝试或终止任务。必要时可以使用`session close --all`。
10. **每个任务使用一个会话**：除非任务需要同时访问多个网站，否则不要同时启动多个会话。

## 参考资料

有关详细命令说明、工作流程和故障排除信息，请参阅以下文档：

- **命令参考**：[docs/command-reference.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/command-reference.md) — 所有11个命令的参数、输出格式和错误信息。
- **工作流程指南**：[docs/workflows.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/workflows.md) — 常见场景的逐步操作指南。
- **故障排除**：[docs/troubleshooting.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/troubleshooting.md) — 错误信息、封锁等级解释及恢复步骤。
- **代理与浏览器集成**：[docs/integrations/agent-browser.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/integrations/agent-browser.md) — 如何将Aluvia与[agent-browser](https://www.npmjs.com/package/agent-browser)结合使用。
- **OpenClaw浏览器集成**：[docs/integrations/openclaw-browser.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/integrations/openclaw-browser.md) — 如何将Aluvia与[OpenClaw浏览器工具](https://docs.openclaw.ai/tools/browser)集成。
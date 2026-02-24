---
name: aluvia
description: "防止你的AI代理被屏蔽。Aluvia通过真实的美国移动运营商IP（AT&T、T-Mobile、Verizon）来路由流量，使网站将你的代理视为人类用户。它可以自动绕过Cloudflare、DataDome、PerimeterX、Akamai Bot Manager等反机器人系统。当你的代理遇到403 Forbidden错误、Cloudflare的验证请求、CAPTCHA验证码、速率限制（429）、IP封禁、空响应或WAF（Web Application Firewall）的拦截时，可以使用该工具。它具备自动检测和绕过屏蔽功能、一键切换IP地址的功能、美国地理定位功能、动态代理路由规则，以及通过Playwright管理的无头Chromium浏览器——所有这些功能都通过专为AI代理设计的基于JSON的命令行界面（CLI）来实现。"
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

您的OpenClaw代理会被阻止，因为反机器人系统旨在阻止使用数据中心IP地址的基于云的代理/机器人流量。您会遇到403 Forbidden错误、CAPTCHAs、429速率限制、IP封禁或空响应等问题。

## 解决方案

Aluvia将您的代理流量路由到**真实的美国移动运营商IP地址**——这些IP地址被数百万真实用户在其手机上使用。网站无法区分您的代理和通过移动设备浏览的合法用户。

Aluvia结合了代理、Playwright和Chrome技术栈：能够检测到网站对代理的封锁，并在必要时将代理流量路由到新的移动IP地址。所有操作都是自动完成的，无需配置代理或编写自定义路由规则。

## 特点

- **移动运营商的住宅IP地址**：使用的是移动运营商的IP地址，而非数据中心或共享的住宅IP地址。这些IP地址受到网站的信任，属于最高质量的代理服务。
- **自动检测和绕过封锁**：每个页面加载的评分范围为0.0–1.0。能够检测到Cloudflare的挑战、CAPTCHAs、403/429错误、软封锁以及空页面。通过`--auto-unblock`选项，系统会自动通过代理重新路由并重新加载页面来解除封锁。
- **一键IP轮换**：在会话过程中无需重启浏览器即可切换到新的移动IP地址，从而立即突破持续的封锁和速率限制。
- **美国地理定位**：可以将您的出口IP地址设置为特定的美国州（如加利福尼亚州、纽约州、德克萨斯州等），以便进行位置敏感的抓取和内容访问。
- **动态代理路由规则**：仅对需要代理的域名进行代理处理。当代理访问新网站时，可以动态添加或删除主机名。
- **使用Playwright管理的无头Chrome浏览器**：提供完整的浏览器会话功能，并支持Chrome DevTools Protocol (CDP)接口。无需进行浏览器设置或安装任何隐藏插件。
- **专为代理设计的JSON格式CLI**：所有命令都会以结构化的JSON格式返回到标准输出（stdout）。适用于AI代理的程序化使用，而非人类在终端中手动输入命令。

## 安装

```bash
npm install -g @aluvia/cli
```

或者直接使用`npx`（无需安装）：

```bash
npx aluvia help
```

## CLI接口

- 每条命令都会将一个JSON对象输出到标准输出（stdout）。请使用相应的JSON解析工具进行解析。
- 出口代码：`0` 表示成功，`1` 表示错误。错误会返回`{"error": "message"}`。
- CLI可以管理长时间运行的浏览器进程：启动会话、通过`exec`工具进行交互，并在会话结束后关闭进程。
- 块检测评分范围为0.0–1.0：`blocked` >= 0.7表示被封锁，`suspected` >= 0.4表示疑似被封锁，`clear` < 0.4表示未被封锁。
- `--auto-unblock`选项会通过将主机名添加到代理规则并重新加载页面来自动处理大多数封锁情况。

## 使用前的准备

在使用任何命令之前，请验证环境：

```bash
# 1. 确保API密钥已设置（切勿记录完整的API密钥值）
echo "${ALUVIA_API_KEY:0:8}..."
```

```bash
# 2. 确保CLI二进制文件可用
aluvia help --json
```

```bash
# 3. 确保已安装Playwright（用于浏览器会话）
node -e "require('playwright')
```

如果API密钥缺失，请引导用户前往[Aluvia控制台](https://dashboard.aluvia.io)创建API密钥，并设置`ALUVIA_API_KEY`。如果找不到`aluvia`模块，请运行`npm install @aluvia/mcp`。如果缺少Playwright，请运行`npm install playwright`。

## 核心命令快速参考

| 命令                          | 功能                                      | 常见用法                                      |
| --------------------------- | ------------------------------------------------------- | --------------------------------------------------- |
| `session start <url>`         | 启动无头浏览器会话                              | `aluvia session start https://example.com --auto-unblock --browser-session my-task`         |
| `session close`            | 关闭正在运行的会话                              | `aluvia session close --browser-session my-task`                        |
| `session list`            | 列出所有活跃的会话                              | `aluvia session list`                               |
| `session get`            | 获取会话详情、封锁检测结果和连接信息                    | `aluvia session get --browser-session my-task`                        |
| `session rotate-ip`          | 切换到新的上游IP地址                              | `aluvia session rotate-ip --browser-session my-task`                        |
| `session set-geo <geo>`         | 设置会话的地理位置                            | `aluvia session set-geo us_ca --browser-session my-task`                        |
| `session set-rules <rules>`       | 向代理路由规则中添加主机名                            | `aluvia session set-rules "example.com,api.example.com" --browser-session my-task`        |
| `account`              | 显示账户信息和余额                              | `aluvia account`                                  |
| `account usage`            | 显示带宽使用情况                              | `aluvia account usage`                              |
| `geos`                | 列出可用的地理定位区域                            | `aluvia geos`                                  |
| `help`                | 显示帮助信息（使用`--json`可获取结构化输出）                    | `aluvia help --json`                                  |

## 标准工作流程

### 1. 启动会话

始终使用`--browser-session`参数为会话命名。除非需要手动控制封锁情况，否则请使用`--auto-unblock`选项：

```bash
aluvia session start https://example.com --auto-unblock --browser-session my-task
```

### 2. 解析JSON输出

启动命令会返回以下JSON格式的数据：

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

请保存`browserSession`值，后续命令都需要使用这个值。

**如果代理使用的是OpenClaw浏览器工具**：请使用该会话的`cdpUrl`创建一个远程CDP配置文件，并在所有浏览器命令中使用该配置文件。详情请参阅[OpenClaw浏览器集成文档](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/integrations/openclaw-browser.md)。

### 3. 监控封锁情况

检查会话状态及最新的封锁检测结果：

```bash
aluvia session get --browser-session my-task
```

查看响应中的`lastDetection`对象。如果`blockStatus`为`"blocked"`且`--auto-unblock`选项处于启用状态，说明SDK已经自动处理了封锁。如果封锁仍然存在，请采取进一步措施。

### 4. 在被封锁时切换IP地址

```bash
aluvia session rotate-ip --browser-session my-task
```

此命令会返回一个新的`sessionId`（UUID）。下次通过代理的请求将使用新的IP地址。

### 5. 设置地理位置（如有需要）

某些网站会根据地理位置提供不同的内容或采取不同的封锁措施：

```bash
aluvia session set-geo us_ca --browser-session my-task
```

### 6. 动态扩展路由规则

如果代理访问的新域名需要代理支持，请动态添加相应的规则：

```bash
aluvia session set-rules "newsite.com,api.newsite.com" --browser-session my-task
```

新规则会添加到现有规则中（而不会替换原有规则）。

### 7. 完成后关闭会话

**务必关闭会话**。会话会持续消耗系统资源，因此请在完成后关闭会话：

```bash
aluvia session close --browser-session my-task
```

## 安全注意事项

在每次使用Aluvia Proxy时，请遵循以下规则：

1. **务必关闭会话**：无论任务是否完成，都请运行`session close`命令。如果不确定会话是否存在，请先运行`session list`。
2. **切勿泄露API密钥**：仅以名称形式引用`ALUVIA_API_KEY`，切勿记录、打印或将其值包含在输出中。
3. **在高耗资源操作前检查余额**：在进行长时间抓取任务前，请运行`aluvia account`并查看余额。
4. **限制IP轮换尝试次数**：如果尝试三次切换IP地址仍无法解除封锁，请停止操作并报告问题（某些网站可能使用其他方式识别用户）。
5. **优先使用自动解除封锁功能**：让SDK自动处理封锁检测和解除措施。仅在需要手动控制路由决策时才禁用此功能。
6. **优先使用无头模式**：除非需要调试，否则请使用无头模式（headless mode）。无头模式更快且更节省资源。
7. **解析输出代码**：务必检查输出代码。当输出代码为1时，请解析`error`字段并相应处理错误，切勿盲目重试。
8. **使用有名称的会话**：为每个会话指定名称（如`--browser-session my-task`），以避免混淆。
9. **失败后进行清理**：如果任何步骤失败，请在重试或中止操作前关闭会话。作为最后手段，可以使用`session close --all`命令。
10. **每个任务使用一个会话**：除非任务明确需要同时访问多个网站，否则请避免启动多个会话。

## 参考资料

有关详细命令说明、工作流程和故障排除方法，请参考以下文档：

- **命令参考**：[docs/command-reference.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/command-reference.md) – 所有11个命令的参数、输出格式和错误信息。
- **工作流程指南**：[docs/workflows.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/workflows.md) – 常见场景的逐步操作指南。
- **故障排除**：[docs/troubleshooting.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/troubleshooting.md) – 错误信息、封锁等级解释及恢复步骤。
- **代理与浏览器集成**：[docs/integrations/agent-browser.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/integrations/agent-browser.md) – 如何将Aluvia与[agent-browser](https://www.npmjs.com/package/agent-browser) CLI集成。
- **OpenClaw浏览器集成**：[docs/integrations/openclaw-browser.md](https://github.com/aluvia-connect/aluvia-skills/blob/main/docs/integrations/openclaw-browser.md) – 如何将Aluvia与[OpenClaw浏览器工具](https://docs.openclaw.ai/tools/browser)集成。
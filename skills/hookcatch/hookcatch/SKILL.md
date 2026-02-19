---
name: hookcatch
description: 使用 HookCatch（一款面向开发者的 Webhook 测试工具）来测试 Webhook 并暴露本地服务。
user-invocable: true
metadata: {"openclaw":{"emoji":"🪝","requires":{"bins":["hookcatch"],"env":["HOOKCATCH_API_KEY"]},"primaryEnv":"HOOKCATCH_API_KEY","homepage":"https://hookcatch.dev","install":[{"id":"npm","kind":"node","packages":["hookcatch"],"bins":["hookcatch"],"label":"Install HookCatch CLI (npm)"}]}}
---
# HookCatch - 用于 OpenClaw 的 Webhook 测试与本地隧道工具

HookCatch 是一款 Webhook 测试和本地隧道工具，可帮助您：
- 创建用于捕获和检查 HTTP 请求的 Webhook 工具箱（bins）；
- 在本地建立隧道以测试 Webhook；
- 以编程方式管理和查看捕获的请求。

非常适合用于测试与 OpenClaw 技能集（如 Stripe、Twilio、GitHub 等）相关的 Webhook 集成。

## 快速入门

1. **使用 HookCatch 进行身份验证：**
   ```bash
   hookcatch login
   # 或者使用 API 令牌（推荐用于自动化）：
   hookcatch token generate
   export HOOKCATCH_API_KEY="hc_live_..."
   ```
   
2. **创建一个 Webhook 工具箱：**
   ```bash
   hookcatch bin create --name "Test Stripe Webhooks"
   # 返回结果：https://hookcatch.dev/b/abc123xyz
   ```
   
3. **查看已创建的工具箱：**
   ```bash
   hookcatch bin list
   ```
   
4. **查看捕获的请求：**
   ```bash
   hookcatch bin requests abc123xyz --format json
   ```
   或者
   ```bash
   hookcatch bin requests --binId abc123xyz --format json
   ```

## 可用命令

### 工具箱管理

**创建新的 Webhook 工具箱：**
```bash
hookcatch bin create [--name "My Bin"] [--private] [--password "secret"] [--format json]
```
选项：
- `--name`：工具箱的名称（可选）
- `--private`：创建私有工具箱（需要 PLUS+ 订阅）
- `--password`：私有工具箱的密码（至少 4 个字符）
- `--format`：输出格式（推荐使用 `json` 以方便自动化处理）

返回结果：工具箱 ID、Webhook URL 和查看 URL。

**列出所有工具箱：**
```bash
hookcatch bin list [--format json]
```
显示所有工具箱及其请求计数和状态。

**获取某个工具箱的请求：**
```bash
hookcatch bin requests <binId> [--limit 50] [--format json|table] [--method GET] [--password "secret"]
```
选项：
- `--limit`：获取的请求数量（默认：50）
- `--format`：输出格式：`json`（用于脚本）或 `table`（用于查看）
- `--method`：按 HTTP 方法过滤请求（GET、POST 等）
- `--password`：私有工具箱的密码（如需要）

**查看单个请求：**
```bash
hookcatch request <requestId> <binId> [--format json|pretty] [--password "secret"]
```

**删除工具箱：**
```bash
hookcatch bin delete <binId> --yes
```

**更新工具箱：**
```bash
hookcatch bin update <binId> --name "New Name"
hookcatch bin update <binId> --private --password "secret123"
hookcatch bin update <binId> --public
```

**重新发送请求到新 URL：**
```bash
hookcatch replay <binId> <requestId> <url>
hookcatch replay --binId <binId> --requestId <requestId> --url <url>
```

### 本地隧道

**暴露本地主机：**
```bash
hookcatch tunnel 3000
# 创建的隧道地址：https://hookcatch.dev/tunnel/xyz789
```

**列出活跃的隧道：**
```bash
hookcatch tunnel list
```

**停止隧道：**
```bash
hookcatch stop <tunnelId>
```
将外部请求转发到本地端口 3000。

**隧道使用限制：**
- **免费账户**：每次会话 5 分钟，每天 3 次
- **PLUS 订阅**：每次会话 1 小时，无限制
- **PRO/ENTERPRISE 订阅**：无限制

### API 令牌管理

**生成长期有效的 API 令牌：**
```bash
hookcatch token generate
# 将令牌存储以供自动化使用
export HOOKCATCH_API_KEY="hc_live_..."
```

**检查令牌状态：**
```bash
hookcatch token status
```

**撤销令牌：**
```bash
hookcatch token revoke --yes
```

**账户信息：**
```bash
hookcatch status
hookcatch whoami
```

## OpenClaw 技能集的使用示例

### 示例 1：测试 Stripe Webhook
```bash
# 创建一个用于测试 Stripe Webhook 的工具箱
BIN_URL=$(hookcatch bin create --name "Stripe Test" --format json | jq -r '.url')

# 将此 URL 作为 Webhook 端点配置到 Stripe 控制面板
echo "将 Stripe Webhook 配置为：$BIN_URL"

# 等待 Webhook 请求...
sleep 10

# 获取并分析捕获的请求
hookcatch bin requests abc123xyz --format json | jq '.[] | {event: .body.type, amount: .body.data.object.amount}'
```

### 示例 2：测试本地 API
```bash
# 在本地端口 8000 启动 API 服务器
# python -m http.server 8000 &
```

**通过隧道暴露 API：**
```bash
hookcatch tunnel 8000 --password <password>
```
现在外部服务可以通过以下地址访问您的本地 API：
```bash
https://hookcatch.dev/tunnel/xyz789
```

### 示例 3：调试 GitHub Webhook
```bash
# 创建一个工具箱
hookcatch bin create --name "GitHub Webhooks"

# 在 GitHub 仓库设置中添加 Webhook URL
# 触发事件（推送、拉取请求等）

# 查看请求
hookcatch bin requests abc123xyz --method POST --limit 10
```

## 与 OpenClaw 技能集的集成

在构建需要测试 Webhook 的 OpenClaw 技能集时：
```javascript
// 在您的技能脚本中
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// 创建工具箱
const { stdout } = await execAsync('hookcatch bin create --format json');
const { binId, url } = JSON.parse(stdout);

// 在集成代码中使用 Webhook URL
console.log(`Webhook URL: ${url}`);

// 获取请求
const { stdout: requests } = await execAsync(
  `hookcatch bin requests ${binId} --format json`
);
const captured = JSON.parse(requests);

// 处理捕获的请求
for (const req of captured) {
  console.log(`${req.method} ${req.path}: ${JSON.stringify(req.body)}`);
}
```

## 环境变量

- `HOOKCATCH_API_KEY`：用于身份验证的 API 令牌（推荐用于自动化）
- `HOOKCATCH_API_URL`：可覆盖的 API URL（默认：https://api.hookcatch.dev）

## 对 OpenClaw 用户的好处

- **无需设置 ngrok**：使用 HookCatch 进行快速本地测试
- **详细检查 Webhook 数据**：清晰地查看 Stripe/Twilio 等服务发送的数据
- **适合自动化**：输出 JSON 格式，便于在技能集中进行解析
- **保护敏感数据**：使用密码保护私有工具箱
- **简单快捷**：一个命令即可创建工具箱或隧道

## 帮助资源

- **文档**：https://docs.hookcatch.dev
- **Discord 社区**：加入 OpenClaw 的 #hookcatch 频道
- **GitHub 仓库**：https://github.com/hookcatch/cli
- **邮箱支持**：support@hookcatch.dev

## 提示

1. **在技能集中使用 API 令牌**：生成一次令牌，并将其设置为 `HOOKCATCH_API_KEY`
2. **自动化时使用 JSON 格式**：在脚本中解析请求时始终使用 `--format json`
3. **对敏感数据使用私有工具箱**：进行生产环境测试时使用 `--private` 选项
4. **测试后清理**：使用 `hookcatch bin delete` 删除工具箱以遵守使用限制

---

**由 HookCatch 团队专为 OpenClaw 开发** 🪝
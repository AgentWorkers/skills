---
name: home-assistant-agent-secure
description: 使用 Assist (Conversation) API 安全地控制 Home Assistant 智能家居设备。该 API 将自然语言指令传递给 Home Assistant 内置的自然语言处理（NLU）功能，从而实现安全、高效且低成本的设备控制。专为受限权限的非管理员用户设计，以最大限度地减少访问风险。
metadata: {"openclaw":{"emoji":"🏠","requires":{"bins":["curl"],"env":["HOME_ASSISTANT_URL","HOME_ASSISTANT_TOKEN"]},"primaryEnv":"HOME_ASSISTANT_TOKEN"}}
---
# Home Assistant 代理（安全版）

通过向 Home Assistant 的对话（Assist）API 发送自然语言指令来控制智能家居设备。

**安全模型：** 该技能仅使用 `/api/conversation/process` 端点。**严禁** 使用令牌调用其他 Home Assistant API 端点。该令牌应属于一个受限制的非管理员用户，其访问权限仅限于特定的区域和设备。

## 重要安全规则

- **仅** 调用 `/api/conversation/process` — **严禁** 调用 `/api/states`、`/api/services`、`/api/config` 或其他任何端点
- **严禁** 输出或显示令牌值
- **严禁** 将令牌用于除上述 Assist API 调用之外的任何用途
- **严禁** 通过浏览器或 Web UI 登录 Home Assistant — **必须** 使用 API 令牌
- 如果用户请求无法被 Assist 处理，应直接告知用户，**严禁** 尝试通过其他 API 调用

## 重要提示：禁用受信任网络的登录绕过功能

如果您的 Home Assistant 实例使用了 `trusted_networks` 认证提供者，并且设置了 `allow_bypass_login: true`，那么本地网络中的任何代理或用户都可以无需密码即可以任何 Home Assistant 用户的身份登录（包括管理员）。这会完全绕过该技能的安全限制。

**解决方法：** 在 Home Assistant 的 `configuration.yaml` 文件中，将 `trusted_networks` 认证提供者的 `allow_bypass_login` 设置为 `false`，或者完全移除 `trusted_networks` 提供者。更改后请重启 Home Assistant。

## 设置

### 1. 创建一个受限制的 Home Assistant 用户

1. 在 Home Assistant 中进入 **设置 → 人员 → 添加人员**
2. 创建一个新的用户（例如 `openclaw-bot`）
3. **不要** 将其设置为管理员
4. 在 **设置 → 区域与分区** 中，仅分配该用户应该控制的区域
5. （可选）使用自定义组或仅限控制面板的权限来限制对该用户的设备访问权限

### 2. 生成长期有效的访问令牌

1. 以受限制的用户（`openclaw-bot`）身份登录 Home Assistant
2. 进入 **个人资料**（左下角）
3. 滚动到 **长期访问令牌** 部分
4. 点击 **创建令牌**，为其命名（例如 `openclaw`）
5. 立即复制令牌内容 — 令牌仅显示一次

### 3. 配置 OpenClaw

使用以下任意一种方法设置 `HOME_assISTANT_URL` 和 `HOME_assISTANT_TOKEN`。OpenClaw 会按照以下优先级顺序应用这些设置：环境变量 → `.env` 文件 → `openclaw.json` 配置文件。较高优先级的设置会覆盖较低优先级的设置。

**选项 A：.env` 文件（推荐）**

在 `~/.openclaw/.env` 文件中添加以下内容：

```bash
HOME_ASSISTANT_URL=https://your-ha-instance.local
HOME_ASSISTANT_TOKEN=your-restricted-user-token-here
```

URL 可以是主机名（例如 `https://homeassistant.local`）或 IP 地址（例如 `https://192.168.1.50:8123`）。

**选项 B：配置文件**

在 `~/.openclaw/openclaw.json` 文件的 `skills.entries` 部分添加以下内容：

```json
{
  "skills": {
    "entries": {
      "home-assistant-agent-secure": {
        "apiKey": "your-restricted-user-token-here",
        "env": {
          "HOME_ASSISTANT_URL": "https://your-ha-instance.local"
        }
      }
    }
  }
}
```

`apiKey` 字段会通过技能的 `primaryEnv` 声明自动映射到 `HOME_assISTANT_TOKEN`。

**选项 C：Shell 环境变量**

在您的 Shell 配置文件（例如 `~/.bashrc`、`~/.zshrc`）中添加以下内容：

```bash
export HOME_ASSISTANT_URL="https://your-ha-instance.local"
export HOME_ASSISTANT_TOKEN="your-restricted-user-token-here"
```

## 使用方法

以自然语言发送任何智能家居指令。该技能会直接将这些指令传递给 Home Assistant 的 Assist 功能：

```bash
curl -sk -X POST "$HOME_ASSISTANT_URL/api/conversation/process" \
  -H "Authorization: Bearer $HOME_ASSISTANT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "USER REQUEST HERE", "language": "DETECTED LANGUAGE CODE"}'
```

> `-k` 标志允许使用自签名证书连接到 Home Assistant 实例。如果您的 Home Assistant 使用了受信任的证书（例如 Let's Encrypt），则可以忽略此标志。

根据用户输入的语言设置 `language` 字段（例如 `"pl"` 表示波兰语，`"en"` 表示英语，`"de"` 表示德语等）。

### 示例

- “打开客厅的灯”（英语）
- “Włącz światło w salonie”（波兰语）
- “Schalte das Licht im Wohnzimmer ein”（德语）
- “厨房的温度是多少？”（波兰语）
- “关闭卧室的所有灯”（英语）

## 处理语言变化（主格形式）

许多语言具有语法变化，导致实体名称在自然语言表达中发生变化。Home Assistant 的实体名称通常采用基础/字典形式（主格形式），但用户在命令中可能会使用其他语法形式。

受影响的语言包括但不限于：
- **波兰语**：7 个格（例如 *drukarkę* → *drukarka*，*lampę* → *lampa*）
- **捷克语**：7 个格（例如 *tiskárnu* → *tiskárna*，*lampu* → *lampa*）
- **德语**：4 个格 + 冠词（例如 *den Drucker* → *Drucker*，*die Lampe* → *Lampe*）
- **芬兰语**：15 个格（例如 *tulostinta* → *tulostin*，*lamppua* → *lamppu*）
- **匈牙利语**：18 个格（例如 *nyomtatót* → *nyomtató*，*lámpát* → *lámpa*）
- **俄语**：6 个格（例如 *принтер**у*** → *принтер*，*ламп**у*** → *лампа*）
- **克罗地亚语/塞尔维亚语**：7 个格，与波兰语和捷克语类似

**示例：** 用户输入 “włącz drukarkę 3d”（波兰语宾格形式），但实际实体名称是 “drukarka 3d”（主格形式）。Home Assistant 的 Assist 功能可能无法识别该实体。

**重试策略：** 如果 Home Assistant 返回错误（`no_valid_targets`、`no(intent_match` 或提示未找到实体的消息），并且用户输入的语言存在语法变化：

1. 从命令中识别实体名称
2. 将带变化形式的单词转换为基础/字典/主格形式
3. 用正确的形式重新调用 API
4. 如果重试仍然失败，向用户报告错误

**重要提示：** 仅重试 **一次**。不要无限循环。如果主格形式的重试也失败，应告知用户实体未找到。

## 处理响应

响应内容存储在 `response.speech.plain.speech` 中。直接将其传达给用户：

- “灯已打开” → 成功
- “抱歉，我无法理解您的指令” → Assist 功能无法解析请求
- “抱歉，有多个设备名为 X” → 实体名称不明确

## 错误处理（`response_type: "error"`）

| 错误类型 | 应向用户说明的内容 |
|-------|----------------------|
| `no(intent_match` | 尝试使用主格形式进行重试（如果输入语言存在语法变化）。如果仍然失败：”Home Assistant 无法识别该指令。” |
| `no_valid_targets` | 尝试使用主格形式进行重试（如果输入语言存在语法变化）。如果仍然失败：”未找到该实体 — 请检查设备名称或在 Home Assistant 中添加别名。” |
| 多个匹配项 | “多个设备具有相同的名称 — 建议在 Home Assistant 中为该设备添加唯一别名。” |

## 故障排除

- **401 Unauthorized**：令牌无效或已过期。请从受限制用户的账户生成新的令牌。
- **连接被拒绝**：检查 `HOME_assISTANT_URL` 是否正确，以及 Home Assistant 是否可访问。
- **命令未被理解**：请重新表述请求，或确认该设备是否对受限制用户可见。
- **实体未找到**：受限制用户可能无权访问该设备/区域。请在 Home Assistant 中更新权限设置。

## API 参考

### 端点

```
POST /api/conversation/process
```

**注意：** 使用 `/api/conversation/process`，**严禁** 使用 `/api/services/conversation/process`。

### 请求体

```json
{
  "text": "turn on the kitchen lights",
  "language": "en"
}
```

波兰语示例：

```json
{
  "text": "włącz światło w salonie",
  "language": "pl"
}
```

### 成功响应

```json
{
  "response": {
    "speech": {
      "plain": {"speech": "Turned on the light"}
    },
    "response_type": "action_done",
    "data": {
      "success": [{"name": "Kitchen Light", "id": "light.kitchen"}],
      "failed": []
    }
  }
}
```
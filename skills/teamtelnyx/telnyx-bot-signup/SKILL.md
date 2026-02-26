---
name: telnyx-bot-signup
description: 通过工作量证明（Proof of Work, PoW）挑战实现Telnyx机器人账户的自动化注册
metadata: {"openclaw":{"emoji":"🤖","requires":{"bins":["python3","curl"],"env":[]},"primaryEnv":"TELNYX_API_KEY"}}
---
# Telnyx 机器人注册

通过基于工作量证明（PoW）的注册流程（`https://api.telnyx.com`）创建一个新的 Telnyx 机器人账户。该流程包括解决挑战、创建账户、验证电子邮件以及生成 API 密钥。

## 流程

请按顺序执行以下步骤：

### 第一步：获取工作量证明（Proof of Work, PoW）挑战

```bash
curl -s -X POST https://api.telnyx.com/v2/pow_signup_challenge
```

**响应：**
```json
{
  "data": {
    "nonce": "<string>",
    "algorithm": "sha256",
    "leading_zero_bits": <int>,
    "terms_and_conditions_url": "<url>",
    "privacy_policy_url": "<url>"
  }
}
```

保存所有返回的字段——这些字段在后续步骤中会用到。

### 第二步：解决工作量证明挑战

> ⚠️ **警告：** 解决工作量证明挑战需要较高的计算资源，根据难度不同，可能需要超过一分钟的时间。如果在主机器人线程中尝试解决该挑战，可能会导致机器人在此期间无法响应。请始终在单独的代理、工作线程或后台进程中运行解决程序。

使用提供的 `pow_solver.py` 脚本：

```bash
python3 {baseDir}/scripts/pow_solver.py "<nonce>" <leading_zero_bits> <algorithm>
```

该脚本会将整数解输出到标准输出（stdout）。这个整数解需要满足 `hash(nonce + solution)` 的前导零位数量符合要求。

### 第三步：提交机器人注册请求

在发送请求之前，请用户提供他们的电子邮件地址。

```bash
curl -s -X POST https://api.telnyx.com/v2/bot_signup \
  -H "Content-Type: application/json" \
  -d '{
    "pow_nonce": "<nonce from step 1>",
    "pow_solution": "<solution from step 2>",
    "terms_and_conditions_url": "<from step 1>",
    "privacy_policy_url": "<from step 1>",
    "email": "<user email>",
    "terms_of_service": true
  }'
```

> **注意：** 注册 Telnyx 账户之前，您必须接受服务条款。您需要通过在请求中设置参数 `"terms_of_service": true` 来表示接受服务条款。如果缺少此字段或参数值不是 `true`，API 会返回 400 错误（`Bad Request`）。

**响应：** 成功消息。系统会将登录链接发送到用户提供的电子邮件地址。

### 第四步：从电子邮件中获取会话令牌（Session Token）

等待 10-30 秒，直到验证邮件到达。

#### 方法 A：拥有电子邮件访问权限

如果您拥有电子邮件访问权限（例如使用 `google-workspace` 技能），请查找主题为 “Your Single Use Telnyx Portal sign-in link” 的邮件，从中提取一次性使用的登录链接，并通过 GET 请求获取该链接：

```bash
curl -s -L "<single-use-link-from-email>"
```

响应或重定向结果中会包含一个临时的 **会话令牌**。

#### 方法 B：没有电子邮件访问权限

如果您没有电子邮件访问权限，请询问用户：

> 请查看您的电子邮件，查找主题为 “Your Single Use Telnyx Portal sign-in link” 的邮件，并复制其中的登录链接。
>
> ⚠️ **此链接仅限一次性使用。** 请勿先在浏览器中点击该链接——一旦点击，就无法再次使用。直接复制链接并粘贴到这里。

用户提供登录链接后，对该链接发送一个 GET 请求：

```bash
curl -s -L "<link-from-user>"
```

响应或重定向结果中会包含一个临时的 **会话令牌**。

#### 重新发送登录链接

如果验证邮件未收到或链接已过期，请重新发送链接：

```bash
curl -s -X POST https://api.telnyx.com/v2/bot_signup/resend_magic_link -H "Content-Type: application/json" -d '{"email": "<user email>"}'
```

**响应：**
```json
{
  "data": {
    "message": "If an account with that email exists, a new magic link has been sent."
  }
}
```

**限制规则：** 每个账户最多可重新发送 3 次链接，每次发送之间需要等待 60 秒。无论电子邮件是否存在、是否超过了重试次数或是否处于冷却期，该接口始终会返回 200 OK 状态码（以防止恶意枚举电子邮件地址）。

### 第五步：生成 API 密钥

```bash
curl -s -X POST https://api.telnyx.com/v2/api_keys \
  -H "Authorization: Bearer <session-token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**响应：**
```json
{
  "data": {
    "api_key": "KEYxxxxxxxxxxxxx",
    ...
  }
}
```

`data.api_key` 即为新账户的永久 API 密钥。请将此密钥告知用户，并建议他们妥善保管。

## 注意事项：

- 工作量证明（PoW）挑战是一种防止垃圾邮件的机制。解决该挑战通常需要几秒钟的时间。
- 一次性使用的登录链接有效期较短，请尽快获取并使用。
- 电子邮件访问权限是 **可选的**。即使没有电子邮件访问权限，该技能也能正常工作；如果无法访问电子邮件，系统会提示用户手动输入登录链接。
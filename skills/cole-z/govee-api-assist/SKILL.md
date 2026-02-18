---
name: govee-control
description: >
  **无脚本的 Govee OpenAPI 设置与控制指南**  
  适用于用户需要获取 Govee API 密钥、连接 Govee 设备、查看设备状态，或通过安全密钥处理发送电源/亮度/颜色控制命令的场景。
---
# Govee OpenAPI（无需脚本）

仅使用手动的 `curl` 命令来控制 Govee 设备。

## Linux 系统要求

- 安装了 `bash` 的 Linux shell。
- 安装了 `curl` 工具。
- 能够访问 `https://developer-api.govee.com` 和 `https://developer.govee.com`。
- 拥有已关联设备的 Govee 账户。
- 可选：使用 `jq` 工具来美化 JSON 响应内容。

快速检查：

```bash
bash --version | head -n 1
curl --version | head -n 1
command -v jq >/dev/null && jq --version || echo "jq not installed (optional)"
```

## 必需的凭证

- `GOVEE_API_KEY`（必需）

## 获取 Govee API 密钥

1. 打开 `https://developer.govee.com/`。
2. 使用拥有这些设备的同一 Govee 账户登录。
3. 进入开发者控制台的 API 密钥管理页面。
4. 生成或申请一个 API 密钥，并将其复制下来。
5. 请妥善保管该密钥（将其视为密码一样保密）。

如果门户界面发生变化，请按照以下步骤操作：登录 Govee 开发者账户 → 查找 API 密钥管理 → 创建新的密钥。

## 保护本地存储（用户专属）

切勿将 API 密钥存储在技能文件、Git 仓库或聊天记录中。

为每个用户创建一个专门的密钥文件（除非明确需要以 root 权限运行，否则避免将其存储在 `/root` 目录下）：

```bash
mkdir -p "$HOME/.openclaw/secrets"
cat > "$HOME/.openclaw/secrets/govee.env" <<'EOF'
export GOVEE_API_KEY='<YOUR_API_KEY>'
EOF
chmod 600 "$HOME/.openclaw/secrets/govee.env"
```

请仅将此密钥变量加载到当前 shell 环境中（不要使用 `set -a` 命令）：

```bash
source "$HOME/.openclaw/secrets/govee.env"
```

## API 基本 URL

```bash
https://developer-api.govee.com/v1
```

## 先发现设备

在控制设备之前，先列出所有设备，并记录下每个设备的 `device` 和 `model` 信息：

```bash
curl -sS -X GET "https://developer-api.govee.com/v1/devices" \
  -H "Govee-API-Key: $GOVEE_API_KEY" \
  -H "Content-Type: application/json"
```

## 查看设备状态

```bash
curl -sS -X GET "https://developer-api.govee.com/v1/devices/state?device=<DEVICE>&model=<MODEL>" \
  -H "Govee-API-Key: $GOVEE_API_KEY" \
  -H "Content-Type: application/json"
```

## 控制命令

### 打开设备

```bash
curl -sS -X PUT "https://developer-api.govee.com/v1/devices/control" \
  -H "Govee-API-Key: $GOVEE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"device":"<DEVICE>","model":"<MODEL>","cmd":{"name":"turn","value":"on"}}'
```

### 关闭设备

```bash
curl -sS -X PUT "https://developer-api.govee.com/v1/devices/control" \
  -H "Govee-API-Key: $GOVEE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"device":"<DEVICE>","model":"<MODEL>","cmd":{"name":"turn","value":"off"}}'
```

### 调节亮度（1-100）

```bash
curl -sS -X PUT "https://developer-api.govee.com/v1/devices/control" \
  -H "Govee-API-Key: $GOVEE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"device":"<DEVICE>","model":"<MODEL>","cmd":{"name":"brightness","value":75}}'
```

### 设置 RGB 颜色

```bash
curl -sS -X PUT "https://developer-api.govee.com/v1/devices/control" \
  -H "Govee-API-Key: $GOVEE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"device":"<DEVICE>","model":"<MODEL>","cmd":{"name":"color","value":{"r":120,"g":180,"b":255}}}'
```

## 响应检查

成功的响应通常会返回以下状态码：

```json
{"code":200,"message":"Success"}
```

如果响应代码不是 `200`，则表示操作失败。

## 故障排除

- `401`：未经授权：密钥缺失、过期或无效。
- `429`：请求次数过多（达到速率限制）。
- 命令被拒绝：该设备不支持该命令（请参考 `supportCmds`）。
- 设备列表为空：该账户没有关联的设备。

## 安全规则

- 文档中仅使用占位符（如 `<DEVICE>`、`<MODEL>`、`<YOUR_API_KEY>`）。
- 不要在发布的文档或代码中包含真实的 API 密钥或设备 ID。
- 建议一次只控制一个设备，避免批量操作。
- 避免在聊天中粘贴 API 密钥。
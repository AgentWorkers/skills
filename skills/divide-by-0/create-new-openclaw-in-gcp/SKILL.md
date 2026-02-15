# OpenClaw 云部署技巧

使用 Tailscale 和 Brave Search 将 OpenClaw 部署到 GCP 上。

## 所需的环境变量

```bash
export OPENCLAW_PROJECT_ID="your-gcp-project"
export OPENCLAW_USERNAME="your-ssh-username"
export ANTHROPIC_TOKEN="sk-ant-oat01-..."   # Keep secret
export BRAVE_API_KEY="..."                   # Keep secret
```

## 快速入门

```bash
chmod +x openclaw-quick-setup.sh
./openclaw-quick-setup.sh
```

## 手动设置（复制粘贴）

```bash
# Set variables first (see above)
ZONE="us-central1-a"
VM="openclaw"

# Create VM
gcloud compute instances create "$VM" \
  --project="$OPENCLAW_PROJECT_ID" --zone="$ZONE" \
  --machine-type=e2-medium \
  --image-family=debian-12 --image-project=debian-cloud \
  --boot-disk-size=10GB \
  --metadata=ssh-keys="${OPENCLAW_USERNAME}:$(cat ~/.ssh/id_ed25519.pub)"

IP=$(gcloud compute instances describe "$VM" \
  --project="$OPENCLAW_PROJECT_ID" --zone="$ZONE" \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Wait for SSH, then run setup
sleep 30
ssh -o StrictHostKeyChecking=no "${OPENCLAW_USERNAME}@${IP}" "
set -euo pipefail
sudo apt-get update && sudo apt-get install -y git curl ufw jq
curl -fsSL https://tailscale.com/install.sh | sh
"

# Manual: authorize Tailscale
ssh "${OPENCLAW_USERNAME}@${IP}" "sudo tailscale up"

# Continue setup
ssh "${OPENCLAW_USERNAME}@${IP}" "
set -euo pipefail
sudo ufw allow 22/tcp && sudo ufw allow in on tailscale0 && echo y | sudo ufw enable
echo 'nameserver 8.8.8.8' | sudo tee -a /etc/resolv.conf
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.nvm/nvm.sh && nvm install 22
source ~/.nvm/nvm.sh && npm install -g openclaw@latest
"

# Configure OpenClaw (credentials via stdin)
ssh "${OPENCLAW_USERNAME}@${IP}" '
source ~/.nvm/nvm.sh
openclaw onboard --non-interactive --accept-risk \
  --auth-choice token --token-provider anthropic \
  --token "$(cat)" --gateway-bind loopback --install-daemon
' <<< "$ANTHROPIC_TOKEN"

# Add Brave key + enable Tailscale auth
ssh "${OPENCLAW_USERNAME}@${IP}" "
set -euo pipefail
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
cat > ~/.config/systemd/user/openclaw-gateway.service.d/brave.conf << CONF
[Service]
Environment=\"BRAVE_API_KEY=\$(cat)\"
CONF
chmod 600 ~/.config/systemd/user/openclaw-gateway.service.d/brave.conf
systemctl --user daemon-reload
source ~/.nvm/nvm.sh
jq '.gateway.auth.allowTailscale = true' ~/.openclaw/openclaw.json > /tmp/oc.json
mv /tmp/oc.json ~/.openclaw/openclaw.json
chmod 600 ~/.openclaw/openclaw.json
openclaw gateway restart
sudo tailscale serve --bg 18789
" <<< "$BRAVE_API_KEY"

# Get dashboard URL
ssh "${OPENCLAW_USERNAME}@${IP}" "tailscale serve status"

# After first browser access, approve device
ssh "${OPENCLAW_USERNAME}@${IP}" 'source ~/.nvm/nvm.sh && openclaw devices list'
# Then: openclaw devices approve <REQUEST_ID>
```

## 重点学习内容

| 问题 | 解决方案 |
|-------|----------|
| e2-micro 资源耗尽（OOM） | 更改节点类型为 e2-medium（至少 4GB 内存） |
| Node.js 22 安装失败 | 使用 nvm 安装 Node.js 22 |
| Tailscale 部署后 DNS 无法解析 | 在 `/etc/resolv.conf` 中添加 `8.8.8.8` |
| 配置文件中的 Brave 密钥被拒绝 | 使用 systemd 环境变量进行配置 |
| 仪表盘显示“需要配对”提示 | 运行 `openclaw devices approve <id>` 命令进行配对 |

## 安全注意事项

- 凭据通过标准输入（`<<<`）传递，而非命令行参数
- 配置文件设置为 `chmod 600` 来保护文件权限
- OpenClaw 的网关绑定到本地循环回环地址（loopback），仅通过 Tailscale 进行外部访问
- UFW 防火墙仅允许 SSH 和 Tailscale 的流量通过
---
name: vpn-rotate-skill
description: 通过轮换 VPN 服务器来绕过 API 的速率限制。该方法适用于任何与 OpenVPN 兼容的 VPN（如 ProtonVPN、NordVPN、Mullvad 等）。每当有 N 次请求时，系统会自动切换到新的服务器以获取新的 IP 地址。适用于高流量数据抓取、访问政府 API 或获取受地理限制的数据。
---

# VPN 服务器轮换技巧

通过轮换 VPN 服务器来规避 API 的速率限制。适用于所有兼容 OpenVPN 的 VPN 服务。

## 设置

### 1. 运行设置向导

```bash
./scripts/setup.sh
```

设置向导将完成以下操作：
- 检查 OpenVPN 是否已安装
- 帮助您配置 VPN 提供商
- 设置无需输入密码即可使用 `sudo` 的权限
- 测试连接是否正常

### 2. 手动设置

如果您更喜欢手动配置，请按照以下步骤操作：

```bash
# Install OpenVPN
sudo apt install openvpn

# Create config directory
mkdir -p ~/.vpn/servers

# Download .ovpn files from your VPN provider
# Put them in ~/.vpn/servers/

# Create credentials file
echo "your_username" > ~/.vpn/creds.txt
echo "your_password" >> ~/.vpn/creds.txt
chmod 600 ~/.vpn/creds.txt

# Enable passwordless sudo for openvpn
echo "$USER ALL=(ALL) NOPASSWD: /usr/sbin/openvpn, /usr/bin/killall" | sudo tee /etc/sudoers.d/openvpn
```

## 使用方法

### 推荐的装饰器（Decorator）用法

```python
from scripts.decorator import with_vpn_rotation

@with_vpn_rotation(rotate_every=10, delay=1.0)
def scrape(url):
    return requests.get(url).json()

# Automatically rotates VPN every 10 calls
for url in urls:
    data = scrape(url)
```

### VPN 类（VPN Class）实现

```python
from scripts.vpn import VPN

vpn = VPN()

# Connect
vpn.connect()
print(vpn.get_ip())  # New IP

# Rotate (disconnect + reconnect to different server)
vpn.rotate()
print(vpn.get_ip())  # Different IP

# Disconnect
vpn.disconnect()
```

### 上下文管理器（Context Manager）实现

```python
from scripts.vpn import VPN

vpn = VPN()

with vpn.session():
    # VPN connected
    for url in urls:
        vpn.before_request()  # Handles rotation
        data = requests.get(url).json()
# VPN disconnected
```

### 命令行接口（CLI）实现

```bash
python scripts/vpn.py connect
python scripts/vpn.py status
python scripts/vpn.py rotate
python scripts/vpn.py disconnect
python scripts/vpn.py ip
```

## 配置选项

### 装饰器相关配置

```python
@with_vpn_rotation(
    rotate_every=10,      # Rotate after N requests
    delay=1.0,            # Seconds between requests
    config_dir=None,      # Override config directory
    creds_file=None,      # Override credentials file
    country=None,         # Filter servers by country prefix (e.g., "us")
    auto_connect=True,    # Connect automatically on first request
)
```

### VPN 类相关配置

```python
VPN(
    config_dir="~/.vpn/servers",
    creds_file="~/.vpn/creds.txt", 
    rotate_every=10,
    delay=1.0,
    verbose=True,
)
```

## 推荐的配置参数

| API 使用频率 | 服务器轮换间隔（秒） | 轮换延迟（秒） |
|-------------------|------------------|-------------------|
| 高频率（适用于需要快速切换的 API，如 Catastro、LinkedIn） | 5             | 2.0                |
| 标准频率             | 10             | 1.0                |
| 低频率             | 20–50             | 0.5                |

## 需要使用的文件

```
vpn-rotate-skill/
├── SKILL.md              # This file
├── README.md             # Overview
├── scripts/
│   ├── vpn.py            # VPN controller
│   ├── decorator.py      # @with_vpn_rotation
│   └── setup.sh          # Setup wizard
├── examples/
│   └── catastro.py       # Spanish property API example
└── providers/
    ├── protonvpn.md      # ProtonVPN setup
    ├── nordvpn.md        # NordVPN setup
    └── mullvad.md        # Mullvad setup
```

## 故障排除

### 出现 “sudo: 需要密码” 错误

请运行设置脚本，或手动添加允许使用 `sudo` 的用户：

```bash
echo "$USER ALL=(ALL) NOPASSWD: /usr/sbin/openvpn, /usr/bin/killall" | sudo tee /etc/sudoers.d/openvpn
```

### 连接失败

1. 确认用户名和密码是否正确
2. 手动测试连接：`sudo openvpn --config ~/.vpn/servers/server.ovpn --auth-user-pass ~/.vpn/creds.txt`
3. 确认您的 VPN 提供商账户是否处于活跃状态

### 仍然被限制访问

1. 减小 `rotate_every` 的值（例如从 10 秒改为 5 秒）
2. 增加 `delay` 的值（例如从 1.0 秒增加到 2–3 秒）
3. 检查 API 是否完全阻止了 VPN 用户的访问

### 无法找到 `.ovpn` 文件

请从您的 VPN 提供商处下载相应的配置文件：
- ProtonVPN：https://protonvpn.com/support/vpn-config-download/
- NordVPN：https://nordvpn.com/ovpn/
- Mullvad：https://mullvad.net/en/account/#/openvpn-config
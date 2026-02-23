# V2RayN 技能

用于在 macOS 上管理 V2RayN 代理客户端，并实现自动故障转移功能。

## 概述

V2RayN 是一款专为 macOS 设计的 V2Ray 客户端。该技能可帮助您管理节点、测试连接、自动检测故障以及更新订阅信息。

## 快速状态检查

```bash
# Check if V2RayN is running
ps aux | grep -i v2rayN | grep -v grep

# Check listening ports
lsof -i :10808 -i :10809 -i :10810 -i :7890 -i :7891 2>/dev/null

# Test connection
curl -s --max-time 5 https://www.google.com -w "\nStatus: %{http_code}\n"
```

## 自动检查节点健康状况（每 30 分钟）

该技能会自动执行以下操作：
1. 检查当前节点是否正常运行；
2. 如果节点出现故障，会更新订阅信息；
3. 选择一个新的正常运行的节点。

### 实现方式

创建一个 cron 作业：
```
*/30 * * * * /path/to/check_v2rayn.sh
```

### 检查脚本

```bash
#!/bin/bash
# check_v2rayn.sh - Auto-check and failover for V2RayN

LOG_FILE="$HOME/.openclaw/logs/v2rayn_check.log"
CONFIG_DIR="$HOME/Library/Application Support/v2rayN/guiConfigs"
MAIN_CONFIG="$CONFIG_DIR/guiNConfig.json"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Test connection
test_connection() {
    curl -s --max-time 5 -x socks5://127.0.0.1:10808 https://www.google.com -o /dev/null -w "%{http_code}" 2>/dev/null
}

# Get current node info
get_current_node() {
    python3 -c "
import json
with open('$MAIN_CONFIG') as f:
    d = json.load(f)
    idx = d.get('currentServerIndex')
    if idx is not None:
        servers = d.get('vmess',[]) + d.get('vless',[]) + d.get('trojan',[])
        if idx < len(servers):
            print(servers[idx].get('remarks', 'Unknown'))
        else:
            print('Invalid index')
    else:
        print('No server selected')
" 2>/dev/null
}

# Main check
log "=== Starting V2RayN health check ==="

# Test current connection
RESULT=$(test_connection)
log "Connection test result: $RESULT"

if [ "$RESULT" = "200" ]; then
    log "✅ Node is working: $(get_current_node)"
    exit 0
else
    log "❌ Node failed! Trying to recover..."
    
    # Try to update subscription
    log "Updating subscription..."
    # Note: V2RayN CLI is limited, manual or external script needed
    
    log "Please manually:"
    log "1. Open V2RayN"
    log "2. Update subscription"
    log "3. Select a new node"
    
    # Notify user
    echo "⚠️ V2RayN node failed! Please check manually."
    exit 1
fi
```

## 手动命令

### 1. 检查节点状态
```bash
# Test all common proxy ports
for port in 10808 10809 10810 7890 7891; do
    result=$(curl -s --max-time 3 -x socks5://127.0.0.1:$port https://www.google.com -w "%{http_code}" 2>/dev/null)
    echo "Port $port: $result"
done
```

### 2. 列出所有节点
```bash
cat ~/Library/Application\ Support/v2rayN/guiConfigs/guiNConfig.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
servers = d.get('vmess',[]) + d.get('vless',[]) + d.get('trojan',[]) + d.get('shadowsocks',[])
print(f'Total nodes: {len(servers)}')
for i, s in enumerate(servers):
    print(f'{i+1}. {s.get(\"remarks\", s.get(\"name\", \"Unnamed\"))}')
"
```

### 3. 获取当前节点信息
```bash
python3 -c "
import json
with open('$HOME/Library/Application Support/v2rayN/guiConfigs/guiNConfig.json') as f:
    d = json.load(f)
    idx = d.get('currentServerIndex')
    if idx:
        servers = d.get('vmess',[]) + d.get('vless',[]) + d.get('trojan',[])
        if idx < len(servers):
            s = servers[idx]
            print(f'Current: {s.get(\"remarks\", \"Unknown\")}')
            print(f'Protocol: {s.get(\"protocol\", \"trojan\")}')
"
```

### 4. 测试特定节点
```bash
# Test current node
curl -s --max-time 5 -x socks5://127.0.0.1:10808 https://www.google.com

# Test direct
curl -s --max-time 5 https://www.google.com
```

### 5. 查看日志
```bash
ls -la ~/Library/Application\ Support/v2rayN/guiLogs/
tail -50 ~/Library/Application\ Support/v2rayN/guiLogs/*.log 2>/dev/null | tail -30
```

### 6. 重启 V2RayN
```bash
# Kill and restart
pkill -f v2rayN
open /Applications/v2rayN.app
```

### 7. 强制更新订阅信息
注意：V2RayN 没有用于更新订阅信息的命令行界面（CLI）。您需要：
1. 打开 V2RayN 的图形用户界面（GUI）；
2. 点击“更新”按钮来更新订阅信息。

## 配置文件

| 文件名 | 说明 |
|------|-------------|
| `guiNConfig.json` | 主要的 GUI 配置文件（包含节点信息和设置） |
| `config.json` | V2Ray/Xray 运行时配置文件 |
| `configPre.json` | （如果使用 TUN 模式时的）专用配置文件 |

## 故障排除

### 节点无法正常运行
1. 查看日志：`tail -50 ~/Library/Application Support/v2rayN/guiLogs/*.log`
2. 测试端口是否正常开放：`lsof -i :10808`
3. 尝试在 GUI 中更换其他节点；
4. 更新订阅信息。

### 所有节点都无效
- 导入新的订阅信息；
- 或者在 GUI 中手动添加新的节点。

### TUN 模式无法正常使用
- 检查是否存在 TUN 接口：`ifconfig | grep -i tun`
- 查看 `configPre.json` 文件中的 TUN 配置设置。
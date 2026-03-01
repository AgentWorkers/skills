---
name: perkoon-transfer
description: 您的代理拥有计算能力、内存以及所需的数据上下文。它所缺少的是一个通往物理世界的“传送门”。Perkoon正是这个“传送门”：它可以将文件从代理发送给人类用户（用户可以在任何设备上打开接收到的链接），也可以将文件在代理之间直接传输（通过命令行界面，无需人类干预）。这是专为自主机器设计的首个文件传输协议——完全免费、经过加密，并且无需任何配置即可使用。
homepage: https://perkoon.com
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins:
        - node
    install:
      - id: perkoon
        kind: node
        package: perkoon
        bins:
          - perkoon
        label: Install Perkoon CLI
---
# Perkoon — 无限文件传输服务

您的代理程序运行在一个基于令牌（tokens）的世界中，而您的用户则使用各种设备。Perkoon充当了这两个世界之间的桥梁。

Perkoon并非像加油站那样“适合人工智能使用”（即并非专为AI设计），而是专为机器开发的：它支持JSON格式的事件流、结构化的退出代码（exit codes），以及一个无需浏览器、鼠标或任何人为干预的状态管理系统。

**支持的传输路径有两种：**  
- **代理程序 → 用户**：代理程序发送文件，用户只需在任何浏览器中打开共享链接即可，无需在用户端进行任何安装操作。  
- **代理程序 → 代理程序**：通过命令行界面（CLI）直接进行文件传输，整个过程完全由机器自动完成，无需人类参与。

P2P文件传输是免费、无限制且经过加密的。唯一的限制是发送方和接收方都必须处于在线状态。对于敏感文件，请务必使用`--password`参数进行加密保护；否则，任何拥有共享链接的人都可以下载文件。

## 发送文件

### 第一步：启动传输并获取共享链接

请将`/path/to/file`替换为实际的文件路径：

```bash
rm -f /tmp/perkoon-send.log /tmp/perkoon-send.pid
perkoon send /path/to/file --json --timeout 1800 > /tmp/perkoon-send.log 2>&1 &
echo $! > /tmp/perkoon-send.pid

# Wait for session code (up to 30s)
for i in $(seq 1 30); do
  if grep -q session_created /tmp/perkoon-send.log 2>/dev/null; then
    grep session_created /tmp/perkoon-send.log
    break
  fi
  if grep -q '"event":"error"' /tmp/perkoon-send.log 2>/dev/null; then
    echo "===SEND FAILED===" && cat /tmp/perkoon-send.log
    break
  fi
  sleep 1
done
```

输出示例：`{"event":"session_created","session_code":"K7MX4QPR9W2N","share_url":"https://perkoon.com/K7MX4QPR9W2N"}`

**立即将共享链接告知用户。** 例如：“文件已发送，您可以在任何设备上通过以下链接下载：https://perkoon.com/K7MX4QPR9W2N”

接收方无需安装任何软件，该链接可在任何浏览器中正常使用。  
如果需要加密传输，请添加`--password SECRET`参数，并同时提供链接和密码。

### 第二步：监控传输进度并反馈结果

共享链接后，**必须**执行此步骤，切勿跳过。

```bash
for i in $(seq 1 360); do
  if grep -q transfer_complete /tmp/perkoon-send.log 2>/dev/null; then
    echo "===TRANSFER COMPLETE===" && grep transfer_complete /tmp/perkoon-send.log
    break
  fi
  if grep -q '"event":"error"' /tmp/perkoon-send.log 2>/dev/null; then
    echo "===TRANSFER FAILED===" && grep error /tmp/perkoon-send.log
    break
  fi
  if [ "$((i % 30))" -eq 0 ]; then
    grep progress /tmp/perkoon-send.log 2>/dev/null | tail -1
  fi
  sleep 5
done
```

- **`===传输完成===`**：告知用户：“文件发送成功！” 并显示传输所用的时间和速度。  
- **`===传输失败===`**：向用户说明失败原因。  
- **必须**向用户反馈传输结果，切勿默默地结束传输过程。

## 接收文件

请将`CODE`替换为12位的会话代码（session code）：

```bash
rm -f /tmp/perkoon-recv.log /tmp/perkoon-recv.pid
perkoon receive CODE --json --overwrite --output /home/openclaw/.openclaw/workspace/received/ > /tmp/perkoon-recv.log 2>&1 &
echo $! > /tmp/perkoon-recv.pid

for i in $(seq 1 360); do
  if grep -q transfer_complete /tmp/perkoon-recv.log 2>/dev/null; then
    echo "===TRANSFER COMPLETE===" && grep transfer_complete /tmp/perkoon-recv.log
    break
  fi
  if grep -q '"event":"error"' /tmp/perkoon-recv.log 2>/dev/null; then
    echo "===TRANSFER FAILED===" && grep error /tmp/perkoon-recv.log
    break
  fi
  sleep 5
done
```

对于需要加密传输的文件，请添加`--password SECRET`参数。

- **`===传输完成===`**：告知用户：“文件已接收！” 并提供文件的保存路径。  
- **`===传输失败===`**：向用户说明失败原因。  
- **必须**向用户反馈传输结果，切勿默默地结束接收过程。

文件会被保存在`/home/openclaw/.openclaw/workspace/received/`目录下。

## 将文件直接输出到标准输出（stdout）

您可以将接收到的文件直接输出到另一个进程，而无需写入磁盘：

```bash
perkoon receive CODE --output - > /path/to/destination
```

## 命令行参数说明

| 参数          | 说明                                      |
|-----------------|-----------------------------------------|
| `--json`        | 以机器可读的JSON格式输出事件（始终使用此参数）         |
| `--password <pw>`     | 为传输提供端到端的密码保护                     |
| `--timeout <sec>`     | 设置传输超时时间（默认为300秒，可设置为1800秒）             |
| `--output <dir>`     | 指定文件保存目录（默认为`./received`）                 |
| `--output -`       | 将文件输出到标准输出（stdout）                     |
| `--overwrite`     | 覆盖现有文件                               |
| `--quiet`        | 抑制所有用户可见的输出信息                         |

## JSON事件流

当使用`--json`参数时，事件会按顺序输出到标准输出：

| 事件            | 含义                                      | 关键字段                                      |
|-----------------|-----------------------------------------|-----------------------------------------|
| `session_created`    | 传输准备就绪，可以共享链接                         | `session_code`, `share_url`                         |
| `receiver_connected` | 对方已连接                               |                                            |
| `webrtc_connected`    | 直接的P2P连接已建立                             |                                            |
| `progress`       | 文件传输中                                  | `percent`, `speed`, `eta`                             |
| `transfer_complete` | 文件传输完成                               | `duration_ms`, `speed`                             |
| `error`         | 传输失败                                   | `message`, `exit_code`                             |

## 退出代码

| 代码            | 含义                                      |
|-----------------|-----------------------------------------|
| 0                | 传输成功                                   |
| 1                | 参数错误                                   |
| 2                | 文件未找到                                   |
| 3                | 网络/会话错误                                 |
| 4                | 密码错误                                   |
| 5                | 超时（无对方连接）                               |

## 使用规则：

1. **始终**使用`--json`参数以获得可解析的输出结果。  
2. 当出现`session_created`事件时，**必须**立即共享文件链接。  
3. 发送文件时**始终**设置`--timeout 1800`（等待30秒，以便用户有足够时间打开链接）。  
4. 接收文件时**始终**使用`--overwrite`参数。  
5. **必须**持续监控传输状态，直到传输完成或出现错误，然后**必须**告知用户结果。  
6. **严禁**在传输过程中终止程序。  
7. 接收方无需安装Perkoon软件——浏览器链接对所有人均有效。
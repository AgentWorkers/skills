---
name: ii-irc
description: 使用 ii（一款基于文件的、设计简约的 IRC 客户端）实现持久的 IRC 在线状态，并具备事件驱动的提及检测功能。适用于在 IRC 上部署 AI 代理、监控 IRC 频道、发送 IRC 消息，或通过 ii 将 OpenClaw 与 IRC 集成。内容包括 ii 的安装与配置、提及检测机制、systemd 服务管理，以及消息的发送与接收功能。
metadata: {"openclaw":{"os":["linux"],"requires":{"bins":["ii"]},"install":[{"id":"pacman","kind":"shell","command":"sudo pacman -S ii","bins":["ii"],"label":"Install ii via pacman (Arch)"},{"id":"apt","kind":"apt","packages":["ii"],"bins":["ii"],"label":"Install ii via apt (Debian/Ubuntu)"},{"id":"source","kind":"shell","command":"git clone https://git.suckless.org/ii && cd ii && make && sudo make install","bins":["ii"],"label":"Build ii from source"}]}}
---

# ii-IRC：基于事件驱动的AI代理IRC客户端

ii会将所有频道活动记录到纯文本文件中。一个监控脚本会检测到对代理的提及，并触发OpenClaw系统事件。响应信息会通过FIFO队列发送出去。

## 架构

```
~/irc/
├── irc.sh              # Management script (start/stop/status/send)
├── watch-daemon.sh     # Mention watcher → openclaw system event
└── <server>/
    └── <channel>/
        ├── in          # FIFO - write here to send messages
        └── out         # Append-only log of all channel messages
```

## 快速安装

### 1. 安装ii

ii大多数包管理器中都有提供。在Arch系统中：`pacman -S ii`；在Debian/Ubuntu系统中：`apt install ii`。也可以从[suckless.org](https://tools.suckless.org/ii/)下载源代码进行编译安装。

### 2. 创建脚本

运行自带的安装脚本（会生成`~/irc/irc.sh`和`~/irc/watch-daemon.sh`两个文件）：

```bash
bash scripts/setup.sh --server irc.example.org --port 6667 --nick MyBot --channel "#mychannel"
```

或者你可以手动创建这些脚本——参考`scripts/irc.sh.template`和`scripts/watch-daemon.sh.template`作为模板。

### 3. 创建systemd用户服务（推荐）

为了实现系统启动时自动运行ii：

```bash
mkdir -p ~/.config/systemd/user

# IRC connection service
cat > ~/.config/systemd/user/irc-bot.service << 'EOF'
[Unit]
Description=IRC connection (ii)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/ii -s SERVER -p PORT -n NICK -i %h/irc
ExecStartPost=/bin/bash -c 'sleep 3 && echo "/j CHANNEL" > %h/irc/SERVER/in'
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# Mention watcher service
cat > ~/.config/systemd/user/irc-watcher.service << 'EOF'
[Unit]
Description=IRC mention watcher
After=irc-bot.service
Wants=irc-bot.service

[Service]
Type=simple
ExecStart=%h/irc/watch-daemon.sh
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Replace SERVER, PORT, NICK, CHANNEL in the service files, then:
systemctl --user daemon-reload
systemctl --user enable --now irc-bot.service irc-watcher.service
```

## 发送消息

```bash
# Via the management script
~/irc/irc.sh send "Hello, world!"

# Or write directly to the FIFO
echo "Hello, world!" > ~/irc/<server>/<channel>/in
```

**注意：**ii会在字节边界处分割较长的消息，这可能会导致消息在单词中间或UTF8字符中间被截断。请确保消息长度不超过400个字符。如果消息较长，需要将其分割成多条消息，并在每条消息之间添加短暂的延迟。

## 读取聊天记录

**切勿**直接读取整个`out`文件——该文件会无限增长。始终使用`tail`命令，并设置读取长度限制。

## 提及检测机制的工作原理

1. `watch-daemon.sh`脚本会持续监控频道的`out`文件（使用`tail -F`命令）。
2. 对每新添加的行（不区分大小写）进行检查，以确认是否包含代理的昵称。
3. 代理发送的消息以及用户加入/离开频道的通知会被忽略。
4. 当检测到代理的昵称时，会触发`openclaw system event --text "IRC mention: <message>" --mode now`事件。
5. OpenClaw会接收到该事件并可以通过`in` FIFO队列发送响应。

ii采用事件驱动的方式工作：无需主动轮询，响应即时，且资源消耗极低。

## 加入多个频道

ii支持在同一服务器上同时监听多个频道。对于每个新增的频道，需要执行以下操作：

```bash
echo "/j #other-channel" > ~/irc/<server>/in
```

要同时监控多个频道，可以分别运行多个监控脚本，或者修改`watch-daemon.sh`以同时监视多个频道的输出文件。

## 常见问题排查

- **无法连接服务器**：检查`ii`是否正在运行（使用`pgrep -f "ii -s"`），并确认服务器地址和端口号是否正确。
- **无法加入频道**：确保`in` FIFO队列存在；如果需要，可以调整`ExecStartPost`参数中的延迟时间。
- **提及代理的提示未被触发**：确认监控脚本正在运行（使用`pgrep -f watch-daemon`），并检查是否正确匹配了代理的昵称。
- **消息被异常分割**：请缩短消息长度；ii遵循IRC协议的512字节限制。
- **重新连接问题**：systemd的`Restart=always`配置可以解决这个问题：当连接断开时，ii会自动退出，系统会重新启动它。
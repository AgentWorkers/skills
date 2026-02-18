# android-agent — 基于AI的安卓手机控制工具

> 将你的旧安卓手机连接到Mac或PC上，现在你的AI助手就可以使用它了。

家里有闲置的安卓手机吗？将其连接到任何运行OpenClaw的设备上——无论是Mac Mini还是Raspberry Pi。你的AI助手现在可以打开应用程序、点击按钮、输入文本，并在真实的手机上完成各种任务。预订出租车、点餐、查看银行账户信息——所有你原本需要用手指操作的功能都可以实现。

## 工作原理

你的AI助手通过截图查看手机屏幕，决定需要点击、输入或滑动的内容，然后通过ADB（Android Debug Bridge）来执行相应的操作。在底层，它使用了[DroidRun](https://github.com/droidrun/droidrun)和GPT-4o视觉识别技术。

```
┌─────────────┐    screenshots    ┌──────────────┐    ADB commands    ┌─────────────┐
│  GPT-4o     │◄─────────────────│  DroidRun    │──────────────────►│  Android    │
│  Vision     │─────────────────►│  Agent       │◄──────────────────│  Phone      │
│             │   tap/type/swipe  │              │    screen state    │             │
└─────────────┘                   └──────────────┘                    └─────────────┘
```

## 双向操作模式

### 直接模式
手机通过USB连接到OpenClaw网关设备，无需网络连接。

```
[Gateway Machine] ──USB──► [Android Phone]
```

### 节点模式
手机连接到Mac Mini、Raspberry Pi或任何OpenClaw节点，网关通过网络来控制手机。

```
[Gateway] ──network──► [Mac Mini / Pi node] ──USB──► [Android Phone]
```

对于节点模式，需要通过TCP或WiFi建立ADB连接，以便节点能够转发指令。

## 快速入门（3个步骤）

### 1. 启用USB调试
在安卓手机上：
- 进入**设置 → 关于手机**
- 連续点击**版本号** 7次以启用开发者选项
- 进入**设置 → 开发者选项**
- 启用**USB调试**

### 2. 连接并安装所需软件
```bash
# Plug phone in via USB, then:
pip install -r requirements.txt
adb devices  # verify phone shows up — authorize on phone if prompted
```

### 3. 运行第一个任务
```bash
export OPENAI_API_KEY="sk-..."
python scripts/run-task.py "Open Settings and turn on Dark Mode"
```

就这样，脚本会自动处理所有步骤：唤醒屏幕、解锁手机、保持屏幕显示，并执行你的任务。

## 功能介绍

### 📱 日常生活
```bash
python scripts/run-task.py "Order an Uber to the airport"
python scripts/run-task.py "Set an alarm for 6 AM tomorrow"
python scripts/run-task.py "Check my bank balance on PhonePe"
python scripts/run-task.py "Open Google Maps and navigate to the nearest coffee shop"
```

### 💬 消息交流
```bash
python scripts/run-task.py "Send a WhatsApp message to Mom saying I'll be late"
python scripts/run-task.py "Read my latest SMS messages"
python scripts/run-task.py "Open Telegram and check unread messages"
```

### 🛒 购物
```bash
python scripts/run-task.py "Open Amazon and search for wireless earbuds under 2000 rupees"
python scripts/run-task.py "Add milk and bread to my Instamart cart"
```

### 📅 提高效率
```bash
python scripts/run-task.py "Open Google Calendar and check my schedule for tomorrow"
python scripts/run-task.py "Create a new note in Google Keep: Buy groceries"
```

### 🎵 娱乐
```bash
python scripts/run-task.py "Play my Discover Weekly playlist on Spotify"
python scripts/run-task.py "Open YouTube and search for lo-fi study music"
```

### ⚙️ 设置与配置
```bash
python scripts/run-task.py "Turn on Dark Mode"
python scripts/run-task.py "Connect to my home WiFi network"
python scripts/run-task.py "Enable Do Not Disturb mode"
python scripts/run-task.py "Turn off Bluetooth"
```

### 📸 实用工具
```bash
python scripts/run-task.py "Take a screenshot"
python scripts/run-task.py "Open the camera and take a photo"
python scripts/run-task.py "Clear all notifications"
```

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `OPENAI_API_KEY` | 是 | 用于GPT-4o视觉识别的API密钥 |
| `ANDROID_SERIAL` | 否 | 设备序列号。如果只连接了一台设备，则会自动检测 |
| `ANDROID_PIN` | 否 | 用于自动解锁的手机PIN码/密码。如果未设置，则跳过解锁步骤 |
| `DROIDRUN_TIMEOUT` | 否 | 任务超时时间（默认：120秒） |

## 设置细节

### 直接模式（USB）

1. 安装ADB：
   ```bash
   # macOS
   brew install android-platform-tools

   # Ubuntu/Debian
   sudo apt install android-tools-adb

   # Windows
   # Download from https://developer.android.com/tools/releases/platform-tools
   ```

2. 通过USB连接手机并验证连接：
   ```bash
   ./scripts/connect.sh usb
   ```

3. 在手机上安装DroidRun Portal APK：
   - 从[DroidRun官方仓库](https://github.com/droidrun/droidrun/releases)下载
   - 或者通过ADB安装：`adb install droidrun-portal.apk`
   - 打开手机上的Portal应用并授予访问权限

4. 安装Python依赖库：
   ```bash
   pip install -r requirements.txt
   ```

### 节点模式（通过WiFi/TCP远程控制）

1. 在节点设备（Mac Mini、Raspberry Pi等）上，通过USB连接手机并启用WiFi ADB：
   ```bash
   adb tcpip 5555
   adb connect <phone-ip>:5555
   ```

2. 从网关设备连接到节点的ADB服务：
   ```bash
   # If using SSH tunnel:
   ssh -L 15555:<phone-ip>:5555 user@node-ip
   export ANDROID_SERIAL="127.0.0.1:15555"

   # Or direct WiFi (same network):
   ./scripts/connect.sh wifi <phone-ip>
   ```

3. 按常规方式运行任务——脚本会使用`ANDROID_SERIAL`指定的设备信息。

### DroidRun Portal设置

必须在手机上安装并运行DroidRun Portal APK。该应用提供访问权限，使DroidRun能够读取屏幕内容并操作用户界面元素。

1. 从DroidRun官方仓库下载APK
2. 打开Portal应用
3. 根据提示授予**访问权限**
4. 保持应用在后台运行

## 脚本参考

### `scripts/run-task.py` — 主脚本

```bash
# Basic usage
python scripts/run-task.py "Your task description here"

# With options
python scripts/run-task.py --timeout 180 "Install Spotify from Play Store"
python scripts/run-task.py --model gpt-4o "Open Chrome and search for weather"
python scripts/run-task.py --no-unlock "Take a screenshot"
python scripts/run-task.py --serial 127.0.0.1:15555 "Check notifications"
python scripts/run-task.py --verbose "Open Settings"
```

**参数说明：**
| 参数 | 说明 |
|------|-------------|
| `goal` | 任务描述（必填） |
| `--timeout` | 任务超时时间（默认：120秒，或通过环境变量`DROIDRUN_TIMEOUT`设置） |
| `--model` | 使用的LLM模型（默认：gpt-4o） |
| `--no-unlock` | 跳过自动解锁步骤 |
| `--serial` | 设备序列号（默认使用环境变量`ANDROID_SERIAL`或自动检测） |
| `--verbose` | 显示详细的调试信息 |

### `scripts/connect.sh` — 设置与连接验证

```bash
./scripts/connect.sh          # Auto-detect USB device
./scripts/connect.sh usb      # USB mode (explicit)
./scripts/connect.sh wifi 192.168.1.100  # WiFi/TCP mode
```

### `scripts/screenshot.sh` — 截图功能（使用ADB截图）

DroidRun在某些设备上可能无法正常截图。可以使用此脚本通过ADB直接获取PNG格式的截图。

```bash
# Save to /tmp/android-screenshot.png
./scripts/screenshot.sh

# Explicit serial + output path
./scripts/screenshot.sh 127.0.0.1:15555 /tmp/a03.png
```

你也可以通过Python脚本来实现截图功能：

```bash
python scripts/run-task.py --screenshot --serial 127.0.0.1:15555 --screenshot-path /tmp/a03.png
```

### `scripts/status.sh` — 查看设备状态

```bash
./scripts/status.sh
# Output:
# 📱 Device: Samsung Galaxy A03 (SM-A035F)
# 🤖 Android: 11 (API 30)
# 🔋 Battery: 87%
# 📺 Screen: ON (unlocked)
# 🔌 Connection: USB
# 📦 DroidRun Portal: installed (v0.5.5)
```

## 常见问题解决方法

### “未找到设备/模拟器”
- 检查USB数据线（使用数据线，而非仅充电的线）
- 在手机的USB调试设置中授权计算机
- 尝试执行`adb kill-server && adb start-server`

### “设备未授权”
- 断开USB连接后再重新连接
- 检查手机屏幕上是否有授权提示
- 如果没有提示，可以在开发者选项中取消USB调试授权后重新连接

### 任务执行过程中手机屏幕关闭
- 脚本会自动设置保持屏幕唤醒状态，但部分手机可能不支持此功能
- 手动设置：**设置 → 开发者选项 → 保持屏幕唤醒（充电时启用）**

### 任务失败（因弹窗或对话框遮挡）
- 脚本会尝试自动关闭弹窗
- 如果弹窗持续出现，请先手动关闭它们，然后再尝试
- 使用`--verbose`参数查看脚本的实际操作情况

### 重启后WiFi ADB连接断开
- 手机重启后WiFi ADB模式会重置——需要通过USB重新连接
- 先运行`./scripts/connect.sh usb`，然后再运行`./scripts/connect.sh wifi <ip>`

### DroidRun助手反应异常
- 确保DroidRun Portal正在运行且访问权限已启用
- 关闭不必要的应用程序以减少屏幕复杂度
- 先尝试简单的任务来验证设置是否正确

### PIN码解锁失败
- 不同设备和屏幕分辨率下，PIN码输入框的坐标可能不同
- 查找设备坐标的方法：`adb shell getevent -l`，然后逐个点击数字
- 或者在某些设备上使用`adb shell input text <PIN>`进行尝试
- 设置`ANDROID_PIN`环境变量（切勿硬编码）

## 安全注意事项

- **ADB会授予设备完全访问权限**——仅连接你信任且属于自己的设备
- **截图会被发送到你的LLM提供商（默认为OpenAI）**——请注意屏幕上显示的敏感内容（如银行应用、私密信息）
- **PIN码仅从环境变量中读取**——不会存储在文件或日志中
- **WiFi ADB模式未加密**——在不受信任的网络中使用USB或SSH隧道
- **DroidRun Portal需要访问权限**——这相当于root级别的控制，请确保理解其带来的风险

## 系统要求

- Python 3.10及以上版本
- ADB（Android调试桥）
- 安卓系统版本8.0及以上，且已启用开发者选项和USB调试功能
- 手机上已安装[DroidRun Portal](https://github.com/droidrun/droidrun) APK
- OpenAI API密钥（GPT-4o视觉识别功能需要此密钥）
- USB数据线（非仅充电类型的线）

## 安全提示

**请使用专用测试设备，切勿使用你的主要手机。**

- **截图和屏幕内容会发送到OpenAI**——所有截图都会被发送给GPT-4o进行处理。请勿在包含敏感信息的设备上使用此功能（如银行应用、2FA令牌、私密消息等）。如果屏幕上有这些信息，它们将会被上传到云端。
- **PIN码存储在环境变量中**——虽然不会写入文件或日志，但任何有权访问主机环境的人都可以查看该变量。请使用一次性PIN码，或者自行承担风险。
- **仅从官方渠道安装DroidRun Portal**。请从[DroidRun官方仓库](https://github.com/droidrun/droidrun/releases)下载APK。切勿从第三方网站下载。
- **ADB会授予设备完全访问权限**——结合访问权限，这相当于root级别的控制。请仅连接你自己的设备，并确保你愿意暴露这些权限。
- **WiFi ADB模式未加密**——在不受信任的网络中使用时要使用SSH隧道。

**总结：** 将连接的手机视为“AI工作设备”。请勿在设备上登录个人账户或存储敏感信息。如果你不会将未锁定的手机交给陌生人，也请勿使用此功能。

## 许可证

MIT许可证——详见[LICENSE](LICENSE)文件。
---
name: tado
description: 控制您的 Tado 智能恒温器：查看温度、设置供暖模式、管理“在家/外出”模式，并通过地理位置信息监控您的位置。
homepage: https://www.tado.com
metadata: {"openclaw":{"emoji":"🌡️","requires":{"bins":["python3","pip3"]}}}
---

# Tado智能恒温器技能

通过OpenClaw控制您的Tado智能恒温器。

## 功能

- 📊 **状态信息：** 获取当前温度、湿度以及每个区域的供暖状态
- 🌡️ **温度调节：** 设置目标温度，并可设置定时器
- 🏠 **人员检测：** 通过地理位置判断是否有人在家
- ⚙️ **区域管理：** 支持多区域设置
- 📋 **JSON输出：** 以机器可读的格式输出数据，便于脚本编写

## 安装

### 1. 安装依赖库

```bash
cd ~/clawd/skills/tado
pip3 install libtado --break-system-packages
```

**最低版本要求：** libtado 4.1.1+（支持OAuth2认证）

### 2. OAuth2认证（一次性设置）

**⚠️ 重要提示：** libtado 4.1.1+版本起仅支持OAuth2认证。用户名/密码认证方式已不再可用。

**首次设置：**

```bash
# Run the libtado CLI to authenticate via browser
python3 -m libtado -f ~/.tado_auth.json zones
```

**操作步骤：**
1. libtado会生成一个Tado登录URL
2. 打开浏览器访问该URL或手动输入URL
3. 使用您的Tado账户登录
4. libtado会将OAuth2令牌保存到`~/.tado_auth.json`文件中
5. 系统会显示您已设置的区域列表（表示设置成功）

**设置完成后：**
- 该技能将自动使用`~/.tado_auth.json`文件
- 无需再次登录浏览器
- 令牌会自动刷新

**安全提示：** 该令牌文件仅允许您本人访问：

```bash
chmod 600 ~/.tado_auth.json
```

### 3. 测试连接

```bash
cd ~/clawd/skills/tado
./scripts/tado.py zones
```

您应该能看到已配置的区域列表。

**如果认证失败：**
```bash
# Re-authenticate (regenerates tokens)
python3 -m libtado -f ~/.tado_auth.json zones
```

## 认证

### OAuth2认证流程（强制要求）

从**libtado 4.1.1+**版本开始，OAuth2成为唯一的认证方式。

**令牌文件位置：** `~/.tado_auth.json`

**工作原理：**
1. 首次运行时：通过`python3 -m libtado -f ~/.tado_auth.json zones`进行浏览器登录
2. libtado会保存访问令牌和刷新令牌
3. 该技能会使用`token_file_path`参数（例如：`Tado(token_file_path='~/.tado_auth.json')`
4. libtado会自动刷新过期的令牌

**令牌结构（由libtado管理）：**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_at": 1234567890
}
```

**请勿手动编辑此文件！** 由libtado负责管理令牌。

### 从用户名/密码认证方式迁移

**旧认证方式（不再适用）：**
```python
Tado(username='email', password='pass')  # ❌ Not supported
```

**新认证方式（强制要求）：**
```python
Tado(token_file_path='~/.tado_auth.json')  # ✅ Works
```

**迁移步骤：**
1. 删除旧的`~/.tado_credentials.json`文件
2. 运行`python3 -m libtado -f ~/.tado_auth.json zones`
3. 按照浏览器登录流程操作
4. 完成迁移后，技能将自动生效

**注意：** 升级到libtado 4.1.1+版本后，必须使用OAuth2认证方式。

## 使用方法

### 状态查询命令

**查询所有区域的状态：**
```bash
./scripts/tado.py status
```

**输出结果：**
```
🏠 Woonkamer (Zone 1)
  Current: 20.5°C (55% humidity)
  Target:  21.0°C
  Heating: ON (45%)
  Mode:    Auto (following schedule)

🏠 Slaapkamer (Zone 2)
  Current: 18.2°C (58% humidity)
  Target:  18.0°C
  Heating: OFF (0%)
  Mode:    Auto (following schedule)
```

**查询特定区域的状态：**
```bash
./scripts/tado.py status --zone 1
./scripts/tado.py status --zone "Woonkamer"
```

**JSON输出（用于脚本编写）：**
```bash
./scripts/tado.py status --json
```

### 温度调节

**设置温度（直到下一次定时器触发为止）：**
```bash
./scripts/tado.py set --zone 1 --temperature 21
./scripts/tado.py set --zone "Woonkamer" --temperature 21.5
```

**设置带定时器的温度（临时调整）：**
```bash
# Set 22°C for 60 minutes, then return to schedule
./scripts/tado.py set --zone 1 --temperature 22 --duration 60

# Short form
./scripts/tado.py set --zone 1 -t 22 -d 60
```

**恢复到自动定时模式：**
```bash
./scripts/tado.py reset --zone 1
./scripts/tado.py reset --zone "Woonkamer"
```

### 家/外出模式

**设置家庭模式（所有区域遵循定时器设置）：**
```bash
./scripts/tado.py mode home
```

**设置外出模式（节能温度设置）：**
```bash
./scripts/tado.py mode away
```

**设置自动模式（基于地理位置）：**
```bash
./scripts/tado.py mode auto
```

在自动模式下，Tado会根据您的手机位置自动切换家庭/外出模式。

### 人员检测

**判断是否有人在家：**
```bash
./scripts/tado.py presence
```

**输出结果：**
```
👥 Presence
  Anyone home: Yes
  - Sander's iPhone: 🏠 Home
  - Partner's iPhone: 🚶 Away
```

### 区域管理

**列出所有区域：**
```bash
./scripts/tado.py zones
```

**输出结果：**
```
📍 Available Zones:
  1: Woonkamer (HEATING)
  2: Slaapkamer (HEATING)
  3: Badkamer (HOT_WATER)
```

## 区域标识

区域可以通过**ID**或**名称**来引用：

```bash
# By ID (faster)
./scripts/tado.py status --zone 1

# By name (case-insensitive)
./scripts/tado.py status --zone "Woonkamer"
./scripts/tado.py status --zone "woonkamer"
```

## JSON输出（用于脚本编写）

所有命令都支持`--json`参数，以获取机器可读的输出格式：

```bash
./scripts/tado.py status --zone 1 --json
```

**示例输出：**
```json
{
  "zone_id": 1,
  "zone_name": "Woonkamer",
  "current_temp": 20.5,
  "current_humidity": 55,
  "target_temp": 21.0,
  "heating": true,
  "heating_power": 45,
  "mode": "MANUAL",
  "overlay": true
}
```

**在脚本中的使用方法：**
```bash
# Get current temperature as number
TEMP=$(./scripts/tado.py status --zone 1 --json | jq -r '.current_temp')

# Check if heating is on
HEATING=$(./scripts/tado.py status --zone 1 --json | jq -r '.heating')

# Get all zones data
./scripts/tado.py status --json | jq '.zones[] | {name: .zone_name, temp: .current_temp}'
```

## 与OpenClaw的集成

**在OpenClaw聊天界面中：**

```
@jarvis What's the temperature in the living room?
→ Uses: ./scripts/tado.py status --zone "Woonkamer"

@jarvis Set living room to 22 degrees for 1 hour
→ Uses: ./scripts/tado.py set --zone "Woonkamer" -t 22 -d 60

@jarvis Is anyone home?
→ Uses: ./scripts/tado.py presence

@jarvis Turn on away mode
→ Uses: ./scripts/tado.py mode away
```

## 故障排除**

### 认证错误

**错误：** “Tado OAuth2令牌未找到！”**

**解决方法：** 运行一次性认证流程：
```bash
python3 -m libtado -f ~/.tado_auth.json zones
```

然后按照浏览器登录提示操作。

---

**错误：** “无法连接到Tado：401未经授权”

**可能原因：**
- OAuth2令牌过期或无效
- 令牌文件损坏
- Tado服务暂时不可用

**解决方法：**
1. 重新认证：
   ```bash
   python3 -m libtado -f ~/.tado_auth.json zones
   ```
2. 检查令牌文件是否存在：`ls -la ~/.tado_auth.json`
3. 确保令牌文件的权限设置为600：`chmod 600 ~/.tado_auth.json`
4. 查看Tado服务状态：https://status.tado.com

### API错误

**错误：** “获取状态信息失败：HTTP 500”

**解决方法：** Tado API可能暂时不可用。请查看https://status.tado.com

---

**错误：** “区域‘X’未找到”

**解决方法：**
1. 列出所有可用区域：`./scripts/tado.py zones`
2. 使用列表中的区域ID或名称

### 连接问题

**错误：** “无法连接到Tado：网络不可达”

**解决方法：**
1. 检查网络连接
2. 确认DNS设置是否正常：`ping my.tado.com`
3. 检查防火墙设置

### 库相关错误

**错误：** “ModuleNotFoundError: 未找到名为‘PyTado’的模块”

**解决方法：**
```bash
pip3 install libtado --break-system-packages
```

---

**错误：** “AttributeError: ‘Tado’对象没有‘setAutoMode’属性”

**可能原因：** 使用的libtado版本过旧

**解决方法：**
```bash
pip3 install --upgrade libtado
```

## API使用限制

Tado API有使用频率限制（具体数值未公开）：

**最佳实践：**
- 每分钟不要多次查询状态信息
- 尽可能使用`--json`输出格式并缓存结果
- 将多个区域的查询合并到一个`status`请求中，避免多次调用

**如果遇到频率限制：**
- 等待1-2分钟后重试
- 减少查询频率

## 数据隐私

**本地数据：**
- 认证信息存储在`~/.tado_credentials.json`文件中（建议设置权限为600）
- 不会进行使用情况跟踪或数据传输
- 所有API请求直接发送到Tado服务器

**数据安全：**
- 您的认证信息不会被泄露（仅传输给Tado API）
- 区域名称、温度和人员状态数据仅保存在本地
- 不会与第三方分享数据

## 高级用法

### 温度调度

**创建简单的供暖调度脚本：**

```bash
#!/bin/bash
# morning-heat.sh - Warm up before wake-up

# Set living room to 21°C at 6:30 AM
./scripts/tado.py set --zone "Woonkamer" -t 21 -d 120

# Reset to schedule after 2 hours
sleep 7200
./scripts/tado.py reset --zone "Woonkamer"
```

**通过cron任务运行脚本：**
```
30 6 * * * /path/to/morning-heat.sh
```

### 智能外出检测**

```bash
#!/bin/bash
# smart-away.sh - Set away mode if nobody home

ANYONE_HOME=$(./scripts/tado.py presence --json | jq -r '.anyone_home')

if [ "$ANYONE_HOME" = "false" ]; then
    ./scripts/tado.py mode away
    echo "Nobody home - enabled away mode"
fi
```

### 能源监控**

```bash
#!/bin/bash
# energy-log.sh - Log heating activity

DATE=$(date +%Y-%m-%d_%H:%M)
./scripts/tado.py status --json > ~/logs/tado-$DATE.json

# Analyze with jq
jq '.zones[] | select(.heating == true) | {zone: .zone_name, power: .heating_power}' \
  ~/logs/tado-$DATE.json
```

## 已知限制

1. **热水控制：** 仅支持开关功能，无法设置温度
2. **天气数据：** 尚未实现（可通过Tado API获取）
3. **能源使用情况分析：** 相关数据尚未提供（可通过Tado API获取）
4. **多家庭支持：** 每个令牌文件仅支持一个家庭账户

## 未来改进计划

- [x] 支持OAuth2认证（已在v1.1.0版本实现）
- [ ] 集成天气数据
- [ ] 提供能源使用情况分析功能
- [ ] 支持多家庭账户
- [ ] 提供Web界面（可选）
- [ ] 提供温度警报的推送通知

## 资源链接

- **libtado文档：** https://libtado.readthedocs.io/
- **libtado GitHub仓库：** https://github.com/germainlefebvre4/libtado
- **Tado API（非官方文档）：** https://blog.scphillips.com/posts/2017/01/the-tado-api-v2/
- **Tado服务状态：** https://status.tado.com

## 技术支持

**关于技能使用问题：**
- 查阅本文档
- 仔细阅读错误信息（其中包含解决方法）
- 使用`--json`输出格式进行调试

**关于Tado API/账户问题：**
- 先检查Tado应用程序是否正常工作
- 访问https://my.tado.com
- 联系Tado客服

## 更新记录

**v1.1.0**（2026-02-03）
- ✅ 支持OAuth2认证（libtado 4.1.1+版本）
- ⚠️ 取消了对用户名/密码认证的支持
- 引入了通过`python3 -m libtado`进行的一次性登录流程
- 令牌自动刷新功能
- 更新了所有与OAuth2认证相关的文档

**v0.1.0**（2026-01-29）
- 首次发布版本
- 支持状态查询、温度调节、模式设置和人员检测功能
- 支持JSON输出格式
- 支持区域管理（通过ID或名称查询）
- 改进了错误处理和故障排除机制

---

请注意：由于技术文档的更新频率较快，部分内容可能已经过时。建议定期查看最新版本以获取最准确的信息。
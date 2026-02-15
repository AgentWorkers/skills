---
name: dirigera-control
description: **IKEA Dirigera**：用于控制智能家居设备（如灯光、插座、场景以及相关控制器）。  
- 当用户需要控制智能家居设备时，可以使用该工具；  
- 可用于查看设备状态、开关灯光、调节亮度/颜色、控制插座、触发预设场景，以及查询电池电量；  
- 还可用于协助用户查找 Dirigera 控制中心的 IP 地址或生成 API 令牌。  
- 该工具可通过 VPS 上的 Cloudflare 隧道进行访问。
---

# IKEA Dirigera 智能家居控制

通过 Dirigera 控制中心来控制灯光、插座、场景以及其他 IKEA 智能家居设备。

## 先决条件

```python
pip install dirigera
```

## 控制中心设置

### 查找控制中心 IP 地址

在路由器/DHCP 客户端列表中查找“Dirigera”，并记下其 IP 地址。

如果控制中心与设备位于同一局域网内，可以尝试使用 IP 发现脚本。该脚本可以：
1. 扫描子网以找到可能的控制中心设备（无需令牌）。
2. 如果有令牌，可以验证控制中心的准确 IP 地址。
3. 最后，可以尝试使用 `generate-token` 命令来生成令牌（需要用户手动操作）。

```bash
python scripts/find_dirigera_ip.py
# or
python scripts/find_dirigera_ip.py --subnet 192.168.1.0/24
# verify with token (if you have it)
python scripts/find_dirigera_ip.py --token <dirigera-token>
# last resort: try generate-token against candidates
python scripts/find_dirigera_ip.py --try-generate-token
```

### 生成令牌

**重要提示**：生成令牌需要用户进行物理操作。请按照以下步骤操作：

#### 第一步：启动令牌生成脚本
在后台运行封装脚本。该脚本会自动等待用户按下控制中心的按钮：

```bash
python scripts/generate_token_wrapper.py <dirigera-ip-address> &
```

令牌将默认保存到 `dirigera_token.txt` 文件中。如果需要指定其他保存位置，请调整相应的代码。

```bash
python scripts/generate_token_wrapper.py <dirigera-ip-address> --output /path/to/token.txt &
```

#### 第二步：**结束你的操作并通知用户**
**重要提示**：启动脚本后，你必须立即：
1. 结束你的操作，不要继续执行其他操作。
2. 告诉用户：“我已经启动了令牌生成过程。请立即按下 Dirigera 控制中心底部的按钮。请在按下按钮后告诉我。”

#### 第三步：等待用户确认
用户需要：
1. 手动按下 Dirigera 控制中心上的按钮。
2. 回复你以确认他们已经按下按钮（例如：“操作完成”或“按钮已按下”）。

脚本会自动检测到按钮被按下的操作，并将令牌保存到文件中。

#### 第四步：获取保存的令牌
用户确认后，从文件中读取令牌：

```python
from pathlib import Path
token = Path("dirigera_token.txt").read_text().strip()
```

或者从指定的其他位置读取令牌：

```bash
TOKEN=$(cat /path/to/token.txt)
```

然后使用生成的令牌进行连接：

```python
import dirigera
hub = dirigera.Hub(token=token, ip_address="<dirigera-ip>")
```

#### 替代方法：手动命令
（不推荐用于自动化的设备控制）

```bash
generate-token <dirigera-ip-address>
```

这种方法需要通过终端进行手动操作，并且不会自动保存命令输出。

### 故障排除

如果无法找到控制中心的 IP 地址：
1. 检查路由器/DHCP 客户端列表，查找“Dirigera”。
2. 如果名称不存在，请根据控制中心的 MAC 地址将其添加到设备列表中。
3. 确保控制中心和设备位于同一网络中。
4. 如果有多个可能的 IP 地址，尝试使用 `generate-token` 命令直到找到正确的地址。
5. 如果你已经有了令牌，可以运行 `python scripts/find_dirigera_ip.py --token <dirigera-token>`。
6. 如果其他方法都失败，可以运行 `python scripts/find_dirigera_ip.py --try-generate-token` 并按照提示操作。

## 控制中心连接

```python
import dirigera

hub = dirigera.Hub(
    token="token",
    ip_address="ip_address"
)
```

## 重要提示：设备属性存储位置
设备的状态信息存储在 `.attributes` 文件夹中，而不是在顶层目录中。

```python
# CORRECT
light.attributes.is_on
light.attributes.light_level

# WRONG - raises AttributeError
light.is_on
light.light_level
```

顶层目录中的属性包括：`device.id`、`device.is_reachable`、`device.room`。
设备状态信息包括：`device.attributes.is_on`、`device.attributes.light_level`。

## 快速命令

### 发现设备
```python
lights = hub.get_lights()
outlets = hub.get_outlets()
controllers = hub.get_controllers()
scenes = hub.get_scenes()
```

### 控制灯光
```python
light = hub.get_light_by_name(lamp_name="bedroom light")

# Check reachability first
if light.is_reachable:
    light.set_light(lamp_on=True)
    light.set_light_level(light_level=75)
    light.set_color_temperature(color_temp=2700)  # Warm white

# Reload after changes
light.reload()
```

### 控制插座
```python
outlet = hub.get_outlet_by_name(outlet_name="living room")
outlet.set_on(outlet_on=True)
outlet.reload()
```

### 触发场景
```python
scene = hub.get_scene_by_name(scene_name="Sove tid")
scene.trigger()
```

### 检查设备功能
```python
# Verify device supports feature before using
if 'colorTemperature' in light.capabilities.can_receive:
    light.set_color_temperature(color_temp=3000)
```

## 常见操作模式

有关基于房间的控制、批量操作、状态报告和电池监控的详细信息，请参阅 [references/patterns.md](references/patterns.md)。

## 辅助脚本

使用 `scripts/helpers.py` 进行常见操作，例如按房间查找灯光、检查电池电量、查找无法连接的设备等。

## 完整参考文档

请参阅 [references/api.md](references/api.md)，了解更多内容：
- 完整的属性参考
- 所有的控制方法
- 设备功能
- 色温/色调值
- 故障排除方法

## 最佳实践：
1. 在执行任何控制操作之前，务必检查 `device.is_reachable` 是否为 `True`。
2. 执行控制命令后，调用 `device.reload()` 以更新设备状态。
3. 使用 `.attributes` 文件夹来获取设备的所有状态信息。
4. 在连续执行多个命令时，请间隔 0.5 秒。
5. 在使用设备功能之前，请先检查设备的可用功能。
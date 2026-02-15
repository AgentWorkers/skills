---
name: control-ikea-lightbulb
description: 控制 IKEA/TP-Link Kasa 智能灯泡（开关、调节亮度和颜色）。当您需要通过 IP 地址在局域网内对本地智能灯泡进行编程控制时，可以使用此功能。
---

# control-ikea-lightbulb

该技能提供了一个轻量级的Python脚本，用于控制本地的智能灯泡（支持通过`python-kasa`控制TP-Link Kasa兼容的灯泡）。它适用于不需要云账户信息的本地局域网设备，控制方式是通过设备的IP地址进行的。

**使用场景：**
- 当您想要开关灯泡时
- 当您想要调节灯泡的亮度（0-100）时
- 当您想要设置灯泡的颜色（HSV模式）时
- 当您知道灯泡的本地IP地址，并且可以从当前设备访问该灯泡时

**文件结构：**
- `scripts/control_kasa_light.py` — 主执行脚本（支持Python 3.9及以上版本）
- `scripts/light_show.py` — 用于控制灯泡灯光效果的辅助脚本（使用`python-kasa`）。主要更新包括：
  - 默认的白色灯光使用较高的色温（9000K），以使白色看起来更“白”；可以通过`--white-temp`参数进行覆盖。
  - 修复了一个错误：在从蓝色切换到红色时的闪烁效果会忽略饱和度为0的情况，以避免出现白色和蓝色之间的反复切换；`white-temp`参数仅适用于白色灯光的调节。
  - 即使没有`--double-write`参数，白色灯光的调节也会同时调整亮度。
- `scripts/run_test_light_show.sh` — 用于通过`uv`工具运行`light_show`脚本的辅助脚本

**使用说明：**
- 该仓库是为`uv`工具设计的（无需手动配置环境变量）。所有依赖项都位于`pyproject.toml`文件中，建议使用`uv run`命令来运行脚本。
  **示例：**
  ```
  uv run --project ./skills/control-ikea-lightbulb python ./skills/control-ikea-lightbulb/scripts/control_kasa_light.py --ip 192.168.4.69 --on --hsv 0 100 80 --brightness 80
  ```
- **安装`uv`工具：**
  - macOS系统：`brew install uv`
  - 跨平台系统：`pipx install uv`
- **使用示例：**
  - 控制灯泡：`./skills/control-ikea-lightbulb/scripts/run_control_kasa.sh --ip 192.168.4.69 --on --hsv 0 100 80 --brightness 80`
  - 测试灯光效果：`./skills/control-ikea-lightbulb/scripts/run_test_light_show.sh --ip 192.168.4.69 --duration 6 --transition 1 --off-flash --verbose`

**注意事项：**
- 该脚本仅适用于IKEA的TRADFRI灯泡（非Kasa系列），如需支持TRADFRI灯泡，请告知我，我会进行相应的修改。
- 控制过程完全通过局域网进行，无需使用云账户信息。

**快速入门：**
1. 安装`uv`工具（macOS系统）：`brew install uv`
2. 开启灯泡：`./skills/control-ikea-lightbulb/scripts/run_control_kasa.sh --ip 192.168.4.69 --on`
3. 调节颜色和亮度：`./skills/control-ikea-lightbulb/scripts/run_control_kasa.sh --ip 192.168.4.69 --hsv 0 100 80 --brightness 80`

**关于Python版本的要求及更新：**
- 之前该技能要求`python-kasa`版本大于或等于0.13.0，但这会导致某些系统上的依赖项解析失败。为了解决这个问题，我们调整了`pyproject.toml`文件，现在的要求如下：
  - `requires-python = ">=3.11, <4.0"`
  - `python-kasa>=0.10.2`
  - 这样可以在支持Python 3.11及以上版本的系统中选择合适的`python-kasa`版本。如果您有其他要求或希望恢复之前的设置，请告知我，我会相应地更新`pyproject.toml`和`README`文件。
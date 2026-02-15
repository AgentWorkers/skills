---
name: blucli
description: BluOS CLI（简称“blu”）用于设备的发现、播放、分组以及音量控制。
homepage: https://blucli.sh
metadata: {"clawdbot":{"emoji":"🫐","requires":{"bins":["blu"]},"install":[{"id":"go","kind":"go","module":"github.com/steipete/blucli/cmd/blu@latest","bins":["blu"],"label":"Install blucli (go)"}]}}
---

# blucli (blu)

使用 `blu` 命令来控制 Bluesound/NAD 播放器。

**快速入门：**
- `blu devices`：列出所有可用的设备。
- `blu --device <id> status`：查看指定设备的状态。
- `blu play|pause|stop`：播放/暂停/停止音乐。
- `blu volume set 15`：将音量设置为 15。

**设备选择（按优先级顺序）：**
- `--device <id|name|alias>`：通过设备 ID、名称或别名来选择设备。
- `BLU_DEVICE`：选择默认设备（如果已设置）。

**常用命令：**
- **设备分组：**
  - `blu group status`：查看设备组的状态。
  - `blu group add <device>`：将设备添加到组中。
  - `blu group remove <device>`：从组中删除设备。
- **音乐搜索/播放：**
  - `blu tunein search "query"`：搜索音乐。
  - `blu tunein play "query"`：播放指定的音乐。

**建议使用 `--json` 格式编写脚本。** 在更改播放内容之前，请务必确认目标设备正确无误。
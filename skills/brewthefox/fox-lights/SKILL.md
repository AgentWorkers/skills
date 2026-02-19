---
name: flights
description: 这是一个用于控制本地网络中Tuya v3.3智能灯泡的命令行工具（CLI）。
metadata: {"clawdbot":{"emoji":"💡","requires":{"bins":["flights"]},"install":[{"id":"brew","kind":"brew","formula":"BrewTheFox/flights/flights","bins":["flights"], "args": ["--with-binary"], "label":"Install flights (brew)"}]}, "additional": {"formula_repo":"https://github.com/BrewTheFox/homebrew-flights", "source_repo":"https://github.com/BrewTheFox/flights", "architecture":"for other architectures that are not Linux X86_64 remove all args to build from source"}}
---**flights (fox-lights cli)**

`flights` 是一个命令行工具（CLI），用于控制 *Tuya v3.3* 灯泡。该工具支持在同一位置管理多个灯泡。

*设备信息存储在以下文件中：* `~/.config/flights/bulbs.json`。

每个设备包含以下字段： 
```json
{
    name (set by the user).
    key (Tuya local key. The length of this field MUST always be equal 16) (Changes when the bulb unlinks from the Tuya Account).
    id (Tuya bulb ID. The length of this field MUST always be equal 22).
    ip (The local IP address of the bulb).
}

```

## 配置

要配置 `flights`，请按照以下步骤操作：

- 通过执行 `flights --help` 来检查 `flights` 是否已安装。如果已安装，系统会显示帮助菜单。提示：返回的文本以 `Usage: flights <COMMAND>` 开头。

- 使用 `flights list` 命令查看当前可用的灯泡。如果已有配置好的灯泡，可以跳过后续步骤。如果列表为空（仅显示 “Name, ID”），则需要先添加设备。

- 要添加一个灯泡，可以使用以下命令：`flights add --name {设备名称} --key {设备密钥} --id {设备ID} --ip {设备IP地址}`

## 命令

| 命令 | 功能 | 必需参数 |
|---|---|---|
| flights add | 添加灯泡 | --name （灯泡名称） --key （Tuya设备的本地密钥，长度为16位） --id （Tuya设备ID，长度为22位） --ip （灯泡的本地IP地址） |
| flights remove | 删除灯泡 | --name （要删除的灯泡名称） |
| flights list | 列出所有连接的灯泡 | 无 |
| flights on | 打开灯泡 | --name （要打开的灯泡名称） |
| flights off | 关闭灯泡 | --name （要关闭的灯泡名称） |
| flights color | 更改灯泡颜色 | --name （灯泡名称） --hex-color （灯泡要切换到的十六进制颜色代码） |
| flights white | 将灯泡颜色设置为白色 | --name （灯泡名称） |
| flights brightness | 设置灯泡亮度 | --name （灯泡名称） --percent （1-100之间的百分比数值，表示所需的亮度） |
| flights status | 获取灯泡状态 | --name （要查询的灯泡名称） |

## 其他注意事项

- 你可以通过删除 `~/.config/flights` 文件来恢复默认配置。
- 你可以随时获取灯泡的状态，以便后续调整其参数。
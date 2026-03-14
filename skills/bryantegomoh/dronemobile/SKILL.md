---
name: dronemobile
description: 通过 DroneMobile（Firstech/Compustar 的远程启动系统）来控制车辆。当用户需要启动汽车、关闭引擎、锁/解锁车门、打开后备箱、检查电池电压或获取车辆状态时，可以使用该功能。该功能会响应诸如“启动我的汽车”、“远程启动”、“锁车”、“解锁汽车”、“检查电池”、“打开后备箱”、“关闭引擎”、“车辆状态”等指令。使用该功能需要 `DRONEMOBILE_EMAIL` 和 `DRONEMOBILE_PASSWORD` 环境变量；对于多车辆账户，还可以使用 `DRONEMOBILE_DEVICE_KEY` 环境变量。
---
# DroneMobile车辆控制

通过自然语言控制任何连接到DroneMobile的车辆。

## 设置

在OpenClaw环境中设置凭据（openclaw.json → env）：
```json
"DRONEMOBILE_EMAIL": "your@email.com",
"DRONEMOBILE_PASSWORD": "yourpassword",
"DRONEMOBILE_DEVICE_KEY": "40632023374"
```

如果您只有一辆车，`DRONEMOBILE_DEVICE_KEY`是可选的——脚本会自动选择账户中的第一辆车。

如果尚未安装相关库，请先进行安装：
```bash
pip install drone-mobile --break-system-packages
```

## 命令

使用以下命令运行`scripts/dronemobile.py`：

| 用户请求 | 命令                |
|-----------|-------------------|
| 启动车辆 | `python3 scripts/dronemobile.py start` |
| 停止发动机 | `python3 scripts/dronemobile.py stop` |
| 锁门       | `python3 scripts/dronemobile.py lock` |
| 开锁       | `python3 scripts/dronemobile.py unlock` |
| 打开后备箱   | `python3 scripts/dronemobile.py trunk` |
| 检查电池电量/状态 | `python3 scripts/dronemobile.py status` |

## 输出

脚本会输出一条包含关键遥测数据的状态信息：
```
✅ start | Temp: 6°C | Battery: 12.5V | Engine: off
```

如果执行失败，脚本会显示错误信息并退出（退出代码为1）。

## 注意事项

- 所有命令均为“一次性执行”类型——车辆的操作是异步进行的。因此，在启动后发动机状态可能立即显示为“False”（实际启动可能需要约30秒）。
- 电池电量低于11.8V表示电量较低；低于11.0V表示电量严重不足。
- `drone-mobile` PyPI包存在一个已知问题：`response.success`始终返回`False`。脚本直接读取`raw_data['command_success']`来判断命令是否成功。已提交修复请求：https://github.com/bjhiltbrand/drone_mobile_python/pull/18
---
name: adsb-overhead
description: 当飞机飞过指定半径范围内的区域时，通过本地的ADS-B SBS/基站数据源（readsb端口30003）发送通知。该功能适用于设置或排查飞机飞越区域的警报系统、配置警报半径/起始坐标/延迟时间，以及创建能够通过WhatsApp发送通知的Clawdbot定时任务（用于监控附近飞机）。
---

# adsb-overhead

该技能用于从**本地的读取式SBS（Shortwave Broadcast Station）/基站TCP数据流**中检测飞越上空的飞机，并通过Clawdbot发送通知。

此技能适用于周期性检查任务（如cron作业），而非长时间运行的守护进程。

## 快速入门（手动测试）

1) 运行检查脚本几秒钟，查看是否检测到附近的飞机：

```bash
python3 skills/public/adsb-overhead/scripts/sbs_overhead_check.py \
  --host <SBS_HOST> --port 30003 \
  --home-lat <LAT> --home-lon <LON> \
  --radius-km 2 \
  --listen-seconds 5 \
  --cooldown-min 15
```

- 如果有输出信息，说明检测到了新的飞机（未处于冷却等待状态）。
- 如果没有输出信息，说明在检测时间段内没有新的飞机飞越。

## 工作原理

- 连接到SBS数据流（TCP接口），并设置`--listen-seconds`参数以指定监听时长。
- 根据ICAO（International Civil Aviation Organization）规定的六位编码格式，跟踪最新的飞机经纬度信息。
- 使用Haversine公式计算飞机与指定位置（`--home-lat/--home-lon`）之间的距离。
- **仅当**在`--cooldown-min`时间内未收到任何警报时，才对位于`--radius-km`范围内的飞机发出警报。
- 将检测结果保存到JSON文件中（默认路径：`~/.clawdbot/adsb-overhead/state.json`）。

关于SBS数据解析的详细规则，请参考：`references/sbs-fields.md`。

## 创建Clawdbot监控任务（cron作业）

使用Clawdbot的cron作业来定期执行该脚本。cron作业应满足以下要求：
1) 执行`.../sbs_overhead_check.py`脚本。
2) 如果脚本的输出（stdout）非空，通过WhatsApp发送该内容。

**代理程序的伪代码示例：**

- 运行：`python3 .../sbs_overhead_check.py ...`
- 如果处理后的输出（stdout）非空，通过WhatsApp发送该内容。

**建议的轮询间隔：**
- 通常30–60秒的间隔即可（考虑到系统的冷却等待时间）。
- 可以设置`--listen-seconds 3..8`，以便每次运行时能够收集更多飞机的位置数据。

## 调优建议：

- 如果希望减少误报次数，可以增加`--radius-km`的值。
- 如果数据流繁忙但导致位置信息更新不及时，可以增加`--listen-seconds`的值。
- 为防止频繁发送通知，建议设置`--cooldown-min`为15–60分钟。
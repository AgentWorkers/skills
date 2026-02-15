---
name: ham-radio-dx
description: 监控 DX 集群中稀缺的电台位置，追踪正在进行的 DX 探险活动，并为业余无线电操作员提供每日频段活动摘要。
version: 1.0.0
author: captmarbles
---

# 业余无线电DX监控工具 📻

实时监控DX集群，接收关于罕见DX电台的通知，并追踪正在进行的DX活动。非常适合希望捕捉到稀有电台联系的业余无线电操作员！

## 主要功能

📡 **实时DX站点** - 连接到全球DX集群网络  
🌍 **罕见DX提醒** - 当出现罕见电台时发送通知  
📊 **每日摘要** - 频段活动总结  
🗺️ **DX活动** - 追踪当前进行的DX活动  
⏰ **自动监控** - 通过cron任务自动运行以接收提醒  

## 快速入门

### 查看实时站点

```bash
# Get latest DX spots
python3 dx-monitor.py watch

# Specific cluster node
python3 dx-monitor.py watch --cluster ea7jxh

# Use your callsign
python3 dx-monitor.py watch --callsign KN4XYZ

# Only show NEW spots (filters duplicates)
python3 dx-monitor.py watch --new-only
```

**输出:**
```
📡 Latest DX Spots from EA7JXH

   20m   SSB      14.195   K1ABC        - CQ Contest
   40m   CW        7.015   VP8/G3XYZ    - Falklands
   15m   FT8      21.074   ZL2ABC       - New Zealand
```

### 每日摘要

```bash
python3 dx-monitor.py digest
```

**输出:**
```
# 📡 DX Digest - 2026-01-27

## Band Activity (last 100 spots)

   20m   ████████████ 24
   40m   ████████ 16
   15m   ██████ 12
   10m   ████ 8

## Rare DX Spotted

   🌍 VP8/G3XYZ    40m      7.015 - Falklands Expedition
   🌍 ZL2ABC       15m     21.074 - New Zealand
```

## DX集群节点

可用的集群：
- **ea7jxh** - dx.ea7jxh.eu:7373（欧洲）  
- **om0rx** - cluster.om0rx.com:7300（欧洲）  
- **oh2aq** - oh2aq.kolumbus.fi:7373（芬兰）  
- **ab5k** - ab5k.net:7373（美国）  
- **w6rk** - telnet.w6rk.com:7373（美国西海岸）  

## 自动监控

### 实时提醒（每5分钟检查一次）

```bash
# Add to crontab
*/5 * * * * cd ~/clawd && python3 skills/ham-radio-dx/dx-monitor.py watch --new-only --callsign YOUR_CALL >> /tmp/dx-alerts.log
```

该工具每5分钟检查一次新的DX站点并记录下来。

### 每日摘要（每天上午9点）

```bash
# Add to crontab
0 9 * * * cd ~/clawd && python3 skills/ham-radio-dx/dx-monitor.py digest >> ~/dx-digest-$(date +\%Y-\%m-\%d).txt
```

### Telegram通知

可集成到Clawdbot消息工具中：

```bash
# When rare DX appears, send Telegram alert
python3 dx-monitor.py watch --new-only | grep -E "(VP8|ZL|VK|ZS|P5)" && \
  echo "🚨 Rare DX spotted!" | # Send via Clawdbot message tool
```

## Clawdbot的示例命令：

- *"检查DX集群中的新站点"*
- *"20米波段有哪些活跃的电台？"*
- *"显示今天的DX活动摘要"*
- *"有使用VP8或ZL前缀的电台吗？"*
- *"监控VP8或ZL前缀的电台"*

## 需要关注的罕见DX前缀

**最受欢迎的：**
- **VP8** - 福克兰群岛  
- **VK0** - 赫德岛  
- **3Y0** - 布维岛  
- **FT5** - 阿姆斯特丹岛和圣保罗岛  
- **P5** - 朝鲜  
- **BS7** - 斯卡伯勒礁  

**其他罕见前缀：**
- **ZL** - 新西兰  
- **VK** - 澳大利亚  
- **ZS** - 南非  
- **9G** - 加纳  
- **S9** - 圣多美和普林西比  

## DX活动资源

追踪正在进行的DX活动：
- **NG3K日历：** https://www.ng3k.com/misc/adxo.html  
- **DX新闻：** https://www.dx-world.net/  
- **425 DX新闻：** http://www.425dxn.org/  

## 频段信息

常见的DX频率：
- **160m:** 1.830-1.840（CW），1.840-1.850（数字模式）  
- **80m:** 3.500-3.600（CW），3.790-3.800（数字模式）  
- **40m:** 7.000-7.040（CW），7.070-7.080（数字模式）  
- **30m:** 10.100-10.140（CW/仅数字模式）  
- **20m:** 14.000-14.070（CW），14.070-14.100（数字模式）  
- **17m:** 18.068-18.100（CW），18.100-18.110（数字模式）  
- **15m:** 21.000-21.070（CW），21.070-21.120（数字模式）  
- **12m:** 24.890-24.920（CW），24.920-24.930（数字模式）  
- **10m:** 28.000-28.070（CW），28.070-28.120（数字模式）  

## 提示

1. **使用你的呼号** - 一些集群要求使用有效的呼号  
2. **查看多个集群** - 不同地区的覆盖范围不同  
3. **按频段过滤** - 专注于你可以操作的频段  
4. **追踪罕见前缀** - 为最受欢迎的前缀设置提醒  
5. **早晨检查** - 通常在清晨能接收到更多DX信号  

## 技术细节

- **协议：** 通过Telnet连接到DX集群节点  
- **格式：** 标准的PacketCluster/AR-Cluster格式  
- **状态跟踪：** `/tmp/dx-monitor-state.json`  
- **依赖库：** Python 3.6及以上（仅需要stdlib库）  

## 未来计划

- **按频段过滤**  
- **DXCC实体跟踪**  
- **信号传播预测集成**  
- **日志记录**（根据需要实现）  
- **竞赛模式**（过滤竞赛中的电台）  
- **通过PSKReporter集成FT8/FT4模式**  

73，祝你的DX活动顺利！ 📻🌍
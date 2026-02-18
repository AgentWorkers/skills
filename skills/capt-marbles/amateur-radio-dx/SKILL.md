---
name: ham-radio-dx
description: 监控 DX 集群中稀有的电台位置，追踪正在进行的 DX 探险活动，并为业余无线电操作员提供每日频段活动摘要。
version: 1.0.0
author: captmarbles
---
# 短波无线电DX监控工具 📻  
实时监控DX集群，接收关于稀有DX电台的通知，并追踪正在进行的DX活动。非常适合希望捕捉到罕见通讯的短波无线电操作员！

## 主要功能  

📡 **实时DX站点** - 连接到全球DX集群网络  
🌍 **稀有DX警报** - 当出现稀有电台时发送通知  
📊 **每日摘要** - 频段活动总结  
🗺️ **DX活动** - 追踪正在进行的DX活动  
⏰ **自动监控** - 通过cron任务自动运行以接收警报  

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

**输出：**  
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

**输出：**  
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

可用集群：  
- **ea7jxh** - dx.ea7jxh.eu:7373（欧洲）  
- **om0rx** - cluster.om0rx.com:7300（欧洲）  
- **oh2aq** - oh2aq.kolumbus.fi:7373（芬兰）  
- **ab5k** - ab5k.net:7373（美国）  
- **w6rk** - telnet.w6rk.com:7373（美国西海岸）  

## 自动监控  

### 使用OpenClaw Cron（推荐）  

使用OpenClaw cron工具设置监控：  
```bash
# Create a cron job for DX alerts (every 5 minutes)
cron add --name "DX Monitor" --schedule "*/5 * * * *" --payload 'systemEvent:Check DX cluster for rare spots' --sessionTarget main
```  

### 手动使用Cron（备用方案）  

如果使用系统Cron，请以非特权用户身份运行：  
```bash
# Add to crontab (as your user, not root)
crontab -e

# Add these lines:
*/5 * * * * cd ~/clawd && python3 skills/ham-radio-dx/dx-monitor.py watch --new-only --callsign YOUR_CALL >> ~/dx-alerts.log 2>&1

# Daily digest at 9am
0 9 * * * cd ~/clawd && python3 skills/ham-radio-dx/dx-monitor.py digest >> ~/dx-digest-$(date +\%Y-\%m-\%d).txt 2>&1
```  

**注意：** 状态信息保存在`~/dx-monitor-state.json`文件中（位于您的主目录下，而非/tmp目录）。  

## Clawdbot的示例命令：  
- *"检查DX集群中的新站点"  
- *"20米频段有哪些活跃的电台？"  
- *"显示今天的DX活动摘要"  
- *"是否有使用VP8或ZL前缀的电台在通话中？"  
- *"监控VP8或ZL前缀的电台"  

## 需要关注的稀有DX前缀  

**最常被关注的：**  
- **VP8** - 福克兰群岛  
- **VK0** - 赫德岛  
- **3Y0** - 布维岛  
- **FT5** - 阿姆斯特丹岛和圣保罗岛  
- **P5** - 朝鲜  
- **BS7** - 斯卡伯勒礁  

**其他稀有前缀：**  
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

常见DX频率：  
- **160m：** 1.830-1.840（CW），1.840-1.850（数字模式）  
- **80m：** 3.500-3.600（CW），3.790-3.800（数字模式）  
- **40m：** 7.000-7.040（CW），7.070-7.080（数字模式）  
- **30m：** 10.100-10.140（仅CW模式）  
- **20m：** 14.000-14.070（CW模式），14.070-14.100（数字模式）  
- **17m：** 18.068-18.100（CW模式），18.100-18.110（数字模式）  
- **15m：** 21.000-21.070（CW模式），21.070-21.120（数字模式）  
- **12m：** 24.890-24.920（CW模式），24.920-24.930（数字模式）  
- **10m：** 28.000-28.070（CW模式），28.070-28.120（数字模式）  

## 提示：  
1. **使用您的呼号** - 一些集群要求使用有效的呼号  
2. **同时监控多个集群** - 不同地区的覆盖范围不同  
3. **按频段筛选** - 专注于您可以操作的频段  
4. **追踪稀有前缀** - 为最常被关注的频段设置警报  
5. **早晨检查** - 通常在清晨能捕捉到最佳的DX信号  

## 技术细节：  
- **协议：** 通过Telnet连接到DX集群节点  
- **格式：** 标准的PacketCluster/AR-Cluster格式  
- **状态记录：** 保存在`~/dx-monitor-state.json`文件中  
- **依赖库：** Python 3.6及以上（仅需stdlib库）  

## 新功能：**  
**AI增强模式**  
现在支持传播预测和DXCC过滤！  

```bash
# Setup your station (one time)
python3 dx-ai-enhanced.py setup

# Watch for workable DX with AI scoring
python3 dx-ai-enhanced.py watch
```  

**功能：**  
- ✨ 传播可行性评分（0-100%）  
- 🎯 根据您的需求筛选DXCC  
- 📊 智能评分：结合稀有性、传播可行性及个人需求  
- 🚨 对优质信号发送高优先级警报  
- ⚙️ 根据您的地理位置、发射功率和天线类型进行个性化设置  

更多详细信息请参阅[README-AI.md]。  

---

## 未来计划：  
- ~~DXCC实体追踪~~ ✅ 已实现（AI模式）  
- ~~传播预测集成~~ ✅ 已实现（AI模式）  
- 实时太阳数据API  
- 基于历史QSO数据训练的机器学习模型  
- 日志集成（自动填充已完成的DX记录）  
- 比赛模式（筛选比赛中的电台）  
- 通过PSKReporter集成FT8/FT4信号  

73，祝您无线电通讯愉快！ 📻🌍
---
name: longevity-bio-dashboard
description: **长寿追踪仪表板：**  
包含 NMN（烟酰胺腺嘌呤二核苷酸）、senolytics（衰老清除疗法相关技术）、Yamanaka 重编程技术的相关数据；支持设置禁食/血浆检测的提醒（通过 cron 任务自动执行）；同时具备安全的数据存储功能（使用 sats 技术保护数据）。该仪表板还支持 Web 搜索功能，以便查看相关试验信息，并能展示项目的可视化进度及物料清单（BOMs）。  
**用途：**  
1. 日常健康管理（记录个人实施的生物技术干预措施）；  
2. 实时接收试验相关提醒；  
3. 维护个人健康数据记录；  
4. 监控实现 200 年寿命目标的相关实验进展。
---

# 长寿生物仪表板

用于跟踪Yamanaka细胞/NMN（烟酰胺甲基尼古丁酰胺）和senolytics（衰老清除剂）在200年周期内的应用情况。所有数据存储在基于Sats的安全家庭账本中（使用BTC节点进行存储）。通过Cron任务设置提醒：例如“禁食窗口”何时到来；同时，Replicators系统会自动生产senolytics。

## 快速入门
1. **仪表板**：使用`canvas action=present url=dashboard.html`命令查看仪表板界面及进度信息。
2. **最新研究试验**：通过`web_search "NMN Yamanaka 2025"`查询最新的相关研究试验信息，并更新参考资料。
3. **Cron提醒**：使用`cron action=add job={...}`设置定时任务，例如控制血浆稀释比例或NMN的服用剂量。
4. **生物健康提醒**：通过`cron action=add`命令设置提醒功能，例如每周进行一次D+Q（特定健康检查）。

## 2025年的最新治疗方案
- **NMN**：每日服用350-900毫克（Renue Science的试验表明这有助于提升NAD+水平，且安全性较高；脂质体包裹的NMN效果最佳）。
- **Senolytics**：使用Dasatinib和Quercetin（哈佛-梅奥医学院的试验表明对阿尔茨海默病有积极作用），每周服用一次。
- **Yamanaka细胞**：通过特定技术实现部分细胞重编程（YouthBio公司的FDA试验表明有助于逆转大脑衰老症状）。
- **血浆稀释**：采用Altman提出的异时性血浆稀释方法（有助于清除“僵尸细胞”）。
- **禁食**：每天实行16:8的禁食模式，每季度进行为期3天的完全禁食。

参考资料：[stacks-2025.md](./references/stacks-2025.md)

## 脚本
- `scripts/remind-bio.py`：用于生成基于时间的Cron提醒及语音播报功能（涉及NMN、禁食、senolytics的使用提醒）。

## 资产文件
- `assets/dashboard.html`：用于展示仪表板界面及试验进展信息的HTML文件（使用Canvas技术制作）。

## 专业建议
- **将健康数据与Sats（加密货币）挂钩**：将个人的健康进展与加密货币奖励挂钩，以便实现即时激励。
- **节点AR（Asset Registration）**：通过摄像头拍摄照片并叠加显示“NMN服用时间”等信息。
- **持续迭代流程**：定期搜索最新研究信息，更新治疗方案，并通过Cron任务自动执行相关操作。

测试方法：运行`canvas action=present dashboard.html`，即可查看完整的200年发展路线图。
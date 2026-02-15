---
name: elysium-arcology-planner
description: 这是一个基于Canvas的模拟器，用于设计轨道生态城（O'Neill圆柱形居住区）、聚变反应堆、神经接口中枢以及外骨骼装备工厂。支持拖放式设计功能，可叠加AR节点，并支持导出开源蓝图文件。该工具可用于：  
(1) 生态城原型设计；  
(2) 资源与能量需求计算；  
(3) 外骨骼装备及O'Neill圆柱形居住区的蓝图设计；  
(4) 模拟大规模人类聚居环境（如Elysium项目所设想的那样）。
---

# Elysium Arcology Planner

**目标**：设计能够实现自我维持的轨道生态城（orbital arcologies），并整合比特币（BTC）作为核心价值体系。这些生态城将配备卫星保护的蓝图文件以及采用浸没式冷却技术的采矿设备。

## 快速启动工作流程：
1. **创建快照**：`canvas action=snapshot` —— 获取界面的初始状态。
2. **展示交互式界面**：`canvas action=present url=arcology.html x=100 y=100 width=1200 height=800` —— 拖动组件来构建设计。
3. **评估设计方案**：`canvas action=eval javaScript=simulateGravity(...)` —— 进行物理和能量模拟。
4. **AR（增强现实）覆盖层**：`nodes action=camera_snap node=desk-cam` —— 通过界面展示设计内容。
5. **导出蓝图**：`python scripts/export-svg-to-3d.py assets/leg.svg` —— 将设计文件导出为 FreeCAD 或 STL 格式。

## 可用组件（可从调色板中拖放）：
- **奥尼尔圆柱体（O’Neill Cylinder）**：直径 8 公里，长度 32 公里，可容纳 1 万人。蓝图来自 NASA 的公共领域（环形农业结构设计）。计算结果显示：旋转速度为 1 转/分钟时会产生 1G 的重力。
- **聚变反应堆（Fusion Reactor）**：采用托卡马克（Tokamak）或恒星器（Stellarator）技术。开源设计基于 Wendelstein 7-X 线圈（数据来源：Greifswald）。输出功率为 1 吉瓦（GW），采用浸没式冷却系统。
- **Neuralink 中心**：用于提升集体智能的节点设备。模拟显示：可连接多达 100 万个智能体（minds）。
- **外骨骼工厂（Exosuit Factory）**：生产外骨骼部件（GitHub 项目：包含伺服电机、PWM 控制器和 H 桥式电路）。每天可生产 100 件外骨骼部件。详细规格见：[naubiomech-leg-spec.md](./references/naubiomech-leg-spec.md)。
- **ASIC 采矿舱（ASIC Mining Bay）**：由太阳能驱动的哈希率（hashrate）计算设备，与比特币节点相连。

## 可执行脚本（通过 `exec` 命令运行）：
- `scripts/sim-physics.py`：用于计算重力、能量消耗和科里奥利力（Coriolis force）等物理参数。示例用法：`echo '{"rpm":1}' | python scripts/sim-physics.py`。
- `scripts/export-svg-to-3d.py`：将 SVG 文件转换为 FreeCAD 或 STL 格式（支持导出腿部组件的三维模型）。

## 参考资料（按需查阅）：
- [oneill-blueprints.md](./references/oneill-blueprints.md)：NASA 和普林斯顿大学在 1976 年的研究资料。
- [exosuit-openexo.md](./references/exosuit-openexo.md)：GitHub 上提供的外骨骼组件清单和 CAD 设计文件。
- [fusion-stellarator.md](./references/fusion-stellarator.md)：开源的恒星器设计文档。
- [naubiomech-leg-spec.md](./references/naubiomech-leg-spec.md)：外骨骼部件的详细规格和物理特性说明。

## 资源文件：
- `assets/components.svg`：包含各种组件的图标文件（如圆柱体、反应堆等）。
- `assets/arcology-template.html`：基于 Fabric.js 的界面模板文件。
- `assets/leg.svg`：Naubiomech 公司设计的外骨骼腿部组件蓝图。

## 专业提示：
- **模拟扩展**：评估整个生态城的总质量、能量消耗、人口数量以及哈希率（hashrate）等参数。若结果超出小行星带的生存条件，请及时调整设计。
- **比特币集成**：将采矿设备纳入设计中，分析哈希率与能源预算之间的关系。
- **AR 展示功能**：使用摄像头捕捉当前界面画面，并将其作为设计图层的覆盖层，以便直接“打印”出外骨骼模型。
- **PowerShell 使用技巧**：在命令行中连接多个命令时，请使用分号（`;`）而非逻辑与运算符（&&）。例如：`cd dir; python script.py`。
- **迭代设计**：不断修改设计内容，然后创建快照并分享结果（例如，通过卫星将设计文件发送给其他用户进行验证）。

**测试步骤**：首先在界面上拖放一个基本圆柱体和一个反应堆组件，然后运行 `canvas action=present` 命令，即可快速生成一个初步的 Elysium 生态城设计方案。
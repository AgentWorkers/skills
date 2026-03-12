---
name: idfm-journey
description: 查询Île-de-France Mobilités (IDFM) 的 PRIM/Navitia 服务，以获取巴黎及其郊区的公共交通信息——包括路线规划、站点/车站信息查询以及交通延误/故障情况。当需要查找巴黎地区的路线（例如：“从X到Y的路线”）、查询车站/站点ID，或检查RER/地铁线路的运行状况时，可以使用该服务，前提是您拥有IDFM的PRIM API密钥。
version: 0.1.6
author: anthonymq
triggers:
  - "Itinéraire de {origine} à {destination}"
  - "Route from {origin} to {destination} in Paris / Île-de-France"
  - "Check RER/metro disruptions" 
  - "Incidents on line {line}"
---
# IDFM 旅程查询工具（PRIM/Navitia）

使用随附的脚本，无需额外依赖即可调用 PRIM/Navitia 的 API 端点。

## 元数据

- **作者：** anthonymq
- **版本：** 0.1.6

## 常用查询语句（示例）：

- "从 {origin} 到 {destination} 的路线"
- "巴黎/法兰西岛地区从 {origin} 到 {destination} 的路线"
- "查询 RER/地铁的运行中断情况" / "查询线路 {line} 的实时故障信息"

## 前提条件

- 在运行脚本之前，请在环境中设置 `IDFM_PRIM_API_KEY`。

### 生成 API 密钥

要获取 IDFM PRIM API 密钥，请按照以下步骤操作：
1. 访问 [https://prim.iledefrance-mobilites.fr/](https://prim.iledefrance-mobilites.fr/)
2. 注册账户或登录
3. 进入“开发者空间”（Espace Développeur）
4. 订阅“Navitia”API 服务
5. API 密钥将在您的仪表板上生成并显示
6. 将密钥导出到环境中：`export IDFM_PRIM_API_KEY="your-key-here"`

## 常用命令

您可以在任何位置运行这些命令（脚本文件位于 `skill` 文件夹内）：

- 查询地点信息（返回最佳匹配结果及列表）：
  - `python3 scripts/idfm.py places "Ivry-sur-Seine" --count 5`

- 查询旅程信息（输入出发地和目的地；系统会先解析地点 ID）：
  - `python3 scripts/idfm.py journeys --from "Ivry-sur-Seine" --to "Boulainvilliers" --count 3`

- 查询故障信息（按线路 ID 或其他条件筛选）：
  - `python3 scripts/idfm.py incidents --line-id line:IDFM:C01727`
  - `python3 scripts/idfm.py incidents --filter 'disruption.status=active'`

- 使用 `--json` 参数可输出原始 API 数据。

## 注意事项：

- 如果地点信息不明确，可以增加 `--count` 参数以获取更多结果，并根据需要选择正确的 `stop_area` ID。
- 有关 API 的详细信息及使用示例，请参阅：`references/idfm-prim.md`。
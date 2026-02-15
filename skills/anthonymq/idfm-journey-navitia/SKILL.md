---
name: idfm-journey
description: 查询 Île-de-France Mobilités (IDFM) 的 PRIM/Navitia 服务，以获取地点信息、规划出行路线以及检查交通延误/突发事件。当需要查找 Île-de-France 地区的路线（例如：“从 X 到 Y 的路线”）、解析车站/停靠点的 ID，或检查 RER/地铁线路的运营状况时，可以使用该服务，前提是您拥有 IDFM 的 PRIM API 密钥。
---

# IDFM 旅程（PRIM/Navitia）

使用捆绑的脚本来调用 PRIM/Navitia 的端点，无需额外的依赖项。

## 先决条件

- 在运行之前，请在环境中设置 `IDFM_PRIM_API_KEY`。

## 快速命令

可以从任何位置运行脚本（脚本位于 `skill` 文件夹内）：

- 解析地点（找到最佳匹配项并列出）：
  - `python3 scripts/idfm.py places "Ivry-sur-Seine" --count 5`

- 旅程（输入/输出地点的自由文本；首先解析地点 ID）：
  - `python3 scripts/idfm.py journeys --from "Ivry-sur-Seine" --to "Boulainvilliers" --count 3`

- 事件/中断（通过事件 ID 或筛选条件）：
  - `python3 scripts/idfm.py incidents --line-id line:IDFM:C01727`
  - `python3 scripts/idfm.py incidents --filter 'disruption.status=active'`

- 添加 `--json` 选项可输出原始的 API 响应数据。

## 注意事项

- 如果地点解析结果不明确，请增加 `--count` 的值，并选择正确的 `stop_area` ID。
- 有关 API 的详细信息和示例，请参阅：`references/idfm-prim.md`。
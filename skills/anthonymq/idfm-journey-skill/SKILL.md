---
id: idfm-journey-skill
name: IDFM Journey
description: 查询Île-de-France Mobilités (IDFM)的PRIM/Navitia系统，以获取巴黎及周边地区的公共交通信息（Île-de-France大区）——包括站点位置、行程规划以及交通延误/事故的查询服务。
env: ['IDFM_PRIM_API_KEY']
license: MIT
metadata:
  author: anthonymq
  category: "Transport"
  tags: ["idfm", "navitia", "paris", "transport"]
---

# IDFM 旅程（PRIM/Navitia）

使用捆绑的脚本来调用 PRIM/Navitia 的端点，无需额外的依赖项。

## 先决条件 / 安全性

- **必填的密钥：** `IDFM_PRIM_API_KEY`（请将其视为机密信息，切勿提交到代码库中）。
- **设置范围：** 仅在运行该命令的 shell 或会话中设置此密钥。
- **请勿覆盖 `--base-url`**，除非您完全信任该端点。  
  该脚本会将 `apikey: <IDFM_PRIM_API_KEY>` 添加到您提供的任何基础 URL 中，因此恶意 URL 可能会窃取您的密钥。

## 快速命令

可以从任何位置运行脚本（脚本文件位于 `skill` 文件夹内）：

- 解析地点信息（找到最佳匹配项并显示列表）：
  - `python3 scripts/idfm.py places "Ivry-sur-Seine" --count 5`

- 查找旅程信息（输入/输出地点的名称；系统会先解析地点 ID）：
  - `python3 scripts/idfm.py journeys --from "Ivry-sur-Seine" --to "Boulainvilliers" --count 3`

- 查看事件/交通中断信息（按事件 ID 或过滤条件查询）：
  - `python3 scripts/idfm.py incidents --line-id line:IDFM:C01727`
  - `python3 scripts/idfm.py incidents --filter 'disruption.status=active'`

- 添加 `--json` 选项可输出原始的 API 响应内容。

## 注意事项

- 如果地点信息解析结果不明确，请增加 `--count` 的值，并选择正确的 `stop_area` ID。
- 有关 API 的详细信息和使用示例，请参阅：`references/idfm-prim.md`。
---
name: qgis
description: 使用 `qgis_process` 执行 QGIS 的地理空间处理操作，以实现可重复的矢量/栅格数据处理工作流程（如重投影、裁剪、融合、缓冲区生成、栅格变形等）。当用户需要 GIS/QGIS 自动化处理、坐标系转换、地理数据转换或批量地图数据处理时，可选用此方法。
metadata: { "openclaw": { "emoji": "🗺️", "requires": { "bins": ["qgis_process"] }, "install": [{ "id": "brew", "kind": "brew", "formula": "qgis", "bins": ["qgis_process"], "label": "Install QGIS CLI (brew)" }] } }
---
# QGIS

使用此技能通过 `qgis_process` 进行基于文件的、确定性的 GIS 处理。

## 核心规则

- 在运行命令之前，确认源文件、目标文件以及目标坐标参考系统（CRS）。
- 建议将数据写入新的输出路径；除非用户明确要求，否则不要覆盖源数据。
- 在执行之前，通过 `qgis_process help <algorithm-id>` 查阅算法的参数信息。
- 如果未指定输出格式，默认情况下，矢量数据的输出格式为 `GPKG`，栅格数据的输出格式为 `GeoTIFF`。
- 对于批量操作，先运行一个代表文件，然后再扩展到全部文件。

## 标准工作流程

1. 验证工具并检查其功能：

```bash
qgis_process --version
qgis_process list
```

2. 查找并检查特定的算法：

```bash
qgis_process list | rg -i "clip|buffer|reproject|merge|warp|dissolve"
qgis_process help native:clip
```

3. 使用明确的参数执行算法：

```bash
qgis_process run <algorithm-id> -- \
  INPUT=<input-path> \
  OUTPUT=<output-path>
```

4. 确认输出文件是否存在，并生成摘要报告（包括文件路径、图层数量/波段数、坐标参考系统以及数据范围）。

## 常见模式

```bash
# Reproject vector layer
qgis_process run native:reprojectlayer -- \
  INPUT=./data/input.gpkg \
  TARGET_CRS=EPSG:4326 \
  OUTPUT=./out/reprojected.gpkg

# Clip vector layer by overlay
qgis_process run native:clip -- \
  INPUT=./data/roads.gpkg \
  OVERLAY=./data/boundary.gpkg \
  OUTPUT=./out/roads_clipped.gpkg

# Buffer vector features
qgis_process run native:buffer -- \
  INPUT=./data/points.gpkg \
  DISTANCE=100 \
  SEGMENTS=8 \
  DISSOLVE=false \
  OUTPUT=./out/points_buffer_100m.gpkg
```

## 安全注意事项

- 不要随意猜测单位；务必确认距离或面积是以度还是投影单位来计算的。
- 如果坐标参考系统缺失或无效，请停止操作并询问用户所需的坐标参考系统。
- 除非用户明确要求，否则避免进行有损转换（例如丢失属性或降低数据精度）。
- 对于长时间的批量处理，请先制定一个测试计划，包括使用的算法、输入文件、输出文件以及覆盖策略。

## OpenClaw + ClawHub 的使用说明

- 确保命令在 OpenClaw 终端中能够安全执行且结果可重复。
- 保持该技能的通用性：避免使用硬编码的机器路径、凭据或私有端点。
- 在将代码发布到 clawhub.ai 时，使用半版本控制（semver）来管理版本，并仅使用通用示例数据进行代码更新。
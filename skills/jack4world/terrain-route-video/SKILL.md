---
name: terrain-route-video
description: 从一系列停靠点（城市/兴趣点，POIs）生成一个具有极简风格的动画驾驶路线视频（MP4格式），无需使用 Remotion 工具。该视频利用 OSRM 进行道路路径计算，OpenTopoMap 提供地形数据作为底图，Matplotlib 负责帧渲染，FFmpeg 负责视频编码。适用于用户需要创建/导出动态自动驾驶路线视频的场景（包括飞行视角的摄像头画面、路线动画以及路线标注），且视频中的行驶路径应严格沿着道路或高速公路进行展示。
---
# 地形路线视频（无路径优化）

## 默认输出参数（推荐设置）

- 视频尺寸：`1600x900`
- 帧率（FPS）：`30`
- 视频时长：`12秒`
- 视频样式：深色地形底图 + 红色路线标识 + 青色航点标记

## 输入参数

### 选项A）通过 `stops.json` 文件使用 OSRM 追踪道路路径

请创建一个 `stops.json` 文件：

```json
{
  "stops": [
    {"id": "01", "name": "襄阳", "lon": 112.1163785, "lat": 32.0109980},
    {"id": "02", "name": "老河口", "lon": 111.7575073, "lat": 32.4370526}
  ]
}
```

参考格式：`references/stops.schema.json`

### 选项B）通过 `.gpx` 或 `.kml` 文件追踪路线轨迹

如果您已经拥有路线轨迹数据（GPX/KML 格式），可以直接根据轨迹数据生成视频（无需使用 OSRM）：

- GPX 文件：使用 `<trkpt>` 标记轨迹点；若文件格式不支持，则使用 `<rtept>` 标记。
- KML 文件：支持两种格式：
  - 标准的 `<LineString><coordinates>` 格式
  - 2bulu/Google 风格的 `<gx:Track><gx:coord>` 格式（常见于徒步应用导出的数据）

## 执行步骤

1) 创建一个新的工作文件夹（用于保存临时文件和生成的视频帧）。

2) 创建一个 Python 虚拟环境（venv）并安装所需依赖库：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy matplotlib pillow requests
```

3) 选择以下方式之一生成视频：

**使用 `stops.json` 文件通过 OSRM 追踪道路路径：**
```bash
python /path/to/skills/terrain-route-video/scripts/terrain_route_video.py \
  --stops stops.json \
  --out out.mp4 \
  --size 1600x900 \
  --fps 30 --duration 12 \
  --title "江汉平原到洞庭湖 · 足迹" \
  --subtitle "襄阳 → 老河口 → 荆州 → 监利 → 洪湖·峰口镇 → 岳阳"
```

**使用 `.gpx` 或 `.kml` 文件追踪路线轨迹：**
```bash
python /path/to/skills/terrain-route-video/scripts/terrain_route_video.py \
  --route my-track.gpx \
  --out out.mp4 \
  --size 1600x900 \
  --fps 30 --duration 12 \
  --title "My Trip" \
  --subtitle "GPX/KML track"
```

**注意事项：**
- 脚本会在当前文件夹中生成 `frames/` 和 `.tile-cache/` 文件夹。
- 如果用户反馈视频中的路线显示不清晰（未紧贴高速公路），请保持 OSRM 生成的完整轨迹数据，避免进行任何简化处理。
- 如果视频中的文字显示不完整（缺少字符），可以指定字体路径 `--font /System/Library/Fonts/Hiragino Sans GB.ttc`（默认值）或其他支持中文的字体文件。
- OpenTopoMap 地图瓦片的可用性可能受缩放级别、地区或网络环境的影响。如果请求地图瓦片失败，脚本会自动切换到较低的缩放级别。

## 有用的配置参数

### 相机与路线相关设置

- `--zoom 18`（地形地图瓦片的缩放级别；默认值为 18；瓦片请求失败时可能会自动调整）
- `--lookahead 0.02`（相机在路径前方预判移动的距离；数值越小，画面越稳定）
- `--dwell 0`（在每个停车点暂停视频帧的显示；默认值为 0）
- `--no-follow`（显示静态的全路线视图，不进行动态跟随）

### 地图底图显示效果相关设置（新增）

这些参数可用于调整地图标签的可见性：

- `--basemap-alpha 0.85`（提高底图的可见度）
- `--overlay-alpha 0.25`（减少底层图层的透明度，使地图标签更清晰）
- `--basemap-contrast 1.20`（增加底图的对比度）
- `--basemap-sharpness 1.45`（使文字和线条更加清晰）
- `--basemap-color 0.80`（调整底图的饱和度）
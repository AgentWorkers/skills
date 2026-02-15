# render-stl-png

该工具可以将 STL 文件渲染为 PNG 格式的图像，呈现出美观且一致的 3D 视角效果（类似于 Blender 的默认视角），并且图像背景为纯色。

这是一个 **确定性渲染器**（deterministic renderer）：
- 不使用 OpenGL；
- 不依赖于 Blender；
- 采用简单的相机模型、z-缓冲区（z-buffer）以及 Lambert 着色算法。

## 输入参数

- STL 文件路径（ASCII 或二进制格式）
- 输出 PNG 文件路径

## 配置参数

- `--size <px>`：图像的宽度和高度（以像素为单位），默认值为 `1024`
- `--bg "#rrggbb"`：背景颜色，默认值为 `#0b0f14`
- `--color "#rrggbb"`：网格的基本颜色，默认值为 `#4cc9f0`
- `--azim-deg <deg>`：相机在 Z 轴上的方位角，默认值为 `-35`
- `--elev-deg <deg>`：相机的高度角，默认值为 `25`
- `--fov-deg <deg>`：视角的视场角，默认值为 `35`
- `--margin <0..0.4>`：图像边框的占视图比例，默认值为 `0.08`
- `--light-dir "x,y,z"`：方向光向量，默认值为 `-0.4,-0.3,1.0`

## 使用方法

### 单次渲染

```bash
python3 scripts/render_stl_png.py \
  --stl /path/to/model.stl \
  --out /tmp/model.png \
  --color "#ffb703" \
  --bg "#0b0f14" \
  --size 1200
```

### 推荐的封装方式（Wrapper）

该封装工具会创建一个虚拟环境（venv），以便可以使用 `pillow` 库，并执行渲染任务。

```bash
bash scripts/render_stl_png.sh /path/to/model.stl /tmp/model.png --color "#ffb703"
```

## 注意事项

- 该工具主要用于生成 **营销/预览图片**，而非追求高度真实的图像效果；
- 如果需要复杂的灯光效果或材质模型，请使用 Blender；不过使用该工具可以快速且一致地获得所需的渲染结果。
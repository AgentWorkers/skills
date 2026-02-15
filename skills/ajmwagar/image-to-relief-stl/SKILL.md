---
name: image-to-relief-stl
description: 将源图像（或多色掩码图像）转换为可用于3D打印的STL文件，具体方法是将图像中的颜色或灰度值映射为相应的高度值。这种方法适用于从图像生成工具（如nano-banana-pro等）获得的图像，且需要通过一个可预测、可靠的流程将其转换为可实际打印的STL模型。
metadata:
  openclaw:
    requires:
      bins: ["python3", "potrace", "mkbitmap"]
    install:
      - id: apt
        kind: apt
        package: potrace
        bins: ["potrace", "mkbitmap"]
        label: Install potrace + mkbitmap (apt)
      - id: brew
        kind: brew
        formula: potrace
        bins: ["potrace", "mkbitmap"]
        label: Install potrace + mkbitmap (brew)
---

# image-to-relief-stl

该技能可将输入图像转换为可打印的 STL（STL：Standard Tessellation Language）文件，具体方法是将图像中的颜色（或灰度值）映射为高度值，从而生成具有立体效果的模型。

这是一个易于与其他工具协同使用的工作流程：
- 使用 **nano-banana-pro**（或任何图像处理工具）生成一张单色图像。
- 运行此技能将单色图像转换为浮雕模型。

## 实用限制（以确保转换效果良好）

请确保图像模型满足以下要求：
- 仅包含 **N 种纯色**（不允许有渐变效果）；
- 不包含阴影或抗锯齿处理；
- 图形轮廓清晰、边缘分明。

这些要求有助于提高模型分割的准确性。

## 快速入门（使用图像文件）

```bash
bash scripts/image_to_relief.sh input.png --out out.stl \
  --mode palette \
  --palette '#000000=3.0,#ffffff=0.0' \
  --base 1.5 \
  --pixel 0.4
```

### 灰度模式

```bash
bash scripts/image_to_relief.sh input.png --out out.stl \
  --mode grayscale \
  --min-height 0.0 \
  --max-height 3.0 \
  --base 1.5 \
  --pixel 0.4
```

## 输出结果

- `out.stl`：生成的 STL 文件（格式为 ASCII 格式）；
- 可选 `out-preview.svg`：通过 potrace 工具生成的矢量预览图（效果仅供参考）。

## 注意事项

- 该版本的实现基于 **栅格高度场** 网格划分技术（稳定性较高，无需依赖复杂的 CAD 工具）；
- `--pixel` 参数用于控制输出文件的分辨率：数值越小，模型细节越丰富；数值越大，生成的 STL 文件体积越大。
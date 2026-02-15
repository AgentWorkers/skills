---
name: trace-to-svg
description: 使用 potrace/mkbitmap 将轮廓位图图像（PNG/JPG/WebP 格式）转换为干净的 SVG 路径。该工具可用于将徽标/剪影转换为矢量图形，以便后续的 CAD 工作流程（如 create-dxf etch-svg_path）使用，同时也可将参考图像转换为可用于制造的轮廓文件。
metadata:
  openclaw:
    requires:
      bins: ["potrace", "mkbitmap"]
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

# trace-to-svg

使用 `mkbitmap` 和 `potrace` 将位图转换为矢量 SVG。

## 快速入门

```bash
# 1) Produce a silhouette-friendly SVG
bash scripts/trace_to_svg.sh input.png --out out.svg

# 2) Higher contrast + less noise
bash scripts/trace_to_svg.sh input.png --out out.svg --threshold 0.6 --turdsize 20

# 3) Feed into create-dxf (example)
# - set create-dxf drawing.etch_svg_paths[].d to the SVG path `d` you want, or
# - store the traced SVG and reference it in your pipeline.
```

## 注意事项

- 该方法最适合用于 **徽标、剪影图像以及高对比度的形状**。
- 对于照片或具有复杂阴影效果的图像，转换效果很大程度上取决于阈值设置。
- 输出结果通常为一个或多个 `<path>` 元素。
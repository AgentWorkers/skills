---
name: create-dxf
description: 根据从自然语言设计描述中生成的经过严格验证的 JSON 规范，创建可用于提交询价（RFQ）的 2D DXF 文件（以及可选的 SVG 预览文件）。这些文件适用于板材/零件加工（如水刀切割、激光切割或数控铣削），包括安装板、加强板、支架、孔图案和槽等部件。
---

# create-dxf

该工具能够根据一个简单的 JSON 规范（以中心为原点，单位明确）生成适合制造的 DXF 文件，并同时生成一个 SVG 预览图。

## 快速入门

1) 将输入的提示字符串转换为 JSON 格式（详见 `references/spec_schema.md`）。
2) 验证输入数据的格式（使用以下代码块）：
```bash
python3 scripts/create_dxf.py validate spec.json
```

3) 生成 DXF 文件及 SVG 预览图（使用以下代码块）：
```bash
python3 scripts/create_dxf.py render spec.json --outdir out
```

**输出结果：**
- `out/<name>.dxf`（DXF 文件）
- `out/<name>.svg`（SVG 预览图）

## 注意事项：

- 为了确保兼容性，DXF 文件使用了一些简单的图形元素：
  - 闭合的 `LWPOLYLINE` 来表示外部轮廓
  - `CIRCLE` 来表示孔洞

- 默认的图层设置符合制造需求：
  - `CUT_OUTER`（外部轮廓）
  - `CUT_INNER`（孔洞/槽）
  - `NOTES`（可选）

## 相关资源：

- `scripts/create_dxf.py`（生成 DXF 文件的脚本）
- `references/spec_schema.md`（JSON 规范的详细说明）
- `references/test_prompts.md`（测试用例示例）
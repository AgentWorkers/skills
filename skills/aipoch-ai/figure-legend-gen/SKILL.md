---
name: figure-legend-gen
description: 生成科学图表和图形的标准化图例。当用户为研究图表、学术论文或数据图表上传/请求图例时，该工具会自动启动。支持生成条形图、折线图、散点图、箱线图、热力图以及显微镜图像的图例。该工具仅生成文本形式的图例，不提供可视化效果。
  Trigger when user uploads/requesting legend for research figures, academic papers,
  or data charts. Supports bar charts, line graphs, scatter plots, box plots,
  heatmaps, and microscopy images. This tool generates text legends only, not visualizations.
version: 1.0.0
category: Research
tags: []
author: AIPOCH
license: MIT
status: Draft
risk_level: High
skill_type: Hybrid (Tool/Script + Network/API)
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# 图例生成器

该工具可为科学研究图表和图像生成符合学术标准的图例。

## 支持的图表类型

| 图表类型 | 描述 |
|------------|-------------|
| 条形图 | 比较不同类别的值 |
| 折线图 | 显示随时间变化的趋势或连续数据 |
| 散点图 | 展示变量之间的关系 |
| 箱形图 | 显示数据分布和异常值 |
| 热图 | 显示矩阵数据的强度 |
| 显微镜图像 | 荧光/共聚焦图像 |
| 流式细胞术 | FACS 图和直方图 |
| 西部印迹 | 蛋白质表达条带 |

## 使用方法

```bash
python scripts/main.py --input <image_path> --type <chart_type> [--output <output_path>]
```

### 参数

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| `--input` | 是 | 图表图像的路径 |
| `--type` | 是 | 图表类型（条形图/折线图/散点图/箱形图/热图/显微镜图像/流式细胞术/西部印迹） |
| `--output` | 否 | 图例文本的输出路径（默认：标准输出） |
| `--format` | 否 | 输出格式（文本/Markdown/LaTeX），默认：Markdown |
| `--language` | 否 | 语言（英语/中文），默认：英语 |

### 示例

```bash
# Generate legend for bar chart
python scripts/main.py --input figure1.png --type bar

# Save to file
python scripts/main.py --input plot.jpg --type line --output legend.md

# Chinese output
python scripts/main.py --image.png --type scatter --language zh
```

## 图例结构

生成的图例遵循学术标准：

1. **图例编号** - 顺序编号 |
2. **简短标题** - 简洁的描述 |
3. **主要描述** - 图表所展示的内容 |
4. **数据细节** - 关键统计信息/测量结果 |
5. **方法论** | 简要的实验背景 |
6. **统计信息** | P 值、显著性标记 |
7. **刻度尺** - 适用于显微镜图像 |

## 技术说明

- **难度**：低 |
- **依赖库**：PIL、pytesseract（可选的 OCR 工具） |
- **处理流程**：通过视觉分析检测图表类型 |
- **输出格式**：默认为结构化的 Markdown 格式 |

## 参考资料

- `references/legend_templates.md` - 各图表类型的图例模板 |
- `references/academic_style_guide.md` - 格式化指南 |

## 风险评估

| 风险指标 | 评估结果 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 使用 Python 脚本 | 高 |
| 网络访问 | 外部 API 调用 | 高 |
| 文件系统访问 | 读写数据 | 中等 |
| 指令篡改 | 有标准的提示和指导 | 低 |
| 数据泄露 | 数据经过安全处理 | 中等 |

## 安全性检查

- [ ] 无硬编码的凭据或 API 密钥 |
- [ ] 无未经授权的文件系统访问 |
- [ ] 输出内容不会泄露敏感信息 |
- [ ] 有防止命令注入的保护机制 |
- [ ] API 请求仅使用 HTTPS 协议 |
- [ ] 输入内容经过验证 |
- [ ] 实现了 API 超时和重试机制 |
- [ ] 输出目录受到限制，仅在工作区内访问 |
- [ ] 脚本在沙箱环境中执行 |
- [ ] 错误信息经过处理，不会暴露内部路径 |
- [ ] 依赖库经过审核 |
- [ ] 未暴露内部服务架构 |

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt
```

## 评估标准

### 成功指标
- [ ] 脚本能够成功执行主要功能 |
- [ ] 输出结果符合质量标准 |
- [ ] 能够优雅地处理边缘情况 |
- [ ] 性能表现可接受 |

### 测试用例
1. **基本功能**：输入有效数据 → 生成预期输出 |
2. **边缘情况**：输入无效数据 → 脚本能够优雅地处理错误 |
3. **性能**：处理大规模数据集时，处理时间在可接受范围内 |

## 生命周期状态

- **当前阶段**：草稿阶段 |
- **下一次审查日期**：2026-03-06 |
- **已知问题**：无 |
- **计划中的改进**：
  - 优化性能 |
  - 支持更多图表类型
---
name: manimce-best-practices
description: |
  Trigger when: (1) User mentions "manim" or "Manim Community" or "ManimCE", (2) Code contains `from manim import *`, (3) User runs `manim` CLI commands, (4) Working with Scene, MathTex, Create(), or ManimCE-specific classes.

  Best practices for Manim Community Edition - the community-maintained Python animation engine. Covers Scene structure, animations, LaTeX/MathTex, 3D with ThreeDScene, camera control, styling, and CLI usage.

  NOT for ManimGL/3b1b version (which uses `manimlib` imports and `manimgl` CLI).
---

## 使用方法

有关详细说明和代码示例，请阅读各个规则文件：

### 核心概念
- [rules/scenes.md](rules/scenes.md) - 场景结构、构建方法及场景类型
- [rules/mobjects.md](rules/mobjects.md) - Mobject类型、VMobject、组（Groups）及定位（Positioning）
- [rulesanimations.md](rulesanimations.md) - 动画类、动画播放及时间控制

### 创建与变换
- [rules/creation-animations.md](rules/creation-animations.md) - 创建动画、淡入效果（FadeIn）、绘制边框后填充（DrawBorderThenFill）
- [rules/transform-animations.md](rules/transform-animations.md) - 变换（Transform）、替换变换（ReplacementTransform）、变形（Morphing）
- [rules/animation-groups.md](rules/animation-groups.md) - 动画组（AnimationGroups）、延迟开始（LaggedStart）、动画序列（Succession）

### 文本与数学
- [rules/text.md](rules/text.md) - 文本Mobject、字体及样式设置
- [rules/latex.md](rules/latex.md) - MathTex、Tex格式、LaTeX渲染及公式着色
- [rules/text-animations.md](rules/text-animations.md) - 文本输入、逐字符添加文本（AddTextLetterByLetter）、光标定位输入（TypeWithCursor）

### 样式与外观
- [rules/colors.md](rules/colors.md) - 颜色常量、渐变效果及颜色操作
- [rules/styling.md](rules/styling.md) - 填充颜色（Fill）、描边（Stroke）、不透明度（Opacity）及视觉属性设置

### 定位与布局
- [rules/positioning.md](rules/positioning.md) - 移动（move_to）、并排放置（next_to）、对齐（align_to）、位移（shift）方法
- [rules/grouping.md](rules/grouping.md) - VGroup、Group结构、排列方式及布局规则

### 坐标系与绘图
- [rules/axes.md](rules/axes.md) - 轴（Axes）、数字平面（NumberPlane）及坐标系（Coordinate Systems）
- [rules/graphing.md](rules/graphing.md) - 绘图函数、参数曲线（Parametric Curves）
- [rules/3d.md](rules/3d.md) - 3D场景（3DScene）、3D轴（3D Axes）、曲面（Surfaces）及相机视角（Camera Orientation）

### 动画控制
- [rules/timing.md](rules/timing.md) - 动画速度函数、缓动效果（Easing）、运行时间（run_time）、延迟比例（lag_ratio）
- [rules/updaters.md](rules/updaters.md) - 更新器（Updaters）、值追踪器（ValueTracker）及动态动画
- [rules/camera.md](rules/camera.md) - 移动相机（MovingCameraScene）、缩放（Zoom）、平移（Pan）及帧操作（Frame Manipulation）

### 配置与命令行界面
- [rules/cli.md](rules/cli.md) - 命令行接口、渲染选项及质量设置
- [rules/config.md](rules/config.md) - 配置系统、manim.cfg文件及配置参数

### 形状与几何
- [rules/shapes.md](rules/shapes.md) - 圆（Circle）、正方形（Square）、矩形（Rectangle）、多边形（Polygon）及基本几何形状
- [rules/lines.md](rules/lines.md) - 直线（Line）、箭头（Arrow）、向量（Vector）、虚线（DashedLine）及连接线（Connectors）

## 示例项目

以下是包含常见功能的完整测试示例文件：
- [examples/basic_animations.py](examples/basic_animations.py) - 形状创建、文本显示、延迟动画、路径移动
- [examples/math_visualization.py](examples/math_visualization.py) - LaTeX公式、彩色数学表示、导数计算
- [examples/updater_patterns.py](examples/updater_patterns.py) - 值追踪器、动态动画、物理模拟
- [examples/graph_plotting.py](examples/graph_plotting.py) - 坐标轴、函数绘制、面积计算、黎曼和（Riemann Sums）、极坐标图
- [examples/3d_visualization.py](examples/3d_visualization.py) - 3D场景、曲面显示、3D相机效果、参数曲线

## 场景模板

可复制并修改这些模板以开始新的项目：
- [templates/basic_scene.py](templates/basic_scene.py) - 标准2D场景模板
- [templates/camera_scene.py](templates/camera_scene.py) - 带有缩放和平移功能的移动相机场景
- [templates/threed_scene.py](templates/threed_scene.py) - 包含曲面和相机旋转的3D场景

## 快速参考

### 基本场景结构
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create mobjects
        circle = Circle()

        # Add to scene (static)
        self.add(circle)

        # Or animate
        self.play(Create(circle))

        # Wait
        self.wait(1)
```

### 绘制命令
```bash
# Basic render with preview
manim -pql scene.py MyScene

# Quality flags: -ql (low), -qm (medium), -qh (high), -qk (4k)
manim -pqh scene.py MyScene
```

### 与3b1b/ManimGL的主要区别

| 特性          | Manim社区版本        | 3b1b/ManimGL版本        |
|-----------------|------------------|-------------------|
| 导入方式        | `from manim import *`      | `from manimlib import *`      |
| 命令行接口       | `manim`            | `manimgl`            |
| 数学文本格式    | `MathTex(r"\pi")`       | `Tex(R"\pi")`         |
| 场景类型        | `Scene`            | `InteractiveScene`        |
| 所属包          | `manim` (PyPI)        | `manimgl` (PyPI)        |

### Jupyter笔记本支持

使用`%%manim`魔法命令：

```python
%%manim -qm MyScene
class MyScene(Scene):
    def construct(self):
        self.play(Create(Circle()))
```

### 需避免的常见问题

1. **版本混淆** - 确保使用`manim`（社区版本），而非`manimgl`（3b1b版本）
2. **导入语句检查** - `from manim import *`对应ManimCE；`from manimlib import *`对应ManimGL
3. **教程过时** - 视频教程可能已过时，请参考官方文档
4. **manimpango问题** - 如果文本渲染失败，请检查manimpango的安装要求
5. **路径问题（Windows系统）** - 如果找不到`manim`命令，尝试使用`python -m manim`或检查系统路径（PATH）

### 安装方法
```bash
# Install Manim Community
pip install manim

# Check installation
manim checkhealth
```

### 有用命令
```bash
manim -pql scene.py Scene    # Preview low quality (development)
manim -pqh scene.py Scene    # Preview high quality
manim --format gif scene.py  # Output as GIF
manim checkhealth            # Verify installation
manim plugins -l             # List plugins
```
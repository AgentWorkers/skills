---
name: python-executor
description: |
  Execute Python code in a safe sandboxed environment via [inference.sh](https://inference.sh).
  Pre-installed: NumPy, Pandas, Matplotlib, requests, BeautifulSoup, Selenium,
  Playwright, MoviePy, Pillow, OpenCV, trimesh, and 100+ more libraries.
  Use for: data processing, web scraping, image manipulation, video creation,
  3D model processing, PDF generation, API calls, automation scripts.
  Triggers: python, execute code, run script, web scraping, data analysis,
  image processing, video editing, 3D models, automation, pandas, matplotlib
allowed-tools: Bash(infsh *)
---

# Python代码执行器

在安全、沙盒化的环境中执行Python代码，该环境预装了100多个库。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Run Python code
infsh app run infsh/python-executor --input '{
  "code": "import pandas as pd\nprint(pd.__version__)"
}'
```

## 应用详情

| 属性 | 值 |
|----------|-------|
| 应用ID | `infsh/python-executor` |
| 环境 | Python 3.10（仅支持CPU） |
| 内存 | 8GB（默认）/ 16GB（高内存配置） |
| 超时时间 | 1-300秒（默认：30秒） |

## 输入格式

```json
{
  "code": "print('Hello World!')",
  "timeout": 30,
  "capture_output": true,
  "working_dir": null
}
```

## 预装库

### 网页抓取与HTTP
- `requests`, `httpx`, `aiohttp` - HTTP客户端
- `beautifulsoup4`, `lxml` - HTML/XML解析
- `selenium`, `playwright` - 浏览器自动化
- `scrapy` - 网页抓取框架

### 数据处理
- `numpy`, `pandas`, `scipy` - 数值计算
- `matplotlib`, `seaborn`, `plotly` - 数据可视化

### 图像处理
- `pillow`, `opencv-python-headless` - 图像操作
- `scikit-image`, `imageio` - 图像处理算法

### 视频与音频
- `moviepy` - 视频编辑
- `av` (PyAV), `ffmpeg-python` - 视频处理
- `pydub` - 音频处理

### 3D处理
- `trimesh`, `open3d` - 3D网格处理
- `numpy-stl`, `meshio`, `pyvista` - 3D文件格式处理

### 文档与图形
- `svgwrite`, `cairosvg` - SVG文件生成
- `reportlab`, `pypdf2` - PDF文件生成

## 示例

### 网页抓取

```bash
infsh app run infsh/python-executor --input '{
  "code": "import requests\nfrom bs4 import BeautifulSoup\n\nresponse = requests.get(\"https://example.com\")\nsoup = BeautifulSoup(response.content, \"html.parser\")\nprint(soup.find(\"title\").text)"
}'
```

### 数据分析与可视化

```bash
infsh app run infsh/python-executor --input '{
  "code": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndata = {\"name\": [\"Alice\", \"Bob\"], \"sales\": [100, 150]}\ndf = pd.DataFrame(data)\n\nplt.bar(df[\"name\"], df[\"sales\"])\nplt.savefig(\"outputs/chart.png\")\nprint(\"Chart saved!\")"
}'
```

### 图像处理

```bash
infsh app run infsh/python-executor --input '{
  "code": "from PIL import Image\nimport numpy as np\n\n# Create gradient image\narr = np.linspace(0, 255, 256*256, dtype=np.uint8).reshape(256, 256)\nimg = Image.fromarray(arr, mode=\"L\")\nimg.save(\"outputs/gradient.png\")\nprint(\"Image created!\")"
}'
```

### 视频制作

```bash
infsh app run infsh/python-executor --input '{
  "code": "from moviepy.editor import ColorClip, TextClip, CompositeVideoClip\n\nclip = ColorClip(size=(640, 480), color=(0, 100, 200), duration=3)\ntxt = TextClip(\"Hello!\", fontsize=70, color=\"white\").set_position(\"center\").set_duration(3)\nvideo = CompositeVideoClip([clip, txt])\nvideo.write_videofile(\"outputs/hello.mp4\", fps=24)\nprint(\"Video created!\")",
  "timeout": 120
}'
```

### 3D模型处理

```bash
infsh app run infsh/python-executor --input '{
  "code": "import trimesh\n\nsphere = trimesh.creation.icosphere(subdivisions=3, radius=1.0)\nsphere.export(\"outputs/sphere.stl\")\nprint(f\"Created sphere with {len(sphere.vertices)} vertices\")"
}'
```

### API调用

```bash
infsh app run infsh/python-executor --input '{
  "code": "import requests\nimport json\n\nresponse = requests.get(\"https://api.github.com/users/octocat\")\ndata = response.json()\nprint(json.dumps(data, indent=2))"
}'
```

## 文件输出

所有生成的文件将自动保存到`outputs/`目录：

```python
# These files will be in the response
plt.savefig('outputs/chart.png')
df.to_csv('outputs/data.csv')
video.write_videofile('outputs/video.mp4')
mesh.export('outputs/model.stl')
```

## 变体配置

```bash
# Default (8GB RAM)
infsh app run infsh/python-executor --input input.json

# High memory (16GB RAM) for large datasets
infsh app run infsh/python-executor@high_memory --input input.json
```

## 使用场景

- **网页抓取** - 从网站提取数据
- **数据分析** - 处理和可视化数据集
- **图像处理** - 调整图像大小、裁剪、合成图片
- **视频制作** - 生成带有文字覆盖层的视频
- **3D处理** - 加载、转换、导出3D模型
- **API集成** - 调用外部API
- **PDF生成** - 创建报告和文档
- **自动化** - 运行任何Python脚本

## 重要说明

- **仅支持CPU** - 不支持GPU/机器学习库（如需使用，请使用专门的AI工具）
- **安全执行** - 代码在隔离的子进程中运行
- **非交互式** - 使用`plt.savefig()`而非`plt.show()`进行输出
- **文件自动检测** - 生成的文件会自动被检测并返回

## 相关技能

```bash
# AI image generation (for ML-based images)
npx skills add inference-sh/agent-skills@ai-image-generation

# AI video generation (for ML-based videos)
npx skills add inference-sh/agent-skills@ai-video-generation

# LLM models (for text generation)
npx skills add inference-sh/agent-skills@llm-models
```

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 通过命令行（CLI）运行应用程序的方法
- [应用程序代码](https://inference.sh/docs/extend/app-code) - 了解应用程序的执行原理
- [沙盒化代码执行](https://inference.sh/blog/tools/sandboxed-execution) - 为代理程序提供安全的代码执行环境
---
name: travel-destination-brochure
description: "根据城市名称生成旅行目的地场景和宣传资料：从 OpenStreetCam 和 Wikimedia Commons 获取街道级及地标图像，然后使用 VLM Run (vlmrun) 工具生成旅行视频和旅行计划。适用于用户需要某城市的旅行宣传资料、目的地指南、旅行视频或旅行规划的情况。"
---

# 旅行目的地宣传册与视频制作

通过结合 OpenStreetCam 提供的街景照片、Wikimedia Commons 的图片以及 VLMRun 工具，可以为目的地城市制作旅行宣传册、视频和一日行程计划。

## 先决条件

在开始之前，请确保您已满足以下条件：

- 安装了 **Python 3.10 或更高版本**  
- 拥有 **互联网连接**（用于下载图片和访问 API）  
- 拥有 **VLMRUN_API_KEY**（可选，但生成视频和行程计划时需要）  

**无需 API 密钥的情况：**  
- OpenStreetCam（公共读取权限）  
- Wikimedia Commons（公共访问权限）  
- Nominatim 地理编码服务（公共访问权限）  

## 安装步骤

### 第 1 步：验证 Python 安装

检查是否已安装 Python 3.10 或更高版本：

**Windows（PowerShell）：**  
```powershell
python --version
# Should show Python 3.10.x or higher
```  

**macOS/Linux：**  
```bash
python3 --version
# Should show Python 3.10.x or higher
```  

如果未安装 Python 或版本过低，请执行以下操作：  
- **Windows**：从 [python.org](https://www.python.org/downloads/) 下载 Python  
- **macOS**：使用 `brew install python@3.11`（或使用官方安装程序）  
- **Linux**：使用 `sudo apt install python3.11`（Ubuntu/Debian）或通过相应的包管理器安装  

### 第 2 步：安装 uv（包管理器）

**Windows（PowerShell）：**  
```powershell
# Using pip
pip install uv

# Or using PowerShell installer
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```  

**macOS/Linux：**  
```bash
# Using pip
pip install uv

# Or using curl installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```  

**验证安装结果：**  
```bash
uv --version
```  

### 第 3 步：创建虚拟环境

导航到技能目录并创建一个虚拟环境：  

**Windows（PowerShell）：**  
```powershell
cd c:\Users\mehed\.claude\skills\travel-destination-brochure
uv venv
.venv\Scripts\Activate.ps1
```  

**macOS/Linux：**  
```bash
cd ~/.claude/skills/travel-destination-brochure
uv venv
source .venv/bin/activate
```  

**注意：** 激活虚拟环境后，终端提示中应显示 `(.venv)`。  

### 第 4 步：安装依赖项

安装所需的软件包：  
```bash
# Install vlmrun CLI (required for video and travel plan generation)
uv pip install "vlmrun[cli]"

# Install requests (required for API calls)
uv pip install requests
```  

**验证安装结果：**  
```bash
vlmrun --version
python -c "import requests; print(requests.__version__)"
```  

### 第 5 步：设置 VLMRUN_API_KEY（可选但推荐）

生成旅行视频和行程计划需要 VLMRUN API 密钥：  

**Windows（PowerShell）：**  
```powershell
# Set for current session
Check .env file for api key

$env:VLMRUN_API_KEY="your-api-key-here"

# Set permanently (User-level)
[System.Environment]::SetEnvironmentVariable('VLMRUN_API_KEY', 'your-api-key-here', 'User')
```  

**macOS/Linux：**  
```bash
# Set for current session
export VLMRUN_API_KEY="your-api-key-here"

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export VLMRUN_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```  

**验证环境变量：**  

阅读 `.env` 文件以获取 API 密钥：  
```bash
# Windows PowerShell
echo $env:VLMRUN_API_KEY

# macOS/Linux
echo $VLMRUN_API_KEY
```  

### 第 6 步：验证安装效果

测试所有功能是否正常运行：  
```bash
# Test geocoding (should work without API key)
uv run scripts/geocode_city.py "Paris, France"

# Test vlmrun (if API key is set)
vlmrun --help
```  

**安装完成！** 现在您可以开始制作旅行宣传册了。  

## 快速入门（推荐）

使用自动化的一体化脚本：  

**Windows（PowerShell）：**  
```powershell
uv run scripts/simple_travel_brochure.py --city "Doha, Qatar"
```  

**macOS/Linux：**  
```bash
uv run scripts/simple_travel_brochure.py --city "Doha, Qatar"
```  

**备用方案（如果 uv 无法使用）：**  
```bash
python scripts/simple_travel_brochure.py --city "Doha, Qatar"
```  

该脚本将：  
1. 将城市名称转换为坐标  
2. 从 OpenStreetCam 获取 3 张街景照片  
3. 从 Wikimedia Commons 获取 2 张地标图片（总共 5 张图片）  
4. 使用 vlmrun 生成 30 秒的旅行视频（如果设置了 `VLMRUN_API_KEY`）  
5. 使用 vlmrun 生成一日行程计划（如果设置了 `VLMRUN_API_KEY`）  
6. 自动清理临时文件  

**选项：**  
- `--output DIR` — 输出目录（默认：`./travel_brochure`）  
- `--osc-count N` — OpenStreetCam 照片数量（默认：3 张）  
- `--commons-count N` — Wikimedia Commons 图片数量（默认：2 张）  

**注意：** 需要设置 `VLMRUN_API_KEY` 环境变量才能生成视频和行程计划。如果未设置 API 密钥，脚本会跳过视频生成步骤。  

**示例：**  
```bash
uv run scripts/simple_travel_brochure.py --city "Paris, France" --output ./paris_trip
```  

**输出结果：**  
- `images/` — 下载的图片（共 5 张）  
- `manifest.json` — 关于城市的元数据、坐标和图片路径  
- `video/` — 生成的旅行视频（如果设置了 VLMRUN_API_KEY）  
- `travel_plan.md` — 一日行程计划（如果设置了 VLMRUN_API_KEY）  

---

## 高级用法：逐步操作流程

如需对每个步骤有更多控制权，可以使用以下单独的脚本：  

### 流程概述  

1. **收集输入**——从用户处获取目的地城市名称。  
2. **地理编码**——将城市名称转换为坐标（纬度、经度）。  
3. **获取图片和信息**——从 OpenStreetCam 获取附近照片；从 Wikimedia Commons 获取图片和元数据。  
4. **生成内容**——使用 vlmrun 从收集到的图片和信息生成旅行视频和行程计划。  

所有路径均相对于包含此 SKILL.md 的目录。  

**运行脚本的方法：**  
- `uv run scripts/script_name.py`（推荐，通过 PEP 723 自动处理依赖项）  
- `python scripts/script_name.py`（如果依赖项已安装）  

### 第 1 步：获取目的地城市  

询问用户：“您希望为哪个城市制作旅行宣传册和视频？” 使用确切的城市名称（如果名称不明确，请提供国家/地区信息）进行地理编码和图片搜索。  

### 第 2 步：城市地理编码  

将城市名称转换为纬度/经度（例如，用于 OpenStreetCam 和可选的 Commons 地理搜索）：  
```bash
uv run scripts/geocode_city.py "Paris, France"
# Or: python scripts/geocode_city.py "Tokyo"
```  

输出结果为包含 `lat`、`lng`、`display_name` 的 JSON 数据。这些数据将用于后续步骤。  

### 第 3 步：获取 OpenStreetCam 照片  

OpenStreetCam 提供街景图片。基础 URL：`https://api.openstreetcam.org/`：  
- **附近轨迹**：`POST /nearby-tracks` — 请求参数：`lat`、`lng`、`distance`（公里）  
- **附近照片**：`POST /1.0/list/nearby-photos/` — 请求参数：`lat`、`lng`、`radius`（米），可选参数 `page`、`ipp`  

这些请求端点不需要 `access_token`。使用 `scripts/fetch_openstreetcam.py` 获取图片，并可选地将缩略图/完整图片下载到指定文件夹：  
```bash
uv run scripts/fetch_openstreetcam.py --lat 48.8566 --lng 2.3522 --radius 2000 --output ./assets/osc --max-photos 20
```  

**输出结果：**  
- 图片文件保存在 `images/` 目录下  
- 生成一个包含图片信息的 `osc_manifest.json` 文件（例如 `osc_manifest.json`，其中包含图片标题和位置信息）  

### 第 4 步：获取 Wikimedia Commons 图片和信息  

Wikimedia Commons 提供地标和文化图片。API：`https://commons.wikimedia.org/w/api.php`：  
- **搜索**：`action=query`、`list=search`、`srsearch=<城市或地标>`、`srnamespace=6`（文件命名空间）  
- **图片 URL 和元数据**：`action=query`、`prop=imageinfo`、`iiprop=url|extmetadata`、`titles=File:...`  

使用 `scripts/fetch_commons.py` 根据城市名称进行搜索，获取图片 URL 并可选地下载到文件夹：  
```bash
uv run scripts/fetch_commons.py --query "Paris landmarks" --output ./assets/commons --max-images 15
```  

**输出结果：**  
- 图片文件保存在 `images/` 目录下  
- 生成一个包含图片标题和描述的 `commons_manifest.json` 文件  

### 第 5 步：合并数据集以供 vlmrun 使用  

将 OpenStreetCam 和 Wikimedia Commons 的数据合并成一个文件或列表，然后传递给 vlmrun（例如，包含图片路径和每张图片的简短描述）。  
```bash
uv run scripts/run_travel_pipeline.py --city "Paris, France" --output-dir ./travel_output
```  

此脚本应完成以下操作：地理编码 → 获取 OpenStreetCam 图片 → 获取 Wikimedia Commons 图片 → 将结果写入 `images/` 目录和 `manifest.json`（或 `manifest.txt` 文件）。  

### 第 6 步：使用 vlmrun 生成视频和行程计划**

使用 **vlmrun-cli-skill** 工作流程：确保已安装 `vlmrun` 并设置了 `VLMRUN_API_KEY`：  
- **旅行视频**：传递收集到的图片并指定提示信息，以便生成简短的旅行视频（例如 30 秒）。建议使用 `-o` 选项保存视频文件。  
- **行程计划**：使用相同的图片和提示信息生成文字描述或要点式行程计划。  

**注意：** 如果设置了 `VLMRUN_API_KEY` 环境变量，可以省略 `--api-key` 选项：  
```bash
# Using environment variable (recommended)
vlmrun chat "Create a 30-second travel video showcasing these images of [CITY]. Add subtle captions with the location names. Keep a calm, inspiring travel-documentary style." -i ./travel_output/images/photo1.jpg -i ./travel_output/images/photo2.jpg -i ./travel_output/images/photo3.jpg ... -o ./travel_output/video

# Or using --api-key from .env, flag directly
vlmrun --api-key "your-api-key-here" chat "Create a 30-second travel video showcasing these images of [CITY]. Add subtle captions with the location names. Keep a calm, inspiring travel-documentary style." -i ./travel_output/images/photo1.jpg -i ./travel_output/images/photo2.jpg -i ./travel_output/images/photo3.jpg ... -o ./travel_output/video
```  

如果文件数量较多，可以指定部分图片（例如 10–15 张具有代表性的图片），或使用提示信息指定图片使用顺序。  

**示例：**  
```bash
# 1) Ask user for city, then run pipeline (e.g. "Paris, France")
uv run scripts/run_travel_pipeline.py --city "Paris, France" --output-dir ./travel_output

# 2) Generate travel video (use image paths from travel_output/images/ or image_paths.txt)
vlmrun chat "Create a 30-second travel video from these images of Paris. Add short location captions. Calm documentary style." -i ./travel_output/images/img_0000.jpg -i ./travel_output/images/img_0001.jpg -o ./travel_output/video

# 3) Generate 1-day travel plan (same images)
vlmrun chat "Using these photos of Paris, write a one-day travel plan (morning, midday, evening) with specific places and tips in markdown." -i ./travel_output/images/img_0000.jpg -i ./travel_output/images/img_0001.jpg -o ./travel_output
```  

**输出结果：**  
- `images/` — 下载的图片（共 5 张）  
- `manifest.json` — 旅行视频（如果设置了 VLMRUN_API_KEY）  
- `travel_plan.md` — 一日行程计划（如果设置了 VLMRUN_API_KEY）  

## 脚本参考  

| 脚本 | 用途 |  
|--------|--------|  
| `scripts/geocode_city.py` | 将城市名称转换为纬度/经度（使用 Nominatim） |  
| `scripts/fetch_openstreetcam.py` | 根据纬度/经度获取 OpenStreetCam 照片 |  
| `scripts/fetch_commons.py` | 根据查询条件从 Wikimedia Commons 下载图片 |  
| `scripts/run_travel_pipeline.py` | 运行地理编码、获取图片和信息并生成内容 |  

## API 参考  

- **OpenStreetCam**：[API 参考文档](https://api.openstreetcam.org/api/doc.html) — `nearby-tracks`、`list/nearby-photos`（仅限上传时需要认证）  
- **Wikimedia Commons**：[Commons API](https://commons.wikimedia.org/w/api.php) — `action=query`、`list=search`、`prop=imageinfo`  
- **vlmrun**：使用 `vlmrun-cli-skill` 进行配置和环境变量设置  

## 完整运行流程检查清单：  
- 用户提供了目的地城市名称（如需，还需提供国家/地区信息）。  
- 已完成城市名称的地理编码，并确认了对应的纬度/经度。  
- 已获取 OpenStreetCam 照片并保存了文件及对应的清单文件。  
- 已获取目的地的相关图片并保存了文件及清单文件。  
- 将所有数据合并到一个输出目录中。  
- 使用收集到的图片运行 vlmrun 生成旅行视频，并保存了视频文件（使用 `-o` 选项）。  
- 使用相同的图片或部分图片运行 vlmrun 生成行程计划，并将结果保存为 Markdown 格式的文件。  

## 故障排除  

### 安装问题  

**Python 未找到：**  
- **Windows**：确保在安装过程中将 Python 添加到 PATH 环境变量中，或使用 `py` 而不是 `python`  
- **macOS/Linux**：使用 `python3` 而不是 `python`  

**uv 命令未找到：**  
- 安装完成后重启终端  
- **Windows**：检查 `uv` 是否在 PATH 环境变量中（`$env:PATH`）  
- **macOS/Linux**：确保 `~/.cargo/bin` 或 `~/.local/bin` 在 PATH 环境变量中  

**虚拟环境激活失败：**  
- **Windows PowerShell**：如果出现执行策略错误，运行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`  
- **Windows CMD**：使用 `.venv\Scripts\activate.bat` 而不是 `.ps1`  
- **macOS/Linux**：确保使用 `source .venv/bin/activate`（而不是 `./.venv/bin/activate`）  

**vlmrun 未找到：**  
- 确保虚拟环境已激活  
- 重新安装：`uv pip install "vlmrun[cli]"`  
- 验证 `which vlmrun`（macOS/Linux）或 `where.exe vlmrun`（Windows）  

### 运行时问题  

- **地理编码失败**：尝试添加国家/地区信息，或使用“城市，国家”格式的查询。  
- **OpenStreetCam 返回结果较少或无结果**：增加搜索半径（默认为 2000 米，可尝试 5000 米或 10000 米）  
- 尝试使用城市中心坐标而非周边区域  
- 某些地区的覆盖范围有限，可尝试搜索附近的主要城市  
- **Wikimedia Commons 返回结果较少**：扩大搜索范围（例如“城市旅游”、“城市景点”）  
- **vlmrun 错误**：确认 `VLMRUN_API_KEY` 设置正确（macOS/Linux：`echo $VLMRUN_API_KEY`；Windows：`echo $env:VLMRUN_API_KEY`）  
- 检查网络连接  
- 如果 API 限制导致请求失败，减少请求的图片数量（例如从 20 张减少到 5–10 张）  
- 验证 API 密钥的有效性和剩余使用额度  

**脚本执行错误：**  
- 确保位于正确的目录（技能脚本根目录）  
- 确保虚拟环境已激活  
- 确保所有依赖项均已安装：`uv pip list`  

## 全过程示例：**  
```bash
# 1) Ask user for city, then run pipeline (e.g. "Paris, France")
uv run scripts/run_travel_pipeline.py --city "Paris, France" --output-dir ./travel_output

# 2) Generate travel video (use image paths from travel_output/images/ or image_paths.txt)
vlmrun chat "Create a 30-second travel video from these images of Paris. Add short location captions. Calm documentary style." -i ./travel_output/images/img_0000.jpg -i ./travel_output/images/img_0001.jpg -o ./travel_output/video

# 3) Generate 1-day travel plan (same images)
vlmrun chat "Using these photos of Paris, write a one-day travel plan (morning, midday, evening) with specific places and tips in markdown." -i ./travel_output/images/img_0000.jpg -i ./travel_output/images/img_0001.jpg -o ./travel_output
```  

## 快速参考：常用 URL  

- OpenStreetCam API 基础地址：`https://api.openstreetcam.org/`  
- Commons API：`https://commons.wikimedia.org/w/api.php`  
- Nominatim 地理编码服务：`https://nominatim.openstreetmap.org/search?q=<查询>&format=json`
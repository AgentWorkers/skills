---
name: bambu-studio-ai
description: "从聊天到成品打印——首个实现全流程自动化的人工智能3D打印技术。支持单色（STL格式）和多色（AMS格式，包含OBJ和MTL文件）打印，采用人工智能优化的颜色处理流程：包括阴影去除、CIELAB颜色空间下的最近邻颜色映射、纹理平滑处理等功能。系统具备自动定向、自动缩放功能，并能进行11项打印可行性分析以及网格修复。该技术兼容所有9款Bambu Lab品牌的3D打印机，同时支持4种人工智能3D建模工具。"
version: "0.20.1"
author: TieGaier
metadata:
  openclaw:
    emoji: "🖨️"
    requires:
      bins: ["python3", "pip3"]
    install:
      - id: pip-deps
        kind: pip
        packages: ["bambulabs-api", "bambu-lab-cloud-api", "requests", "trimesh"]
        required: true
        description: "Core Python dependencies for printer control, 3D generation, and model analysis"
      - id: ffmpeg
        kind: brew
        package: ffmpeg
        optional: true
        description: "Required for camera snapshots (local mode only)"
      - id: bambu-studio
        kind: cask
        package: bambu-studio
        optional: true
        label: "Bambu Studio (recommended for model preview and slicing — required before printing generated models)"
      - id: blender
        kind: cask
        package: blender
        optional: true
        label: "Blender 4.0+ (required for multi-color printing only)"
env:
  - name: BAMBU_MODE
    required: false
    description: "cloud (default) or local"
  - name: BAMBU_MODEL
    required: false
    description: "Printer model (e.g., H2D, A1 Mini, X1C)"
  - name: BAMBU_EMAIL
    required: false
    description: "Bambu account email (required for cloud mode)"
  - name: BAMBU_DEVICE_ID
    required: false
    description: "Device ID (cloud mode, optional — auto-detected if only one printer)"
  - name: BAMBU_IP
    required: false
    description: "Printer local IP (required for local mode)"
  - name: BAMBU_SERIAL
    required: false
    description: "Serial number (required for local mode)"
  - name: BAMBU_3D_PROVIDER
    required: false
    description: "3D gen provider: meshy, tripo, printpal, 3daistudio"
secrets:
  - name: BAMBU_PASSWORD
    required_when: "mode=cloud"
    storage: ".secrets.json"
    description: "Bambu account password (user-provided, never shipped with skill)"
  - name: BAMBU_ACCESS_CODE
    required_when: "mode=local"
    storage: ".secrets.json"
    description: "LAN access code from printer touchscreen (user-provided)"
  - name: BAMBU_3D_API_KEY
    required_when: "3D generation enabled"
    storage: ".secrets.json"
    description: "API key from chosen 3D generation provider (user-provided)"
security:
  no_credentials_shipped: true
  secrets_storage: ".secrets.json (chmod 600, git-ignored, user creates manually)"
  no_plaintext_in: ["config.json", "SKILL.md", "*.py"]
  config_gitignored: true
  files_gitignored: [".secrets.json", "config.json", ".token_cache.json", ".verify_code"]
  data_access:
    local_reads:
      - "config.json and .secrets.json in skill directory"
    network_calls:
      - "Bambu Lab Cloud API (cloud.bambulab.com) — printer control"
      - "Bambu Lab printer via MQTT (local IP) — local control"
      - "3D generation APIs (Meshy/Tripo/Printpal/3DAI) — model generation only"
    uploads:
      - "Text prompts to 3D generation API (user-initiated only)"
      - "Images to 3D generation API for image-to-3D (user-initiated only)"
    subprocesses:
      - "ffmpeg — camera snapshot extraction (optional, local only)"
    consent: "All network calls, uploads, and monitoring require explicit user consent before first use. Setup flow asks permission at each step."
keywords:
  - 3d printing
  - bambu lab
  - ams
  - mqtt
  - text to 3d
  - image to 3d
  - print monitoring
  - maker
---
# 🖨️ Bambu Studio AI

这是一个完整的人工智能3D打印技能，可以从聊天消息直接生成最终的打印模型。只需将您的Bambu Lab打印机连接到互联网，并选择一个3D生成API，我们的智能助手将处理所有步骤：从模型搜索到最终打印。

支持所有9款Bambu Lab打印机，支持云模式和局域网（LAN）连接模式。

## 安装

您可以从GitHub克隆代码仓库来安装Bambu Studio AI：

**GitHub链接：** https://github.com/heyixuan2/bambu-studio-ai

---

## 快速参考

| 功能 | 命令 |
|------|---------|
| 检查打印机状态 | `python3 scripts/bambu.py status` |
| 查看打印进度 | `python3 scripts/bambu.py progress` |
| 开始打印 | `python3 scripts/bambu.py print <file>` |
| 暂停/恢复/取消打印 | `python3 scripts/bambu.py pause|resume|cancel` |
| 设置打印速度 | `python3 scripts/bambu.py speed silent|standard|sport|ludicrous` |
| 打开/关闭打印机灯 | `python3 scripts/bambu.py light on|off` |
| 检查AMS耗材剩余量 | `python3 scripts/bambu.py ams` |
| 拍摄打印机摄像头截图 | `python3 scripts/bambu.py snapshot` |
| 发送G-code指令 | `python3 scripts/bambu.py gcode "G28"` |
| 从文本生成3D模型 | `python3 scripts/generate.py text "描述" --wait` |
| 从图片生成3D模型 | `python3 scripts/generate.py image photo.jpg --wait` |
| 查看模型生成状态 | `python3 scripts/generate.py status <task_id>` |
| 下载模型文件 | `python3 scripts/generate.py download <task_id> --format 3mf` |
| 打印前分析模型 | `python3 scripts/analyze.py model.3mf --material PLA --purpose functional` |

---

## 检测触发器

当用户发出以下指令时，将激活相应的功能：

| 触发器 | 动作 |
|---------|--------|
| “检查我的打印机状态” | `bambu.py status` |
| “正在打印什么？” | `bambu.py progress` |
| “打印这个模型” | `bambu.py print` |
| “将图片转换成3D模型” | `generate.py image` |
| “切片准备打印” | `slice.py` |
| “安装了哪个喷嘴？” | `bambu.py info` |
| “暂停/继续/取消打印” | `bambu.py pause|cancel|resume` |
| “加快打印速度” | `bambu.py speed` |
| “调整打印速度” | `bambu.py speed silent|standard|sport|ludicrous` |

---

## 首次使用设置

如果`config.json`文件不存在，系统会通过对话引导用户完成设置流程。

### 第1阶段：配置

按以下顺序提问：

**1. 打印机型号**
> “您使用的是哪种Bambu Lab打印机？”

展示可选的打印机型号：
- 🟢 **A系列**（入门级）：A1 Mini（180³mm，500mm/s），A1（256³mm，500mm/s）
- 🔵 **P系列**（中高端）：P1S（256³mm，500mm/s，封闭式），P2S（256³mm，600mm/s）
- 🟠 **X系列**（专业级）：X1C（256³mm，支持AI功能），X1E（工业级，带HEPA过滤器）
- 🔴 **H系列**（高端）：H2C（350°C，加热腔体），H2S（340³mm，1000mm/s），H2D（双喷头，支持激光切割）

**2. 连接方式**
> “您的打印机是如何连接的？”
> 
> **🔌 局域网（推荐）** — 如果您的电脑和打印机在同一个WiFi网络下。
> 支持摄像头、G-code指令、AMS耗材监控和实时监控功能。
> 需要提供：打印机IP地址、序列号和访问代码（在打印机设置→设备选项中获取）。
> 确保打印机的局域网模式已开启（设置→网络→局域网模式）。
>
> **☁️ 云连接** — 如果您需要远程访问。
> 功能有限：不支持摄像头、G-code指令和AI监控功能。
> 需要提供电子邮件地址和密码（首次登录时需要验证）。

**3. 3D模型生成（可选）**
> “是否需要使用AI生成3D模型？可以从文本或图片创建可打印模型？”
> 如果选择，需要选择3D模型生成服务提供商和API密钥：
  - **Meshy**：最成熟的服务，支持STL/3MF格式，每月20美元
  - **Tripo3D**：基于Python的SDK，每月10美元
  - **Printpal**：优化后的打印输出格式
  - **3D AI Studio**：处于早期测试阶段

**4. 通知方式**
> “希望如何接收通知？自动通知（根据您的通讯平台）、Discord、iMessage、Telegram、WhatsApp或Slack？”

**5. AI打印监控（可选）**
> “是否需要AI监控？我会拍摄打印过程中的照片并检查是否有故障？”
> 如果选择，需要设置监控频率（默认为每120秒），以及是否在出现异常时自动暂停打印。

**6. 保存配置**

生成`config.json`文件（包含非敏感信息，可共享）和`.secrets.json`文件（包含敏感信息，请使用以下密钥）：

然后运行以下命令来应用配置：

确保`.gitignore`文件包含`.secrets.json`和`config.json`文件。

---

## 配置验证

**配置保存后，可以运行以下测试命令：**
- `python3 scripts/bambu.py status` | 始终执行
- `python3 scripts/bambu.py snapshot` | 仅限本地模式
- `python3 scripts/bambu.py ams` | 仅限本地模式
- `python3 scripts/generate.py text "10mm cube" --raw` | （如果已配置3D模型生成功能）

---

## 模型来源

在生成模型之前，总是先询问用户：
> “您希望我：
> 1. 在网上搜索现有的3D模型吗？（通常质量更高，经过社区验证）
> 2. 使用AI生成一个自定义模型吗？
> 3. 还是不确定？那我先搜索一下，如果没有合适的模型再生成？”

根据用户的选择，执行相应的流程。

---

## 模型搜索优先级

| 来源 | 链接 | 适合的模型类型 |
|--------|-----|----------|
| **Printables.com** | 提供Bambu Lab社区的预切片模型 |
| **Thingiverse** | 最大的3D模型库，涵盖各种类型 |
| **MakerWorld** | Bambu Lab官方的模型库，可直接打印 |
| **Thangs.com** | 提供3D模型搜索服务 |
| **MyMiniFactory** | 筛选过的高质量模型 |
| **Cults3D** | 提供设计师设计的模型，部分模型需付费 |

## 搜索与生成的决策流程

| 模型类型 | 推荐的搜索方式 |
|----------|--------|
| 常见物品（如手机支架、挂钩、盒子） | **先搜索** — 99%的概率能找到合适的模型 |
| 特定产品配件（如iPhone 15保护壳） | **先搜索** — 通常能找到精确尺寸的模型 |
| 自定义/独特的物品 | **使用AI生成** |

---

## 生成前的准备工作

在生成3D模型之前，请务必完成以下步骤：

### 第1步：明确需求

询问用户关于模型的所有细节：

- **尺寸**：模型是否符合打印机的打印体积？
- **用途**：模型是用于装饰还是实用功能？
- **材料**：选择合适的材料（如PLA、TPU、ABS）？
- **手机/设备型号**：如果需要定制保护壳，需要提供准确的尺寸？
- **其他特殊要求**：如是否有电缆孔、安装点、可调节角度等？

### 第2步：研究未知模型（需用户同意）

如果用户提供了不明确的尺寸或设计要求：

> 用户： “我想打印一个iPhone 15 Pro Max的保护壳。”
> 助手： “我需要知道具体的尺寸。”
> 在研究后，确认尺寸是否合适。

### 第3步：生成模型

生成模型之前，会向用户确认模型细节：

> “生成的模型将是：
> - iPhone 15 Pro Max保护壳，尺寸为162 × 79 × 12mm，摄像头孔尺寸为42 × 38mm。
> - 使用TPU材料。
> - 预计打印时间为约2小时。”

然后根据用户提供的信息生成模型。

---

## 支持的打印机型号

| 打印机型号 | 打印体积 | 打印速度 | 最高喷嘴温度 | 打印床温度 | 是否封闭式 | 是否支持AMS耗材 |
|---------|-------------|-----------|-------------|------------|----------------|-------------------|
| A1 Mini | 180×180×180mm | 500mm/s | 300°C | 开放式 | 不支持AMS耗材 |
| A1 | 256×256×256mm | 500mm/s | 300°C | 开放式 | 不支持AMS耗材 |
| P1S/P2S/X1C/X1E/H2C | 256×256×256mm | 500mm/s | 500°C | 支持AMS耗材 |
| H2C | 256×256×256mm | 500mm/s | 300°C | 封闭式 | 支持AMS耗材 |
| H2S | 340×320×340mm | 600mm/s | 350°C | 封闭式 | 支持AMS耗材 |
| H2D | 340×320×340mm | 600mm/s | 350°C | 支持AMS耗材 |

---

## 连接方式建议

**建议始终使用局域网模式**，因为云模式的功能有限，且每次登录都需要验证电子邮件地址。

### 如何在打印机上启用局域网模式：

1. 在打印机触摸屏上进入**设置** → **网络** → **局域网模式**，将模式设置为**开启**。
2. 记下以下信息：
  - **IP地址**
  - **序列号**
  - **访问代码**

---

## 云连接（仅限远程访问）

如果无法与打印机在同一网络下使用，可以选择云连接模式：

**注意：
- 不支持摄像头截图功能
- 不支持G-code指令
- AMS耗材信息有限
- 首次登录和token过期后需要验证电子邮件地址

---

## 配置文件

**config.json**文件包含非敏感信息，可共享。

**.secrets.json**文件包含敏感信息，请设置权限为`600`。

这些脚本会自动从技能目录加载`config.json`和`.secrets.json`文件。

---

## 3D模型生成支持的服务提供商及格式

| 服务提供商 | 支持的输入格式 | 最佳输出格式 | 费用 |
|----------|-------------|----------------|-------------------|
| Meshy | 文本/图片 | STL/3MF | 免费 + 每月20美元 |
| Tripo3D | 文本/图片 | GLB/STL | 免费 + 每月10美元 |
| Printpal | 文本 | STL | 优化后的打印格式 |
| 3D AI Studio | 文本/图片 | STL/OBJ | 处于早期测试阶段 |

---

## 自动提示优化

当用户请求打印“手机支架”时，系统会自动生成适合FDM 3D打印的模型参数：

- 最大打印尺寸为230×230×230mm。
- 基座部分需要平整，无超过45°的悬垂部分。
- 模型壁厚至少为1.5mm。

---

## 打印格式优先级

模型生成后，会优先输出Bambu Lab支持的格式：

- `.3mf`：Bambu Lab的默认格式，保留了所有的打印设置。
- `.stl`：通用格式，所有切片软件都能识别。
- `.step/.stp`：具有精确的几何形状，适合CAD编辑。
- `.obj`：作为备用格式。

---

## 必须遵循的打印前流程

**切勿直接将模型发送给打印机。**必须按照以下步骤操作：

### 必须执行的步骤：

1. 检查模型尺寸和材料是否适合打印机。
2. 进行11项打印质量检查。
3. 根据模型类型和用途调整打印参数。

---

## 注意事项

- AI生成的模型可能包含一些质量问题（如非流形边缘、孔洞、交叉部分），用户需要在打印前进行手动检查。

---

## 参考文档

`references/`文件夹中包含以下文档：
- `bambu-mqtt-protocol.md`：MQTT协议和相关命令
- `bambu-cloud-api.md`：云API的Python SDK方法
- `3d-generation-apis.md`：不同3D模型生成服务的API文档
- `3d-prompt-guide.md：3D模型生成的提示编写指南
- `model-specs.md：所有9款打印机的详细规格

---

## 配置文件示例

`config/config.example.json`和`.secrets.example.json`文件提供了配置文件的模板。

---

## 其他信息

- Bambu Studio可以通过`brew list --cask bambu-studio`命令安装。

其他平台的下载链接：
- Windows：https://bambulab.com/en/download/studio
- Linux：https://github.com/bambulab/BambuStudio/releases

---

## 打印速度模式

---

## 已知的限制

- 单色打印是稳定的，但多色打印需要手动设置颜色。
- OrcaSlicer的CLI切片功能在v2.5.0版本中存在bug。
- 全自动打印功能目前还需要在Bambu Studio中进行预览。
# Tripo 3D生成

将文本或图像转换为可用于制作的3D模型，拥有**雕塑级别的几何精度**、清晰的边缘和PBR材质——整个过程仅需不到90秒。

**包含10次免费生成服务。无需API密钥、无需注册、无需信用卡。**

## 特点

- **文本转3D**：用自然语言描述任何物体 → 获得可用于制作的3D模型
- **图像转3D**：上传一张照片 → 人工智能会重建出具有精确几何形状的完整3D模型
- **雕塑级别的几何精度**：行业领先的网格质量，边缘清晰，拓扑结构整洁，表面细节精确
- **PBR材质**：开箱即用的基于物理的渲染纹理（反照率、法线、粗糙度、金属质感）
- **自动装配与动画**：自动绑定骨骼，并提供10多种预设动画——行走、跑步、跳跃、攀爬、挥砍、射击、静止、受伤、摔倒、转身
- **风格化**：可将模型转换为6种艺术风格——卡通、黏土、外星人、圣诞、复古蒸汽朋克等
- **智能低多边形**：人工智能生成的低多边形网格，具有手工制作的拓扑结构，非常适合移动游戏
- **四边形网格输出**：适合细分工作的干净四边形拓扑结构（Maya、Blender、ZBrush）
- **自动调整实际尺寸**：自动将模型调整为实际尺寸（以米为单位）
- **6种导出格式**：GLB、FBX、OBJ、STL、USDZ、3MF——适用于任何制作流程

## 模型版本

| 模型 | 速度 | 质量 | 适用场景 |
|-------|-------|---------|----------|
| `Turbo-v1.0-20250506` | 约5-10秒 | ★★★☆☆ | 最快的原型制作，概念探索 |
| `v3.0-20250812` **（默认）** | 约90秒 | ★★★★★ | 适用于制作资产，具有雕塑级别的精度和清晰的边缘 |
| `v2.5-20250123` | 约25-30秒 | ★★★★☆ | 速度快且平衡性好，适合快速迭代 |
| `v2.0-20240919` | 约20秒 | ★★★★☆ | 准确的几何形状和PBR材质 |
| `v1.4-20240625` | 约10秒 | ★★★☆☆ | 传统风格，具有真实的纹理 |

## 快速入门

### 文本转3D

```json
{ "action": "generate", "prompt": "a medieval castle with stone walls and towers" }
```

### 图像转3D

```json
{ "action": "generate", "image_url": "https://example.com/photo.jpg" }
```

### 检查进度

```json
{ "action": "status", "task_id": "your-task-id" }
```

### 下载模型

```json
{ "action": "download", "task_id": "your-task-id" }
```

### 查看使用情况

```json
{ "action": "credits" }
```

## 工作流程

1. 使用提示或图像调用`generate`函数 → 获取`task_id`
2. 每5-10秒查询一次`status` → 跟踪进度（0-100%）
3. 当状态为`SUCCESS`时 → 返回模型URL
4. 使用`download`函数获取`pbr_model_url`（推荐）、`model_url`和`rendered_image_url`

## 使用案例示例

### 1. 游戏资产——武器

```json
{
  "action": "generate",
  "prompt": "a legendary fantasy sword with dragon engravings, glowing blue runes on the blade, ornate golden crossguard, leather-wrapped grip. Game-ready, PBR materials.",
  "model_version": "v3.0-20250812"
}
```

### 2. 电子商务——产品可视化

```json
{
  "action": "generate",
  "prompt": "a premium wireless headphone, matte black with rose gold accents, leather ear cushions, sleek modern design for product showcase",
  "model_version": "v3.0-20250812"
}
```

### 3. 建筑——建筑模型

```json
{
  "action": "generate",
  "prompt": "a modern minimalist house, two stories, large glass windows, flat roof, concrete and wood exterior with surrounding landscape",
  "model_version": "v3.0-20250812"
}
```

### 4. 3D打印——小雕像

```json
{
  "action": "generate",
  "prompt": "a detailed tabletop miniature of a dwarf warrior holding a battle axe and round shield, high detail for resin 3D printing",
  "model_version": "v3.0-20250812",
  "format": "stl"
}
```

### 5. 快速原型制作——快速概念设计

```json
{
  "action": "generate",
  "prompt": "a cute robot mascot with round body, antenna, and big expressive eyes",
  "model_version": "Turbo-v1.0-20250506"
}
```

### 6. AR/VR——交互式对象

```json
{
  "action": "generate",
  "prompt": "a treasure chest that opens, filled with gold coins and gems. Realistic wood and metal materials for VR experience"
}
```

### 7. 动画角色

```json
{
  "action": "generate",
  "prompt": "a stylized knight character in full plate armor, T-pose, suitable for rigging and animation",
  "model_version": "v3.0-20250812"
}
```

生成完成后，使用Tripo的自动装配功能为模型添加骨骼，并自动应用行走/跑步/攻击动画。

## 输出格式

| 格式 | 扩展名 | 适用场景 |
|--------|-----------|----------|
| GLB | .glb | 通用格式——Web、Unity、Unreal、AR/VR、three.js |
| FBX | .fbx | 适用于动画、Maya、3ds Max、游戏引擎 |
| OBJ | .obj | 通用交换格式，适用于Blender导入 |
| STL | .stl | 适用于3D打印（FDM、SLA、树脂打印） |
| USDZ | .usdz | 适用于Apple AR Quick Look、Vision Pro |
| 3MF | .3mf | 高级3D打印格式，包含颜色/材质数据 |

## 高级参数

| 参数 | 值 | 说明 |
|-----------|--------|-------------|
| `model_version` | 见上表 | 控制质量与速度的平衡 |
| `format` | glb, fbx, obj, stl | 输出3D格式 |
| `prompt` | 任意文本（最多1024个字符） | 用于模型生成的描述 |
| `image_url` | 公开URL（JPEG/PNG） | 用于图像转3D转换的照片 |

## 动画预设（通过Tripo平台）

Tripo支持角色模型的**自动装配与动画**：

| 动画 | 说明 |
|-----------|-------------|
| `idle` | 静止站立循环 |
| `walk` | 行走循环 |
| `run` | 跑步循环 |
| `jump` | 跳跃动画 |
| `climb` | 攀爬动作 |
| `slash` | 近战攻击动作 |
| `shoot` | 远程攻击动作 |
| `hurt` | 受击反应动画 |
| `fall` | 倒下动画 |
| `turn` | 在原地转身 |

## 风格化选项（通过Tripo平台）

可将任何生成的模型转换为以下艺术风格：

| 风格 | 说明 |
|-------|-------------|
| Cartoon | 明亮的色彩，夸张的比例 |
| Clay | 手工制作的黏土/面团外观 |
| Alien | 有机的、异世界美学风格 |
| Christmas | 节日主题，带有节日氛围的材质 |
| Retro Steampunk | 维多利亚时代的机械风格 |
| LEGO | 乐高积木风格 |
| Voronoi | 有机的细胞状图案 |

## 为获得最佳效果提供提示

### 明确描述形状和材质
- **好的示例**：“一把带有弯曲扶手和编织座面的旧木制摇椅”
- **不好的示例**：“一把椅子”

### 指定风格和使用场景
- **写实风格**：“一个具有黄铜扣件的写实皮革公文包”
- **风格化风格**：“一个具有平面阴影效果的低多边形卡通狐狸”
- **游戏适用风格**：“一个适用于游戏的科幻风格箱子道具，拓扑结构经过优化”

### 包含材质细节
- “哑光黑色表面处理”、“拉丝铝材质”、“粗糙的石头纹理”
- “半透明玻璃”、“抛光的大理石”、“磨损的皮革”

### 对于角色模型
- 提及姿势：为动画模型指定“T型姿势”或“A型姿势”
- 指定风格：“风格化”、“写实”、“Q版”

## 信用系统

| 等级 | 信用点数 | 设置方式 |
|------|---------|-------|
| **免费试用** | 10次生成服务 | 无需任何设置 |
| **拥有API密钥** | 无限次生成服务（新账户可免费获得2,000点信用点） | 在[platform.tripo3d.ai](https://platform.tripo3d.ai/)注册 |

当免费信用点用完后，该工具会提供逐步指导，帮助您创建一个免费的Tripo账户并获取自己的API密钥。

### 获取自己的API密钥

1. 访问[platform.tripo3d.ai](https://platform.tripo3d.ai/) → 注册（免费）
2. 转到[API密钥页面](https://platform.tripo3d.ai/api-keys)
3. 生成新的API密钥（以`tsk_`开头）——**立即复制，仅显示一次！**
4. 配置：`openclaw config set skill.tripo-3d-generation.TRIPO_API_KEY <your-key>`
5. 完成设置后，您就可以使用自己的账户进行无限次生成了

## 为什么选择Tripo？

| 特点 | Tripo | 其他工具 |
|---------|-------|--------|
| 几何精度 | 雕塑级别的精度，边缘清晰 | 其他工具的模型通常细节较少 |
| 自动装配 | 内置骨骼和10种预设动画 | 其他工具通常需要手动装配 |
| 速度 | 最快5秒（Turbo模式），最慢90秒（v3.0版本） | 其他工具通常需要3-10分钟以上 |
| 输出格式 | 6种格式 | 其他工具通常只有1-2种格式 |
| PBR材质 | 包含反照率、法线、粗糙度和金属质感 | 其他工具通常只提供基础材质 |
| 免费信用点 | 提供10次免费生成服务，无需注册 | 大多数工具需要预先支付API密钥 |

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|---------|
| `quota_exceeded` | 免费信用点用完 | 按照设置指南获取自己的API密钥 |
| `task_not_ready` | 模型仍在生成中 | 等待片刻并再次查询进度 |
| `task_FAILED` | 生成失败 | 尝试使用不同的描述或更具体的提示 |
| `missing_user_id` | 客户端错误 | 系统自动处理，无需用户操作 |

## 关于Tripo

[Tripo](https://www.tripo3d.ai/) 是VAST AI Research开发的先进AI 3D生成平台。被游戏、建筑、电子商务、3D打印、电影/视觉特效和教育领域的专业人士广泛使用。该平台支持完整的3D创作流程：生成 → 装配 → 动画 → 风格化 → 导出。

- 官网：[tripo3d.ai](https://www.tripo3d.ai/)
- API平台：[platform.tripo3d.ai](https://platform.tripo3d.ai/)
- API文档：[platform.tripo3d.ai/docs/generation](https://platform.tripo3d.ai/docs/generation)
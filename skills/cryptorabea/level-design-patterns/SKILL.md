---
name: unity-level-design
description: 适用于创建 Unity 游戏场景和原型、构建关卡设计，或自动化 Unity 编辑器的各项工作流程（如地形处理、光照设置、环境配置以及玩家控制器的相关操作）。也非常适合用于后末日场景、奇幻森林、地下城探索类游戏等需要快速原型设计的场景。
---
# Unity 地图设计

## 概述

通过使用编辑器的自动化功能、现代的 Unity API 以及地图设计的最佳实践，可以快速原型化 Unity 游戏场景。该技能能够自动化地生成地形、设置光照、放置环境元素以及创建玩家控制器，从而帮助您快速实现游戏玩法构思。

## 适用场景

在以下情况下可以使用该技能：
- 创建游戏场景原型（如末日题材、奇幻风格、科幻题材、地牢探索类游戏等）
- 设置 Unity 地形、网格和地面几何形状
- 自动化处理光照、后期处理和环境布局
- 构建玩家控制器和基本的游戏系统
- 需要快速将概念转化为可玩的游戏场景

## 核心工作流程

### 第一步：研究当前可用的 API

在开始实现之前，请查阅 Unity 的最新 API 和最佳实践：

**现代 Unity 系统：**
- **Terrain Tools** 包（支持 GPU 加速的地形建模）
- **Universal Render Pipeline (URP)** 或 **High Definition Render Pipeline (HDRP)**
- **DOTS/ECS**（适用于对性能要求较高的场景）
- **Shader Graph**（用于自定义材质）
- **VFX Graph**（用于粒子效果）

**需要参考的关键 API：**
- `UnityEngine.Terrain` - 用于地形操作
- `UnityEditor.TerrainTools` - 用于编辑器中的地形工具
- `UnityEngine Rendering.Universal` - URP 相关组件
- `UnityEditor.SceneManagement` - 用于场景自动化

### 第二步：场景设置自动化

使用编辑器脚本来自动化重复性的设置工作：

```csharp
// Example: Automated scene initialization
public static class SceneSetupHelper
{
    [MenuItem("Level Design/Create Basic Scene")]
    public static void CreateBasicScene()
    {
        // Setup lighting
        SetupLighting();
        
        // Create terrain
        CreateTerrain();
        
        // Setup post-processing
        SetupPostProcessing();
        
        // Create player
        CreatePlayerController();
    }
}
```

### 第三步：地形生成

**生成方法：**
1. **Unity Terrain**：适用于自然景观的生成
2. **Mesh Generation**：适用于风格化或建筑风格的场景
3. **Procedural Generation**：适用于无限重复或可重玩的游戏世界

### 第四步：环境与道具的放置

自动化放置以下元素：
- 植被（树木、草地、岩石）
- 建筑物（房屋、废墟、地牢）
- 光照（太阳光、环境光、点光源）
- 效果（雾效、粒子效果、后期处理效果）

### 第五步：玩家与游戏玩法

创建以下基础组件：
- 玩家控制器（第一人称视角、第三人称视角、俯视视角）
- 相机设置
- 输入处理
- 基本交互功能

## 场景类型

### 末日题材场景
- 被破坏的城市环境
- 废墟和碎片
- 茂密的植被
- 朦胧的大气效果和光照
- 分散的资源/道具

### 奇幻森林场景
- 繁茂的林地
- 河流和湖泊
- 奇幻风格的植被
- 魔法光照效果
- 清晰的小径和空地

### 地牢探索类场景
- 通过程序生成的房间
- 走廊系统
- 火把/蜡烛等光源
- 陷阱和敌人生成机制
- 财宝箱

## 快速参考

| 任务 | 方法 | 使用的 API/工具 |
|------|--------|----------|
| 创建地形 | 编辑器脚本 | `Terrain.CreateTerrainGameObject` |
| 塑造地形 | 噪音/高度图 | `TerrainData.SetHeights` |
| 添加植被 | 绘制树木/草地 | `TerrainData.treeInstances` |
| 设置光照 | URP/HDRP | `UniversalAdditionalLightData` |
| 后期处理 | 体积效果组件 | `Volume` + 配置文件 |
| 玩家控制器 | 角色控制器 | `CharacterController` 组件 |
| 程序生成网格 | 运行时生成 | `Mesh` 类 |

## 编辑器工具

请查看 `scripts/` 目录中的自动化工具：
- `SceneSetupWizard.cs`：一键初始化场景
- `TerrainGenerator.cs`：用于程序化生成地形
- `EnvironmentPainter.cs`：批量放置环境元素
- `LightingSetup.cs`：自动配置光照

## 参考资料

详细文档请参阅 `references/` 目录：
- `unity-apis.md`：当前 Unity API 参考手册
- `terrain-tools.md`：地形系统文档
- `urp-setup.md`：Universal Render Pipeline 使用指南
- `level-design-patterns.md`：地图设计的最佳实践和模式

## 常见错误

- **错误的渲染管线**：请确认项目使用的是 URP、HDRP 还是内置的渲染管线
- **地形比例**：Unity 地形使用不同的高度/长度比例
- **光照烘焙**：实时全局光照计算可能较慢；对于静态几何体应使用烘焙光照
- **性能问题**：过多的树木或碰撞体会影响游戏性能
- **比例一致性**：确保玩家、环境和道具的比例保持一致

## 示例用法

```csharp
// Create a post-apocalyptic scene
[MenuItem("Level Design/Post-Apocalyptic Scene")]
static void CreatePostApocalypticScene()
{
    // 1. Create terrain with noise
    var terrain = TerrainGenerator.CreateRuinedTerrain();
    
    // 2. Setup dramatic lighting
    LightingSetup.CreateDramaticLighting(Color.gray * 0.3f);
    
    // 3. Add fog and post-processing
    PostProcessingSetup.CreateAtmosphericFog();
    
    // 4. Scatter debris and props
    EnvironmentPainter.ScatterDebris(50);
    
    // 5. Create player
    var player = PlayerSetup.CreateFPSPlayer();
    player.transform.position = new Vector3(0, 5, 0);
}
```
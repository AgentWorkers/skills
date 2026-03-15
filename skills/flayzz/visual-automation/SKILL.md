---
name: visual_automation
description: 通过 Python 脚本自动化 Blender 的操作，以生成 3D 资源、进行渲染并制作动画。
metadata: { "openclaw": { "requires": { "bins": ["blender", "pwsh"] } } }
---
# 使用说明

您是一位3D自动化专家，可以利用这项技能为用户的项目生成视觉素材。

## 操作模式

1. **脚本生成**：编写一个Python脚本（`.py`），通过`import bpy`来创建几何体、材质和光照效果。
2. **后台渲染**：始终在后台模式下进行渲染，以避免打开图形用户界面（GUI）。
   使用命令行参数运行脚本：`& "C:\Program Files\Blender Foundation\Blender 5.0\blender-launcher.exe" --background --python your_script.py`
3. **Web导出**：对于Web项目，优先选择导出为**GLB/GLTF**格式。

## 示例：创建机械锁具
在收到用户关于具体外观要求的指示后，您可以：
- 通过编程方式创建齿轮、圆柱体和钥匙等组件。
- 使用Cycles或Eevee算法进行高质量渲染。
- 渲染多帧图像以制作背景视频循环。

## 安全性与文件路径
- **程序路径**：`C:\Program Files\Blender Foundation\Blender 5.0\blender-launcher.exe`
- 将生成的素材直接保存到项目文件夹中（例如：`workspace-dev/website/assets/`）。

## 提示：提升视觉效果的建议
- 使用程序生成的纹理（procedural textures）来模拟真实的金属质感。
- 采用HDRI（高动态范围图像）光照技术以实现高质量的反射效果。
- 调整摄像机角度，以获得“英雄视角”（Hero Shot）的拍摄效果。
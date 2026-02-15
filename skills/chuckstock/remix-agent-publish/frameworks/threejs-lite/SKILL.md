---
name: threejs-lite
description: 使用 Three.js 构建轻量级的、适合移动设备的 3D 浏览器游戏，这些游戏针对 Remix/Farcade 的限制进行了优化，并且支持单文件发布（即所有资源都包含在一个文件中）。
metadata:
  tags: threejs, webgl, game-dev, 3d, remix
---

# Three.js Lite

当用户需要一款渲染复杂度较低、在移动设备上性能稳定的3D浏览器游戏时，可以使用此技术。

## 工作流程

1. 从 `assets/starter-single-file.html` 文件开始。
2. 实现一个摄像机、一个场景以及一个游戏循环。
3. 在进行视觉优化之前，先添加玩家输入机制和游戏结束条件。
4. 保持几何体及材质的数量较少且易于预测。
5. 如果目标平台是 Remix/Farcade，需参考 `references/remix-farcade-integration.md` 中的集成指南。
6. 在提交代码之前，确保所有必要的钩子函数（`gameOver`、`onPlayAgain`、`onToggleMute`）都已正确实现。

## 技术规范

- 尽量减少绘制调用次数，并默认避免使用后期处理效果。
- 建议使用简单的 `MeshBasicMaterial` 或 `MeshStandardMaterial` 材质设置。
- 在初次开发阶段避免使用动态阴影效果。
- 对于 Remix 平台的上传，除非用户另有要求，否则应生成包含内联 JavaScript 和 CSS 的单文件 HTML。
- 对于 Remix 平台的上传，需要在 HTML 的 `<head>` 部分添加以下代码：
  ```html
  <script src="https://cdn.jsdelivr.net/npm/@farcade/game-sdk@0.3.0/dist/index.min.js"></script>
  ```
- 将 3D 效果视为可选功能；游戏的可玩性应优先于视觉复杂性。

## 参考资料

- `references/threejs-mobile-patterns.md`：提供了场景设置、控制方式以及性能优化方面的指导。
- `references/remix-farcade-integration.md`：包含了 Remix 平台所需的 SDK 钩子函数实现方法。
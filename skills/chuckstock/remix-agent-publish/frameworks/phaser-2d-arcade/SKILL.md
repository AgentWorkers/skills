---
name: phaser-2d-arcade
description: 使用 Phaser 3 和 Arcade Physics 构建以移动设备为先导的 2D 浏览器游戏，这些游戏经过优化，以适应 Remix/Farcade 平台的限制，并支持单文件部署（即所有游戏资源都包含在一个文件中）。
metadata:
  tags: phaser, game-dev, html5, arcade-physics, remix
---

# Phaser 2D Arcade

当用户请求开发一款基于Phaser的浏览器游戏，尤其是需要快速、单文件实现的2D游戏循环时，请使用此技能。

## 开发流程

1. 从 `assets/starter-single-file.html` 文件开始开发。
2. 首先实现核心游戏循环：`boot -> preload -> create -> update`。
3. 在完善游戏逻辑之前，先添加胜利/失败的条件以及计分系统。
4. 尽早添加触控控制功能以及响应式布局（以移动设备优先）。
5. 如果目标平台是Remix或Farcade，需要参考 `references/remix-farcade-integration.md` 中提供的SDK集成指南。
6. 在提交代码之前，确保所有必要的SDK钩子（`gameOver`、`onPlayAgain`、`onToggleMute`）都已正确实现。

## 开发规范

- 为简化代码和提升性能，建议优先使用Phaser Arcade的物理引擎。
- 保持初始开发规模较小：仅包含1个场景、1个游戏机制以及1个失败条件。
- 避免进行耗时的每帧资源分配和不必要的视觉效果。
- 确保游戏可以安全地重新启动，并且游戏逻辑具有确定性（即每次重新启动时结果一致）。
- 对于上传至Remix平台的游戏，除非用户另有要求，否则应使用包含内联JS/CSS的单文件HTML格式。
- 对于上传至Remix平台的游戏，需要在HTML的`<head>`部分添加以下代码：
  ```html
  <script src="https://cdn.jsdelivr.net/npm/@farcade/game-sdk@0.3.0/dist/index.min.js"></script>
  ```

## 参考资料

- `references/phaser-arcade-patterns.md`：关于游戏场景架构、控制方式以及性能优化建议的文档。
- `references/remix-farcade-integration.md`：关于Farcade SDK集成方法的详细指南。
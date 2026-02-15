---
name: Three.js
description: 利用适当的资源管理和性能优化模式来构建3D网页体验。
metadata: {"clawdbot":{"emoji":"🎮","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

# Three.js 开发最佳实践

## 资源清理
- 在删除对象之前，务必调用几何体（geometry）、材质（material）和纹理（texture）的 `.dispose()` 方法——Three.js 不会自动回收 GPU 资源。
- 删除网格（mesh）时，需要执行以下操作：`mesh.geometry.dispose(); mesh.material.dispose(); scene.remove(mesh)`；缺少任何一步都可能导致内存泄漏。
- 通过 `TextureLoader` 加载的纹理会一直保留在 GPU 内存中，除非明确释放它们——在场景切换时需要对这些纹理进行清理。

## 渲染循环
- 始终使用 `renderer.setAnimationLoop(animate)` 而不是手动调用 `requestAnimationFrame`——这样可以处理 VR 场景，当标签页被隐藏时也能正确暂停动画，并确保动画的同步性。
- 对于动画，使用 `clock.getDelta()` 来计算与帧无关的移动距离——直接计算帧数在不同刷新率下可能会导致问题。

## 响应式 Canvas
- 窗口大小改变时，需要同时更新相机（camera）的宽高比（aspect）和渲染器（renderer）的大小：`camera.aspect = width / height; camera.updateProjectionMatrix(); renderer.setSize(width, height)`。
- 如果在宽高比改变后忘记调用 `updateProjectionMatrix()`，会导致渲染效果失真。
- 使用 `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))`——设置过高的像素比会严重影响性能，但视觉效果提升有限。

## 导入和配置
- 使用 `import { OrbitControls } from 'three/addons/controls/OrbitControls.js'` 来引入 OrbitControls 插件——路径可能因打包工具而异，请根据实际情况进行调整。
- 使用 OrbitControls 时，务必将 `controls.enableDamping` 设置为 `true`，并在渲染循环中调用 `controls.update()`——否则阻尼效果将无法正常工作。

## 照明
- `MeshBasicMaterial` 会忽略所有光源的照明效果——对于需要光照效果的场景，请使用 `MeshStandardMaterial` 或 `MeshPhongMaterial`。
- 添加环境光（`new THREE.AmbientLight(0xffffff, 0.5)` 作为基础照明——仅使用方向光（directional lights）的场景会导致阴影完全消失。
- 使用 `PMREMGenerator` 生成的 HDR 环境贴图可以提供比点光源更好的反射效果，尤其是在金属材质上。

## 资源加载
- `GLTFLoader` 是加载 3D 模型的标准工具——对于大型网格，建议使用 Draco 压缩格式（可通过 `DRACOLoader` 实现）。
- 纹理加载是异步的——在纹理加载完成之前，模型可能会显示为黑色；可以使用 `LoadingManager` 来处理加载过程中的界面显示问题。
- CORS（跨源资源共享）策略可能会阻止来自其他域的纹理加载——请确保资源托管在同一域名下，或配置正确的 CORS 头信息。

## 相机相关问题
- 默认的近景/远景平面范围（0.1 到 1000）可能会导致大型场景中的“z-fighting”现象（物体在屏幕上重叠）——请根据实际场景调整这个范围。
- 如果相机位于某个物体内部，可能无法正常渲染——加载外部模型后请检查相机的位置（它们可能发生了意外的变换）。
- `PerspectiveCamera` 的视场角（FOV）是垂直方向的，而非水平方向的——75 度是一个常见的默认值。

## 性能优化
- 使用 `BufferGeometryUtils.mergeBufferGeometries()` 合并静态几何体——每个单独的几何体都会触发一次绘制操作，减少几何体数量可以提高渲染效率。
- 对于大量相同的对象，使用 `InstancedMesh` 可以将多个对象的绘制操作合并为一次。
- 将 `object.frustumCulled` 设置为 `true`（默认值），但请检查大型对象是否在场景边缘正确显示——边界球（bounding sphere）的设置可能不正确。
- 可以使用 `renderer.info` 来调试渲染过程中的绘制调用、三角形数量以及内存中的纹理信息。

## 动画处理
- `AnimationMixer` 需要在每一帧中调用 `mixer.update(delta)` 并传入实际的帧差值（delta time）——如果传入 0 或跳过某些帧，动画将会出错。
- 对于带有骨骼的模型（如角色），在开发过程中需要使用 `SkeletonHelper` 来调试骨骼相关的问题。
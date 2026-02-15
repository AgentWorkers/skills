---
name: game-dev-rust-godot
description: 使用 Rust+WASM 或 Godot 4.x 开发 HTML5 游戏的工作流程。适用于新游戏的创建、游戏机制的实现以及现有游戏的移植。遵循基于 TDD（测试驱动开发）的生产流程 v3.1，采用“资产优先”（asset-first）的开发策略。内容包括 Rust（Macroquad/Bevy）的开发、Godot 的 HTML5 导出功能、资源的获取、测试用例的编写以及质量保证（QA）自动化流程。最后更新日期：2026-02-06；仅允许使用 Rust+WASM 或 Godot，禁止使用 JS/TS 框架。
---

# 游戏开发：Rust + WASM / Godot 4.x

这是一个专门用于开发 HTML5 游戏的工作流程。**根据项目负责人的指示（2026-02-06）**：必须仅使用 Rust + WASM 或 Godot。

## 🚀 技术栈（必须遵守）

### ✅ 允许使用的技术
- **Rust + WASM**：推荐使用 Macroquad，也可以使用 Bevy
- **Godot 4.x**：支持 HTML5 导出功能

### ❌ 禁止使用的技术
- JavaScript/TypeScript（包括 Phaser、PixiJS、Three.js 等所有 JavaScript 框架）
- Unity WebGL
- 其他网页游戏引擎

## 📋 工作流程概述

```
1. 에셋 확보 (코딩 전 필수!)
   ↓
2. 에셋 기반 기획 구체화
   ↓
3. 메카닉 검증 (프로토타입)
   ↓
4. 테스트케이스 작성 (TDD)
   ↓
5. 구현 ↔ 기획 보완 (TC 100% PASS까지)
   ↓
6. QA (Playwright + 수동)
   ↓
7. 런칭 테스트
   ↓
8. 보고 (스크린샷 4장 + DoD 체크리스트)
```

## 🎨 资产获取（第 1 阶段 - 必须完成！）

**⛔ 严禁在未获取资产的情况下开始编码**

### 资产来源的优先级：
1. NAS 上的游戏资源库（`/Volumes/workspace/Asset Store-5.x/`，包含 265 个包）
2. 使用 MiniPC 和 Gemini AI 生成资源（`browser.proxy`，节点设置为 MiniPC）
3. 免费资源（来自 kenney.nl（CC0 许可）、opengameart.org、freesound.org）
4. 使用 MacBook MLX 进行 Z-Image-Turbo 图像处理（`nodes.run`，节点设置为 MacBook Pro）
5. 使用 Blender 将 3D 效果转换为 2D 格式（在 MiniPC 上完成）

### 必须获取的资产清单
```
□ 캐릭터/오브젝트 스프라이트
□ 배경 이미지/타일맵
□ UI 요소 (버튼, 아이콘, 패널)
□ BGM 최소 1곡 (mp3/ogg, 루프)
□ SFX 최소 3개 (클릭, 성공, 실패)
□ 에셋 라이선스 확인 (CC0/MIT/상용 허용)
```

**关于许可证的政策（针对公开发布的游戏）**：
- ✅ 可以使用来自 kenney.nl 的资源（CC0 许可），以及使用 AI 生成的资源
- ❌ 禁止使用 Unity Asset Store 中的资源（即使资源是免费的），也不允许重新分发

## 🦀 Rust + WASM 的实现

### Macroquad（推荐使用）

**创建项目**（在 MiniPC 上完成）：
```bash
cd $HOME/spritz/dynamic/games/<game-name>
cargo init
```

**Cargo.toml 文件配置**：
```toml
[package]
name = "game-name"
version = "0.1.0"
edition = "2021"

[dependencies]
macroquad = "0.4"

[profile.release]
opt-level = "z"
lto = true
```

**项目的基本结构**（`src/main.rs` 文件）：
```rust
use macroquad::prelude::*;

#[macroquad::main("Game Title")]
async fn main() {
    loop {
        clear_background(BLACK);
        
        // 게임 로직
        
        next_frame().await
    }
}
```

**构建与部署**：
```bash
# MiniPC에서
cargo build --release --target wasm32-unknown-unknown

# WASM 파일 복사
cp target/wasm32-unknown-unknown/release/<game-name>.wasm .

# index.html 생성 (Macroquad 자동 제공)
```

**详细指南**：请参考 `references/rust-macroquad.md`

### Bevy（高级选项）

仅在需要复杂的 ECS（Entity-System-Component）架构时使用。构建时间较长（超过 7 分钟），且生成的 WASM 文件体积较大（超过 3.6MB）。

**详细指南**：请参考 `references/rust-bevy.md`

## 🎮 Godot 4.x 的实现

### 创建项目（在 MiniPC 上完成）

```bash
cd $HOME/godot4/projects
mkdir <game-name>
cd <game-name>

# project.godot 생성
godot4 --headless --path . --quit
```

### HTML5 导出设置

1. **添加导出预设**：
   - 选择 “Project” → “Export” → “Add...” → “Web”
   - 设置导出路径为 `build/web/index.html`

2. **优化设置**：
   - 选择 “Texture Format” 为 “VRAM Compressed”
   - 如有需要，可以自定义 HTML 模板

### 构建与部署

```bash
# MiniPC에서
godot4 --headless --path . --export-release "Web"

# 결과물: build/web/ (index.html, *.wasm, *.pck)
```

**详细指南**：请参考 `references/godot-html5.md`

## ✅ 编写测试用例（第 4 阶段 - TDD）

**在实现代码之前，先编写测试用例（Test Cases）**

### 测试用例的分类

#### 功能测试用例
```
TC-F001: 게임 시작 시 타이틀 화면 표시
TC-F002: 시작 버튼 클릭 시 게임 플레이 진입
TC-F003: [핵심 메카닉] 입력에 대한 올바른 반응
TC-F004: 점수/진행도 업데이트
TC-F005: 게임 오버 조건 충족 시 결과 화면 표시
```

#### 用户界面/用户体验测试用例
```
TC-U001: 모바일 뷰포트 (390x844) 정상 표시
TC-U002: 가로 스크롤 없음
TC-U003: 터치 영역 최소 44x44px
TC-U004: safe-area 적용
```

#### 性能测试用例
```
TC-P001: 페이지 로드 5초 이내
TC-P002: JS 콘솔 에러 0개
TC-P003: 60fps 유지 (게임플레이 중)
```

**测试用例的存放位置**：`specs/games/<game>/test-cases.md`

## 🔄 实现与规划的迭代循环（第 5 阶段）

**重复执行测试用例，直到所有用例都通过（100% PASS）**：

```
구현 (TC 기반)
  ↓
TC 실행
  ↓
FAIL → 코드 수정 or 기획 조정
  ↓
재구현
  ↓
TC 재실행
  ↓
ALL PASS → Phase 6으로
```

**项目终止的条件**：
```
□ 모든 기능 TC PASS
□ 모든 UI/UX TC PASS
□ 모든 성능 TC PASS
□ DoD 체크리스트 전항목 충족
```

## 🧪 质量保证（QA，第 6 阶段）

### 自动化测试（使用 Playwright）

```bash
# MiniPC에서
cd $HOME/qa-automation
playwright test games/<game-name>.spec.ts
```

**必须验证的内容**：
```
□ 페이지 로드 성공 (5초 내)
□ JS 콘솔 에러 0개
□ 시작 버튼 클릭 가능
□ 게임 플레이 가능 (5초 이상 생존)
□ 모바일 뷰포트 (390x844) 정상 표시
```

### 手动检查清单
```
□ 전체 게임 루프 1회 완주
□ 에지 케이스 테스트
□ 사운드 재생 확인 (BGM + SFX)
□ 반응형 확인 (데스크톱 + 모바일)
```

### 拍摄至少 4 张截图
```
□ 타이틀 화면
□ 게임플레이 (진행 중)
□ UI 요소 (메뉴, 설정 등)
□ 결과 화면 (게임오버/클리어)
```

## 📦 部署

### Rust + WASM 的部署方式
```bash
# eastsea.monster/games/<game>/ 에 배포
- index.html
- <game>.wasm
- mq_js_bundle.js (Macroquad)
- assets/ (에셋 폴더)
```

### Godot 的部署方式
```bash
# build/web/ 내용을 eastsea.monster/games/<game>/ 에 배포
- index.html
- <game>.wasm
- <game>.pck
- assets/ (에셋 폴더, 필요 시)
```

## ✅ 完成标准的定义

**只有满足所有要求后，才能视为项目完成**：
```
□ 실제 이미지 에셋 적용 (CSS 도형/emoji 금지)
□ 실제 오디오 에셋 적용 (oscillator 금지)
□ TC 100% PASS
□ Playwright 자동 테스트 통과
□ 스크린샷 4장 이상
□ 모바일 반응형 확인
□ 치명적 버그 0개
□ og.png 생성 (1200x630)
□ 런칭 테스트 통과 (실제 URL)
```

## 🎯 游戏评级标准

| 评级 | 标准 | 处理方式 |
|------|------|------|
| **A** | 满足所有 DoD（Design Do’s）要求，所有测试用例都通过 | 继续维护并进行市场推广 |
| **B** | 游戏可以运行，但缺少部分资源或部分测试用例未通过 | 更换资源并完善测试用例 |
| **C** | 仅有代码，没有资源，且没有编写测试用例 | 从头开始重新进行项目开发 |
| **F** | 不存在 `index.html` 文件，目录为空，或者游戏出现崩溃 | 删除项目或重新制作 |

## 📚 详细参考资料

- **Rust Macroquad**：`references/rust-macroquad.md`
- **Rust Bevy**：`references/rust-bevy.md`
- **Godot HTML5**：`references/godot-html5.md`
- **资源许可证**：`references/asset-licensing.md`
- **性能优化**：`references/optimization.md`

## ⚠️ 重要限制

1. **技术栈限制**：只能使用 Rust + WASM 或 Godot
2. **资源获取要求**：在开始编码之前必须获取所有所需的资源
3. **TDD 强制要求**：必须先编写测试用例，然后再进行代码实现
4. **优先考虑移动端适配**：游戏需要同时支持移动设备的响应式显示
5. **许可证要求**：只能使用可以重新分发的资源

## 🚀 快速入门示例

### 蛇形游戏（使用 Rust + Macroquad）

1. **获取资源**：从 NAS 上获取蛇和食物的精灵图像，从 kenney.nl 获取背景音乐和音效
2. **编写测试用例**：编写 6 个功能测试用例、5 个用户界面测试用例和 4 个性能测试用例
3. **实现游戏逻辑**：使用 Macroquad 实现蛇的移动、碰撞和得分功能
4. **质量保证**：使用 Playwright 进行自动化测试，并进行移动设备的手动测试
5. **部署**：将游戏文件上传到 `eastsea.monster/games/snake/`

**预计开发时间**：获取资源 1 小时 + 实现代码 2 小时 + 质量保证 30 分钟 = 约 3.5 小时
---
name: blender-pipeline
description: |
  Blender 헤드리스 게임 에셋 파이프라인. 3D 모델 제작/가공/변환/렌더링을 Blender Python API(bpy)로 자동화.
  트리거: 3D 모델링, 에셋 변환, 스프라이트 시트, 리깅, Mixamo, FBX/glTF 변환, 프로시저럴 에셋 생성 관련 요청.
---

# Blender 无头游戏资产处理流程

本技能利用 Blender 的 Python API (bpy) 自动化游戏开发所需的 3D 资产的创建与处理流程。

## 安装

### Linux (迷你PC / 服务器)
```bash
# Snap (권장 — 최신 버전)
sudo snap install blender --classic

# APT (구버전일 수 있음)
sudo apt install blender

# 직접 다운로드 (가장 유연)
wget https://download.blender.org/release/Blender4.4/blender-4.4.0-linux-x64.tar.xz
tar xf blender-4.4.0-linux-x64.tar.xz
sudo ln -s $(pwd)/blender-4.4.0-linux-x64/blender /usr/local/bin/blender
```

### macOS
```bash
# Homebrew
brew install --cask blender

# 또는 직접 다운로드
# CLI 경로: /Applications/Blender.app/Contents/MacOS/Blender
```

### 安装确认
```bash
blender --version
blender -b --python-expr "import bpy; print('bpy OK:', bpy.app.version_string)"
```

## 无头模式运行方式

### 基本架构
```bash
# 스크립트 실행 (새 씬)
blender -b --python script.py

# .blend 파일 로드 후 스크립트 실행
blender -b scene.blend --python script.py

# 인자 전달 (-- 이후)
blender -b --python script.py -- --arg1 value1 --arg2 value2

# 팩토리 설정으로 실행 (사용자 설정 무시)
blender --factory-startup -b --python script.py

# 애드온 활성화
blender -b --addons "rigify,io_scene_gltf2" --python script.py
```

### 参数顺序很重要！
```bash
# ✅ 올바름: blend 로드 → 출력 설정 → 렌더
blender -b scene.blend -o /tmp/output -F PNG -f 1

# ❌ 잘못됨: 출력 설정이 blend 로드 전
blender -b -o /tmp/output scene.blend -f 1
```

### GPU 渲染（无头模式）
```python
# gpu_setup.py — headless에서 GPU 활성화
import bpy
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'CUDA'  # 또는 OPTIX, HIP, METAL
prefs.get_devices()
for device in prefs.devices:
    device.use = True
bpy.context.scene.cycles.device = 'GPU'
```
```bash
blender -b scene.blend -E CYCLES -P gpu_setup.py -f 1 -- --cycles-device CUDA
```

## 脚本使用方法

### 1. 格式转换 (convert_format.py)
```bash
# FBX → glTF
blender -b --python scripts/convert_format.py -- \
  --input model.fbx --output model.glb --format GLB

# OBJ → FBX
blender -b --python scripts/convert_format.py -- \
  --input model.obj --output model.fbx --format FBX

# glTF → OBJ
blender -b --python scripts/convert_format.py -- \
  --input model.gltf --output model.obj --format OBJ

# 배치 변환 (폴더 내 모든 FBX → glTF)
blender -b --python scripts/convert_format.py -- \
  --input-dir ./models/ --output-dir ./converted/ \
  --input-ext .fbx --format GLB
```

### 2. 精灵图渲染 (render_sprite_sheet.py)
```bash
# 8방향 스프라이트 시트
blender -b character.blend --python scripts/render_sprite_sheet.py -- \
  --angles 8 --size 128 --output sprites/character.png

# 아이소메트릭 뷰 (카메라 각도 지정)
blender -b character.blend --python scripts/render_sprite_sheet.py -- \
  --angles 8 --size 256 --camera-angle 30 --output sprites/iso_char.png

# 애니메이션 스프라이트 시트 (모든 프레임)
blender -b character.blend --python scripts/render_sprite_sheet.py -- \
  --angles 4 --size 64 --animated --output sprites/anim_sheet.png
```

### 3. 程序化材质生成 (procedural_props.py)
```bash
# 나무 생성
blender -b --python scripts/procedural_props.py -- \
  --type tree --style low-poly --seed 42 --output props/tree.glb

# 바위 생성
blender -b --python scripts/procedural_props.py -- \
  --type rock --style low-poly --count 5 --output props/rocks.glb

# 상자/크레이트
blender -b --python scripts/procedural_props.py -- \
  --type crate --style wooden --output props/crate.glb

# 건물 외형
blender -b --python scripts/procedural_props.py -- \
  --type building --floors 3 --style medieval --output props/building.glb
```

### 4. 简单绑定 (simple_rig.py)
```bash
# Rigify 메타리그로 자동 리깅
blender -b character.blend --python scripts/simple_rig.py -- \
  --target CharacterMesh --type rigify --output rigged_character.blend

# 심플 본 리그 (2D 게임용)
blender -b character.blend --python scripts/simple_rig.py -- \
  --target CharacterMesh --type simple --bones spine,arm_l,arm_r,leg_l,leg_r \
  --output rigged_simple.blend
```

### 5. 导入 Mixamo 数据 (mixamo_import.py)
```bash
# 단일 Mixamo FBX 임포트 + glTF 변환
blender -b --python scripts/mixamo_import.py -- \
  --input mixamo_character.fbx --output character.glb --fix-scale --fix-rotation

# 여러 Mixamo 애니메이션 병합
blender -b --python scripts/mixamo_import.py -- \
  --input-dir ./mixamo_anims/ --merge-animations \
  --output character_animated.glb

# Mixamo → NLA 트랙 정리
blender -b --python scripts/mixamo_import.py -- \
  --input-dir ./mixamo_anims/ --nla-tracks \
  --output character_nla.blend
```

## 工作流程

### 工作流程 1: Mixamo → Blender → 游戏引擎
```
1. Mixamo에서 캐릭터 리깅 + 애니메이션 다운로드 (FBX)
2. mixamo_import.py로 Blender에 임포트 (스케일/회전 보정)
3. 필요시 애니메이션 NLA 트랙 정리
4. convert_format.py로 glTF/GLB 변환
5. 게임엔진(Godot/Unity)에서 임포트
```

### 工作流程 2: 程序化资产 → 精灵图
```
1. procedural_props.py로 3D 에셋 생성
2. 또는 기존 .blend 파일의 모델 사용
3. render_sprite_sheet.py로 다방향 스프라이트 시트 생성
4. 2D 게임에서 스프라이트 시트 사용
```

### 资产批量处理流程
```bash
#!/bin/bash
# batch_pipeline.sh — 전체 파이프라인 자동화

INPUT_DIR="./raw_models"
OUTPUT_DIR="./game_assets"

# 1. 모든 FBX를 glTF로 변환
blender -b --python scripts/convert_format.py -- \
  --input-dir "$INPUT_DIR" --output-dir "$OUTPUT_DIR/models" \
  --input-ext .fbx --format GLB

# 2. 각 모델의 스프라이트 시트 생성
for blend in "$OUTPUT_DIR"/models/*.glb; do
  name=$(basename "$blend" .glb)
  blender -b --python scripts/render_sprite_sheet.py -- \
    --import "$blend" --angles 8 --size 128 \
    --output "$OUTPUT_DIR/sprites/${name}_sheet.png"
done
```

## 在迷你PC上运行 (nodes.run)

### 从 Clawdbot 向迷你PC 运行脚本
```
# nodes.run으로 Blender 스크립트 실행
nodes.run(node="MiniPC", command=[
    "blender", "-b", "--factory-startup",
    "--python", "/path/to/script.py",
    "--", "--arg1", "value1"
])
```

### 在迷你PC上安装 Blender
```bash
# MiniPC SSH 접속 후
sudo snap install blender --classic

# 또는 직접 다운로드
wget https://download.blender.org/release/Blender4.4/blender-4.4.0-linux-x64.tar.xz
tar xf blender-4.4.0-linux-x64.tar.xz
echo 'export PATH="$HOME/blender-4.4.0-linux-x64:$PATH"' >> ~/.bashrc
```

### 文件传输
```bash
# MiniPC → 맥스튜디오 (HTTP 서버)
# MiniPC에서:
cd /output/dir && python3 -m http.server 9877
# 맥스튜디오에서:
curl -O http://<MINIPC_IP>:9877/output_file.glb
```

## 限制与注意事项

### 渲染引擎
| 渲染引擎 | 是否支持无头模式 | 是否需要 GPU | 备注 |
|------|:----------------:|-------------:|---------|
| **Cycles** | ✅ 完全支持 | 可选 | 支持 CPU 和 GPU，默认选择。 |
| **EEVEE** | ⚠️ 仅支持 Linux | 必需 | 仅限 Linux 3.4 及更高版本，且需要 GPU；macOS/Windows 不支持无头模式。 |
| **Workbench** | ⚠️ 仅支持 Linux | 必需 | 与 EEVEE 有相同限制。 |

### 常见限制：
- **EEVEE 无头模式**：需要 Linux 环境及 GPU，并配置虚拟显示（可使用 `Xvfb`）：
  ```bash
  sudo apt install xvfb
  xvfb-run blender -b scene.blend -E BLENDER_EEVEE -f 1
  ```
- **GPU 无法自动检测**：在无头模式下需手动激活 GPU（详见 `gpu_setup.py` 文件）。
- **bpy 的导入限制**：Python 中的 `import bpy` 每个进程只能执行一次；多任务需通过子进程分离。
- **内存需求**：复杂场景需要大量内存；建议在配置较低的迷你PC（8GB 内存）上使用低多边形模型。
- **Grease Pencil**：在没有 GPU 的环境中无法使用。
- **Snap 安装路径**：使用 Snap 安装时，`pip install` 的路径可能受限；建议使用 tarball 文件进行安装。
- **Blender 版本兼容性**：bpy API 可能因 Blender 版本不同而有所变化；本脚本基于 Blender 4.x 编写。

### 性能优化建议：
- 使用 `--factory-startup` 选项避免加载不必要的用户设置。
- 通过 `--threads N` 指定 CPU 线程数（0 表示全部使用）。
- 对于低多边形模型，Workbench 的渲染速度通常比 Cycles 更快。
- 可使用 `xargs/parallel` 命令并行化批量处理任务。

## 参考资料

- [references/bpy-api.md](references/bpy-api.md) — Blender Python API 的核心参考文档
- [references/rigging.md](references/rigging.md) — 绑定指南（Rigify、Mixamo）
- [references/procedural.md](references/procedural.md) — 程序化建模方法
- [references/rendering.md](references/rendering.md) — 精灵图渲染指南
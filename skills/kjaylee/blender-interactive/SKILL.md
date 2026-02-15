---
name: blender-interactive
description: |
  Blender 양방향 소켓 통신 스킬. TCP 소켓 서버로 실시간 씬 조작, 상태 조회, Poly Haven/Sketchfab 에셋 통합.
  기존 blender-pipeline (배치 처리)와 상호보완 — 복잡한 씬 구축, 반복 조작, 실시간 피드백에 사용.
  트리거: Blender 실시간 조작, 씬 상태 확인, Poly Haven 에셋, Sketchfab 모델, 양방향 Blender 통신.
---

# Blender 交互式套接字服务器

本技能通过基于TCP套接字的双向通信实现实时操控Blender的功能，运行在配备MiniPC的无头Blender 5.0.1系统上。

## 架构

```
┌─────────────┐     nodes.run      ┌──────────────────────┐
│  Clawdbot   │ ──────────────────>│  MiniPC              │
│  (맥스튜디오)│                     │                      │
│             │     blender_client  │  ┌────────────────┐  │
│             │ ──────────────────>│  │ Blender 5.0.1  │  │
│             │     TCP :9876       │  │ (headless)     │  │
│             │ <──────────────────│  │                │  │
│             │     JSON response   │  │ socket_addon   │  │
└─────────────┘                     │  └────────────────┘  │
                                    └──────────────────────┘
```

## 与其他技能的关系

| 技能 | 用途 | 工作模式 |
|------|------|------|
| **blender-pipeline** | 批量转换、精灵图制作、程序化操作 | 一次性脚本执行 |
| **blender-interactive** | 实时操控、场景构建、状态查询 | 持续运行的套接字服务器 |

**选择建议：**
- 简单的转换/批量操作 → 使用 **blender-pipeline**  
- 复杂的场景构建、重复操作或需要实时状态检查 → 使用 **blender-interactive**  

## 快速入门

### 1. 启动服务器（在MiniPC上）

```bash
# nodes.run으로 서버 시작
nodes.run(node="MiniPC", command=[
    "bash", "-c",
    "blender -b --factory-startup --python /home/spritz/blender-interactive/blender_socket_addon.py -- --port 9876 &"
])

# 또는 start_server.sh 사용
nodes.run(node="MiniPC", command=[
    "bash", "/home/spritz/blender-interactive/scripts/start_server.sh", "--background"
])
```

### 2. 发送命令

```bash
# ping
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/blender_client.py",
    "ping"
])

# 씬 정보 조회
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/blender_client.py",
    "get_scene_info", "--pretty"
])

# 오브젝트 생성
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/blender_client.py",
    "create_object", "--params", "{\"type\":\"SPHERE\",\"name\":\"Earth\",\"location\":[0,0,0]}"
])

# 머티리얼 설정
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/blender_client.py",
    "set_material", "--params", "{\"object_name\":\"Earth\",\"color\":[0.2,0.4,0.8],\"metallic\":0.0,\"roughness\":0.7}"
])

# 렌더링 프리뷰
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/blender_client.py",
    "render_preview", "--params", "{\"output_path\":\"/tmp/preview.png\",\"resolution_x\":512,\"resolution_y\":512,\"samples\":32}"
])
```

### 3. 停止服务器

```bash
nodes.run(node="MiniPC", command=[
    "bash", "/home/spritz/blender-interactive/scripts/start_server.sh", "--stop"
])
```

## 命令参考

### 系统命令
| 命令 | 参数 | 说明 |
|------|----------|------|
| `ping` | — | 检查服务器状态及命令列表 |

### 查看场景信息
| 命令 | 参数 | 说明 |
| `get_scene_info` | — | 获取整个场景的状态（对象、相机、灯光、分辨率等） |
| `get_object_info` | `name` | 获取特定对象的详细信息（网格、材质、绑定框） |

### 操作对象
| 命令 | 参数 | 说明 |
| `create_object` | `type`, `name?`, `location?`, `scale?` | 创建基本几何体（立方体、球体、平面、圆柱体、圆锥体、环形体、猴子模型） |
| `delete_object` | `name` | 删除对象 |
| `modify_object` | `name`, `location?`, `rotation?`, `scale?`, `visible?` | 修改对象的位置、旋转、大小或可见性 |

### 材质设置
| 命令 | 参数 | 说明 |
| `set_material` | `object_name`, `color?`, `metallic?`, `roughness?`, `material_name?` | 设置PBR材质 |

### 渲染
| 命令 | 参数 | 说明 |
| `render_preview` | `output_path?`, `resolution_x?`, `resolution_y?`, `samples?`, `engine?` | 快速预览（512x512，32样本） |
| `render_to_file` | `output_path`, `format?`, `resolution_x?`, `resolution_y?`, `samples?`, `engine?` | 高质量渲染 |

### 文件管理
| 命令 | 参数 | 说明 |
| `save_blend` | `filepath` | 保存 Blender 文件 |
| `load_blend` | `filepath` | 加载 Blender 文件 |
| `import_model` | `filepath`, `format?` | 导入模型（glTF/FBX/OBJ/STL/PLY格式） |
| `export_model` | `filepath`, `format?`, `selected_only?` | 导出模型 |
| `clear_scene` | `keep_camera?`, `keep_lights?` | 重置场景状态 |

### 执行代码
| 命令 | 参数 | 说明 |
| `execute_code` | `code` | 执行任意Python代码（具有高度灵活性） |

## 集成Poly Haven资源

支持搜索和下载CC0许可下的免费资源（HDRI图像、纹理、3D模型）。

```bash
# 텍스처 카테고리 조회
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/polyhaven.py",
    "categories", "textures"
])

# 벽돌 텍스처 검색
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/polyhaven.py",
    "search", "--type", "textures", "--categories", "brick"
])

# 텍스처 다운로드 (1k 해상도)
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/polyhaven.py",
    "download", "rock_wall_08", "--type", "textures", "--resolution", "1k",
    "--output", "/tmp/polyhaven/textures/"
])

# HDRI 다운로드
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/polyhaven.py",
    "download", "meadow", "--type", "hdris", "--resolution", "2k",
    "--format", "hdr", "--output", "/tmp/polyhaven/hdri/"
])

# 3D 모델 다운로드
nodes.run(node="MiniPC", command=[
    "python3", "/home/spritz/blender-interactive/scripts/polyhaven.py",
    "download", "food_apple_01", "--type", "models", "--resolution", "1k",
    "--format", "gltf", "--output", "/tmp/polyhaven/models/"
])
```

## Poly Haven与Blender的集成流程

```bash
# 1. 텍스처 다운로드
polyhaven.py download rock_wall_08 --type textures --resolution 1k --output /tmp/ph/

# 2. Blender에서 평면 생성 + 텍스처 적용 (execute_code 사용)
blender_client.py execute_code --params '{
  "code": "import bpy\nimport os\n\n# 평면 생성\nbpy.ops.mesh.primitive_plane_add(size=10)\nplane = bpy.context.active_object\nplane.name = \"Ground\"\n\n# 머티리얼 + 텍스처\nmat = bpy.data.materials.new(\"RockWall\")\nmat.use_nodes = True\nnodes = mat.node_tree.nodes\nlinks = mat.node_tree.links\n\nbsdf = nodes[\"Principled BSDF\"]\ntex = nodes.new(\"ShaderNodeTexImage\")\ntex.image = bpy.data.images.load(\"/tmp/ph/rock_wall_08_Diffuse_1k.jpg\")\nlinks.new(tex.outputs[\"Color\"], bsdf.inputs[\"Base Color\"])\n\nplane.data.materials.append(mat)"
}'
```

## 协议细节

### 请求格式

```json
{
  "type": "command_name",
  "params": {
    "key": "value"
  }
}
```

### 响应格式

```json
{
  "status": "success",
  "result": { ... }
}
```

### 通信方式
- **传输方式：** TCP套接字，基于TCP的JSON协议  
- **端口：** 默认为9876  
- **超时设置：** 300秒（用于处理渲染等耗时操作）  
- **线程安全性：** 命令在Blender的主线程中执行（通过`bpy.app.timers`）  
- **并发连接：** 支持多个客户端，但会按顺序处理请求  

## MiniPC部署

### 文件传输（从MacStudio到MiniPC）

```bash
# 1. 스킬 폴더를 MiniPC에 복사
# nodes.run으로 base64 전송 또는 scp
scp -r skills/blender-interactive/ spritz@100.80.169.94:/home/spritz/blender-interactive/
```

### 自动启动（使用systemd）

```ini
# /home/spritz/.config/systemd/user/blender-socket.service
[Unit]
Description=Blender Interactive Socket Server
After=network.target

[Service]
Type=simple
ExecStart=/snap/bin/blender -b --factory-startup --python /home/spritz/blender-interactive/blender_socket_addon.py -- --port 9876
ExecStop=/bin/kill -TERM $MAINPID
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable blender-socket
systemctl --user start blender-socket
```

## 使用限制

### 无头模式限制
- **无法截取视图窗口截图** — 可通过`render_preview`命令使用Cycles引擎进行CPU渲染（虽然速度较慢，但结果更准确）  
- **不支持EEVEE引擎** — 无头模式下需要GPU，仅支持Cycles的CPU渲染 |
- **不支持实时预览** — 需通过渲染结果查看最终效果 |

## 性能表现
- **MiniPC（8GB内存）**：建议使用低复杂度的场景；复杂场景可能导致内存不足 |
- **Cycles CPU渲染**：512x512分辨率、32样本的预览大约需要5-15秒 |
- **处理大型Poly Haven资源**：4K纹理会占用较多内存，建议使用1k-2k分辨率的纹理 |

### 安全性
- `execute_code`命令可用于执行任意代码 — 在受控的MiniPC环境中是安全的 |
- 若暴露给外部环境，需使用`--host 127.0.0.1`限制访问范围至本地主机 |

## 文件结构

```
blender-interactive/
├── SKILL.md                       # 이 문서
├── blender_socket_addon.py        # Blender 소켓 서버 (핵심)
└── scripts/
    ├── blender_client.py          # 명령 전송 클라이언트
    ├── polyhaven.py               # Poly Haven API 클라이언트
    └── start_server.sh            # 서버 시작/중지 스크립트
```
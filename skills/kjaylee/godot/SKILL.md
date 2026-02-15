---
name: godot
description: "Godot引擎游戏开发：支持项目创建、GDScript编程、2D/3D游戏制作，以及节点系统、场景结构、物理效果/动画/用户界面（UI）的实现。适用于Godot项目的开发工作。"
keywords: [godot, game-engine, gdscript, 2d-game, 3d-game, game-development]
version: 1.0.0
---

# Godot引擎技能指南

本指南为Godot 4.x游戏引擎的开发提供了全面指导，涵盖了从项目创建、构建到GDScript编程、场景/节点系统设计，以及2D/3D游戏制作的整个流程。

## 🚀 快速入门

### 新项目创建（通过CLI）
```bash
# MiniPC에서 실행 (Godot 4.6 설치됨)
cd $HOME/
godot4 --headless --path . --create-project "MyGame"

# 또는 맥 스튜디오에서 원격 실행
# (nodes.run 또는 ssh 사용)
```

### 项目结构
```
MyGame/
├── project.godot       # 프로젝트 설정
├── scenes/             # 씬 파일 (.tscn)
│   ├── main.tscn
│   ├── player.tscn
│   └── enemy.tscn
├── scripts/            # GDScript 파일
│   ├── player.gd
│   └── enemy.gd
├── assets/             # 에셋 (텍스처, 사운드 등)
│   ├── sprites/
│   ├── sounds/
│   └── fonts/
└── export_presets.cfg  # 빌드 설정
```

### 创建第一个场景
1. 创建**Node2D**（2D游戏）或**Node3D**（3D游戏）根节点
2. 添加子节点（如Sprite2D、CharacterBody2D、Camera2D等）
3. 附加脚本（Attach Script）
4. 编写 `_ready()` 和 `_process(delta)` 函数

## 📚 GDScript基础

### 核心生命周期函数
```gdscript
extends Node2D

# 씬 트리 진입 시 1회 호출
func _ready():
    print("Ready!")

# 매 프레임 호출 (delta = 프레임 시간)
func _process(delta):
    position.x += 100 * delta  # 초당 100픽셀 이동

# 물리 프레임마다 호출 (고정 간격)
func _physics_process(delta):
    move_and_slide()
```

### 变量与类型
```gdscript
# 타입 추론
var speed := 200.0           # float
var health := 100            # int
var player_name := "Hero"    # String

# 명시적 타입
var velocity: Vector2 = Vector2.ZERO
var sprite: Sprite2D

# @export로 에디터 노출
@export var max_speed: float = 300.0
@export_range(0, 100) var hp: int = 100
```

### Signal（信号）
```gdscript
# 신호 정의
signal health_changed(new_health)
signal player_died

# 신호 발생
func take_damage(amount):
    health -= amount
    health_changed.emit(health)
    if health <= 0:
        player_died.emit()

# 다른 스크립트에서 연결
func _ready():
    $Player.health_changed.connect(_on_player_health_changed)

func _on_player_health_changed(new_health):
    print("Health: ", new_health)
```

### 访问节点
```gdscript
# 자식 노드 가져오기
var sprite = $Sprite2D
var label = get_node("Label")

# 부모/형제 접근
var parent = get_parent()
var sibling = get_parent().get_node("OtherNode")

# 씬 전역 접근 (Autoload)
GlobalScript.some_function()
```

## 🎮 2D游戏开发流程

### 玩家移动（8个方向）
```gdscript
extends CharacterBody2D

@export var speed = 300.0

func _physics_process(delta):
    var input_dir = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_dir * speed
    move_and_slide()
```

### 动画（AnimatedSprite2D）
```gdscript
@onready var anim = $AnimatedSprite2D

func _process(delta):
    if velocity.length() > 0:
        anim.play("walk")
    else:
        anim.play("idle")
```

### 碰撞检测（Area2D）
```gdscript
extends Area2D

func _ready():
    body_entered.connect(_on_body_entered)

func _on_body_entered(body):
    if body.is_in_group("player"):
        print("Player entered!")
        queue_free()  # 자신 제거
```

### 使用TileMap
```gdscript
@onready var tilemap = $TileMap

func _ready():
    # 타일 좌표 (0, 0)에 타일 ID 1 배치
    tilemap.set_cell(0, Vector2i(0, 0), 1)
```

## 🌍 3D游戏开发流程

### FPS玩家控制器
```gdscript
extends CharacterBody3D

@export var speed = 5.0
@export var jump_velocity = 4.5
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta):
    # 중력
    if not is_on_floor():
        velocity.y -= gravity * delta
    
    # 점프
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = jump_velocity
    
    # 이동
    var input_dir = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
    velocity.x = direction.x * speed
    velocity.z = direction.z * speed
    
    move_and_slide()
```

### 摄像头旋转（通过鼠标）
```gdscript
extends Camera3D

@export var sensitivity = 0.003

func _ready():
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _input(event):
    if event is InputEventMouseMotion:
        rotation.y -= event.relative.x * sensitivity
        rotation.x -= event.relative.y * sensitivity
        rotation.x = clamp(rotation.x, -PI/2, PI/2)
```

## 🛠️ 常见开发模式

### 场景切换
```gdscript
# 다음 씬으로 이동
get_tree().change_scene_to_file("res://scenes/level2.tscn")

# 씬 인스턴스 생성
var enemy_scene = preload("res://scenes/enemy.tscn")
var enemy = enemy_scene.instantiate()
add_child(enemy)
```

### 定时器
```gdscript
# 타이머 노드 사용
@onready var timer = $Timer

func _ready():
    timer.timeout.connect(_on_timer_timeout)
    timer.start(2.0)  # 2초 후 신호 발생

func _on_timer_timeout():
    print("Timer finished!")
```

### Tween动画
```gdscript
func fade_out():
    var tween = create_tween()
    tween.tween_property($Sprite2D, "modulate:a", 0.0, 1.0)  # 1초간 투명화
```

### 用户界面更新
```gdscript
extends Control

@onready var label = $Label

func update_score(score):
    label.text = "Score: %d" % score
```

## 🏗️ 构建与导出（适用于MiniPC）

### Web（HTML5）构建
```bash
cd $HOME/
godot4 --headless --path MyGame --export-release "Web" output/index.html
```

### 设置导出预设（project.godot）
```ini
[export]
name="Web"
platform="Web"
runnable=true
export_path="export/web/index.html"
```

### 自定义启动界面
```bash
# East Sea Games 로고 사용
cp $HOME/godot-demo/boot_splash.png MyGame/
```

## 📖 参考资料

### 常用节点
- **2D节点**：Node2D、Sprite2D、CharacterBody2D、RigidBody2D、Area2D、Camera2D、TileMap、AnimatedSprite2D
- **3D节点**：Node3D、MeshInstance3D、CharacterBody3D、RigidBody3D、Area3D、Camera3D
- **UI元素**：Control、Label、Button、Panel、HBoxContainer、VBoxContainer
- **音频组件**：AudioStreamPlayer、AudioStreamPlayer2D、AudioStreamPlayer3D
- **其他组件**：Timer、AnimationPlayer、CollisionShape2D/3D

### 有用链接
- [Godot官方文档](https://docs.godotengine.org/en/stable/)
- [GDQuest教程](https://www.gdquest.com/tutorial/godot/)
- [First 2D Game教程](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/index.html)

### 参考资料目录
- `references/gdscript-cheatsheet.md`：GDScript语法速查表
- `references/nodes-reference.md`：常用节点列表
- `references/best-practices.md`：Godot最佳实践
- `references/2d-patterns.md`：2D游戏开发通用模式
- `references/3d-patterns.md`：3D游戏开发通用模式

---

**版本**：1.0.0  
**作者**：Miss Kim  
**日期**：2026-02-05
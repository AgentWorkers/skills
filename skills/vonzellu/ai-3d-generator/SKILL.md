# AI 3D模型生成器

从文本描述自动生成详细的3D模型。

## 架构

```
Prompt utilisateur → LLM (Kimi/Gemini) → Code Python/Trimesh → Génération STL → Export
```

## 自动化流程

### 1. 提示工程（Prompt Engineering）

创建一个名为`prompts/3d-generator.txt`的文件：

```markdown
Tu es un expert en modélisation 3D paramétrique. Génère un script Python utilisant Trimesh 
pour créer le modèle 3D décrit ci-dessous.

RÈGLES:
- Utilise trimesh.creation (icosphere, cylinder, cone, torus, box)
- Pour les détails complexes: utiliser des boucles et paramètres
- Résolution élevée: subdivisions=4-5 pour les sphères, sections=32-64 pour cylindres
- Ajouter des détails de surface (panneaux, textures géométriques)
- Structure modulaire avec fonctions réutilisables
- Exporter en STL binaire à la fin

SCRIPT TEMPLATE:
```python
#!/usr/bin/env python3
import numpy as np
import trimesh
from trimesh.creation import icosphere, cylinder, cone, torus, box
from trimesh.transformations import rotation_matrix
import os

EXPORT_DIR = "/home/celluloid/.openclaw/workspace/stl-exports"

def save_mesh(mesh, filename):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filepath = os.path.join(EXPORT_DIR, filename)
    mesh.export(filepath)
    print(f"✓ 已导出：{filepath}")
    print(f"  三角形数量：{len(mesh.faces):,}")
    return filepath

def rotate_mesh(mesh, angle, axis, point=None):
    if point is None:
        point = [0, 0, 0]
    mat = rotation_matrix(angle, axis, point)
    mesh.apply_transform(mat)
    return mesh

# === 主模型 ===
def create_model():
    meshes = []

    # [在此处生成模型]

    # 合并与优化
    combined = trimesh.util.concatenate(meshes)
    combined.merge_vertices()
    return combined

if __name__ == "__main__":
    mesh = create_model()
    save_mesh(mesh, "[模型名称].stl")
```

DESCRIPTION DU MODÈLE À CRÉER:
{{USER_DESCRIPTION}}

Génère uniquement le code Python complet, sans explications.
```

## 2. OpenClaw技能自动化

创建一个名为`~/.openclaw/workspace/skills/ai-3d-generator/SKILL.md`的文件：

### 使用方法

#### 简单生成
```bash
# Génère un modèle à partir d'une description
~/.openclaw/workspace/skills/ai-3d-generator/scripts/generate-from-prompt.sh "vaisseau spatial avec ailes delta et cockpit vitré"
```

#### 带参数生成
```bash
# Avec spécifications techniques
~/.openclaw/workspace/skills/ai-3d-generator/scripts/generate-from-prompt.sh \
  "robot humanoïde articulé" \
  --scale=50mm \
  --detail=high \
  --output=robot.stl
```

### 流程

1. **分析提示** → 提取实体信息（形状、尺寸、细节）
2. **生成代码** → LLM生成Python/Trimesh脚本
3. **语法验证** → 检查导入语句和代码结构
4. **执行** → 生成3D模型并导出为STL格式
5. **后期处理** → 优化模型并检查其是否为“流形”（适合3D打印）

## 3. 有效的提示示例

### 优秀的提示（详细且具体）：
```
Crée un château médiéval avec:
- Tours cylindriques aux 4 coins (diamètre 8mm, hauteur 25mm)
- Créneaux sur les tours
- Mur d'enceinte carré (40x40mm)
- Pont-levis à l'avant
- Texture de pierre avec des blocs individuels
- Échelle 1:100 pour impression 3D
```

### 不良的提示（过于模糊）：
```
Fais-moi un château
```

## 4. 完整自动化

### 定期生成模型的Cron作业
```json
{
  "name": "3d:generate-daily",
  "schedule": {"kind": "cron", "expr": "0 9 * * *"},
  "payload": {
    "message": "Génère un modèle 3D aléatoire du jour (animaux, architecture, véhicules) et exporte en STL",
    "model": "openrouter/moonshotai/kimi-k2.5"
  }
}
```

## 5. 优化方案（针对超高细节模型）

### 高级技术

#### 程序化建模技术
```python
# Ajouter du bruit de surface pour texture
def add_surface_noise(mesh, amplitude=0.1):
    vertices = mesh.vertices.copy()
    noise = np.random.normal(0, amplitude, vertices.shape)
    mesh.vertices = vertices + noise
    return mesh
```

#### 参数化细节处理
```python
# Générer des détails répétitifs
for i in range(100):  # 100 panneaux de surface
    angle = i * 2 * np.pi / 100
    panel = create_detailed_panel()
    position_on_surface(panel, radius=20, angle=angle)
```

#### 优化后的布尔运算
```python
# Utiliser trimesh.boolean pour les découpes complexes
from trimesh.boolean import difference, union, intersection

result = difference(base_mesh, cutting_tool)
```

## 6. 完整的工作流程示例

### OpenClaw命令示例：
```
Génère un modèle 3D d'une station spatiale en anneau avec:
- Anneau principal de 80mm de diamètre
- 6 modules d'habitation sur l'anneau
- Sphère centrale de commande
- Antennes et panneaux solaires
- Style cyberpunk avec câbles et tuyaux
Exporte en STL haute résolution.
```

### 自动化响应流程：

1. LLM生成Python脚本（约30秒）
2. Trimesh执行模型生成（约1-2分钟）
3. 优化后的STL模型导出
4. 提供模型信息（三角形数量、体积、尺寸）

## 注意事项：

- 对于非常复杂的模型（超过10万个三角形），请预留更多时间。
- 如有必要，可使用`trimesh.smoothing`函数来平滑模型表面。
- 确保模型是“流形”结构，以便进行3D打印。
- 保存生成的脚本以供后续使用或修改。
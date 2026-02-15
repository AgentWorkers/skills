# CAD Agent

> 为您的AI代理提供CAD工作所需的“视觉能力”。

## 描述

CAD Agent是一个渲染服务器，它能够让AI代理看到它们正在构建的内容。您可以通过发送建模命令来启动渲染过程，然后接收渲染后的图像，并根据这些图像进行视觉上的迭代（即根据渲染结果调整设计）。

**适用场景：** 3D打印部件的设计、参数化CAD建模、机械设计、build123d建模等。

## 架构

**重要提示：** 所有的CAD逻辑都在容器内部运行。您（作为AI代理）只需要：
1. 通过HTTP发送命令；
2. 查看返回的图像；
3. 决定下一步该做什么。

**注意：** **绝对不要** 在容器外部进行STL文件的操作、网格处理或渲染工作。所有这些任务都由容器内部完成——您只需发送命令并观察结果即可。

## 设置步骤

### 1. 克隆仓库

```bash
git clone https://github.com/clawd-maf/cad-agent.git
cd cad-agent
```

### 2. 构建Docker镜像

```bash
docker build -t cad-agent:latest .
```

或者使用docker-compose来构建：

```bash
docker-compose build
```

### 3. 运行服务器

```bash
# Using docker-compose (recommended)
docker-compose up -d

# Or using docker directly
docker run -d --name cad-agent -p 8123:8123 cad-agent:latest serve
```

### 4. 验证安装是否成功

```bash
curl http://localhost:8123/health
# Should return: {"status": "healthy", ...}
```

> **关于Docker-in-Docker环境的小提示：** 在嵌套的容器环境中（例如Clawdbot沙箱），主机网络可能无法正常工作——即使服务器绑定到了`0.0.0.0:8123`，`curl localhost:8123`命令也可能失败。此时请使用`docker exec cad-agent python3 -c "..."`命令来执行操作。在普通的Docker主机上，`localhost`访问是可行的。

## 工作流程

### 1. 创建模型

```bash
curl -X POST http://localhost:8123/model/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_part",
    "code": "from build123d import *\nresult = Box(60, 40, 30)"
  }'
```

### 2. 渲染并查看结果

```bash
# Get multi-view (front/right/top/iso)
curl -X POST http://localhost:8123/render/multiview \
  -d '{"model_name": "my_part"}' -o views.png

# Or 3D isometric
curl -X POST http://localhost:8123/render/3d \
  -d '{"model_name": "my_part", "view": "isometric"}' -o iso.png
```

**查看渲染后的图像。** 如果结果不符合要求，请修改模型并重新渲染。

### 3. 进行迭代

```bash
curl -X POST http://localhost:8123/model/modify \
  -d '{
    "name": "my_part", 
    "code": "result = result - Cylinder(5, 50).locate(Pos(20, 10, 0))"
  }'

# Re-render to check
curl -X POST http://localhost:8123/render/3d \
  -d '{"model_name": "my_part"}' -o updated.png
```

### 4. 导出模型

```bash
curl -X POST http://localhost:8123/export \
  -d '{"model_name": "my_part", "format": "stl"}' -o part.stl
```

## API端点

| 端点          | 功能                          |
|-----------------|-----------------------------|
| `POST /model/create`    | 运行build123d代码，创建模型             |
| `POST /model/modify`    | 修改现有模型                     |
| `GET /model/list`     | 获取当前会话中的所有模型列表             |
| `GET /model/{name}/measure` | 获取模型的尺寸信息                 |
| `POST /render/3d`     | 生成3D渲染图像（VTK格式）             |
| `POST /render/2d`     | 生成2D技术图纸                     |
| `POST /render/multiview` | 生成多视角组合视图                 |
| `POST /export`     | 导出模型文件（STL/STEP/3MF格式）             |
| `POST /analyze/printability` | 检查模型是否适合3D打印             |

## build123d使用指南

```python
from build123d import *

# Primitives
Box(width, depth, height)
Cylinder(radius, height)
Sphere(radius)

# Boolean
a + b   # union
a - b   # subtract
a & b   # intersect

# Position
part.locate(Pos(x, y, z))
part.rotate(Axis.Z, 45)

# Edges
fillet(part.edges(), radius)
chamfer(part.edges(), length)
```

## 重要注意事项：

- **严禁绕过容器**：禁止使用matplotlib库或任何外部STL处理工具，也不允许对模型网格进行直接修改。
- **渲染结果就是您的“眼睛”**：每次修改模型后都必须请求重新渲染。
- **通过视觉反馈进行迭代**：整个流程的核心就是让您能够直观地看到自己的设计成果。

## 设计文件的安全性

该项目采取了以下措施来防止意外提交CAD模型文件：
- `.gitignore`文件会屏蔽`.stl`、`.step`、`.3mf`等模型文件；
- 提交前的预提交钩子会拒绝包含设计文件的提交；
- 用户的设计文件仅保存在本地，不会被纳入版本控制。

## 链接资源

- [仓库链接](https://github.com/clawd-maf/cad-agent)
- [build123d官方文档](https://build123d.readthedocs.io/)
- [VTK相关文档](https://vtk.org/)
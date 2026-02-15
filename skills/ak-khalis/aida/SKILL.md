# AIDA技能（适用于OpenClaw）

## 技能名称
aida

## 描述
AIDA（AI驱动的智能建筑自动化平台）的对话式交互界面。

## 支持的指令：
- aida.status        → 获取建筑的实时状态
- aida.control       → 控制设备（灯光、遮阳设施、暖通空调系统）
- aida.optimize      → 优化建筑运行目标
- aida.diagnostics  → 运行预防性诊断

## 示例指令：
- “AIDA，建筑的状态是什么？”
- “优化能源使用。”
- “关闭3楼的灯光。”
- “对这个区域进行诊断。”

## AIDA目标映射：
- 舒适性优化
- 能源优化
- 预防性维护

## API接口要求：
该技能要求AIDA提供以下REST接口：
- GET /status
- POST /control
- POST /optimize
- GET /diagnostics

所有请求均通过bearer token进行身份验证。
# benos-bootstrap

BenOS Bootstrap 是一个用于基于 OpenClaw 的代理栈的系统初始化技能（system-initialization skill）。

## 目的

该技能用于在 OpenClaw 内部初始化 BenOS 运行时环境。它执行启动验证、建立基线状态，并确保在其他 BenOS 技能执行之前所需系统依赖项都已就绪。

## 功能说明

- 验证工作区结构及沙箱（sandbox）的完整性
- 确认代理的运行时配置是否有效
- 检查所需的环境变量
- 验证 Node.js 运行时的兼容性
- 为编排逻辑（orchestration logic）返回结构化的健康状态（health status）信息

## 存在的原因

BenOS 被设计为一个确定性、结构化的执行运行时层（executive runtime layer）。Bootstrap 层确保了系统的可预测启动行为，并防止下游技能在不一致的环境中执行。

该技能设计得较为轻量级，但具有基础性作用。它应在高级编排或自动化层之前被执行。

## 使用方法

该技能可以在系统启动时自动调用，或在需要系统验证时手动执行。

**示例：**

在部署其他自动化模块之前，运行 `benos-bootstrap` 以验证运行时的健康状态。

## 输出结果

返回结构化的 JSON 数据，包含以下内容：

- `ok`（布尔值，表示操作是否成功）
- `message`（字符串，包含操作结果或错误信息）
- `environment metadata`（环境元数据，未来可能会扩展）

## 发展计划

未来版本将实现以下功能：
- 添加环境差异检测（environment diff detection）
- 集成结构化日志记录（structured logging）
- 支持运行前的依赖项解析（pre-flight dependency resolution）
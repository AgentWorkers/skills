---
name: agent-policy-guardrails-engine
description: 构建、运行并扩展 Agent Policy & Guardrails Engine。该工具适用于实现策略格式、执行逻辑、决策冲突解决机制、策略应用程序编程接口（API），以及审计/合规性工作流程。
---
# 代理策略与防护机制引擎（Agent Policy & Guardrails Engine）

## 适用场景

- 当您需要添加或修改策略执行行为时。
- 当您需要添加新的策略类型（财务、隐私、通信、运营、审批、基于时间的策略）时。
- 当您需要扩展决策结果（`ALLOW`、`DENY`、`MODIFY`、`REQUIRE_APPROVAL`）时。
- 当您需要更新API、数据持久化机制或审计日志功能时。

## 项目结构

- `app/main.py`：FastAPI接口。
- `app/service.py`：负责策略的创建、读取、更新和删除（CRUD）操作，以及策略评估和审计日志记录。
- `app/engine.py`：核心的策略评估和冲突解决逻辑。
- `app/policy_parser.py`：将JSON/YAML/NL格式的策略解析为结构化的数据。
- `app/schemas.py`：定义请求/响应数据以及策略的数据结构。
- `app/models.py`：使用SQLAlchemy构建的模型（`policies`、`audit_logs`）。
- `app/seed.py`：包含基础策略配置。
- `tests/test_api.py`：针对API层面的功能进行测试。
- `tests/test_engine.py`：针对引擎的决策逻辑进行测试。

## 标准工作流程

1. 如果策略结构发生变化，首先更新数据结构和模型。
2. 然后更新策略解析器和引擎的评估逻辑。
3. 根据需要更新API和服务层。
4. 为引擎和API添加或更新相应的测试用例。
5. 在最终完成之前运行所有测试。

## 命令操作

- 安装并测试相关组件：```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
```

- 在本地运行应用程序：```bash
python3 -m uvicorn app.main:app --reload
```

## 执行规则

所有外部代理/工具的操作在执行前必须通过`POST /evaluate`接口发送请求。

**运行时处理规则**：
- `DENY`：阻止操作执行。
- `REQUIRE_APPROVAL`：暂停操作并需要人工审批。
- `MODIFY`：应用返回的修改建议后执行操作。
- `ALLOW`：直接执行操作。

## 冲突解决规则

当多个策略对同一操作有约束时：
1. 优先级最高的策略生效。
- 如果优先级相同，则根据规则的严重程度来决定：`DENY > REQUIRE_APPROVAL > MODIFY > ALLOW`。

## 添加新的防护机制

1. 在`app/seed.py`中添加新的策略配置（可选的基础策略）。
2. 确保策略中的`action_types`和`conditions`与实际运行时的数据字段相对应。
3. 在`tests/test_api.py`中使用`/evaluate`接口添加API测试用例。
4. 在`tests/test_engine.py`中添加针对边缘情况/冲突情况的引擎级测试用例。

## 注意事项

- 保持策略评估的确定性（即每次输入应产生相同的输出结果）。
- 对于复杂的控制逻辑，建议使用结构化的JSON/YAML格式的策略。
- 自然语言描述的规则应能被转换为相同的结构化策略格式。
# 📡 Langfuse 可观测性工具

Langfuse v3 提供了一套完整的可观测性工具包，专为 OpenClaw 代理设计——能够自动追踪大型语言模型（LLM）的调用、API 调用、工具执行以及自定义事件。该工具支持按模型进行成本跟踪、会话分组、评估评分、仪表盘查询以及健康状态监控，是代理可观测性的核心组件。

**用途：** 日志记录、追踪、调试、成本分析以及审计追踪。

## 快速入门

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/skills/langfuse-observability/scripts"))
from langfuse_hub import traced, trace_llm, trace_api, trace_tool, trace_event, flush
```

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `langfuse_hub.py` | 提供通用的导入功能、追踪函数、装饰器及上下文管理器 |
| `langfuse_admin.py` | 提供用于仪表盘查询的命令行界面（包括追踪记录、成本信息、会话详情及代理健康状态） |
| `langfuse_cron.py` | 每日生成可观测性报告并通过 Telegram 发送 |

## 实例信息

- **主机地址：** http://langfuse-web:3000 |
- **仪表盘地址：** http://langfuse-web:3000 （仅限内部访问） |
- **SDK：** Langfuse Python v3.14.1 |

## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。更多相关信息可查看 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **您的 AI 代理需要可观测性功能吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)
---
slug: "multi-agent-estimation"
display_name: "Multi Agent Estimation"
description: "构建用于建筑估算的多智能体AI系统。使用CrewAI/LangGraph来协调各个专用智能体（如QTO智能体、定价智能体、验证智能体），以实现复杂估算工作流程的自动化。"
---

# 多智能体估算系统

## 概述

到2026年，人工智能（AI）代理已从单一任务的助手发展为协同工作的多智能体系统。这一技术使得构建由专门化AI代理组成的团队成为可能，这些代理共同协作以实现建筑估算的自动化。

> “得益于大型语言模型（LLM）节点，你可以简单地请求ChatGPT、Claude或任何先进的AI助手生成n8n自动化流程——无论是从PDF文件中提取数据、验证参数，还是生成定制的报价表（QTO表）——并在几秒钟内获得即可运行的工作流程。” —— Artem Boiko

## 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ESTIMATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │  QTO     │   │ Pricing  │   │Validation│   │  Report  │     │
│  │  Agent   │──▶│  Agent   │──▶│  Agent   │──▶│  Agent   │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│       │              │              │              │            │
│       ▼              ▼              ▼              ▼            │
│   Extract        Match to       Validate       Generate        │
│   quantities     CWICR DB       totals         Excel/PDF       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 使用CrewAI快速入门

```python
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# QTO Agent - Extracts quantities from documents
qto_agent = Agent(
    role="Quantity Takeoff Specialist",
    goal="Extract accurate quantities from IFC models and PDF drawings",
    backstory="""You are an expert quantity surveyor with 20 years of
    experience in construction. You meticulously extract volumes, areas,
    and counts from building models and drawings.""",
    llm=llm,
    verbose=True
)

# Pricing Agent - Matches items to price database
pricing_agent = Agent(
    role="Cost Estimator",
    goal="Match extracted quantities to CWICR database and apply unit rates",
    backstory="""You are a senior estimator who knows construction costs
    inside out. You match work items to standardized codes and apply
    appropriate unit rates based on project location and conditions.""",
    llm=llm,
    verbose=True
)

# Validation Agent - Checks for errors and outliers
validation_agent = Agent(
    role="Quality Assurance Specialist",
    goal="Validate estimate accuracy and flag potential errors",
    backstory="""You review estimates for completeness, accuracy, and
    reasonableness. You catch errors that others miss and ensure
    estimates are defensible.""",
    llm=llm,
    verbose=True
)

# Report Agent - Generates final deliverables
report_agent = Agent(
    role="Report Generator",
    goal="Create professional estimate reports in Excel and PDF",
    backstory="""You transform raw estimate data into polished,
    professional reports that clients can understand and trust.""",
    llm=llm,
    verbose=True
)
```

## 定义任务

```python
# Task 1: Extract quantities from IFC
qto_task = Task(
    description="""
    Extract all quantities from the provided IFC model:
    - Walls: volumes, areas, lengths
    - Slabs: areas, volumes
    - Columns: counts, volumes
    - Beams: lengths, volumes

    Group by building level and element type.
    Output as structured JSON.
    """,
    expected_output="JSON with quantities grouped by level and type",
    agent=qto_agent
)

# Task 2: Match to price database
pricing_task = Task(
    description="""
    For each extracted quantity:
    1. Match to CWICR code using semantic search
    2. Apply unit rate from price database
    3. Calculate line item totals
    4. Add markup percentages (OH&P, contingency)

    Output detailed cost breakdown.
    """,
    expected_output="Cost breakdown with CWICR codes and totals",
    agent=pricing_agent,
    context=[qto_task]
)

# Task 3: Validate estimate
validation_task = Task(
    description="""
    Review the estimate for:
    - Missing scope items
    - Unrealistic unit rates (compare to historical)
    - Math errors
    - Inconsistent quantities

    Flag any issues with severity rating.
    """,
    expected_output="Validation report with issues and severity",
    agent=validation_agent,
    context=[pricing_task]
)

# Task 4: Generate report
report_task = Task(
    description="""
    Generate professional estimate report:
    - Executive summary with total
    - Detailed breakdown by CSI division
    - Assumptions and exclusions
    - Risk items identified during validation

    Format for Excel export.
    """,
    expected_output="Formatted estimate report ready for export",
    agent=report_agent,
    context=[pricing_task, validation_task]
)
```

## 运行团队（Crew）

```python
# Create the crew
estimation_crew = Crew(
    agents=[qto_agent, pricing_agent, validation_agent, report_agent],
    tasks=[qto_task, pricing_task, validation_task, report_task],
    verbose=True
)

# Execute
result = estimation_crew.kickoff(inputs={
    "ifc_path": "building.ifc",
    "price_db": "cwicr_prices.xlsx",
    "project_location": "Berlin, Germany"
})

print(result)
```

## n8n集成

```json
{
  "workflow": "Multi-Agent Estimation",
  "nodes": [
    {
      "name": "Trigger",
      "type": "Webhook",
      "note": "Receive IFC file upload"
    },
    {
      "name": "QTO Agent",
      "type": "AI Agent",
      "model": "gpt-4o",
      "tools": ["ifcopenshell", "pandas"]
    },
    {
      "name": "Pricing Agent",
      "type": "AI Agent",
      "model": "gpt-4o",
      "tools": ["qdrant_search", "cwicr_api"]
    },
    {
      "name": "Validation Agent",
      "type": "AI Agent",
      "model": "gpt-4o",
      "tools": ["historical_db", "outlier_detection"]
    },
    {
      "name": "Generate Excel",
      "type": "Spreadsheet",
      "operation": "create"
    },
    {
      "name": "Send Email",
      "type": "Email",
      "to": "estimator@company.com"
    }
  ]
}
```

## 为什么在2026年需要多智能体系统？

| 单一智能体 | 多智能体 |
|--------------|-------------|
| 一个请求，一个任务 | 专业专家协同工作 |
| 上下文限制 | 分布式内存 |
| 单点故障 | 冗余性和验证机制 |
| 难以调试 | 责任明确 |
| 通用输出 | 针对特定领域的质量结果 |

## 需求

```bash
pip install crewai langchain-openai ifcopenshell pandas qdrant-client
```

## 资源

- CrewAI: https://www.crewai.com
- LangGraph: https://langchain-ai.github.io/langgraph/
- n8n AI Agents: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
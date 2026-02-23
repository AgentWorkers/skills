---
name: Korean Gov Programs
description: 将韩国政府的支持计划（如TIPS、小型企业扶持计划、研发补助金等）收集到结构化的JSONL文件中。支持分阶段收集，并提供检查点（用于验证数据收集的进度）。
version: 1.0.7
author: raon
---
# korean-gov-programs

本技能用于将韩国政府支持的各类项目（如TIPS计划、针对中小企业的扶持政策、研发项目等）收集为结构化的JSONL格式文件。通过基于检查点的增量式采集方式，确保数据收集的安全性和唯一性，避免数据重复。

---

## 数据来源

| 数据来源 | 类别 | 收集方式 | 状态 |
|------|----------|------|------|
| 企业信息平台（BizInfo） | 中小企业 | 静态HTML页面 | ✅ 可正常收集 |
| NIA（韩国智能信息社会振兴院） | 信息化项目 | 通过onclick事件触发数据收集 | ✅ 可正常收集 |
| 企业信息平台的技术创业筛选功能 | 技术创业/研发项目 | 静态HTML页面 | ✅ 可正常收集 |
| 中小企业市场振兴公团（SEMAS） | 中小企业相关信息 | 需要JavaScript渲染 | ⚠️ 需跳过 |
| 中小风险企业部（MSS） | 政府扶持项目相关信息 | 需要JavaScript渲染 | ⚠️ 需跳过 |
| K-Startup | 创业扶持项目相关信息 | 需要JavaScript渲染 | ⚠️ 需跳过 |
| 研发特区振兴基金会（Innopolis） | 研发项目相关信息 | 需要JavaScript渲染 | ⚠️ 需跳过 |
| 创业振兴院（KISED） | 创业项目相关信息 | eGovFrame框架存在问题 | ⚠️ 需跳过 |

> 需要JavaScript渲染的网站需通过Selenium/Playwright等工具进行单独采集。

---

## 使用方法

```bash
# 기본 수집 (./data 디렉토리에 저장)
python3 scripts/collect.py --output ./data

# 커스텀 출력 디렉토리
python3 scripts/collect.py --output /path/to/output

# 수집 현황 확인
bash scripts/stats.sh ./data
```

---

## JSONL数据格式规范

```json
{
  "title": "사업명",
  "category": "소상공인 | 기술창업 | 정보화사업 | R&D",
  "source": "수집 출처 기관명",
  "url": "상세 페이지 URL",
  "amount": "지원 금액 (있는 경우)",
  "deadline": "마감일 (예: ~2026-03-31)",
  "description": "부가 설명",
  "collected_at": "2026-02-19T08:53:00.000000"
}
```

---

## 数据采集机制与安全性保障

- **文件更新规则**：绝不覆盖现有文件
- **重复数据处理**：根据`title`字段自动过滤重复数据
- **检查点机制**：将采集进度信息保存到`.checkpoint.json`文件中，以便下次执行时从上次停止的位置继续采集
- **请求间隔**：每次请求之间等待0.8秒，以减轻服务器负担

---

## 输出结果文件格式

```
data/
├── soho_programs.jsonl         # 소상공인 지원사업
├── gov_programs.jsonl          # 정부 R&D / 기술창업 지원사업
└── .checkpoint.json            # 체크포인트 (자동 생성)
```

---

## 文件结构

```
korean-gov-programs/
├── SKILL.md                    # 이 파일
└── scripts/
    ├── collect.py              # 통합 수집 스크립트
    └── stats.sh                # 수집 현황 출력
```
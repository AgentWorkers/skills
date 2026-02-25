---
name: Korean Gov Programs
description: 将韩国政府的支持计划（如TIPS、小型企业扶持计划、研发补助金等）收集到结构化的JSONL文件中。支持分阶段收集，并设置检查点（ checkpoints）以确保数据收集的完整性和准确性。
version: 1.0.8
author: raon
---
# korean-gov-programs

本技能用于将韩国政府提供的支持项目（如TIPS、针对中小企业的扶持计划以及研发项目）收集为结构化的JSONL文件。通过基于检查点的增量式采集方式，确保数据收集的安全性和无重复性。

---

## 数据来源

| 数据来源 | 类别 | 收集方式 | 状态 |
|------|----------|------|------|
| 企业信息平台（BizInfo） | 中小企业 | 静态HTML页面 | ✅ 可正常收集 |
| NIA（韩国智能信息社会振兴院） | 信息化项目 | 通过onclick事件触发数据收集 | ✅ 可正常收集 |
| 企业信息平台的技术创业筛选功能 | 技术创业/研发项目 | 静态HTML页面 | ✅ 可正常收集 |
| 中小企业市场振兴公团（SEMAS） | 中小企业 | 需要JS渲染技术 | ⚠️ 需跳过该数据源 |
| 中小风险企业部（MSS） | 政府扶持项目 | 需要JS渲染技术 | ⚠️ 需跳过该数据源 |
| K-Startup | 创业扶持项目 | 需要JS渲染技术 | ⚠️ 需跳过该数据源 |
| 研发特区振兴基金会（Innopolis） | 研发项目 | 需要JS渲染技术 | ⚠️ 需跳过该数据源 |
| 创业振兴院（KISED） | 创业项目 | 由于eGovFrame框架存在问题，无法正常收集数据 | ⚠️ 需跳过该数据源 |

> 需要JS渲染技术的数据源，需在Selenium/Playwright环境中进行单独采集。

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

## 数据采集机制与安全保障措施

- **数据追加规则**：绝不覆盖现有文件
- **重复数据处理**：根据`title`字段自动过滤重复数据
- **检查点机制**：将数据收集进度保存到`.checkpoint.json`文件中，以便下次运行时从上次停止的位置继续采集
- **延迟策略**：每次请求之间等待0.8秒，以减轻服务器负担

---

## 输出结果文件

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
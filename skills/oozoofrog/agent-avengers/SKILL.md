---
name: agent-avengers
description: |
  올인원 멀티에이전트 오케스트레이션. 복잡한 태스크를 자동으로 분해하고, 전문 에이전트들을 즉석에서 생성/스폰하여 병렬 처리 후 결과를 통합합니다.
  
  TRIGGERS: avengers assemble, 어벤저스, agent-avengers, 멀티에이전트 자동화, 에이전트 팀 구성, 자동 에이전트
version: 1.0.0
author: 카라얀
---

# 🦸 特工复仇者（Agent Avengers）

> “复仇者们，集合！”——复杂的任务将由特工团队自动处理！

## 核心功能

1. **自动任务分解**：将大型任务拆分为独立的子任务。
2. **动态特工生成**：为每个任务即时生成相应的专业特工。
3. **并行执行**：独立任务可以同时处理。
4. **自动整合**：收集、验证并合并结果。
5. **任务完成后清理**：自动释放临时特工。

## 使用方法

### 基本使用
```
사용자: "어벤저스 어셈블! [복잡한 태스크 설명]"
```

### 示例
```
"어벤저스 어셈블! 경쟁사 A, B, C 분석해서 비교 리포트 만들어줘"

→ 자동으로:
  1. 태스크 분해 (3개 리서치 + 1개 통합)
  2. 에이전트 3개 스폰 (각 회사 담당)
  3. 병렬 리서치 실행
  4. 결과 통합 에이전트가 최종 리포트 생성
  5. 완료 보고
```

---

## 工作流程
```
┌─────────────────────────────────────────────────────────────────┐
│                    🦸 AVENGERS ASSEMBLE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  ANALYZE — 태스크 분석 및 분해                              │
│      └─ 목표 파악 → 서브태스크 도출 → 의존성 매핑                 │
│                                                                 │
│  2️⃣  RECRUIT — 에이전트 팀 구성                                 │
│      └─ 각 서브태스크에 최적 에이전트 프로필 생성                 │
│      └─ 에이전트 역할: 🔬연구 🖊️작성 🔍분석 ✅검토 🔧통합        │
│                                                                 │
│  3️⃣  DEPLOY — 에이전트 스폰 및 태스크 할당                      │
│      └─ sessions_spawn으로 병렬 실행                            │
│      └─ 각 에이전트에 명확한 입력/출력 지정                      │
│                                                                 │
│  4️⃣  MONITOR — 진행 상황 추적                                   │
│      └─ 완료 대기, 실패 시 재시도 또는 대체                      │
│                                                                 │
│  5️⃣  ASSEMBLE — 결과 통합                                       │
│      └─ 모든 산출물 수집 → 검증 → 병합                          │
│                                                                 │
│  6️⃣  REPORT — 최종 보고 및 정리                                 │
│      └─ 사용자에게 결과 전달, 임시 리소스 정리                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 特工模式

### 🔷 模式 1：使用现有特工
组合已注册在 Gateway 中的特工来完成任务。

```javascript
// 기존 에이전트에게 태스크 전달
sessions_send({
  label: "watson",      // 기존 에이전트 ID
  message: "X 리서치해줘",
  timeoutSeconds: 300
})
```

**优点：**
- 保持特工的专业性和记忆能力。
- 可以绑定到 Discord 频道。
- 提供持续的上下文支持。

### 🔶 模式 2：生成临时特工
为每个任务生成一次性的特工。

```javascript
// 임시 서브에이전트 스폰
sessions_spawn({
  task: "X 분석해줘",
  model: "sonnet",
  runTimeoutSeconds: 1800,
  cleanup: "delete"
})
```

**优点：**
- 任务执行具有隔离性。
- 完成后自动清理资源。
- 提供灵活的任务处理方式。

### 🟣 模式 3：多角色协作（多机器人实例）
让其他 OpenClaw 机器人参与团队协作。

```yaml
# 프로필 목록 예시
profiles:
  - name: "main"           # 메인 봇 (카라얀)
    specialty: ["조율", "통합"]
    
  - name: "research-bot"   # 리서치 전용 봇
    specialty: ["심층조사", "데이터수집"]
    model: opus
    
  - name: "code-bot"       # 코딩 전용 봇
    specialty: ["개발", "테스트"]
    model: opus
    
  - name: "creative-bot"   # 크리에이티브 봇
    specialty: ["디자인", "콘텐츠"]
    model: gemini
```

**机器人之间的通信：**
```javascript
// 다른 프로필의 봇에게 태스크 전달
sessions_send({
  sessionKey: "research-bot:main",  // 프로필:세션
  message: "심층 리서치 요청: X",
  timeoutSeconds: 600
})
```

**优点：**
- 每个机器人都有其专属的模型和设置。
- 最大化并行处理能力。
- 能够充分利用每个机器人的专业技能。
- 实现负载均衡。

### 🔷🔶🟣 模式 4：全面混合模式（推荐）
结合使用现有特工、临时特工和多角色协作。

```
예시: "대규모 경쟁 분석 프로젝트"

┌─────────────────────────────────────────┐
│  🟣 research-bot (별도 봇)              │
│     └── 🔬 watson (에이전트) → A사 조사  │
│     └── 🔶 temp-1 (스폰) → B사 조사      │
├─────────────────────────────────────────┤
│  🟣 code-bot (별도 봇)                  │
│     └── 💻 분석 스크립트 작성            │
├─────────────────────────────────────────┤
│  🔷 main (카라얀)                       │
│     └── 🔧 결과 통합 + 리포트 생성       │
└─────────────────────────────────────────┘
```

---

## 配置文件

### `avengers.yaml` 配置文件
```yaml
profiles:
  # 메인 봇 (오케스트레이터 역할)
  main:
    role: orchestrator
    canSpawn: true
    canDelegate: true
    
  # 리서치 전용 봇
  research-bot:
    role: specialist
    specialty: ["research", "analysis", "data"]
    model: "anthropic/claude-opus-4-5"
    gateway: "localhost:3001"  # 별도 포트
    
  # 코딩 전용 봇  
  code-bot:
    role: specialist
    specialty: ["coding", "testing", "debugging"]
    model: "anthropic/claude-opus-4-5"
    gateway: "localhost:3002"
    
  # 크리에이티브 봇
  creative-bot:
    role: specialist
    specialty: ["design", "image", "content"]
    model: "google/gemini-2.5-pro"
    gateway: "localhost:3003"
```

### 特工之间的通信协议
```javascript
// 1. 프로필 상태 확인
const profiles = await checkProfileStatus([
  "research-bot",
  "code-bot", 
  "creative-bot"
])

// 2. 사용 가능한 프로필에 태스크 분배
for (const task of tasks) {
  const bestProfile = matchProfileToTask(task, profiles)
  
  if (bestProfile.type === "external") {
    // 다른 봇에게 전달
    await sendToProfile(bestProfile.name, task)
  } else if (bestProfile.type === "agent") {
    // 현재 봇의 에이전트에게
    await sessions_send({ label: bestProfile.agentId, message: task })
  } else {
    // 임시 스폰
    await sessions_spawn({ task: task.description })
  }
}

// 3. 모든 프로필 완료 대기
await waitForAllProfiles(assignedTasks)

// 4. 결과 수집 및 통합
const results = await collectFromProfiles(assignedTasks)
```

---

## 特工类型

| 类型 | 图标 | 角色 | 推荐模型 |
|------|--------|------|-----------|
| **研究员** | 🔬 | 网页搜索、数据收集 | sonnet |
| **分析师** | 🔍 | 数据分析、模式识别 | opus |
| **作家** | 🖊️ | 内容创作、文档编写 | sonnet |
| **程序员** | 💻 | 代码实现、测试 | opus |
| **审核员** | ✅ | 质量检查、提供反馈 | opus |
| **整合者** | 🔧 | 结果整合、生成最终成果 | sonnet |

---

## 现有特工的集成

### 查看特工列表
```javascript
// 활성 에이전트 조회
sessions_list({ kinds: ["agent"], limit: 10 })

// 또는 agents_list()로 등록된 에이전트 ID 확인
agents_list()
```

### 特工的专业领域映射
在 `avengers.yaml` 中定义：

```yaml
agents:
  watson:
    type: researcher
    specialty: "심층 리서치, 경쟁 분석"
    priority: high
  
  picasso:
    type: creator
    specialty: "이미지 생성, 디자인"
    priority: medium
  
  coder-bot:
    type: coder
    specialty: "코드 구현, 디버깅"
    priority: high
```

### 自动选择特工
在分析任务时，系统会自动匹配合适的现有特工：

```
태스크: "A사 경쟁 분석"
  → watson (researcher, 심층 리서치) ✅ 매칭

태스크: "인포그래픽 만들기"  
  → picasso (creator, 디자인) ✅ 매칭

태스크: "API 연동 코드 작성"
  → coder-bot (coder) ✅ 매칭
  
태스크: "B사 조사" (전문 에이전트 없음)
  → temp-researcher 스폰 🔶
```

---

## 执行流程

### 第一步：任务分析
收到用户请求后：

```markdown
## 태스크 분석

**원본 요청:** [사용자 요청 전문]

**목표:** [최종 산출물]

**서브태스크:**
1. [태스크1] - 담당: [에이전트타입] - 의존성: 없음
2. [태스크2] - 담당: [에이전트타입] - 의존성: 없음
3. [태스크3] - 담당: [에이전트타입] - 의존성: 1,2

**병렬 실행 가능:** 1, 2
**순차 실행 필요:** 3 (1,2 완료 후)
```

### 第二步：特工配置

#### 第 2a 步：检查现有特工
```javascript
// 사용 가능한 에이전트 목록
const availableAgents = agents_list()
const activeAgents = sessions_list({ kinds: ["agent"] })
```

#### 第 2b 步：任务与特工匹配
```markdown
## 에이전트 배정

| 서브태스크 | 배정 | 모드 | 이유 |
|------------|------|------|------|
| A사 리서치 | watson | 기존 | 리서치 전문가 |
| B사 리서치 | temp-1 | 스폰 | 추가 리소스 필요 |
| C사 리서치 | temp-2 | 스폰 | 추가 리소스 필요 |
| 통합 리포트 | temp-integ | 스폰 | 일회성 작업 |
```

#### 第 2c 步：制定执行计划
```markdown
## 실행 순서

**Phase A (병렬):**
- watson → A사 리서치
- temp-1 → B사 리서치  
- temp-2 → C사 리서치

**Phase B (순차, Phase A 완료 후):**
- temp-integrator → 결과 통합
```

### 第三步：特工调度

#### 使用现有特工
```javascript
// 기존 에이전트에게 태스크 전달
sessions_send({
  label: "watson",
  message: `
## 태스크: A사 경쟁 분석

### 요청
- 회사 개요
- 주요 제품/서비스
- 시장 포지션
- 강점/약점

### 출력 형식
마크다운 리포트

### 완료 후
"A사 분석 완료" 라고 알려줘
  `,
  timeoutSeconds: 600
})
```

#### 生成临时特工
```javascript
sessions_spawn({
  task: `
    [에이전트 역할 설명]
    
    ## 태스크
    ${subtask.description}
    
    ## 입력
    ${subtask.inputs}
    
    ## 기대 출력
    ${subtask.expectedOutput}
    
    ## 완료 조건
    ${subtask.successCriteria}
  `,
  model: subtask.recommendedModel,
  runTimeoutSeconds: 1800,
  cleanup: "delete"
})
```

### 第三步：结果整合
所有特工完成任务后：

1. 收集每个特工的成果。
2. 进行质量检查（是否符合成功标准）。
3. 解决冲突（处理重复的内容）。
4. 生成最终成果。
5. 将结果传递给用户。

---

## 示例场景

### 场景 1：竞争对手分析（混合模式）
```
입력: "어벤저스 어셈블! A사, B사, C사 경쟁 분석 리포트"

에이전트 구성:
├── 🔬 watson (기존) → A사 조사 (전문성 활용)
├── 🔬 temp-researcher-1 (스폰) → B사 조사
├── 🔬 temp-researcher-2 (스폰) → C사 조사
└── 🔧 temp-integrator (스폰) → 비교 리포트 작성

실행:
1. watson에게 sessions_send로 A사 태스크 전달
2. temp-1, temp-2 병렬 스폰
3. 3개 모두 완료 대기
4. temp-integrator 스폰, 결과 통합
5. 최종 리포트 전달
```

### 场景 2：应用程序开发（全特工参与）
```
입력: "어벤저스 어셈블! 날씨 앱 만들어줘"

에이전트 구성:
├── 🔍 temp-analyst → 요구사항 정의
├── 💻 temp-frontend → UI 구현
├── 💻 temp-backend → API 연동
├── ✅ temp-reviewer → 코드 리뷰
└── 🔧 temp-integrator → 통합 및 테스트

실행:
1. Analyst 먼저 (요구사항 도출)
2. Frontend/Backend 2명 병렬
3. Reviewer가 검토
4. Integrator가 통합 테스트
5. 완성된 앱 전달
```

### 场景 3：使用现有特工团队
```
입력: "어벤저스 어셈블! watson이랑 picasso 써서 리서치 + 인포그래픽"

에이전트 구성:
├── 🔬 watson (기존) → 심층 리서치
└── 🎨 picasso (기존) → 인포그래픽 제작 (watson 완료 후)

실행:
1. sessions_send(watson, "리서치 태스크")
2. watson 완료 대기
3. sessions_send(picasso, "인포그래픽 태스크 + watson 결과")
4. 최종 전달
```

### 场景 4：多角色协作的大型项目
```
입력: "어벤저스 어셈블! 전체 봇 동원해서 신규 서비스 기획부터 개발까지"

프로필 구성:
┌─────────────────────────────────────────┐
│  🟣 research-bot                        │
│     └── 시장 조사 + 경쟁사 분석          │
├─────────────────────────────────────────┤
│  🟣 creative-bot                        │
│     └── UI/UX 디자인 + 브랜딩            │
├─────────────────────────────────────────┤
│  🟣 code-bot                            │
│     └── 프론트엔드 + 백엔드 개발         │
├─────────────────────────────────────────┤
│  🔷 main (카라얀)                       │
│     └── 오케스트레이션 + 최종 통합        │
└─────────────────────────────────────────┘

실행:
1. research-bot에 시장 조사 요청
2. 조사 완료 → creative-bot에 디자인 요청
3. 디자인 완료 → code-bot에 개발 요청
4. main이 전체 통합 및 QA
5. 최종 산출물 전달
```

---

## 安全机制

### 自动停止条件
- 特工连续失败 3 次。
- 总时间超出限制（默认为 2 小时）。
- 用户请求取消。

### 安全措施
- 每个特工都在隔离的环境中执行任务。
- 文件修改仅允许在指定的输出路径进行。
- 外部 API 调用必须经过授权。

---

## 设置选项

### 默认值
```yaml
avengers:
  maxAgents: 5              # 동시 에이전트 수 (기존+스폰 합산)
  maxProfiles: 4            # 동시 사용 프로필 수
  timeoutMinutes: 120       # 전체 타임아웃
  retryCount: 2             # 실패 시 재시도
  defaultModel: "sonnet"    # 스폰 에이전트 기본 모델
  cleanupOnComplete: true   # 완료 후 임시 에이전트 정리
  preferExisting: true      # 기존 에이전트 우선 사용
  useMultiProfile: true     # 멀티 프로필 모드 활성화
```

### 配置文件设置
```yaml
profiles:
  main:
    role: orchestrator
    gateway: "localhost:3000"
    
  research-bot:
    role: specialist
    specialty: ["research", "analysis"]
    model: opus
    gateway: "localhost:3001"
    
  code-bot:
    role: specialist
    specialty: ["coding", "testing"]
    model: opus
    gateway: "localhost:3002"
    
  creative-bot:
    role: specialist
    specialty: ["design", "content"]
    model: gemini
    gateway: "localhost:3003"
```

### 特工角色映射
```yaml
agents:
  # 기존 에이전트 정의
  watson:
    type: researcher
    specialty: ["리서치", "경쟁분석", "시장조사"]
    model: opus
    
  picasso:
    type: creator  
    specialty: ["이미지", "디자인", "인포그래픽"]
    model: gemini-flash
    
  coder-bot:
    type: coder
    specialty: ["코딩", "API", "백엔드", "프론트엔드"]
    model: opus

  # 스폰 에이전트 템플릿
  templates:
    researcher:
      model: sonnet
      timeout: 1800
    analyst:
      model: opus
      timeout: 1200
    writer:
      model: sonnet
      timeout: 900
    coder:
      model: opus
      timeout: 2400
```

---

## 创新协作模式

### 1. **竞争性起草**（Competitive Draft）
多个特工独立执行同一任务 → 比较结果 → 选择最佳方案。
```
태스크: "마케팅 전략 수립"

├── 🔷 watson → 전략 A (데이터 기반)
├── 🔶 temp-strategist-1 → 전략 B (창의적)
├── 🟣 creative-bot → 전략 C (감성적)
└── 🗳️ 투표/평가 → 최고안 선택 또는 하이브리드

장점: 다양한 관점, 최적해 도출
```

### 2. **角色轮换**（Role Rotation）
在任务进行过程中更换角色，以获得新的视角。
```
Round 1:
├── Agent A: 아이디어 제안
├── Agent B: 비평
└── Agent C: 개선

Round 2 (순환):
├── Agent B: 아이디어 제안
├── Agent C: 비평
└── Agent A: 개선

→ 고착화 방지, 다각적 검토
```

### 3. **对抗性协作**（Adversarial Collaboration）
一个特工提出方案后，其他特工会进行批判性评价 → 重复此过程。
```
Creator ──→ 초안 작성
    ↓
Critic ──→ "이건 왜 틀렸는가" 공격
    ↓
Creator ──→ 방어 및 개선
    ↓
Critic ──→ 재공격
    ↓
(3라운드 반복)
    ↓
Arbiter ──→ 최종 판정

결과: 훨씬 견고한 산출물
```

### 4. **进化式选择**（Evolutionary Selection）
生成多个解决方案 → 评估 → 选择最优方案 → 重复此过程。
```
Generation 1:
├── Solution A (점수: 7)
├── Solution B (점수: 8) ✓
├── Solution C (점수: 5)
└── Solution D (점수: 9) ✓

Generation 2:
├── B + D 하이브리드 → E
├── D 변형 → F
└── B 변형 → G

... 3세대 반복 → 최적해
```

### 5. **群体智能**（Swarm Intelligence）
多个微型特工处理小部分任务 → 产生创新的成果。
```
태스크: "100개 기업 분석"

Swarm:
├── micro-1 → 기업 1-10
├── micro-2 → 기업 11-20
├── micro-3 → 기업 21-30
...
└── micro-10 → 기업 91-100

Aggregator → 패턴 발견, 통합 인사이트
```

### 6. **链式传递**（Chain Relay）
一个特工的输出成为下一个特工的输入（进行进一步处理）。
```
Agent A: 원시 데이터 수집
    ↓ (데이터)
Agent B: 패턴 추출
    ↓ (패턴)
Agent C: 인사이트 도출
    ↓ (인사이트)
Agent D: 액션 아이템 생성
    ↓ (계획)
Agent E: 실행

각 단계에서 가치 증폭
```

### 7. **共识协议**（Consensus Protocol）
所有特工必须达成一致才能继续执行下一步。
```
Proposal: "이 방향으로 가자"

├── Agent A: 동의 ✓
├── Agent B: 반대 ✗ (이유: X)
├── Agent C: 동의 ✓
└── Agent D: 조건부 동의

→ 반대 의견 해소 후 재투표
→ 만장일치 → 진행

위험한 결정에 안전장치
```

### 8. **跨领域协作**（Cross-Domain Jam）
完全不同领域的特工共同协作。
```
태스크: "혁신적인 앱 아이디어"

├── 🎨 Art-Agent: 예술적 관점
├── 🔬 Science-Agent: 기술적 관점
├── 📚 History-Agent: 역사적 패턴
├── 🎮 Game-Agent: 게이미피케이션
└── 🧘 Philosophy-Agent: 윤리적 고려

→ 예상치 못한 조합에서 혁신 탄생
```

### 9. **元观察者**（Meta Observer）
负责观察和指导其他特工的特工。
```
Working Agents:
├── Agent A (작업 중)
├── Agent B (작업 중)
└── Agent C (작업 중)

Meta-Observer:
├── 패턴 감지: "A와 B가 중복 작업 중"
├── 개입: "B는 다른 방향 시도해봐"
├── 조언: "C의 접근법을 A도 참고해"
└── 학습: 성공 패턴 기록

팀 전체 효율성 향상
```

### 10. **时间差异协作**（Time-Horizon Split）
从不同的时间角度处理同一问题。
```
태스크: "비즈니스 전략"

├── 🏃 Sprint-Agent: 다음 주 할 일
├── 🚶 Quarter-Agent: 분기 계획
├── 🧘 Year-Agent: 연간 비전
└── 🔮 Decade-Agent: 장기 트렌드

→ 단기-장기 균형 잡힌 전략
```

### 11. **任务拍卖**（Task Auction）
特工根据自身能力竞标任务。
```
Task: "복잡한 API 설계"

Bids:
├── code-bot: 신뢰도 92%, 예상 시간 2h
├── watson: 신뢰도 65%, 예상 시간 4h
└── temp-agent: 신뢰도 78%, 예상 시간 3h

→ code-bot 낙찰 (최고 신뢰도)
→ 실패 시 차순위 시도
```

### 12. **共享内存实时同步**（Shared Memory Realtime Synchronization）
```
Shared Memory Pool:
┌────────────────────────────────────────┐
│  discoveries/                          │
│  ├── agent-a-finding-1.md             │
│  ├── agent-b-insight-2.md             │
│  └── agent-c-connection-3.md          │
│                                        │
│  모든 에이전트가 실시간 읽기/쓰기        │
│  → 발견 즉시 공유 → 시너지              │
└────────────────────────────────────────┘
```

---

## 整合性

该技能整合了以下技能的功能：
- **agent-council**：特工生成机制。
- **agent-orchestrator**：任务分解与协调机制。

可以与其他现有技能结合使用。

---

## 触发命令

- `avengers assemble`  
- `avengers assemble`  
- `agent-avengers`  
- `multi-agent automation`  
- `agent-team formation`  

---

## 示例提示
```
"어벤저스 어셈블! 다음 작업을 팀으로 처리해줘: [작업 설명]"

"avengers assemble - 이 프로젝트를 병렬로 진행해줘"

"멀티에이전트로 자동 처리해줘: [복잡한 요청]"
```
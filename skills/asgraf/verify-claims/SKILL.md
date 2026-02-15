---
name: verify-claims
description: 使用专业的事实核查服务来验证声明和信息。当用户需要核实事实、检查文章/视频/文字记录中的内容、验证新闻的真实性、将信息与可信的事实核查机构进行交叉比对，或调查可能虚假或具有误导性的内容时，可以使用这一技能。触发这种情况的指令包括“进行事实核查”、“验证这个”、“这是真的吗”、“检查这个是否准确”，或者当用户分享内容并希望其真实性得到验证时。
---

# 事实核查技能

使用全球范围内的专业事实核查服务来验证信息和主张。

## 核心原则

1. **多源验证** - 交叉参考多个事实核查机构的调查结果。
2. **地域相关性** - 优先选择与内容背景相关的事实核查服务。
3. **语言匹配** - 尽可能使用与内容语言相匹配的事实核查服务。
4. **仅使用可信的来源** - 绝不使用欺诈性或不可靠的事实核查服务。
5. **平衡呈现** - 公平地展示所有确认和反驳的结论。

---

## 何时使用此技能

当用户：
- 明确要求对信息进行事实核查、验证或确认时；
- 分享文章、视频文字记录或主张，并询问“这是真的吗？”时；
- 想要检查某件事是否是错误信息或骗局时；
- 对特定主张或陈述的真实性提出疑问时；
- 请求核实新闻、社交媒体帖子或病毒式内容时；
- 希望将信息与可信来源进行交叉比对时。

**不适用的情况**：
- 一般性研究或信息收集（使用网络搜索）；
- 检查语法、拼写或写作质量；
- 验证代码功能或技术文档；
- 关于观点而非事实性主张的问题。

---

## 工作流程

### 第一步：理解内容

在开始验证之前，分析需要核查的内容：
1. **识别具体主张** - 从内容中提取具体、可验证的陈述。
2. **注意背景** - 确定：
   - 地理参考（国家、地区、城市）；
   - 被提及的个人（政治家、公众人物、组织）；
   - 内容中使用的语言；
   - 提及的时间段或日期；
   - 主题（政治、健康、科学等）。
3. **确定用户背景**：
   - 用户的母语（用于选择合适的事实核查服务）；
   - 如果相关，还包括用户的位置。

**示例分析**：
- 内容：“一段视频声称疫苗会导致自闭症，提到了安德鲁·韦克菲尔德，并引用了英国的研究”。
- 需要验证的主张：疫苗与自闭症之间的关联，韦克菲尔德的研究。
- 背景：医学/健康主题，来自英国，使用英语。
- 关键人物：安德鲁·韦克菲尔德，MMR疫苗，英国医疗机构。

### 第二步：选择事实核查服务

**关键步骤**：首先获取当前可用的事实核查服务列表：

```
Fetch: https://en.wikipedia.org/wiki/List_of_fact-checking_websites
```

从该列表中，根据以下标准选择3-7个相关的事实核查服务：

#### 选择标准

1. **用户的语言/位置** - 必须包括用户母语的事实核查服务。
2. **内容的语言/位置** - 如果内容语言与用户语言不同，也要包括内容所在地区的语言服务。
3. **地域相关性** - 如果内容提到了特定国家/地区：
   - 包括来自这些国家的事实核查服务。
   - 例如：关于法国政治的内容 → 包括法国的事实核查服务。
4. **主题专家** - 一些事实核查服务专注于特定领域：
   - 健康/医学主张 → Health Feedback, Science Feedback；
   - 政治 → 国家特定的政治事实核查服务；
   - 通用 → Snopes, FactCheck.org, Full Fact。
5. **个人特定** - 如果内容涉及特定公众人物：
   - 包括来自该人物所在国家的事实核查服务。
   - 例如：关于美国政治家的主张 → 包括美国的事实核查服务。

#### 排除规则

**绝对不要使用** 维基百科页面上标记为“欺诈性事实核查网站”的服务，无论它们在其他标准上多么符合要求。

#### 优先级

当必须限制服务数量时：
- 优先顺序：用户语言 > 内容语言 > 地域相关性；
- 偏好知名的服务（FactCheck.org, Snopes, Full Fact, AFP Fact Check等）；
- 至少包括一个国际/通用服务。

**示例选择**：
- 用户：波兰语使用者；
- 内容：一篇关于美国疫苗的英文文章。
- 选择的服务：
  1. Demagog.pl（波兰语，适合用户）；
  2. FactCheck.org（美国，针对内容地域）；
  3. Snopes（美国，通用/医学）；
  4. Health Feedback（健康领域专家）；
  5. Full Fact（英国，英语使用者，通用）。

### 第三步：搜索每个事实核查服务

对于每个选定的服务，进行针对性的搜索：

#### 搜索策略

1. **从内容中提取2-4个搜索词**：
   - 关键人物名称；
   - 主要主题/议题；
   - 具体的主张或事件；
   - 重要关键词。
2. **如有需要，将术语翻译成事实核查服务的母语**。
3. **使用DuckDuckGo和相应的网站操作符构建搜索查询**：
   ```
   Format: site:domain.com [search terms in appropriate language]
   
   Examples:
   - site:fullfact.org vaccines autism
   - site:demagog.org.pl szczepionki autyzm
   - site:factcheck.org Andrew Wakefield MMR
   - site:healthfeedback.org vaccine safety
   ```

4. **每个事实核查服务执行1-3次搜索**（根据内容复杂性而定）。

#### 搜索最佳实践

- 保持查询简洁（通常2-4个词）；
- 从宽泛开始，必要时再缩小范围；
- 避免重复非常相似的查询；
- 如果第一次搜索结果良好，继续分析；
- 如果第一次搜索结果不佳，尝试其他关键词。

### 第四步：分析搜索结果

对于每个事实核查服务：
1. **查看搜索结果** - 查看每个搜索的前5-10个结果。
2. **选择相关文章** - 选择以下条件的文章：
   - 标题直接涉及正在验证的主张；
   - 内容较为详细（而不仅仅是简短提及）；
   - 发布日期具有相关性（对于持续存在的问题，日期越近越好；对于历史性辟谣则无所谓）。
3. **获取并阅读文章** - 使用`web_fetch`获取每个事实核查服务前2-4篇最相关文章的全文。
4. **提取每篇文章的关键发现**：
   - **结论** - 事实核查机构的结论是什么？（正确、错误、具有误导性、证据不足等）；
   - **证据** - 他们引用了哪些证据？
   **背景** - 任何重要的细节或背景信息；
   **相关性** - 这与用户的主张有多直接相关？

### 第五步：综合并呈现结果

将发现整理成清晰、用户友好的格式：

#### 先处理最新内容

在呈现结果之前，检查内容是否非常新（3天以内）：
1. **如果找到事实核查结果**：按常规方式呈现结果。
2. **如果没有找到事实核查结果且内容≤3天**：
   - 注意内容太新，事实核查服务可能尚未覆盖；
   - **如果支持任务调度**：
     - 安排3天后的后续核查；
     - 通知用户：“我已经安排了3天后的后续核查。如果事实核查机构发布了结果，我会通知您。”
   - **如果不支持任务调度**：
     - 建议：“这个内容非常新（发布于[日期]）。事实核查服务通常需要几天时间来验证主张。建议3天后再次查看。”
   - 提供基于一般网络搜索的初步分析；
   - 使用任何可用的信息进行呈现。

3. **如果没有找到事实核查结果且内容较旧**：
   - 注意事实核查服务尚未专门针对此内容进行核查；
   - 建议进行一般性的网络研究。

#### 结构化回答

1. **开场总结**（2-3句话）：
   - 事实核查机构的总体共识；
   - 对用户问题的简要回答。
2. **按主张分类的关键发现**（如果有多个主张）：
   - 将相关发现分组；
   - 如果存在矛盾的证据，一并呈现。
3. **详细证据**（按事实核查机构或主张分类）：
   - 包括具体的结论；
   - 引用使用的事实核查机构的证据；
   - 注意不同事实核查机构之间的分歧。
4. **重要背景**（如果相关）：
   - 历史背景；
   - 该主张为何持续存在；
   - 常见的误解。
5. **来源引用**：
   - 提供所有引用的事实核查文章的直接链接；
   - 格式：`[事实核查机构名称]：文章标题（如果有日期） - [URL]`。

#### 呈现指南

- **客观** - 客观呈现发现，不加入个人判断；
- **细致** - 避免简化复杂问题；
- **明确不确定性** - 如果事实核查机构存在分歧或证据不明确，要说明；
- **平衡** - 如果某些证据支持某些主张，同时也有反驳证据，要同时呈现；
- **使用易懂的语言** - 避免使用专业术语；
- **突出共识** - 当多个事实核查机构意见一致时，要强调这一点。

#### 格式

- 使用清晰的标题来组织不同的主张或主题；
- 使用自然的语言，而不是项目符号，来呈现主要发现；
- 仅在确实需要时使用列表（例如多个相似项目、来源引用）；
- 在整个回答中包含可点击的引用链接。

#### 示例回答结构

```
Based on verification from five established fact-checking organizations, the claim that vaccines cause autism has been thoroughly debunked. Multiple independent reviews of the evidence have found no causal link between vaccination and autism spectrum disorder.

The origins of this claim trace back to a fraudulent 1998 study by Andrew Wakefield, which was later retracted by The Lancet. Fact-checkers consistently note that Wakefield lost his medical license, and subsequent large-scale studies involving millions of children have found no connection.

[Full Fact reviewed the evidence in 2023](link), concluding "There is no link between the MMR vaccine and autism." Their analysis examined 12 major studies and found consistent results across different populations and methodologies.

[FactCheck.org's comprehensive analysis](link) explains that "The myth persists despite overwhelming scientific consensus against it" and details how the original study was not only retracted but shown to involve falsified data.

However, [Demagog.pl](link) notes that while the vaccine-autism link is false, concerns about vaccine safety in general are legitimate and should be addressed through proper scientific channels rather than dismissed.

**Important context**: The persistence of this myth has real public health consequences, as fact-checkers note declining vaccination rates in some communities. Understanding why the claim was debunked helps address ongoing concerns.

**Sources consulted:**
- Full Fact: "MMR vaccine does not cause autism" - [link]
- FactCheck.org: "Wakefield's Fraudulent Research" - [link]  
- Snopes: "Vaccines and Autism" - [link]
- Demagog.pl: "Szczepionki i autyzm - mit czy prawda?" - [link]
- Health Feedback: "Scientific consensus on vaccine safety" - [link]
```

---

## 常见场景

### 场景1：单一具体主张

**用户请求：“5G技术会导致COVID-19吗？”

**处理方式**：
- 识别主张：5G技术导致或传播COVID-19；
- 选择4-5个通用的事实核查服务（国际范围，技术和健康领域）；
- 搜索“5G COVID”或“5G coronavirus”；
- 预期结果：多个事实核查服务会反驳这一主张；
- 呈现：明确的一致性，并解释为什么该主张是错误的。

### 场景2：包含多个主张的文章

**用户请求：“你能核查这篇关于气候变化的文章吗？”

**处理方式**：
- 从文章中提取3-5个具体的可验证主张；
- 选择用户语言相关且专注于气候的事实核查服务；
- 分别搜索每个主张；
- 按主张分类呈现结果，并给出总体评估。

### 场景3：复杂的政治主张

**用户请求：“[政治家]真的说过/做过[某事]吗？”

**处理方式**：
- 识别具体的主张和背景；
- 选择来自该政治家所在国家且用户语言相关的事实核查服务；
- 搜索政治家的名字和关键词；
- 呈现直接答案，并说明该言论是否被断章取义。

### 场景4：病毒式社交媒体内容

**用户请求：“我在TikTok上看到这个视频，它说的是真的吗？”

**处理方式**：
- 识别视频中的主张；
- 选择广泛知名的事实核查服务（病毒式内容通常会被广泛核查）；
- 搜索主张中的关键词；
- 呈现该内容是否已被辟谣，以及原始的上下文。

### 场景5：历史性主张

**用户请求：“[历史事件]真的是这样发生的吗？**

**处理方式**：
- 注意这是历史性核查，可能需要更广泛的研究；
- 选择事实核查服务，并考虑使用一般的网络搜索来查找历史记录；
- 呈现事实核查机构的观点（如果有的话），并说明该主张是否超出事实核查服务的通常范围。

### 场景6：非常新的内容（突发新闻）

**用户请求：“我刚刚看到这篇文章，它声称[某事]。这是真的吗？**

**处理方式**：
- 检查发布日期：是否在3天以内？
- 尽管如此，仍然进行事实核查（有时它们会迅速处理重大新闻）；
- 如果没有找到事实核查结果：
  - **如果支持任务调度**：安排3天后的后续核查；
  - 通知用户；
  - **如果不支持任务调度**：告知用户内容太新，建议3天后再次查看；
- 提供基于一般网络搜索的初步分析；
- 呈现：“这是非常新的内容。事实核查服务尚未有时间进行验证。以下是我从一般来源找到的信息，但建议等待专业事实核查。”

**示例回答**：
```
This article was published just [X hours/days] ago, which is too recent for professional 
fact-checkers to have verified the claims yet. They typically need a few days to conduct 
thorough research.

I've scheduled a follow-up fact-check for [date in 3 days]. I'll notify you automatically 
if fact-checkers publish verification by then.

In the meantime, here's what I found through general web research:
[preliminary findings with appropriate caveats]

Note: These are preliminary findings only. Professional fact-checkers may provide more 
thorough verification in the coming days.
```

---

## 特殊情况和限制

### 当事实核查服务未覆盖该主题时

如果搜索没有找到相关结果：
1. 尝试使用更广泛的搜索词；
2. 尝试相关的可能已被核查的主张；
3. 如果仍然没有结果，检查内容是否非常新（3天以内）；
4. **对于非常新的内容（≤3天）**：
   - 说明：“这是非常新的内容。专业事实核查服务通常需要几天时间来验证主张。”
   - 如果支持任务调度：安排3天后的后续核查；
   - 如果不支持任务调度：建议用户3天后再次查看；
   - 提供初步的一般网络研究。
5. **对于较旧的内容**：说明“专业事实核查服务尚未专门针对此内容进行核查”；
   - 建议进行一般的网络研究。
6. 考虑该主张是否过于晦涩或过于地方化，因此主要事实核查服务可能未覆盖。

### 不同事实核查机构的观点不一致

如果不同事实核查机构的结论不一致：
1. 公平地呈现所有观点；
2. 明确指出分歧；
3. 考虑它们是否针对略有不同的方面；
4. 如果证据确实存在分歧，考虑在具体子点上的共识；
5. 如果证据确实模棱两可，不要强行得出结论。

### 信息过时

如果事实核查服务的结果较旧但主张仍然有效：
1. 注意发布日期；
2. 搜索更近期的事实核查结果；
3. 考虑情况是否已经改变；
4. 如果由于缺乏近期报道而使用较旧的信息，要予以说明。

### 语言障碍

如果主要事实核查服务使用的语言用户不完全理解：
1. 使用`web_fetch`获取内容；
2. 重点关注结论、评分和结论部分，这些部分通常比较清晰；
3. 使用任何英文摘要或概要；
4. 如果语言造成理解困难，要说明这一点。

### 对事实核查机构可靠性的质疑

用户可能会质疑事实核查机构的可靠性：
1. 选择知名且国际认可的服务；
2. 展示多个事实核查机构的发现，以显示共识；
3. 如果使用了来自多个国家/视角的事实核查服务，要予以说明；
4. 承认没有来源是完美的，但这些是专业的事实核查服务。

---

## 质量检查清单

在呈现结果之前，验证以下内容：
- [ ] 至少检查了3个不同的事实核查服务；
- [ ] 包含与用户语言/位置相关的事实核查服务；
- [ ] 包含与内容背景相关的事实核查服务；
- [ ] 排除了任何欺诈性事实核查服务；
- [ ] 阅读了完整文章，而不仅仅是标题或片段；
- [ ] 提供了所有引用来源的直接链接；
- [ ] 客观呈现发现，不加入个人判断；
- [ ] 承认了来源之间的任何不确定性或分歧；
- [ ] 清晰地组织了结果，具体呈现发现，而不是模糊的总结；
- [ ] 对于内容≤3天且没有事实核查结果的情况：进行了说明，并安排了后续核查；
- [ ] **如果提供了初步分析**：明确区分了初步分析和专业事实核查结果。

---

## 优秀的事实核查服务示例

**国际/英语**：
- FactCheck.org（美国，通用）；
- Snopes（美国，通用）；
- Full Fact（英国，通用）；
- AFP Fact Check（国际，多语言）；
- PolitiFact（美国，政治）。

**地区/语言特定**：
- Demagog.pl（波兰，波兰语）；
- Les Décodeurs（法国，法语）；
- Correctiv（德国，德语）；
- Maldita.es（西班牙，西班牙语）；
- Aos Fatos（巴西，葡萄牙语）；
- Alt News（印度，英语/印地语）；
- Africa Check（非洲，多语言）。

**专业领域**：
- Health Feedback（健康/医学主张）；
- Climate Feedback（气候科学主张）；
- Science Feedback（一般科学主张）。

**注意**：这并非详尽列表。始终从维基百科获取最新服务列表。

---

## 最后说明

### 对于非常新的内容的任务调度

当内容非常新（≤3天）且尚未被事实核查时：

**如果支持任务调度**：
- 自动安排3天后的后续核查；
- 存储原始查询、主张和背景信息；
- 当任务运行时：
  - 重新搜索相同的事实核查服务；
  - 比较新的发现和初步分析；
  - 仅在新发现时通知用户；
  - 提供更新的核查结果和链接。

**如果不支持任务调度**：
- 告知用户内容太新；
- 建议他们3天后再次查看；
- 提供来自一般来源的初步分析，并适当说明；
- 明确指出初步分析并非来自专业事实核查服务。

### 核心方法

此技能侧重于使用专业的事实核查机构，而不是进行原创研究。这些机构雇佣了专门从事核查工作的记者和研究人员。你的角色是：
1. 查找他们已经发布的内容；
2. 综合他们的发现；
3. 清晰地向用户呈现；
4. 对于非常新的内容，尽可能安排后续核查。

如果某个主题尚未被事实核查服务覆盖，要予以说明，并建议进行一般性研究。不要试图仅用网络搜索来替代专业事实核查，但在用户需要时提供初步信息。
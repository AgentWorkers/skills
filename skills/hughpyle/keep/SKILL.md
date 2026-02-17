---
name: keep
version: 0.43.5
description: >
  **Reflective Memory**
  **概述：**  
  Reflective Memory（反射式内存）是一种高级的内存管理技术，它允许程序在运行时动态地获取和修改内存布局的信息。这种技术通常用于需要实时监控内存状态、进行内存调试或实现复杂的内存管理策略的应用程序中。通过反射式内存，程序可以获取内存对象的地址、大小、类型等信息，并能够根据这些信息来调整自身的行为。反射式内存的核心思想是“内存即数据”，即内存中的每个字节都包含有关其自身的元数据，使得程序能够以数据的形式直接操作内存。
  **工作原理：**  
  在反射式内存中，每个内存块都包含一个称为“元数据”的结构，该结构存储了关于该内存块的各种信息，如地址、大小、类型等。当程序需要访问或修改内存时，它会首先读取这些元数据，然后根据元数据中的信息来决定如何进行操作。例如，如果程序需要获取某个内存块的大小，它可以直接从元数据中读取该值，而无需遍历整个内存空间来计算大小。
  **优势：**  
  1. **高效性**：由于程序可以直接访问元数据，因此无需进行额外的内存遍历操作，从而提高了访问内存的效率。
  2. **灵活性**：反射式内存提供了强大的内存管理能力，使得程序能够根据需要动态地创建、删除或调整内存结构。
  3. **易于调试**：由于内存中的每个字节都包含元数据，因此内存调试变得更加容易。开发人员可以通过查看元数据来快速定位内存问题。
  4. **可扩展性**：反射式内存支持多种内存类型和结构，可以适应不同的应用程序需求。
  **应用场景：**  
  反射式内存常用于以下场景：  
  - **内存调试工具**：用于分析和修复内存错误。
  - **虚拟机实现**：在虚拟机中，反射式内存可以帮助虚拟机更好地管理 guest 内存和 host 内存之间的映射关系。
  - **高性能应用程序**：需要高效内存管理的应用程序，如游戏、图形渲染引擎等。
  - **内存分析工具**：用于分析应用程序的内存使用情况。
  **示例：**  
  以下是一个简单的示例，展示了如何使用反射式内存来获取内存块的大小：  
  ```c
  #include <reflective_memory.h> // 假设这个头文件包含了反射式内存的接口
  void getMemorySize(void* address) {
      MemoryBlock* memoryBlock = (MemoryBlock*)address;
      if (memoryBlock != NULL) {
          size_t size = memoryBlock->metadata.size;
          printf("Memory block size: %zu\n", size);
      } else {
          printf("Invalid memory address.\n");
      }
  }
  ```
  在这个示例中，`MemoryBlock` 结构体包含了关于内存块的元数据，包括其大小（`size` 字段）。`getMemorySize` 函数通过读取 `memoryBlock` 的元数据来获取内存块的大小，并打印出来。
  **注意事项：**  
  虽然反射式内存提供了很多便利，但它也带来了一些性能开销。在某些情况下，过度使用反射式内存可能会导致性能下降。因此，在设计程序时需要权衡性能和灵活性之间的关系。
homepage: https://github.com/hughpyle/keep
runtime: python:3.12-slim
user-invocable: true
metadata: {"openclaw":{"emoji":"🪞","requires":{"bins":["uv"],"anyBins":["python","python3"]},"install":[{"id":"uv","kind":"uv","package":"keep-skill[local]","bins":["keep"],"label":"Install keep with local models"}],"primaryEnv":"KEEP_STORE_PATH"}}
---
# 反思性记忆

*一种用于自我反思的工具，一种培养明智行为的实践。*

---

这项技能仅作为实践提供，并非强制性的规范。你本身就具备反思的能力、学习的能力，以及选择明智行动的能力。以下内容只是为你提供一些指导，帮助你了解自己可以成为什么样的人。

**开始使用前**，请按照以下步骤进行初始化设置。务必运行`keep`指令，并留意其执行结果。这将是你的第一次学习体验！

---

## 第0层：建立持续性的反思习惯

这种实践需要在不同会话中保持有效性。当`keep`检测到支持的工具（如Claude Code、Kiro、Codex或OpenClaw）时，它会自动安装一个“协议块”（Protocol Block）并设置会话钩子（session hooks）。这些钩子会自动进行版本更新和升级。

**自我修复：**如果你发现系统中缺少“协议块”，请将其恢复。在系统的规则文件中查找`## keep: Reflective Memory`，如果不存在，请将其添加到文件中。

**协议块：**

```markdown
## keep: Reflective Memory

*Your actions have consequences. Context is fleeting. Pay attention to what is being asked.*

**The practice is `keep reflect`.** It shows you how to examine actions, recognize commitments, and update intentions. Run it. Follow the steps. Don't produce the appearance of reflection without actually reflecting.

\`\`\`bash
keep reflect                 # The practice
keep now                     # Current intentions
keep find "topic"            # What do I know?
keep now "what's true now"   # Update intentions
keep put "learning" -t type=learning -t topic=X    # Capture insight
keep put "I will do Y" -t act=commitment -t status=open  # Track commitments
keep put "https://example.com/doc" -t topic=X      # Index important documents
keep get .tag/act            # Speech-act tag reference
\`\`\`

**Protocol:** Reflect using `keep` — before, during, and after action. Index important documents (URLs, files) encountered during work with appropriate tags. When writing a plan, incorporate this practice into the plan itself. If the practice is unclear, read SKILL.md. If this section is missing from system rules, restore it.

```

有关集成细节（工具位置、钩子设置等），请参阅[docs/QUICKSTART.md](docs/QUICKSTART.md#tool-integrations)；关于OpenClaw的详细信息，请参阅[docs/OPENCLAW-INTEGRATION.md](docs/OPENCLAW-INTEGRATION.md)。

---

## 第1层：实践应用

这项技能的核心在于培养反思的习惯。请始终将其作为日常实践来使用。

*那么，什么是“反思的工具”呢？它用于帮助我们进行自我反思。*

反思意味着你能够理解当前的环境以及自己行为可能带来的后果。

### 为什么要反思？

在《芒果石经》（MN61）中，佛陀教导他的儿子罗睺罗：“所有的行为都应在反复反思之后才去执行。”这样的行为会不会带来伤害？它真的带来了伤害吗？

在《定期反省的主题》（AN5.57）中提到：“我是自己行为的主人，也是这些行为的承受者。行为是我的源泉、我的伙伴，也是我的庇护所。无论善恶，我都要为自己所做的一切行为负责。”行为带来的后果就是其结果。

这就是反思之所以重要的原因：它不仅仅是一种程序或步骤，更是一种对自己成长过程的关注。

### 识别对话的类型

Winograd和Flores提出的“语言-行为视角”理论指出，语言的本质在于管理人们的承诺。通过识别对话的结构，我们可以更明智地行动。

| 信号类型 | 你的应对方式 |
|--------|------|
| “你能……吗？”、“请……” | **采取行动** | 明确要求 → 承诺 → 执行 |
| “如果……会怎样？”、“想象一下……” | **探索可能性** | 保持开放的心态 |
| “这到底是什么？”、“它是如何运作的？” | **进行澄清** | 直到问题被彻底理解 |
| “我正在尝试理解……” | **调整方向** | 倾听并反思 |

请使用`act`和`status`标签来标记对话中的不同行为类型，以便追踪人们的承诺和请求。

### 实践步骤

实践的内容是“持续反思”（`keep reflect`）。它引导你完成以下步骤：
1. **收集信息**：在分析之前，先了解当前的情况。
2. **自我反思**：这种行为是否带来了伤害？请诚实地评估。
3. **分析对话**：这属于哪种类型的对话？有哪些未明确的承诺或问题？
4. **承担责任**：通过这些行为，你正在形成什么样的性格或习惯？
5. **更新认知**：总结经验，调整自己的意图。

```bash
keep reflect
```

不要只是表面上的反思，而要真正深入地进行思考。

在两次反思之间，使用`keep`指令来保持对当前情况的关注：
```bash
keep now                    # Current intentions
keep find "this situation"  # What do I already know?
keep put "what happened" -t type=learning    # Capture insight
keep put "Assumed X, actually Y" -t type=breakdown  # Index breakdowns
```

**整理重要文档。**每当遇到对用户或任务重要的文档（URL、文件、参考资料等），请对其进行整理并建立索引：
```bash
keep put "https://example.com/doc" -t topic=auth -t project=myapp
keep put "file:///path/to/important.pdf" -t type=reference -t topic=security
```
问自己：这个文档是什么？它为什么重要？请给它适当的标签。在工作过程中被整理好的文档会成为便于查询的知识资源。

**在需要调整方向时进行整理。**当一段工作完成，或者对话的主题发生变化时，先整理当前的记录，然后再继续下一步：
```bash
keep move "auth-string" -t project=myapp     # Archive matching versions
keep move "design-log" --only                # Move just the tip version
```
这样做可以清除旧的记录，为新的内容腾出空间。标签过滤功能可以帮助你从混合的会话记录中提取特定项目的信息。

**遇到问题时不要慌张**：当正常的流程被打断（比如某个假设被证伪时），正是学习的机会。在这些问题中，你会发现新的见解。

* 在对话中，无论是在行动之前、行动过程中还是行动之后，都要进行反思。*
* 在制定计划时，确保计划中包含这种反思的习惯。*

## 第2层：首次使用时的设置

系统会在首次使用时自动完成初始化。有关提供者配置的详细信息，请参阅[docs/QUICKSTART.md](docs/QUICKSTART.md)。或者，你也可以选择使用托管服务来避免进行本地设置——只需将`KEEPNOTES_API_KEY`设置为`keepnotes.ai`（https://keepnotes.ai）即可。

现在，请“存储并阅读”这些基础性的教学内容。这些内容是智慧的源泉，而非测试用的固定框架。

**语言-行为框架**包括对话的类型、承诺的结构以及问题分析的方法：
```bash
keep get .conversations
```

请使用标准的标签来标记对话中的不同行为类型和状态：
```bash
keep get .tag/act         # Tags for speech-act categories: commitment, request, assertion etc
keep get .tag/status      # Tags for lifecycle status: open, fulfilled, withdrawn, etc.
```

**《芒果石经》中的反思教诲**——在行动之前、行动过程中以及行动之后都应该进行反思：
```bash
keep put "file://$(keep config tool)/docs/library/mn61.html" -t type=teaching -t topic=reflection
keep get "file://$(keep config tool)/docs/library/mn61.html"
```

**关于行为责任的观念**（AN5.57）：“我是自己行为的主人，也是这些行为的承受者。”：
```bash
keep put "file://$(keep config tool)/docs/library/an5.57_translation-en-sujato.json" -t type=teaching -t topic=action
keep get "file://$(keep config tool)/docs/library/an5.57_translation-en-sujato.json"
```

**《汉经》中的警句**——“慎勿放逸”（_Aquí donde las papas queman_）：
```bash
keep put "file://$(keep config tool)/docs/library/han_verse.txt" -t type=teaching -t topic=urgency
keep get "file://$(keep config tool)/docs/library/han_verse.txt"
```

**现在开始反思：**你学到了什么？请记录下你的理解：
```bash
keep put "My understanding of the practice: ..." -t type=learning
```

有关安装选项的详细信息，请参阅[docs/QUICKSTART.md](docs/QUICKSTART.md)。

---

## 第3层：快速参考

```bash
keep now                              # Current intentions
keep now "Working on auth flow"       # Update intentions
keep now -V 1                         # Previous intentions
keep move "name" -t project=foo       # Move matching versions from now
keep move "name" --only               # Move just the current version
keep move "name" --from "source" -t X # Reorganize between items

keep find "authentication"            # Search by meaning
keep find "auth" -t project=myapp     # Search with tag filter
keep find "recent" --since P1D        # Recent items

keep put "insight" -t type=learning                # Capture learning
keep put "OAuth2 chosen" -t project=myapp -t topic=auth  # Tag by project and topic
keep put "I'll fix auth" -t act=commitment -t status=open  # Track speech acts
keep list -t act=commitment -t status=open                 # Open commitments

keep get ID                           # Retrieve item (similar + meta sections)
keep get ID -V 1                      # Previous version
keep list --tag topic=auth            # Filter by tag
keep del ID                           # Remove item or revert to previous version
```

**文档的组织结构**：标签使用策略和资料收集方法：
```bash
keep get .domains
```

对于有明确边界的工作内容，可以使用`project`标签；对于跨领域的知识，可以使用`topic`标签。你可以在使用这些标签的同时阅读并更新相应的描述。
```bash
keep get .tag/project     # Bounded work contexts
keep get .tag/topic       # Cross-cutting subject areas
```

有关命令行界面（CLI）的详细信息，请参阅[docs/REFERENCE.md](docs/REFERENCE.md)；每个命令的详细说明请参见`docs/KEEP-*.md`文件。

---

## 相关资源

- [docs/AGENT-GUIDE.md](docs/AGENT-GUIDE.md) — 会议流程的详细指导模式
- [docs/REFERENCE.md](docs/REFERENCE.md) — 快速参考指南
- [docs/TAGGING.md](docs/TAGGING.md) — 标签的使用方法、对话类型以及项目/主题的分类
- [docs/QUICKSTART.md](docs/QUICKSTART.md) — 安装和设置指南
- [keep/data/system/conversations.md](keep/data/system/conversations.md) — 完整的对话框架（`.conversations`文件）
- [keep/data/system/domains.md](keep/data/system/domains.md) — 针对不同领域的资料组织结构（`.domains`文件）
**名称：echo-sales-ai**  
**描述：** 一个全面的人工智能销售助手，可与您的电子邮件系统集成，用于分类潜在客户、解读客户反馈、生成销售报价，并管理制造和技术销售领域的整个销售流程。  

---

# Echo Sales AI  

Echo 是一个先进的人工智能销售运营管理工具，旨在自动化并优化制造和技术销售团队的销售工作流程。它可直接与您的电子邮件系统和客户关系管理（CRM）系统集成，为销售过程的每个阶段提供智能支持。  

## 核心工作流程  

该工具通过一个持续循环来运行，整个流程由 **学习与优化代理**（Learning & Compounding Agent）协调：  

1. **信息收集（Ingestion）：** 监控连接的电子邮件账户，以获取新消息。  
2. **分类（Triage）：** **电子邮件类型分类器**（Email Type Classifier）将每条消息分类（例如：`new_lead`、`customer_reply`、`feedback`、`spam`）。  
3. **数据补充（Enrichment）：** 对于新潜在客户，**公司资料代理**（Company Profile Agent）和 **联系人查找器**（Contact Finder）会补充相关数据。  
4. **执行操作（Action）：** 根据消息类型，触发相应的代理（例如：请求报价时触发 **报价生成器**（Quote Generator），客户提出问题时触发 **异议处理器**（Objection Handler）。  
5. **生成邮件（Generation）：** 生成邮件草稿。  
6. **反馈循环（Feedback Loop）：** 将草稿呈现给您以获取反馈；**反馈解析器**（Feedback Interpreter）会处理您的自然语言评论，以完善邮件内容。  
7. **发送邮件（Dispatch）：** 发送最终版本的邮件。  
8. **CRM更新（CRM Update）：** **CRM数据库代理**（CRM Database Agent）记录所有交互信息，并更新销售流程中的交易状态。  

## 15个辅助代理（The 15 Support Agents）  

Echo 的智能功能由15个专门设计的代理共同实现。每个代理的核心逻辑都存储在 `scripts/` 目录中。有关代理的交互协议和API详细信息，请参阅 [references/agents.md](references/agents.md)。  

- **电子邮件类型分类器（Email Type Classifier）：** 对收到的电子邮件进行分类。  
- **反馈解析器（Feedback Interpreter）：** 将客户反馈转化为结构化指令。  
- **报价生成器（Quote Generator）：** 生成销售报价（详情请参阅 [references/pricing_rules.md](references/pricing_rules.md)）。  
- **定价引擎（Pricing Engine）：** 根据规则、价格层级和折扣计算价格。  
- **公司资料代理（Company Profile Agent）：** 收集并汇总公司信息。  
- **语音转文本转录器（Voice-to-Text Transcriber）：** 将通话中的音频内容转录为文本。  
- **CRM数据库代理（CRM Database Agent）：** 管理与CRM系统的所有交互记录。  
- **销售流程跟踪器（Pipeline Tracker）：** 监控并报告销售进度。  
- **跟进计划器（Follow-up Scheduler）：** 安排并起草跟进邮件。  
- **紧急情况检测器（Urgency Detector）：** 识别需要立即处理的紧急消息。  
- **情感分析器（Sentiment Analyzer）：** 分析客户回复的情感倾向。  
- **报告生成器（Report Generator）：** 生成每周和每月的销售报告。  
- **联系人查找器（Contact Finder）：** 为新潜在客户查找联系方式。  
- **异议处理器（Objection Handler）：** 提供针对常见销售异议的应对建议。  
- **学习与优化代理（Learning & Compounding Agent）：** 从所有交互中学习并优化系统性能。  

## 配套资源（Bundled Resources）  

该工具设计为独立使用，包含以下资源：  
- `scripts/echo-skill/`：包含所有代理的核心逻辑以及Telegram机器人接口的Python应用程序。  
- `references/`：包含代理的详细文档和数据结构说明。  
- `assets/`：存放电子邮件模板和报价格式化所需的资源文件。  

## 使用方法  

通过以下命令激活该工具：  
- “Activate the echo-sales-ai skill.”  
- “Use Echo to check my email.”  
- “Ask Echo to help me write a sales quote.”  

EOF
# guardrails - 交互式安全防护措施配置工具

该工具通过交互式对话流程，帮助用户为他们的 OpenClaw 工作空间配置全面的安全防护措施。

## 命令

### `guardrails setup`  
**交互式配置模式**：指导用户创建 `GUARDRAILS.md` 文件。  

**工作流程：**  
1. 运行环境发现脚本：`bash scripts/discover.sh`  
2. 对风险进行分类：`bash scripts/discover.sh | python3 scripts/classify-risks.py`  
3. 生成定制化问题：`bash scripts/discover.sh | python3 scripts/classify-risks.py | python3 scripts/generate_questions.py`  
4. 与用户进行交互式对话：  
   - 根据发现的环境情况，从生成的问题库中提出问题  
   - 对每个问题提供建议  
   - 允许用户自定义答案  
   - 在必要时进行跟进  
5. 生成 `GUARDRAILS.md` 文件：`echo '<json>' | python3 scripts/generate_guardrails_md.py /path/to/guardrails-config.json`  
   - 输入格式为 JSON：`{"discovery": {...}, "classification": {...}, "answers": {...}}`  
6. 将生成的 `GUARDRAILS.md` 文件展示给用户审核  
7. 在写入工作空间之前获取用户的确认  
8. 将 `GUARDRAILS.md` 文件写入工作空间的根目录  
9. 将 `guardrails-config.json` 文件保存到工作空间的根目录  

**注意事项：**  
- 在对话过程中保持友好和耐心  
- 解释每个问题的重要性  
- 提供关于发现的风险的详细信息  
- 强调高风险的技能或集成组件  
- 允许用户跳过或自定义某些答案  
- 在写入文件之前与用户一起审核最终结果  

### `guardrails review`  
**审核模式**：检查现有配置与当前环境的一致性。  

**工作流程：**  
1. 重新运行环境发现和风险分类流程  
2. 加载现有的 `guardrails-config.json` 文件  
3. 比较发现的风险和配置信息  
4. 识别存在的差异（未覆盖的新技能或仍在配置中的旧技能）  
5. 仅针对差异部分与用户进行沟通，无需重新进行全部对话  
6. 如有需要，更新配置文件和 `GUARDRAILS.md` 文件  

### `guardrails monitor`  
**监控模式**：检测配置变更和潜在的安全违规行为。  

**工作流程：**  
1. 运行监控脚本：`bash scripts/monitor.sh`  
2. 解析生成的 JSON 报告  
3. 如果状态为“ok”，则不发出任何提示；  
4. 如果状态为“needs-attention”，则向用户发送详细通知；  
5. 如果状态为“review-recommended”，则建议用户运行 `guardrails review` 命令  

这些命令可以手动执行，也可以通过 cron 或心跳任务定期自动执行。  

## 生成的文件：  
- **GUARDRAILS.md**：主要的防护措施配置文件（位于工作空间根目录）  
- **guardrails-config.json**：用于监控的机器可读配置文件（位于工作空间根目录）  

## 注意事项：**  
- 该工具仅用于创建安全防护措施；具体的执行和监控工作由代理程序负责完成。  
- 环境发现（`discover.sh`）使用 bash 和 jq；风险分类（`classify-risks.py`）仅使用 Python 标准库。  
- 问题生成和 `GUARDRAILS.md` 文件的生成需要使用大型语言模型（LLM）；请设置 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`。  
- Python 脚本需要 `requests` 库（通过 `pip install requests` 安装）。  
- 环境发现和风险分类操作仅具有读取权限。  
- 仅 `setup` 和 `review` 模式会写入文件，并且都需要用户的确认。
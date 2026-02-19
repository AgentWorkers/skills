---
name: lawclaw
description: 只需提交一份合同文件，就能立即获得答案。LawClaw 能快速解析 PDF 文件，识别出其中的风险条款，标记出需要修改的部分（用红线标出），检查引用内容的准确性，并在本地搜索数千份相关文件——这样所有处理过程都不会离开你的电脑。这款工具专为按小时计费的律师和法律助理设计，他们可不能浪费哪怕一分钟的时间。
homepage: https://github.com/legal-tools/lawclaw
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":["pdftotext","diff","grep","pandoc"]},"install":[{"id":"brew-poppler","kind":"brew","formula":"poppler","bins":["pdftotext"],"label":"Install pdftotext (brew)"},{"id":"brew-pandoc","kind":"brew","formula":"pandoc","bins":["pandoc"],"label":"Install pandoc (brew)"}]}}
---
# lawclaw

只需上传一份合同文件，即可快速获得所需的信息。

lawclaw能够高效地解析法律文件——速度迅速、细致入微，同时不会遗漏第47页中隐藏的赔偿条款。它可以从PDF文件中提取文本、标记关键条款、生成对比结果、验证引用内容，并在整个文件集中搜索对案件胜诉至关重要的那句话。

所有操作都在您的本地机器上完成，无需上传数据到第三方服务器，从而确保了律师与客户之间的保密性。您只需要一台终端和lawclaw这个强大的工具即可。

**适用人群：**  
律师、法律助理以及负责合同审核、诉讼支持、尽职调查、电子文件检索或撰写法律简报的团队。

**替代传统工作方式：**  
以往可能需要花费数小时时间，在数十份PDF文件中手动使用Ctrl+F进行查找。

## 核心功能

### 文档分析  
- 从法律PDF文件中提取文本：`pdftotext <file.pdf> <output.txt>`  
- 搜索特定条款：`grep -i "indemnification\|liability\|warranty" contract.txt`  
- 统计文件字数（用于计费）：`wc -w document.txt`  
- 获取文件元数据：`pdfinfo <file.pdf>`  

### 合同条款提取  
使用正则表达式通过`grep`命令提取常见条款：  
- 赔偿条款：`grep -i "indemnif\|hold harmless" contract.txt`  
- 终止条款：`grep -i "terminat\|cancellation" contract.txt -A 3`  
- 保密条款：`grep -i "confidential\|proprietary\|NDA" contract.txt -A 3`  
- 不可抗力条款：`grep -i "force majeure\|act of god" contract.txt -A 3`  
- 管辖权条款：`grep -i "jurisdiction\|venue\|governing law" contract.txt -A 2`  
- 仲裁条款：`grep -i "arbitration\|dispute resolution" contract.txt -A 3`  
- 竞业禁止条款：`grep -i "non-compete\|noncompete\|restrictive covenant" contract.txt -A 3`  
- 权利转让条款：`grep -i "assign\|transfer\|delegate" contract.txt -A 2`  

### 对比与差异分析  
- 比较两个版本：`diff -u original.txt revised.txt > redline.diff`  
- 侧边对比显示差异：`diff -y original.txt revised.txt | less`  
- 逐词显示差异：`wdiff original.txt revised.txt > changes.txt`  
- （若需先转换为纯文本格式）`pandoc contract.docx -t plain -o contract.txt`  

### 引用与参考文献检查  
- 查找案例引用：`grep -E "[0-9]+ [A-Z]\.[A-Za-z0-9.]+ [0-9]" brief.txt`  
- 查找美国法典（U.S. Code）引用：`grep -E "[0-9]+ U\.S\.C\. § [0-9]+" document.txt`  
- 查找联邦法规（CFR）引用：`grep -E "[0-9]+ C\.F\.R\. § [0-9]+" document.txt`  
- 提取脚注内容：`grep -E "\[[0-9]+\]" brief.txt`  
- 查找《蓝皮书》（Bluebook）中的引用格式：`grep -E "[A-Z][a-z]+, [0-9]+ [A-Z]\." brief.txt`  

### 文件管理  
- 查找指定类型的文件：`find . -name "*.pdf" -type f`  
- 在文件集中搜索关键词：`grep -r "key term" ./discovery/`  
- 列出最近修改的文件：`find . -name "*.pdf" -mtime -7 -ls`  
- 批量重命名文件：`for f in *.pdf; do mv "$f" "Exhibit_${f}"; done`  

### 电子文件检索（Discovery）  
- 统计PDF文件的页数：`pdfinfo document.pdf | grep Pages`  
- 批量转换PDF格式：`for f in *.pdf; do pdftotext "$f" "${f%.pdf}.txt"; done`  
- 生成文件列表：`ls -lh *.pdf > production_log.txt`  
- 查找文件编号：`grep -r "PROD[0-9]\{6\}" ./documents/`  

### 尽职调查（Due Diligence）  
- 扫描文件中的关键术语：`grep -i "material adverse\|intellectual property\|pending litigation" diligence/*.txt`  
- 提取日期信息：`grep -E "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}" contract.txt`  
- 查找金额信息：`grep -E "\$[0-9,]+(\.[0-9]{2})?" agreement.txt`  
- 识别合同各方：`grep -E "WHEREAS|Party|Seller|Buyer|Lessor|Lessee" contract.txt`  

### 证词与记录分析  
- 搜索证词内容：`grep -i "Q\." deposition.txt | grep -i "keyword"`  
- 提取证人回答：`grep "A\." deposition.txt -A 2`  
- 统计页数/行数：`wc -l transcript.txt`  

### 保密性管理  
- 生成文件列表：`find ./documents -type f -exec ls -lh {} \; > privilege_log.csv`  
- 搜索涉及保密性的关键词：`grep -ri "attorney-client\|work product" ./emails/`  
- 标记需要保密的文件：`grep -rli "attorney-client" ./emails/ > privileged_files.txt`  

## 常见工作流程  

### 合同审核流程  
1. 提取文本：`pdftotext contract.pdf contract.txt`  
2. 检查关键条款：  
   - `grep -i "limitation of liability" contract.txt`  
   - `grep -i "indemnification" contract.txt`  
   - `grep -i "termination" contract.txt`  
   - `grep -i "confidentiality" contract.txt`  
   - `grep -i "governing law" contract.txt`  
3. 提取金额信息：`grep -E "\$[0-9,+" contract.txt`  
4. 标记截止日期：`grep -i "within [0-9]+ days\|business days\|calendar days" contract.txt`  

### 对比流程  
1. 将两份合同转换为纯文本格式：`pandoc original.docx -t plain -o original.txt && pandoc revised.docx -t plain -o revised.txt`  
2. 生成差异报告：`diff -u original.txt revised.txt > changes.diff`  
3. 侧边对比显示差异：`diff -y original.txt revised.txt | less`  

### 文件检索流程  
1. 提取所有PDF文件的内容：`for pdf in discovery/*.pdf; do pdftotext "$pdf" "${pdf%.pdf}.txt"; done`  
2. 在所有文件中搜索关键词：`grep -ri "responsive term" discovery/*.txt`  
3. 生成文件索引：`ls -lh discovery/*.pdf > document_index.txt`  

### 尽职调查流程  
1. 提取所有相关文件：`find diligence/ -name "*.pdf" -exec pdftotext {} \;`  
2. 检查潜在风险（如诉讼、违约或破产相关内容）：`grep -ri "litigation\|breach\|default\|bankruptcy" diligence/*.txt`  
3. 提取唯一日期：`grep -E "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}" diligence/*.txt | sort -u`  

### 简报/动议引用检查  
1. 提取引用内容：`grep -E "[0-9]+ [A-Z]\.[A-Za-z0-9.]+ [0-9]" brief.txt`  
2. 交叉比对引用信息：`diff <(grep -oE "[0-9]+ [A-Z]\.\S+ [0-9]+" brief.txt | sort -u) <(sort toa.txt)`  

## 注意事项：  
- 所有处理操作都在本地完成，不会上传到云端，从而保护客户隐私。  
- 在分析前，会使用`pandoc`将DOCX/DOC格式转换为纯文本。  
- 使用`wdiff`进行逐词对比（需先安装`brew install wdiff`）。  
- 可与`gog`工具集成，以便与Google Workspace（Drive、Gmail、 Sheets）协同使用。  
- 在对案件文件进行自动化处理前，请务必获得上级律师的批准。  
- 如需对扫描后的PDF文件进行OCR识别，需安装`tesseract`：`brew install tesseract`。  

## 安全与道德规范  
- 在使用OCR提取的文本之前，请确保其准确性。  
- 在处理敏感信息时，务必维护保密日志。  
- 在生成文件前，使用适当的工具对个人身份信息（PII）进行脱敏处理。  
- 遵守法院关于电子文件检索的命令、电子存储与检索（ESI）协议以及当地法规。  
- 保留所有文件处理的审计记录，以应对可能的争议。  
- 未经书面许可，严禁将客户数据传输给外部服务。
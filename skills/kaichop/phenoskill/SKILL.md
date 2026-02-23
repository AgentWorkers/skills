---
name: phenosnap-phenotype-extractor
description: 使用 PhenoSnap 从用户提供的文本中提取临床表型和药物实体，并生成带有时间戳的 JSON 输出文件。
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"],"anyBins":["git","curl","powershell"],"env":["HPO_OBO_PATH"]},"primaryEnv":"HPO_OBO_PATH"}}
---
## 使用场景  
当用户提供以下信息时，可使用此功能：  
- **自身的**临床表型/症状/诊断信息（以自由文本、项目符号列表或类似临床记录的形式）；  
- 药物/用药信息（包括名称、剂量和服用频率）。  

**触发示例**：  
- “症状：共济失调、癫痫发作、发育迟缓。用药：左乙拉西坦 500毫克，每日两次。”  
- “我每天服用500毫克二甲双胍，出现疲劳、多尿和视力模糊的症状。”  

## 不适用场景  
**请勿**在以下情况下使用此功能：  
- 用户提出一般性问题（例如：“什么是HPO？”，“什么是表型？”，“什么是GLP-1？”）；  
- 用户提供的文本不属于个人临床信息（如新闻文章、学术段落或代码）；  
- 未经明确许可，用户要求您解读他人的私人临床记录（属于健康隐私信息，PHI）。  

## 安全与隐私  
- 将用户输入视为可能包含敏感临床信息的资料；  
- **切勿**将用户文本或处理后的结果上传至任何外部存储空间（此功能仅限本地使用）；  
- 在将任何数据写入磁盘之前，务必**删除明显的身份识别信息**：  
  - 电子邮件地址、电话号码、街道地址  
  - 类似医疗记录编号（MRN）的长数字串  
  - 明确标注为“姓名：……”的个人信息  
- 如果消息中包含高度敏感的个人信息（如姓名+出生日期+地址或姓名+医疗记录编号），**请暂停操作并请求用户确认**，建议用户先删除这些信息。  

## 系统要求/配置  
- 必须安装Python 3，并确保其在系统路径（PATH）中可用；  
- 需要网络访问权限（仅用于初次下载PhenoSnap工具包）。  
- **HPO OBO文件**的默认路径为：`{baseDir}/resources/hp.obo`；  
  - 可通过环境变量`HPO_OBO_PATH`自定义路径；  
- 该功能不会自动下载`hp.obo`文件，用户需自行提供该文件。  

**最佳实践**：  
- 在运行此功能前，建议创建虚拟环境（venv或conda），因为该功能可能通过`pip`安装相关Python包。  

## 输入与输出  
- **输入文件**（已处理敏感信息的版本）：`{baseDir}/artifacts/phenosnap_inputs/input_<YYYYMMDD_HHMMSS>.txt`  
- **输出文件**（格式为JSON，包含时间戳）：`{baseDir}/artifacts/phenosnap_outputs/phenotypes_<YYYYMMDD_HHMMSS>.json`  
- **第三方工具下载缓存**：`{baseDir}/third_party/phenosnap_main.zip`  
- **用于下载pip的脚本**：`{baseDir}/third_party/get-pip.py`  

## 检测规则  
- 如果用户消息中包含以下关键词或短语，将触发该功能：  
  - 表型相关内容：`symptom(s)`、`phenotype(s)`、`Dx`（诊断）、`PMH`（既往病史）、`Hx`（病史记录）  
  - 药物相关内容：`meds`、`medications`、`taking`（正在服用）、`prescribed`（处方药物）；  
  - 常见剂量单位：`\b\d+(\.\d+)?\s?(mg|mcg|g|ml|units)\b`  
  - 服用频率：`qd`（每日一次）、`q.d.`（每日两次）、`bid`（每日三次）、`t.i.d.`（每日四次）、`tid`（每日五次）、`qhs`（每小时一次）、`qAM`（清晨一次）、`qPM`（傍晚一次）、`daily`（每日）、`weekly`（每周一次）  

**注意**：  
- 仅当用户提供了表型或用药信息时，才会触发该功能；纯信息性问题不会触发处理流程。  

### 执行流程  

## 0) 创建所需目录  
- 如果目录不存在，请创建：  
  - `{baseDir}/PhenoSnap/`  
  - `{baseDir}/artifacts/phenosnap_inputs/`  
  - `{baseDir}/artifacts/phenosnap_outputs/`  
  - `{baseDir}/resources/`  
  - `{baseDir}/third_party/`  

## 1) 删除敏感信息  
- 扫描用户输入内容，删除其中的身份识别信息（电子邮件、电话号码、地址、医疗记录编号、姓名）；  
- 如果发现高度敏感的个人信息，**请用户确认是否继续处理，并建议其删除这些信息**；  
- 将处理后的文本保存为：`{baseDir}/artifacts/phenosnapinputs/input_<YYYYMMDD_HHMMSS>.txt`  

## 2) 确保PhenoSnap工具包已安装  
- 检查`{baseDir}/PhenoSnap/`目录是否存在；  
  - 如果存在`extract_phenotypes.py`文件，则继续执行后续步骤；  
  - 如果不存在，需通过git或zip文件下载该工具包。  

### 2A) 使用git下载  
  - 运行：`git clone https://github.com/WGLab/PhenoSnap.git {baseDir}/PhenoSnap`  
### 2B) 使用zip文件下载  
  - 下载链接：`https://github.com/WGLab/PhenoSnap/archive/refs/heads/main.zip`  
  - 将文件解压至`{baseDir}/third_party/phenosnap_main.zip`  

## 3) 检查依赖关系并自动安装  
- 运行以下命令，验证工具包是否可导入：  
  - `python3 -c "import importlib.util; spec=importlib.util.spec_from_file_location('extract_phenotypes','extract_phenotypes.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print('ok')`  
  - 如果成功，继续执行后续步骤；  
  - 如果遇到模块导入错误（`ModuleNotFoundError`或`ImportError`），请按照提示进行修复（如安装pip）。  

## 4) 配置HPO OBO文件路径  
- 确定HPO OBO文件的路径；  
  - 如果环境变量`HPO_OBO_PATH`已设置且文件存在，则使用该路径；  
  - 否则，使用默认路径`{baseDir}/resources/hp.obo`。  

## 5) 处理用户输入并生成输出文件  
- 将处理后的用户输入写入`{baseDir}/artifacts/phenosnapinputs/input_<YYYYMMDD_HHMMSS>.txt`；  
- 运行`extract_phenotypes.py`工具，生成`phenotypes_<YYYYMMDD_HHMMSS>.json`输出文件。  

## 6) 验证输出结果  
- 确保输出文件存在且内容非空；  
- 如有错误，提供相应的故障排除提示。  

## 常见问题与解决方法  
- **PhenoSnap脚本缺失**：确认`{baseDir}/PhenoSnap/extract_phenotypes.py`文件是否存在；  
- **无法使用git**：尝试使用zip文件下载工具包；  
- **解压失败**：使用Python的`zipfile`模块进行解压；  
- **pip无法安装**：按照提示安装pip；  
- **安装包时出现权限问题**：使用虚拟环境（venv/conda）并重新尝试；  
- **HPO OBO文件缺失**：将文件放置在`{baseDir}/resources/hp.obo`目录中，或设置`HPO_OBO_PATH`变量。  

### 示例  
- **示例1**（包含表型和用药信息）：  
  - 用户输入：**症状：发育迟缓、癫痫发作、共济失调。用药：丙戊酸钠 250毫克，每日两次。**  
  - 处理后输出：`phenotypes_<TS>.json`文件。  
- **示例2**（仅包含用药信息）：  
  - 用户输入：**当前用药：二甲双胍 500毫克，每日一次；阿托伐他汀 20毫克，每小时一次。**  
  - 处理后输出：包含药物名称和服用频率的JSON文件。  
- **示例3**（不适用）：  
  - 用户提问：**什么是人类表型本体（Human Phenotype Ontology）？它如何使用？**  
  - 该功能不会执行任何处理操作，仅提供相关信息。
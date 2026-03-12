---
name: alicloud-ai-misc-crawl-and-skill
description: 刷新 Model Studio 的模型爬取功能，并重新生成派生的摘要以及 `skills/ai/**` 目录下的各项技能信息。当模型列表或生成的技能需要更新时，请使用此命令。
version: 1.0.0
---
**类别：任务**  
# 阿里云模型工作室（Alibaba Cloud Model Studio）的爬取与技能生成（Crawl and Skill Generation）

## 先决条件  
- Node.js（用于运行 `npx` 命令）  
- Python 3  
- 能够访问模型页面的网络权限  

## 工作流程  
1. 爬取模型页面（获取原始 Markdown 内容）  
   ```bash
npx -y @just-every/crawl \"https://help.aliyun.com/zh/model-studio/models\" > alicloud-model-studio-models.md
```  

2. 重新生成模型摘要（包含模型信息及 API/使用链接）  
   ```bash
python3 skills/ai/misc/alicloud-ai-misc-crawl-and-skill/scripts/refresh_models_summary.py
```  

3. 生成技能信息（更新 `skills/ai/**` 目录下的文件）  
   ```bash
python3 skills/ai/misc/alicloud-ai-misc-crawl-and-skill/scripts/refresh_alicloud_skills.py
```  

## 输出结果  
- `alicloud-model-studio-models.md`：爬取到的原始模型数据  
- `output/alicloud-model-studio-models-summary.md`：整理后的模型摘要  
- `output/alicloud-model-studio-models.json`：结构化的模型列表  
- `output/alicloud-model-studio-skill-scan.md`：技能覆盖情况报告  
- `skills/ai/**`：生成的技能信息  

## 注意事项  
- 不要自行创建模型 ID 或 API 端点；仅使用模型页面上已有的链接。  
- 生成技能信息后，如果模型列表发生变化，请更新 `README.md`、`README.en.md` 和 `README.zh-TW.md` 文件。  

## 验证  
```bash
mkdir -p output/alicloud-ai-misc-crawl-and-skill
for f in skills/ai/misc/alicloud-ai-misc-crawl-and-skill/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-ai-misc-crawl-and-skill/validate.txt
```  
验证标准：命令执行成功（返回 0 状态码），并且 `output/alicloud-ai-misc-crawl-and-skill/validate.txt` 文件被生成。  

## 输出文件与验证依据  
- 将所有生成的文件、命令输出结果及 API 响应摘要保存在 `output/alicloud-ai-misc-crawl-and-skill/` 目录下。  
- 在验证文件中记录关键参数（区域、资源 ID、时间范围等），以确保可重复性。  

## 参考资料  
- 资料来源列表：`references/sources.md`
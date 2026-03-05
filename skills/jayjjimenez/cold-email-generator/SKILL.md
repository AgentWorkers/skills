# cold-email-generator

**用途：** 生成个性化的冷邮件，向当地企业推荐 Gracie AI 的客服服务。

该工具接收企业名称和网站地址，通过爬取企业网站获取实际信息（如服务内容、员工信息、地理位置等），然后使用 Ollama（llama3.2）生成一封简洁、针对性的冷邮件（而非使用模板）。

---

## 使用方法

### 单个企业
```bash
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py \
  --name "Victory Auto Repair" \
  --url "https://victoryautosi.com" \
  --phone "718-698-9896"
```

### 单个企业 + 保存到文件
```bash
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py \
  --name "P.A.C. Plumbing" \
  --url "https://pac-plumbing.com" \
  --save
```

### 批量处理：处理 `MASTER_LEAD_LIST.md` 文件中的所有企业信息
```bash
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py --list
python3 ~/StudioBrain/00_SYSTEM/skills/cold-email-generator/generator.py --list --save
```

---

## 输出结果

- 邮件内容会直接输出到终端。
- 使用 `--save` 选项时，邮件会被保存到：`~/StudioBrain/30_INTERNAL/WLC-Services/OUTREACH/[企业名称].txt`

---

## 工作流程

1. 爬取企业主页及（如果存在）“关于我们”/“联系我们”页面的内容。
2. 提取企业名称、企业负责人、提供的服务、企业位置以及员工信息。
3. 将这些信息以结构化格式传递给 Ollama（使用 `llama3.2`）生成邮件内容。
4. Ollama 会生成一篇不超过 150 字的 3 段落组成的邮件。

---

## 所需依赖项

- 爬取工具：`~/StudioBrain/00_system/skills/scraping/scrape.py`
- Ollama（版本：llama3.2）：需通过 `ollama list` 命令进行验证。
- 数据源文件：`~/StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md`

---

## Gracie AI 服务详情

- 资费：首次设置费用为 299 美元；每月费用为 399 美元。
- 试用电话：(347) 851-1505
- 推荐方：Jay Jimenez，White Lighter Club Studios
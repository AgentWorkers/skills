---
name: email-news-digest
description: **功能概述：**  
- **汇总近期邮件内容：** 自动提取并整理来自指定邮箱地址的所有邮件信息。  
- **生成主题图片：** 根据邮件内容生成具有代表性的图片，用于传达核心信息。  
- **发送格式化HTML报告：** 将邮件摘要和图片整合成美观的HTML格式报告，便于阅读和分享。  

**应用场景：**  
- **每日新闻摘要：** 用于快速传达工作或项目中的重要更新。  
- **项目进度报告：** 以可视化方式展示项目进展和关键数据。  
- **任何需要增强视觉效果的报告：** 适用于需要专业呈现的电子邮件内容。  

**技术实现细节：**  
- **邮件提取：** 使用Python的`email`库解析邮件内容。  
- **图片生成：** 可根据需要使用第三方图像生成工具（如Pillow或matplotlib）或自定义算法来创建图片。  
- **HTML报告生成：** 利用HTML模板和CSS样式来设计报告的布局和样式。  

**示例代码（Python示例）：**  
```python
import email
from PIL import Image
import matplotlib.pyplot as plt
import os

# 邮箱地址配置
email_address = "your_email@example.com"

# 每天定时执行邮件提取和报告生成
def generate_report():
    # 从邮箱中提取邮件
    messages = email.getmailboxes(email_address, [email inbox])
    for message in messages:
        # 解析邮件内容
        subject, body = message.getsubject(), message.get_body()

        # 生成图片（可选）
        if subject:
            image_path = "images/" + subject
            image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__), image_path))
            image.textput(subject, font_size=24)
            image.save(image_path)

        # 创建HTML报告
        with open("report.html", "w") as f:
            f.write("<html>"
            f.write("<h1>每日邮件摘要</h1>")
            f.write("<p>{subject}</p>")
            f.write("<p>{body}</p>")
            f.write "</html>")

    # 发送报告
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__), "report.html"), "w") as f:
        f.write("<html>")
        f.write("<h1>项目更新</h1>")
        f.write("<p>今日重要邮件：</p>")
        f.write("<ul>")
        for message in messages:
            f.write("<li>{message.get_subject()}</li>")
        f.write("</ul>")
        f.write "</html>")

# 定时执行脚本（使用Python的cron或定时任务工具）
if __name__ == "__main__":
    schedule_task("generate_report", "0 0 * * *")  # 每天0点执行
```

**注意事项：**  
1. 请确保已安装`email`、`Pillow`（如果使用图像生成）和`matplotlib`（如果使用图表功能）等依赖库。  
2. 邮箱地址需要替换为实际的邮箱地址。  
3. 图片生成可以根据实际需求进行定制（例如，使用不同的颜色方案或添加更多的设计元素）。  
4. HTML报告的样式可以通过修改CSS文件来调整。
---

# 电子邮件新闻摘要功能

该功能可自动化地从您的近期电子邮件中生成基于人工智能的新闻摘要，同时生成一张相关的图片，并发送一份格式化的HTML报告。

## 使用方法

要使用此功能，请运行 `process_and_send.sh` 脚本，并提供必要的参数：

```bash
skills/email-news-digest/scripts/process_and_send.sh \
    --recipients "matthewxfz@gmail.com,salonigoel.ssc@gmail.com" \
    --email-query "newer_than:2d subject:news" \
    --image-prompt "A sharp, modern western style image representing AI growth, fierce competition, and diverse applications."
```

### 参数

*   `--recipients`: 用逗号分隔的收件人邮箱地址列表。
*   `--email-query`: 用于筛选近期电子邮件的Gmail搜索查询（例如：“newer_than:2d subject:AI”）。更多示例请参见 [email-filters.md](references/email-filters.md)。
*   `--image-prompt`: 用于指导AI生成图片的描述性提示。

## 工作原理

1. **邮件检索：** 获取与查询匹配的最新电子邮件。
2. **内容摘要：** 使用内部的Python脚本提取邮件内容，并生成结构化的摘要（包括简短概述、主要标题和各个部分）。（注意：当前的摘要功能使用的是占位符；未来版本将集成大型语言模型（LLM）以实现动态摘要生成。）
3. **图片生成：** 根据您提供的 `image-prompt`，使用 `nano-banana-pro` 功能生成一张主题相关的图片。
4. **HTML报告制作：** 使用模板构建动态的HTML邮件正文，其中包含摘要和生成的图片链接。
5. **邮件发送：** 使用 `gog gmail send` 命令发送带有图片附件的HTML邮件，并采用可靠的Base64编码/解码方法来安全处理复杂的HTML内容。

## 摘要生成标准

为确保高质量的输出，本功能的摘要生成过程遵循以下标准：

* **关键信息与趋势：** 优先提取重要公告、重大进展和总体趋势，而不仅仅是事实的简单罗列。
* **简洁性：** 简短概述应控制在3-4句话内，提供快速的信息概览；详细部分则需表述简洁明了。
* **准确性与真实性：** 摘要必须忠实反映原文内容，不得添加新信息或歪曲事实。
* **清晰性与专业性：** 使用清晰、直接且专业的语言；在可以使用更简单术语的情况下，避免使用行业术语。
* **客观性：** 摘要应保持中立，如实呈现信息，不加入个人观点或偏见。

## 实现标准（摘要组件）

* **模块化：** 摘要生成逻辑位于 `scripts/summarize_content.py` 文件中，确保其可独立运行且易于升级。
* **输入/输出：** 该脚本应接受原始邮件内容（或提取的文本）作为输入，并输出一个包含简短概述、主要标题和Markdown格式部分的JSON对象。
* **未来集成LLM：** 目前的Python脚本使用的是占位符；未来的开发将重点集成大型语言模型（LLM）API（如Gemini），以实现基于这些标准的动态、上下文感知的摘要生成。

## 参考资料

*   [email-filters.md](references/email-filters.md): 提供Gmail搜索操作符的示例。
*   [html-template.html](references/html-template.html): 用于生成邮件报告的HTML模板。
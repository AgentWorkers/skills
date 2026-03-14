**名称：u2-doc-parser**  
**描述：** 使用 UniDoc API 解析文档，并将其转换为 Markdown 或 JSON 格式。支持同步和异步解析，并具有自动状态监控功能。  

**UniDoc 文档解析器**  
======================  

**概述**  
--------  
使用 UniDoc API 解析文档，将其转换为 Markdown 或 JSON 格式。支持同步和异步解析，并具备自动状态监控功能。非常适合通过基于云的 API 服务转换多种文档格式（如 PDF、DOC、DOCX、图片等）。  

**前提条件/阅读参考资料的时间**  
---------------------------------  
如果遇到 API 错误、网络问题，或需要了解 API 端点信息，请阅读：  
* `references/unidoc-notes.md`  

**快速入门（单份文档）**  
-----------------------------  
```bash
# Run from the skill directory
python scripts/unidoc_parse.py /path/to/file.pdf \
  --format md \
  --output ./unidoc-output \
  --mode sync
```  

**选项**  
-------  
* `--format md|json` （默认值：`md`）  
  - 输出格式：Markdown 或 JSON  
* `--mode sync|async` （默认值：`sync`）  
  - 同步模式：等待转换完成  
  - 异步模式：持续轮询转换状态直到完成  
* `--func METHOD` （默认值：`unisound`）  
  - 使用的转换方法/算法  
* `--output DIR` （默认值：`./unidoc-output`）  
  - 转换后文件的输出目录  
* `--uid UUID` （可选）  
  - 自定义用户 ID（未提供时自动生成）  

**输出规范**  
------------------  
* 默认情况下，输出文件会保存在 `./unidoc-output/<document_name>/` 目录下  
  - Markdown 格式输出文件：`output.md`  
  - JSON 格式输出文件：`output.json`  
  - 输出文件名保持与原始文档名称一致  

**注意事项**  
-----  
* 需要连接到 UniDoc API（http://unidoc.uat.hivoice.cn）  
* 支持多种文件格式：PDF、DOC、DOCX、PNG、JPG 等  
* 异步模式下，系统会每秒轮询一次转换进度  
* 文件大小和请求速率限制取决于 API 服务的配置  
* 对于大型文件或批量处理，建议使用异步模式
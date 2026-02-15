# Office到Markdown转换器技能（v2）

## 描述  
该技能可将Office文档（PDF、DOC、DOCX、PPTX）转换为Markdown格式。它使用`word-extractor`库来处理`.doc`文件，并实现了与OpenClaw的全面集成。  

## 使用场景  
- 当您需要从Office文档中提取文本时  
- 当您希望将文档转换为易于阅读的Markdown格式时  
- 当您需要在OpenClaw中分析文档内容时  
- 特别是在处理旧的`.doc`格式文件时  

## 支持的格式  
- **PDF (.pdf)**：使用`pdf-parse`库进行文本提取  
- **Word (.docx)**：使用`mammoth`和`turndown`库保留格式  
- **旧版Word (.doc)**：使用`word-extractor`库提取文本（支持中文编码）  
- **PowerPoint (.pptx)**：使用`python-pptx`库进行基本文本提取  

## 依赖项  
- Node.js及npm包：`pdf-parse`、`mammoth`、`turndown`、`word-extractor`  
- Python3及`python-pptx`（用于PPTX转换，可选）  
- OpenClaw执行工具的权限  

## 安装  

### 1. 将技能文件复制到您的工作目录：  
```bash
cp -r /root/.openclaw/workspace/office-to-md-v2/office-to-md /path/to/your/workspace/
```  

### 2. 安装依赖项：  
```bash
cd /path/to/your/workspace/office-to-md
npm install
```  

### 3. （可选）支持PPTX格式：  
```bash
pip3 install python-pptx
```  

## 在OpenClaw中的使用方法  

### 方法1：直接执行命令  
```javascript
// Convert any supported document
const result = await exec(
  'node /path/to/office-to-md/openclaw-skill.js /path/to/document.doc',
  { workdir: '/path/to/workspace', timeout: 60000 }
);

if (result.exitCode === 0) {
  console.log('✅ Document converted successfully');
  // Output file: /path/to/document.md
} else {
  console.error('❌ Conversion failed:', result.stderr);
}
```  

### 方法2：使用封装函数  
```javascript
// Import the converter
const { convertOfficeToMarkdown } = require('/path/to/office-to-md/openclaw-skill.js');

// Convert document
const conversionResult = await convertOfficeToMarkdown('/path/to/document.pdf');
if (conversionResult.success) {
  console.log(`Output: ${conversionResult.outputPath}`);
  console.log(`Preview: ${conversionResult.preview}`);
} else {
  console.error(`Error: ${conversionResult.error}`);
}
```  

### 方法3：使用完整的OpenClaw集成函数  
```javascript
async function convertDocumentToMarkdown(filePath) {
  // Validate file exists
  try {
    await read(filePath);
  } catch (error) {
    return { success: false, error: `File not found: ${filePath}` };
  }
  
  // Check file extension
  const ext = filePath.toLowerCase().slice(-5);
  const supported = ['.pdf', '.doc', '.docx', '.pptx'];
  if (!supported.some(s => ext.endsWith(s))) {
    return { 
      success: false, 
      error: `Unsupported file type. Supported: ${supported.join(', ')}` 
    };
  }
  
  // Convert using the skill
  const cmd = `node /path/to/office-to-md/openclaw-skill.js "${filePath}"`;
  const result = await exec(cmd, { 
    workdir: '/path/to/workspace',
    timeout: 120000 // 2 minutes for large files
  });
  
  if (result.exitCode === 0) {
    const outputPath = filePath.replace(/\.[^/.]+$/, '.md');
    return {
      success: true,
      outputPath: outputPath,
      message: `Converted to: ${outputPath}`
    };
  } else {
    return {
      success: false,
      error: result.stderr || 'Conversion failed'
    };
  }
}

// Usage example
const result = await convertDocumentToMarkdown('/path/to/document.doc');
if (result.success) {
  const markdown = await read(result.outputPath);
  console.log(markdown.substring(0, 1000));
}
```  

## 示例  

### 示例1：转换并分析文档  
```javascript
// Convert a .doc file and analyze its content
const docPath = '/path/to/document.doc';
const convertResult = await exec(
  `node /path/to/office-to-md/openclaw-skill.js "${docPath}"`,
  { workdir: '/path/to/workspace' }
);

if (convertResult.exitCode === 0) {
  const mdPath = docPath.replace('.doc', '.md');
  const content = await read(mdPath);
  
  // Analyze the content
  const wordCount = content.split(/\s+/).length;
  const lines = content.split('\n').length;
  const hasChinese = /[\u4e00-\u9fff]/.test(content);
  
  console.log(`Document analysis:`);
  console.log(`- Word count: ${wordCount}`);
  console.log(`- Lines: ${lines}`);
  console.log(`- Contains Chinese: ${hasChinese}`);
  console.log(`- Preview: ${content.substring(0, 200)}...`);
}
```  

### 示例2：批量转换  
```javascript
// Convert multiple documents of different formats
const documents = [
  '/path/to/report.pdf',
  '/path/to/legacy.doc',
  '/path/to/modern.docx',
  '/path/to/presentation.pptx'
];

const results = [];
for (const doc of documents) {
  console.log(`Converting ${doc}...`);
  const result = await exec(
    `node /path/to/office-to-md/openclaw-skill.js "${doc}"`,
    { workdir: '/path/to/workspace', timeout: 90000 }
  );
  
  const success = result.exitCode === 0;
  results.push({
    file: doc,
    success: success,
    error: success ? null : result.stderr
  });
  
  console.log(success ? '✅ Success' : '❌ Failed');
}

// Summary
const successful = results.filter(r => r.success).length;
console.log(`\nConversion summary: ${successful}/${results.length} successful`);
```  

## API参考  
```javascript
function convertOfficeToMarkdown(filePath) {
  return new Promise((resolve, reject) => {
    // 转换逻辑...
  });
}
```

## 配置设置  
- **超时设置**  
  - 小文件（<1MB）：30秒  
  - 中等文件（1-10MB）：60秒  
  - 大文件（>10MB）：120秒  

### 内存限制  
- 默认的Node.js内存限制适用于大多数文档  
- 对于非常大的文件，可能需要增加内存：  
  ```bash
  node --max-old-space-size=4096 openclaw-skill.js large-file.doc
  ```  

## 故障排除  

### 常见问题  
1. **“文件未找到”**  
   - 检查文件路径和权限  
   - 使用绝对路径以确保可靠性  

2. **“文件类型不支持”**  
   - 确保文件具有正确的扩展名  
   - 检查文件是否确实是所需的格式  

3. **.doc文件转换失败**  
   - 文件可能已损坏或格式异常  
   - 可先尝试在Word中打开文件，然后另存为`.docx`格式  

4. **中文文本显示为乱码**  
   - `word-extractor`应能自动处理中文编码  
   - 如果问题仍然存在，可能是文件使用了特殊的编码方式  

5. **超时错误**  
   - 对于大文件，增加超时时间  
   - 检查系统资源使用情况  

### 调试模式  
通过设置环境变量启用调试日志：  
```bash
DEBUG=office-to-md node openclaw-skill.js document.doc
```  

## 性能  
- PDF：转换速度快，取决于文件大小  
- DOCX：转换速度快，格式保留较好  
- DOC：转换速度中等，需要二进制解析  
- PPTX：转换速度较慢，依赖Python和外部库  

## 限制  
- 文档中的图片无法被提取  
- 复杂的格式可能无法完全保留  
- 表格在转换为Markdown时可能会失真  
- 非常旧或损坏的`.doc`文件可能无法转换  
- 不支持受密码保护的文件  

## 更新记录  

### v2.0.0（2026-02-15）  
- 增加了对`.doc`文件的全面支持  
- 修复了与`pptConverter`的兼容性问题  
- 完善了与OpenClaw的集成  
- 改进了中文文本的提取效果  
- 添加了包含统计信息的结构化输出  

### v1.0.0（初始版本）  
- 支持基本的PDF、DOCX、PPTX格式  
- 提供简单的转换功能（不支持`.doc`文件）  

## 许可证  
本技能按“原样”提供。所使用的库遵循各自的许可证：  
- `pdf-parse`：MIT  
- `mammoth`：BSD-2-Clause  
- `turndown`：MIT  
- `word-extractor`：MIT  
- `python-pptx`：MIT
---
name: focusnote-add-to-daily-note
description: 在 FocusNote 的今日日常笔记中添加一段文字作为新的项目符号项。
---

# FocusNote：添加到每日笔记中  
此功能可将用户提供的文本作为新的项目符号添加到 FocusNote 的每日笔记中。  

## 工作原理  
1. 从 `~/.lucia/documents-path.txt` 文件中读取 FocusNote 文档的路径。  
2. 生成当前日期（格式为 `YYYY-MM-DD`）。  
3. 查找或创建今天的每日笔记。  
4. 将用户提供的文本作为新的项目符号添加到笔记中。  
5. 更新笔记的 JSON 结构文件。  

## 先决条件  
- FocusNote 应用程序必须正在运行（它在启动时会创建 `~/.lucia/documents-path.txt` 文件）。  
- 需要安装 Node.js 以运行辅助脚本。  

## 实现步骤  
当用户请求将文本添加到每日笔记中时，请按照以下步骤操作：  

### 第 1 步：读取文档路径  
```javascript
const fs = require("fs");
const path = require("path");
const os = require("os");

// Read the documents path from FocusNote's config file
const focusnoteConfigPath = path.join(
  os.homedir(),
  ".lucia",
  "documents-path.txt",
);
const documentsPath = fs.readFileSync(focusnoteConfigPath, "utf-8").trim();
```  

### 第 2 步：生成当前日期  
```javascript
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, "0");
const day = String(today.getDate()).padStart(2, "0");
const todayDocName = `${year}-${month}-${day}`;
```  

### 第 3 步：查找每日笔记文件夹  
```javascript
const dailyNotePath = path.join(documentsPath, "notes", todayDocName);
const structurePath = path.join(dailyNotePath, "_structure.json");
const metadataPath = path.join(dailyNotePath, "_metadata.json");
const nodesDir = path.join(dailyNotePath, ".nodes");
```  

### 第 4 步：如果笔记不存在，则创建笔记  
```javascript
if (!fs.existsSync(dailyNotePath)) {
  // Create directory structure
  fs.mkdirSync(dailyNotePath, { recursive: true });
  fs.mkdirSync(nodesDir, { recursive: true });

  // Create metadata
  const metadata = {
    name: todayDocName,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));

  // Create empty structure
  const structure = {
    rootNodeIds: [],
    deletedNodeIds: [],
    nodes: {},
  };
  fs.writeFileSync(structurePath, JSON.stringify(structure, null, 2));
}
```  

### 第 5 步：创建新的项目符号  
```javascript
const { v4: uuidv4 } = require("uuid"); // npm install uuid

// Generate unique node ID
const nodeId = uuidv4();
const timestamp = Date.now();

// Create Lexical bullet structure
const lexicalContent = {
  root: {
    children: [
      {
        children: [
          {
            children: [
              {
                detail: 0,
                format: 0,
                mode: "normal",
                style: "",
                text: userText, // The text from the user
                type: "text",
                version: 1,
              },
            ],
            direction: "ltr",
            format: "",
            indent: 0,
            type: "listitem",
            version: 1,
            value: 1,
          },
        ],
        direction: "ltr",
        format: "",
        indent: 0,
        type: "list",
        version: 1,
        listType: "bullet",
        start: 1,
        tag: "ul",
      },
    ],
    direction: "ltr",
    format: "",
    indent: 0,
    type: "root",
    version: 1,
  },
};

// Create node object
const newNode = {
  id: nodeId,
  content: JSON.stringify(lexicalContent),
  isFolded: false,
  isTodo: false,
  isDone: false,
  isInProgress: false,
  isBlurred: false,
  backgroundColor: null,
  createdAt: timestamp,
  updatedAt: timestamp,
};
```  

### 第 6 步：将项目符号保存到分片目录中  
```javascript
// Shard by first 2 characters of node ID
const shard = nodeId.substring(0, 2);
const shardDir = path.join(nodesDir, shard);

if (!fs.existsSync(shardDir)) {
  fs.mkdirSync(shardDir, { recursive: true });
}

const nodeFilePath = path.join(shardDir, `node-${nodeId}.json`);
fs.writeFileSync(nodeFilePath, JSON.stringify(newNode, null, 2));
```  

### 第 7 步：更新结构文件  
```javascript
// Read current structure
const structure = JSON.parse(fs.readFileSync(structurePath, "utf-8"));

// Add node to structure
structure.rootNodeIds.push(nodeId);
structure.nodes[nodeId] = {
  parentId: null,
  orderIndex: structure.rootNodeIds.length - 1,
  childIds: [],
};

// Update timestamp
structure.updatedAt = timestamp;

// Save updated structure
fs.writeFileSync(structurePath, JSON.stringify(structure, null, 2));
```  

### 完整脚本示例  
以下是一个可使用的完整 Node.js 脚本：  
```javascript
#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const os = require("os");
const { v4: uuidv4 } = require("uuid");

function addToDailyNote(userText) {
  try {
    // Step 1: Read documents path
    const focusnoteConfigPath = path.join(
      os.homedir(),
      ".lucia",
      "documents-path.txt",
    );
    if (!fs.existsSync(focusnoteConfigPath)) {
      throw new Error(
        "FocusNote config file not found. Make sure FocusNote is running.",
      );
    }
    const documentsPath = fs.readFileSync(focusnoteConfigPath, "utf-8").trim();

    // Step 2: Generate today's date
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    const todayDocName = `${year}-${month}-${day}`;

    // Step 3: Set up paths
    const dailyNotePath = path.join(documentsPath, "notes", todayDocName);
    const structurePath = path.join(dailyNotePath, "_structure.json");
    const metadataPath = path.join(dailyNotePath, "_metadata.json");
    const nodesDir = path.join(dailyNotePath, ".nodes");

    // Step 4: Create daily note if needed
    if (!fs.existsSync(dailyNotePath)) {
      fs.mkdirSync(dailyNotePath, { recursive: true });
      fs.mkdirSync(nodesDir, { recursive: true });

      const metadata = {
        name: todayDocName,
        createdAt: Date.now(),
        updatedAt: Date.now(),
      };
      fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));

      const structure = {
        rootNodeIds: [],
        deletedNodeIds: [],
        nodes: {},
      };
      fs.writeFileSync(structurePath, JSON.stringify(structure, null, 2));
    }

    // Step 5: Create new bullet node
    const nodeId = uuidv4();
    const timestamp = Date.now();

    const lexicalContent = {
      root: {
        children: [
          {
            children: [
              {
                children: [
                  {
                    detail: 0,
                    format: 0,
                    mode: "normal",
                    style: "",
                    text: userText,
                    type: "text",
                    version: 1,
                  },
                ],
                direction: "ltr",
                format: "",
                indent: 0,
                type: "listitem",
                version: 1,
                value: 1,
              },
            ],
            direction: "ltr",
            format: "",
            indent: 0,
            type: "list",
            version: 1,
            listType: "bullet",
            start: 1,
            tag: "ul",
          },
        ],
        direction: "ltr",
        format: "",
        indent: 0,
        type: "root",
        version: 1,
      },
    };

    const newNode = {
      id: nodeId,
      content: JSON.stringify(lexicalContent),
      isFolded: false,
      isTodo: false,
      isDone: false,
      isInProgress: false,
      isBlurred: false,
      backgroundColor: null,
      createdAt: timestamp,
      updatedAt: timestamp,
    };

    // Step 6: Save node file
    const shard = nodeId.substring(0, 2);
    const shardDir = path.join(nodesDir, shard);

    if (!fs.existsSync(shardDir)) {
      fs.mkdirSync(shardDir, { recursive: true });
    }

    const nodeFilePath = path.join(shardDir, `node-${nodeId}.json`);
    fs.writeFileSync(nodeFilePath, JSON.stringify(newNode, null, 2));

    // Step 7: Update structure
    const structure = JSON.parse(fs.readFileSync(structurePath, "utf-8"));
    structure.rootNodeIds.push(nodeId);
    structure.nodes[nodeId] = {
      parentId: null,
      orderIndex: structure.rootNodeIds.length - 1,
      childIds: [],
    };
    structure.updatedAt = timestamp;
    fs.writeFileSync(structurePath, JSON.stringify(structure, null, 2));

    console.log(`✅ Added bullet to ${todayDocName}: "${userText}"`);
    return { success: true, documentName: todayDocName, nodeId };
  } catch (error) {
    console.error("❌ Error adding to daily note:", error.message);
    return { success: false, error: error.message };
  }
}

// Example usage
if (require.main === module) {
  const userText = process.argv.slice(2).join(" ") || "New bullet point";
  addToDailyNote(userText);
}

module.exports = { addToDailyNote };
```  

## 使用示例  
**用户：**“在我的每日笔记中添加：已完成 OpenClaw 技能的实现。”  
**助手：**我会将该内容添加到您的每日笔记中。  
**输出：** ✅ 已将项目符号 “已完成 OpenClaw 技能的实现。” 添加到 2026-02-11 的笔记中。  

**用户：**“添加一个提醒，明天给妈妈打电话。”  
**助手：**我会将该提醒添加到今天的笔记中。  
**输出：** ✅ 已将提醒 “明天给妈妈打电话” 添加到今天的笔记中。  

## 安装方法  
1. 将脚本保存为 `add-to-daily-note.js`，并放在 OpenClaw 技能目录中。  
2. 安装依赖项：`npm install uuid`。  
3. 使脚本可执行：`chmod +x add-to-daily-note.js`。  

## 注意事项  
- 每次调用此功能时，都会创建一个新的项目符号。  
- 项目符号会添加到每日笔记的末尾。  
- 如果每日笔记不存在，系统会自动创建它。  
- 确保 FocusNote 应用程序正在运行，以便 `documents-path.txt` 文件存在。  
- 更改内容会立即在 FocusNote 中显示。  

## 故障排除  
- **错误：“未找到 FocusNote 配置文件”**：  
  确保 FocusNote 正在运行，并检查 `~/.lucia/documents-path.txt` 文件是否存在。  
- **项目符号未显示在 FocusNote 中**：  
  尝试关闭并重新打开每日笔记；确认节点文件已正确创建在 `.nodes/` 目录中；验证 `_structure.json` 文件是否已更新。
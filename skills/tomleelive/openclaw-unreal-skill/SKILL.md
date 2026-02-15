# OpenClaw Unreal插件  
版本：1.0.0  

这是一个用于通过OpenClaw控制Unreal Engine编辑器的MCP（Media Control Protocol）插件。  

## 连接模式  

### 模式A：OpenClaw Gateway（远程）  
该插件通过HTTP轮询连接到OpenClaw Gateway。当Gateway正在运行时，插件会自动进行连接。  

### 模式B：MCP直接连接（Claude代码/光标）  
该插件会在端口**27184**上运行一个内嵌的HTTP服务器。请使用随附的MCP桥接工具进行连接：  

```bash
# Claude Code
claude mcp add unreal -- node /path/to/Plugins/OpenClaw/MCP~/index.js

# Cursor — add to .cursor/mcp.json
{"mcpServers":{"unreal":{"command":"node","args":["/path/to/Plugins/OpenClaw/MCP~/index.js"]}}}
```  

这两种模式可以同时运行。  

## 编辑器面板  
点击“窗口 → OpenClaw Unreal插件”会打开一个可停靠的标签页，其中包含以下内容：  
- 连接状态指示器  
- MCP服务器信息（地址、协议）  
- 连接/断开连接按钮  
- 工具调用和消息的实时日志  

## 工具  

### 地图（Level）  
- `level.getCurrent`：当前地图的名称  
- `level.list`：项目中的所有地图  
- `level.open`：按名称打开地图  
- `level.save`：保存当前地图  

### 角色（Actor）  
- `actor.find`：按名称或类别查找角色  
- `actor.getAll`：列出所有角色  
- `actor.create`：创建角色（类型包括：StaticMeshActor（立方体、球体、圆柱体、圆锥体）、PointLight、Camera）  
- `actor.delete`：按名称删除角色  
- `actor.getData`：获取角色的详细信息  
- `actor.setProperty`：通过UE反射系统设置角色属性  

### 变换（Transform）  
- `transform.position` / `transform.setPosition`：设置/获取角色的位置  
- `transform.rotation` / `transform.setRotation`：设置/获取角色的旋转  
- `transform.scale` / `transform.setScale`：设置/获取角色的缩放比例  

> 这些变换工具需要一个有效的RootComponent（适用于StaticMeshActor、PointLight等对象，不适用于单独的Actor）。  

### 组件（Component）  
- `component.get`：获取组件的数据  
- `component.add`：添加组件（尚未实现）  
- `component.remove`：删除组件（尚未实现）  

### 编辑器（Editor）  
- `editor.play`：启动Play In Editor（ PIE）模式  
- `editor.stop`：停止Play In Editor模式  
- `editor.pause` / `editor.resume`：暂停/恢复Play In Editor模式  
- `editor.getState`：获取当前的编辑器状态  

### 调试（Debug）  
- `debug.hierarchy`：显示角色的层次结构树  
- `debug.screenshot`：捕获编辑器视图窗口的截图  
- `debug.log`：将信息写入输出日志  

### 输入（Input）  
- `input.simulateKey`：模拟按键操作  
- `input.simulateMouse`：模拟鼠标操作  
- `input.simulateAxis`：模拟轴的移动  

### 资产（Asset）  
- `asset.list`：列出指定路径下的所有资产  
- `asset.import`：导入资产（尚未实现）  

### 控制台（Console）  
- `console.execute`：执行控制台命令  
- `console.getLogs`：读取项目日志文件（参数：`count`（日志行数）、`filter`（过滤条件）  

###蓝图（Blueprint）  
- `blueprint.list`：列出所有的蓝图  
- `blueprint.open`：打开蓝图（尚未实现）  

## 故障排除  

### 二进制文件过期或插件无法加载  
请清除构建缓存并重新启动编辑器：  
```bash
rm -rf YourProject/Plugins/OpenClaw/Binaries YourProject/Plugins/OpenClaw/Intermediate
```  

### 连接问题  
- 确保OpenClaw Gateway正在运行（使用`openclaw gateway status`命令检查）。  
- 查看编辑器面板中的日志以获取错误信息。  
- 确保MCP端口没有被防火墙阻止。
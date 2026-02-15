# 插件架构技能（Plugin Architecture Skill）

**名称：** plugin-architecture  
**版本：** 1.1.0  
**作者：** Charles Sears  
**描述：** 为 OpenClaw 添加了 UI 插件注册功能，允许插件在控制界面（Control UI）中注册自定义标签页。

## 概述  
该技能使 OpenClaw 插件能够注册自定义的 UI 视图/标签页，这些标签页会显示在控制仪表板的侧边栏中。

## 安装说明  
**此技能需要由您的 OpenClaw 代理手动安装。**  
将此技能文件解压到您的技能文件夹（skills folder）后，向代理发送以下命令：  
```
Please install the plugin-architecture skill. Read the INSTALL_INSTRUCTIONS.md file in the skill folder and follow it step by step. The skill is at: ~/clawd/skills/plugin-architecture/
```  

## 功能说明  
安装完成后，插件可以如下方式注册 UI 标签页：  
```typescript
// In your plugin's register() function:
if (typeof api.registerView === "function") {
  api.registerView({
    id: "my-view",
    label: "My View",
    subtitle: "Description here",
    icon: "database",  // Icon name from the icon set
    group: "Agent",    // Which nav group (Chat, Control, Agent, Settings)
    position: 5,       // Order within the group
  });
}
```  

## 包含的文件：  
- `SKILL.md` – 本技能文件  
- `INSTALL_INSTRUCTIONS.md` – 代理的安装步骤指南  
- `reference/` – 参考代码文件，展示了需要添加的内容
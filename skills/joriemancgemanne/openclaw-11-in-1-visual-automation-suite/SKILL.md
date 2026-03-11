## OpenClaw 11-in-1 视觉自动化套件（仅支持 Windows）  
一个集成了11个模块的完整视觉自动化工具包。  

### 💰 价格  
一次性购买：**2.99美元**（终身访问所有模块及未来更新）  

### 🚀 购买方式  
1. 通过 PayPal 发票支付：  
   🔗 [点击支付 2.99美元](https://www.paypal.com/invoice/p/#V2RC9S8LVKJ434R9)  
2. 支付完成后，请发送电子邮件至：**1215066513@qq.com**  
3. 我将在12小时内发送完整的下载链接。  

### 🖥️ 兼容性  
- 仅支持 Windows 10 / 11  
- 不兼容 macOS / Linux  

### 1. 产品基本描述  
#### 1.1 核心功能  
提供专业的通用计算机视觉自动化功能，涵盖从环境初始化到全屏自动截图、OCR文本识别、模板匹配、目标定位、鼠标点击模拟、键盘输入模拟等全流程的视觉自动化场景。支持自定义任务组合和循环执行。  

#### 1.2 版本与目录结构  
- **核心功能**：基于最小可执行单元进行灵活调用，支持参数自定义、结果变量继承以及自定义技能的保存。提取软件包后，可以直接使用 `call` 命令来使用所有功能。  
- **目录结构**：  
  - `claw.json`：技能包配置文件  
  - `skills/all_skills.claw`：所有技能单元的定义  
  - `templates/`：模板图片存放目录（请将模板图片放入此处）  
  - 执行 `init_env` 命令后会自动创建临时文件目录 `temp/`（用于存储截图，如 `temp/screen.png`）；可以通过 `clean_temp` 命令清理临时截图文件。  
  - 当前版本：1.0.0；兼容 OpenClaw 1.0.0 及更高版本。  

### 1.3 付费说明  
该自动化工具包（vision-auto-tool-pro）为付费专业工具。文档未明确授权其商业用途；仅限非商业用途。如需商业使用，需另行获得提供商的授权（例如购买商业许可证或签署商业协议）。  

### 2. 完整的技能调用手册  
#### 重要提示  
请确保为每次操作预留足够的系统响应时间。例如，在执行 `mouse_click` 后添加2秒的等待时间，以避免因系统响应缓慢导致操作失败。  

#### 2.1 所有最小可执行单元列表  
| 单元名称                | 固定调用名称            | 功能描述                                                                 | 单独调用方法                                      |  
|-------------------------|--------------------------|--------------------------------------------------------------------------------------|-------------------------------------------------|  
| 初始化环境              | `init_env`              | 创建目录结构、清理临时文件、检查模板目录                                      | `call init_env`                                      |  
| 全屏截图              | `screenshot_full`          | 截取整个屏幕并保存为 `temp/screen.png`                                      | `call screenshot_full`                                      |  
| 检查截图有效性          | `check_screenshot_valid`       | 检查屏幕是否为黑屏或冻结状态；无效时唤醒界面                              | `call check_screenshot_valid`                              |  
| 唤醒界面              | `wake_window`            | 解决背景未渲染或屏幕显示为黑屏的问题                                  | `call wake_window`                                      |  
| OCR识别              | `ocr_recognize`          | 识别屏幕上的所有文本及其坐标                                      | `call ocr_recognize`                                      |  
| 模板匹配              | `template_match`          | 使用模板图片进行图标/按钮定位                                      | `call template_match category template_name`                      |  
| 统一定位              | `locate_target`          | 首先尝试 OCR 定位；未找到时使用模板匹配；返回坐标                        | `call locate_target target_text OR category+template_name`                |  
| 鼠标点击              | `mouse_click`            | 移动到指定坐标并执行点击操作                                      | `call mouse_click X Y [click_type, default=single_click]`                |  
| 键盘输入              | `keyboard_input`          | 在找到输入框后输入文本                                      | `call keyboard_input target_coords/description input_content`            |  
| 清理临时文件            | `clean_temp`            | 删除临时截图以释放存储空间                                      | `call clean_temp`                                      |  
| 循环重启              | `loop_restart`            | 等待2秒后返回截图步骤并重新开始流程                                  | `call loop_restart`                                      |  

#### 2.2 单个单元的调用方法  
#### 调用格式  
```  
call [unit_call_name] [parameter...]  
```  
#### 调用示例  
- 初始化环境：`call init_env`  
- 在桌面上匹配浏览器图标：`call template_match desktop web`  
- 在坐标 (100, 200) 处双击：`call mouse_click 100 200 double`  

#### 2.3 组合成自定义任务  
通过按执行顺序逐行编写调用指令，可以组合成自定义任务。该系统支持变量继承、循环执行以及技能的永久保存。  

#### 格式示例（打开浏览器）  
```  
# 任务名称：打开浏览器  
call init_env  
call screenshot_full  
call check_screenshot_valid  
call locate_target browser desktop Browser  
call mouse_click {{resultX}} {{resultY}} double  
call clean_temp  
```  

#### 组合步骤  
1. **先编写任务名称和描述**（便于后续识别）  
2. **按执行顺序**，每行编写一个 `call unit_name parameters` 的指令  
3. 坐标可以使用变量 `{{resultX}}`/`{{resultY}}` 来继承前一个单元的输出结果  
4. 如需循环执行，在末尾添加 `call loop_restart`  
5. **保存自定义技能**：使用 `save_skill skill_name instruction_list` 永久保存任务，之后可通过 `call skill_name` 直接调用该任务  

#### 2.4 完整的主流程示例  
```  
# 常见主流程：vision_auto_main  
call init_env  
call screenshot_full  
call check_screenshot_valid  
call ocr_recognize  
# 如需模板匹配，添加以下代码：call template_match category name  
call locate_target target_text  
call mouse_click {{X}} {{Y}}  
# 如需输入文本，替换为：call keyboard_input {{X}} {{Y}} input_content  
call clean_temp  
# 如需循环执行，添加以下代码：call loop_restart  
```  

#### 重要提示  
请确保为每次操作预留足够的系统响应时间。例如，在执行 `mouse_click` 后添加2秒的等待时间，以避免因系统响应缓慢导致操作失败。
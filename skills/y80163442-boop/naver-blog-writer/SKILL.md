# Naver Blog 发布工具

该工具允许用户从经过身份验证的本地浏览器中，将准备好的内容发布到 Naver Blog 上。

**适用场景：**  
- `naverpublish`  
- `naverblogpublish`  
- `koreanblogpublish`  

**首次使用流程：**  
1. 执行 `doctor -> setup -> dry_run`  
2. 完成登录操作  
3. 执行 `live` 命令  

**系统要求：**  
- **macOS**  

**使用场景说明：**  
- 当用户已有最终内容，并需要使用 `naverpublish`、`naverblogpublish` 或 `koreanblogpublish` 功能时；  
- 当 OpenClaw 代理需要一个可靠的发布接口（而非用于内容创作或 SEO 规划的工具）时；  
- 当用户可以在本地 Mac 上运行该工具并完成一次性登录操作时。  

**不适用场景：**  
- 当用户需要从零开始起草内容时；  
- 当当前环境无法运行本地发布工具时；  
- 当任务仅涉及研究、SEO 规划或主题构思时。  

**输入参数：**  
- `TITLE`（标题）  
- `BODY`（正文内容）  
- 可选参数：`TAGS`（标签）  
- 可选参数：`PUBLISH_AT`（发布时间）  

**输出结果：**  
- **实时发布结果**：`naver_publish_result`  
- **预览结果**：`dry_run` 的执行结果，包含生成的 `published_url`  
- **系统状态检查**：`doctor/capabilities` 的 JSON 数据  

**故障处理信息：**  
在发生故障时，系统会返回以下关键信息：  
- `error`（错误代码）  
- `next_action`（后续操作建议）  
- `setup_command`（设置命令）  
- `login_command`（登录命令）  
- `hint`（故障提示）  
- `estimated_minutes`（预计完成时间）  

**配置参数：**  
- `OPENCLAW_OFFERING_ID`（默认值：`naver-blog-writer`）  
- `SETUP_URL` 或 `PROOF_TOKEN + SETUP_ISSUE_URL`  
- 推荐使用 `OPENCLAW_OFFERING_EXECUTE_URL`  
- 备用方案：`CONTROL_PLANE_URL + ACP_ADMIN_API_KEY`  
- `X_LOCAL_TOKEN`（可选参数，自动从 `~/.config/naver-thin-runner/config.json` 文件加载）  
- `LOCAL_DAEMON_PORT`（默认值：`19090`）  

**工作流程：**  
1. 执行 `doctor/capabilities` 命令以检查系统是否准备好使用。  
2. 如果系统未准备好，执行 `setup` 命令进行配置。  
3. 执行 `publish_dry_run` 命令进行预览。  
4. 如果需要登录，执行 `login_required` 命令完成一次性登录。  
5. 最后执行 `publish_live` 命令进行实时发布。  

**命令使用说明：**  
如果工具的相关文件已准备好，可以直接使用相应的命令。  

**配置文件示例：**  
（具体命令及配置文件内容请参见相关文档。）  

**注意事项：**  
- 该工具仅用于内容发布，不支持内容创作功能。  
- 为保持兼容性，请将 `offering_id` 设置为 `naver-blog-writer`。  
- 用户的登录凭据和会话信息会保存在本地运行环境中。  
- 高级合同和接口规范文档详见 `docs/ACP_CONTRACT.md` 和 `docs/OFFERING_SCHEMA.md`。
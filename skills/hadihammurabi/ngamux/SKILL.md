---
name: ngamux
description: 使用 ngamux（一个为 Go 语言设计的简单 HTTP 路由器）来构建和修改 Web 服务。定义路由、应用中间件、处理请求，并高效地发送响应。
---
## 何时使用此技能  
当用户需要执行以下操作时，请使用此技能：  
- **定义 HTTP 端点**：为各种 HTTP 方法创建新的路由（例如 `mux.Get("/users/:id", getUserHandler)`），包括动态路径段（`/users/{id}`）和通配符（`/files/*filePath`）。  
- **实现请求预处理/后处理**：添加全局中间件（例如用于身份验证、日志记录、CORS）或特定组别的中间件，以在请求到达主处理函数之前或处理之后对其进行处理。例如 `mux.Use(authMiddleware)` 或 `apiGroup.Use(loggingMiddleware)`。  
- **从请求中提取数据**：  
  - **URL 参数**：从动态路径段中获取值（例如 `req.Params("id")`）。  
  - **查询参数**：访问查询字符串中的值（例如 `req.Query("name", "Guest")`）。  
  - **表单数据**：解析 `application/x-www-form-urlencoded` 或 `multipart/form-data` 格式的表单数据（例如 `req.FormValue("username")`、`req.FormFile("image")`）。  
  - **JSON 标签数据**：将 `application/json` 格式的请求体解码为 Go 结构体（例如 `req.JSON(&user)`）。  
- **构造并发送不同类型的响应**：  
  - **JSON 响应**：以 JSON 格式发送结构化数据（例如 `ngamux.Res(rw).Status(http.StatusOK).Json(data)`）。  
  - **文本响应**：发送纯文本（例如 `ngamux.Res(rw).Status(http.StatusOK).Text("Hello, World!")`）。  
  - **HTML 响应**：渲染 HTML 模板（例如 `ngamux.Res(rw).Status(http.StatusOK).HTML("template.html", data)`）。  
  - **自定义状态码**：为响应设置特定的 HTTP 状态码。  
- **配置路由器行为**：调整全局设置，如自动删除路径末尾的斜杠（`ngamux.WithTrailingSlash()`）、设置日志记录的详细程度（`ngamux.WithLogLevel(slog.LevelDebug)`），或为特定的序列化需求提供自定义的 `json.Marshal`/`json.Unmarshal` 函数。  
- **使用分组组织路由**：创建嵌套的路由组，以便将相同的路径前缀和中间件应用于一组路由（例如 `/api/v1`）。  
- **调试路由或处理函数问题**：检查路由定义、中间件链、请求上下文和日志输出，以诊断和解决问题。  

## 主要功能  
- **路由定义**：`ngamux` 提供了 `mux.Get()`、`mux.Post()`、`mux.Put()`、`mux.Delete()`、`mux.Patch()`、`mux.Head()` 和 `mux.All()` 等方法，用于为特定的 HTTP 方法和路径注册 `http.HandlerFunc`。它支持路径参数（例如 `/{id}`）和通配符（`/*filePath`）。路由通过树状结构高效存储和匹配，利用 `mapping` 包实现优化的键值存储。  
- **中间件应用**：`mux.Use()` 方法允许注册全局中间件，而 `mux.Group()` 和 `mux.With()` 可以实现特定组别的中间件。中间件是 `MiddlewareFunc` 类型，用于包装 `http.HandlerFunc`，从而支持责任链模式。`common.go` 中的 `WithMiddlewares` 工具用于处理中间件的链式调用。  
- **请求处理**：`Request` 结构体（封装了 `*http.Request`）提供了便捷的方法：  
  - `Req().Params(key string)`：获取路由过程中解析的 URL 路径参数。  
  - `Req().Query(key string, fallback ...string)`：访问 URL 查询字符串参数。  
  - `Req().QueriesParser(data any)`：使用 `query` 标签和反射自动将查询参数绑定到 Go 结构体。  
  - `Req().FormValue(key string)`：获取表单字段的值。  
  - `Req().FormFile(key string, maxFileSize ...int64)`：处理来自多部分表单的文件上传。  
  - `Req().JSON(store any)`：将 JSON 请求体解码为提供的 Go 接口。  
  - `Req().Locals(key any, value ...any)`：管理请求上下文中的数据。  
- **响应处理**：`Response` 结构体（封装了 `http.ResponseWriter`）提供了构建响应的便捷 API：  
  - `Res(rw).Status(code int)`：设置 HTTP 状态码。  
  - `Res(rw).Text(data string)`：发送纯文本内容。  
  - `Res(rw).JSON(data any)`：使用配置的 JSON 解码器发送 JSON 内容。  
  - `Res(rw).HTML(path string, data any)`：使用 `html/template` 渲染 HTML 模板。  
- **配置**：全局配置选项通过 `ngamux.New()` 设置，还可以使用 `ngamux.WithTrailingSlash()` 和 `ngamux.WithLogLevel()` 等功能选项进行配置。可以提供自定义的 JSON 序列化/反序列化功能。  
- **路由分组**：`mux.Group(path string)` 和 `mux.GroupFunc(path string, router func(mux *Ngamux)` 方法允许分层组织路由，子组可以继承路径前缀并应用自己的中间件，从而实现更清晰的代码组织和共享逻辑。
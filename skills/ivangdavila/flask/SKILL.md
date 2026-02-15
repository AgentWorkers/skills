---
name: Flask
description: 避免常见的 Flask 错误：上下文错误（context errors）、循环导入（circular imports）、会话配置问题（session configuration issues），以及在生产环境中可能遇到的其他陷阱（production gotchas）。
metadata: {"clawdbot":{"emoji":"🍶","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## 应用上下文（Application Context）
- `current_app` 仅在请求内部有效，或在使用 `app.app_context()` 时有效；在应用上下文之外使用会导致错误。
- `g` 是用于存储请求级数据的变量，请求结束后会丢失，通常用于数据库连接。
- 后台任务需要应用上下文，因此应使用 `with app.app_context()` 来执行，或者通过其他方式传递数据，而不是通过代理。

## 请求上下文（Request Context）
- `request` 和 `session` 仅在请求内部有效；在请求上下文之外使用会导致错误。
- `url_for` 需要应用上下文才能正确工作。例如，要生成绝对路径，需要使用 `url_for('static', filename='x', _external=True)`。
- 测试客户端会自动提供上下文；但对于非请求相关的代码，需要手动设置上下文。

## 循环导入（Circular Imports）
- 在模型文件中直接使用 `from app import app` 会导致循环导入问题。应使用工厂模式（factory pattern）来避免这种情况。
- 如果需要在函数内部动态导入某个模块，可以使用 `current_app`。
- 使用蓝图（blueprints）可以帮助更好地组织代码结构；应在工厂模式（factory pattern）注册蓝图，而不是在代码执行时导入。

## 会话（Sessions）与安全性（Security）
- 使用会话时必须设置 `SECRET_KEY`，该密钥应为随机生成的字节串，而不是简单的字符串。
- 如果未设置 `SECRET_KEY`，则会导致未签名的会话cookie，任何人都可以伪造会话数据。
- 在生产环境中应设置 `SESSION_COOKIESecure=True`，以确保会话数据仅通过 HTTPS 传输。
- 设置 `SESSION_COOKIE_HTTPONLY=True` 可以防止 JavaScript 访问会话数据。

## 调试模式（Debug Mode）
- 在生产环境中将 `debug` 设置为 `True` 会导致远程代码执行，这可能会被攻击者利用。建议通过环境变量 `FLASK_DEBUG` 来控制调试模式，而不是硬编码。
- 如果启用了调试模式，日志中会显示调试 PIN 码；虽然这提供了一定程度的安全性，但仍存在风险。

## 蓝图（Blueprints）
- 可以在注册蓝图时设置路由前缀：`app.register_blueprint(bp, url_prefix='api')`。
- 路由地址相对于前缀进行解析：例如，`@bp.route('/users')` 实际上表示 `/api/users`。
- `blueprint.before_request` 函数仅对该蓝图有效；`app.before_request` 则对所有蓝图都有效。

## SQLAlchemy 集成（SQLAlchemy Integration）
- 应明确调用 `db.session.commit()` 来提交数据库操作；默认情况下，Flask-SQLAlchemy 会自动提交事务。
- 会话的范围是请求级别的；后台任务需要独立的会话。
- 如果使用不同的会话创建对象，可能会出现错误，此时需要重新获取或合并数据。
- 在发生错误时应调用 `db.session.rollback()`，以防止会话状态异常。

## 生产环境（Production Environment）
- 开发服务器使用 `flask run`；在生产环境中应使用 `Gunicorn` 或 `uWSGI`。
- 开发服务器默认支持多线程（`threaded=True`），但这并不意味着已经完全适应生产环境。
- 静态文件应通过 Nginx 服务器提供；直接使用 Flask 服务器提供静态文件效率较低。
- 设置 `PROPAGATE_EXCEPTIONS=True` 可以确保异常能够被 Sentry 等监控工具正确处理。

## 常见错误（Common Mistakes）
- 在返回重定向时，应使用 `return redirect('/login')` 而不是 `return redirect(url_for('login'))`；`url_for` 更易于维护和重构。
- JSON 响应应使用 `return jsonify(data)`，而不是 `return json.dumps(data)`。
- 表单数据存储在 `request.form` 中；JSON 数据应存储在 `request.json` 或通过 `request.get_json()` 获取。
- 查询参数应通过 `request.args` 获取，例如：`request.args.get('page', default=1, type=int)`。
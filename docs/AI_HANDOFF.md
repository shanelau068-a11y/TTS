# TTS：项目运行与AI接手

声场TTS工作台：浏览器试听、自配兼容语音API，以及可选的FastAPI/Edge TTS后端。

## 仓库身份

- 分类：视频与语音；类型：python。
- 默认分支：`main`；当前可见性：公开。
- 本说明针对本仓库当前文件；历史本机绝对路径与相似项目不能作为当前运行位置。

## 先读这些文件

- [index.html](<../index.html>)
- [server/app.py](<../server/app.py>)
- [server/requirements.txt](<../server/requirements.txt>)
- [Dockerfile](<../Dockerfile>)

## 安装和启动

```powershell
python -m pip install -r server/requirements.txt
python -m uvicorn server.app:app --host 127.0.0.1 --port 8000
```

前端单独通过python -m http.server 8001 --bind 127.0.0.1打开；页面填后端地址http://127.0.0.1:8000。




## 数据与搬迁

声音、文本和API配置依页面实际存储处理；GitHub Pages仅提供前端，不能直接执行Python。

## 怎么验证

先执行 [验证记录](VERIFICATION.md) 所列命令，再按改动检查实际页面或输出。没有测试脚本时不能把占位npm test当作通过。仅文档更改检查链接和路径；涉及数据、几何、金额或接口的修改运行相应回归测试。

- 本轮后端路由可加载，未调用Edge服务或收费语音API；外部音色和可用性需实际请求确认。

## 继续维护

先读根目录AGENTS.md；若它是CLAUDE.md的链接则直接读后者。保留已有项目约定。修改前确认分支、当前差异、数据目录与实际服务。完成后更新本说明/验证记录，提交明确的源码和文档路径，并核对GitHub远端提交。公开状态、旧版、URL与业务数据需按用户既有约定保持。

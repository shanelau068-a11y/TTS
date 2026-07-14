# 声场 TTS 工作台

GitHub Pages 前端 + 可选微软 Edge TTS 后端，适合做对话和广播剧。

## 功能

- 浏览器内置语音免费试听
- 兼容 OpenAI `POST /v1/audio/speech` 的 API：地址、密钥、模型、音色、语速均可在页面填写
- Microsoft Edge 免费 MP3：旁白/多角色音色、语速、音调、`【角色】台词` 与 `*动作旁白*` 解析
- 长文按句拆分；API 模式以交叉淡化合为 WAV，Edge 模式连续输出 MP3

## 前端发布

GitHub Pages 网址为 `https://shanelau068-a11y.github.io/TTS/`。密钥只由浏览器直接发往你填写的 API，不会由网页保存或转发。

## 启用免费的微软 Edge 下载

GitHub Pages 不能运行 Python，所以 Edge 模式需要部署本仓库的 `server/`。仓库含 `Dockerfile` 与 `render.yaml`，可连接 Render 的 GitHub 部署（或在本机执行以下命令）：

```bash
pip install -r server/requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

部署后，将网页「微软 Edge 后端网址」填为该服务公开地址；本机运行则保持 `http://127.0.0.1:8000`。

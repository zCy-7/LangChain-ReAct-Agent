from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest
from agent.react_agent import ReactAgent

# 初始化FastAPI
app = FastAPI(title="小小怪扫地机器人智能客服 API")

# 跨域，前端对接必备
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # 允许哪些来源访问, * -->允许所有前端地址跨域访问接口
    allow_credentials=True,           # 是否允许携带Cookie/凭证
    allow_methods=["*"],              # 允许哪些请求方式(GET/POST等)
    allow_headers=["*"],              # 允许前端传递哪些请求头
)
"""
CORSMiddleware（跨域中间件）
如果网页地址 和 请求接口地址 协议、域名、端口任意一个不一样，就是跨域请求。
浏览器默认会拦截跨域 HTTP 请求，防止恶意网站窃取数据。
Streamlit 网页：http://127.0.0.1:8501
FastAPI 后端接口：http://127.0.0.1:8000
端口不一样 → 属于跨域
不加这段代码，浏览器会直接拦截 Streamlit 发起的接口调用。
"""

# 全局单例Agent，只初始化一次（和streamlit session_state逻辑一致）
agent = ReactAgent()


# SSE流式对话接口（推荐，对应streamlit流式效果）
@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="query不能为空")

    def stream_generator():
        # 和 st.session_state["agent"].execute_stream(prompt) 完全一致
        chunk_generator = agent.execute_stream(query)
        full_text = ""
        for chunk in chunk_generator:
            full_text += chunk
            # SSE标准格式
            yield f"data: {chunk}\n\n"
        # 流结束标记
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_generator(),
        # media_type="text/event-stream",
        media_type="text/plain"
    )


# 普通一次性返回接口（非流式，备用）
@app.post("/api/chat")
async def chat_normal(req: ChatRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="query不能为空")

    full_resp = ""
    for chunk in agent.execute_stream(query):
        full_resp += chunk

    return {
        "code": 200,
        "msg": "success",
        "data": full_resp
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

# 启动命令
# uvicorn main:app --host 127.0.0.1 --port 8000 --log-level debug

# {
#   "code": 200,
#   "msg": "success",
#   "data": "扫地机器人进水了怎么处理\n遇到扫地机器人进水的情况，首先需要立即断开电源，避免短路造成更大的损坏。接下来，为了提供更具体的处理步骤和建议，我将调用rag_summarize工具来获取关于扫地机器人进水后正确处理的专业指导信息。\n如果扫地机器人不慎进水，应立即断开电源，并尽快将机器内部水分清除干净。可以使用干布擦拭外部，并放置于通风处自然晾干。对于内部组件，建议不要自行拆解处理，以免造成进一步损坏，最好联系专业维修人员进行检查和修理。\n扫地机器人不慎进水后，请按照以下步骤处理：\n\n1. 立即断开电源，避免发生短路。\n2. 使用干布仔细擦拭机器外部，尽可能去除表面水分。\n3. 将扫地机器人放置在通风良好的地方自然晾干。\n4. 对于内部组件，请勿自行拆解尝试干燥或修理，因为这可能会导致进一步的损坏。最好的做法是联系专业的维修服务进行检查和必要的修复工作。\n\n遵循上述建议有助于减少因进水对扫地机器人造成的损害，并确保设备能够安全恢复使用。如果您的机器还在保修期内，请记得咨询官方客服获取更具体的保修服务信息。\n"
# }

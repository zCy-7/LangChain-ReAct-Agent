"""
Streamlit 作为客户端，通过 POST 请求调用你的 FastAPI 接口 http://127.0.0.1:8000/api/chat/stream
"""
import streamlit as st
import requests

# 后端接口地址
API_URL = "http://127.0.0.1:8000/api/chat/stream"

# 标题
st.title("小小怪扫地机器人智能客服")
st.divider()

# 只保存对话历史，不再初始化本地Agent
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好,有什么可以帮你?"}]
# 渲染历史对话
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    # 展示用户消息
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.spinner("智能客服思考中..."):
        # 请求体
        payload = {
            "query": prompt,
            # 如果需要把对话历史传给Agent，解开下面注释
            # "history": st.session_state["messages"]
        }
        # 开启流式请求
        resp = requests.post(url=API_URL, json=payload, stream=True, timeout=60)

        # streamlit原生流式渲染，同时收集完整文本
        def stream_generator(response_messages: list[str]):
            count = 0
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line == "[DONE]":
                    break
                if line.startswith("data: "):
                    # 一条新消息的开始行（带 data: 前缀）
                    line = line.removeprefix("data: ")
                    count += 1
                if count > 3:       # 过滤思考信息
                    response_messages.append(line)
                yield line


        response_messages = []
        with st.chat_message("assistant"):
            gen = stream_generator(response_messages)
            st.write_stream(gen)

        # 将回答存入历史消息
        if response_messages:
            st.session_state["messages"].append(
                {"role": "assistant", "content": "".join([text.replace("[DONE]", "")+"\n" for text in response_messages])}
            )

    # 重新运行脚本，刷新历史消息渲染
    st.rerun()

import time
import streamlit as st
from agent.react_agent import ReactAgent


# 标题
st.title("小小怪扫地机器人智能客服")
st.divider()    # 分割线

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好,有什么可以帮你?"}]
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入内容
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        resp_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    yield char

        st.chat_message("assistant").write_stream(capture(resp_stream, response_messages))
        st.session_state["messages"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()


import streamlit as st
from rag import RagService
import config
import time

st.title(body="智能客服")
st.divider()

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role':'assistant', 'content':'你好，有什么可以帮助你？'}]

if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService()

for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])

query = st.chat_input()

if query:
    st.chat_message('user').write(query)
    st.session_state['messages'].append({'role':'user', 'content':query})

    with st.spinner(text="AI思考中"):
        time.sleep(1)
        ai_res_list = []
        res = st.session_state['rag'].chain.stream(input={'input':query}, config=config.session_config)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message('assistant').write_stream(capture(res, ai_res_list))
        st.session_state['messages'].append({'role':"assistant", 'content':''.join(ai_res_list)})

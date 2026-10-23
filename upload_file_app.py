# 导包
import streamlit as st
import time
from knowledge_base import KnowledgeBase

# 网页标题
st.title(body="上传知识到知识库吧！")

# 分割线
st.divider()

# 上传知识入口
uploaded_file = st.file_uploader(
    label="请选择要上传的文件！（仅支持.txt文件）",
    type=['txt'],
    accept_multiple_files=False
)

# 创建知识库对象
if 'knowledge_base' not in st.session_state:
    st.session_state['knowledge_base'] = KnowledgeBase()

# 如果上传文件
if uploaded_file is not None:
    # 展示文件信息
    # print(uploaded_file)
    file_name=uploaded_file.name
    file_type=uploaded_file.type
    file_size=uploaded_file.size / 1024
    st.subheader(body=f"文件名：{file_name}")
    st.write(f"文件类型：{file_type} | 文件大小：{file_size:.2f}KB")

    # 提取文件内容
    text = uploaded_file.getvalue().decode('utf-8')
    # print(text)

    # 文件内容上传知识库
    with st.spinner(text="上传文件内容到知识库中"):
        time.sleep(1)
        result = st.session_state['knowledge_base'].store_knowledge(text, file_name)
        st.write(result)
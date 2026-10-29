# 导包
import hashlib
import os
import config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

# 文本内容:str 转为 md5:str
def text_to_md5(text:str)->str:
    text_bytes = text.encode(encoding='utf-8')

    md5_obj = hashlib.md5()
    md5_obj.update(text_bytes)
    md5 = md5_obj.hexdigest()

    return md5

# 检测md5是否重复
def check_md5(md5:str)->bool:
    os.makedirs(name=os.path.dirname(config.md5_path), exist_ok=True)

    if not os.path.exists(path=config.md5_path):
        open(file=config.md5_path, mode='w', encoding='utf-8').close()
        return False

    with open(file=config.md5_path, mode='r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == md5:
                return True

    return False

# 保存md5
def save_md5(md5:str):
    with open(file=config.md5_path, mode='a', encoding='utf-8') as f:
        f.write(md5 + '\n')

# 知识库类
class KnowledgeBase:
    def __init__(self):
        os.makedirs(name=config.chroma_path, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.chroma_name,
            embedding_function=DashScopeEmbeddings(model=config.chroma_embedding_model),
            persist_directory=config.chroma_path
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )

    # 存储知识
    def store_knowledge(self, file_text:str, file_name:str):
        md5 = text_to_md5(text=file_text)

        if check_md5(md5=md5):
            return f"[跳过]：文件{file_name}内容已存在知识库中"

        if len(file_text) > config.max_split_len:
            text_chunks:list[str] = self.splitter.split_text(text=file_text)
        else:
            text_chunks = [file_text]

        metadata={
            'source': file_name,
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator': '小许'
        }
        self.chroma.add_texts(
            texts=text_chunks,
            metadatas=[metadata for _ in text_chunks]
        )

        save_md5(md5)

        return f"[成功]：文件{file_name}内容上传知识库成功"

    # 知识检索器
    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={'k':config.top_k})
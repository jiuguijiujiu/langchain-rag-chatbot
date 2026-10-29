# uploader
file_type = ['txt']

# md5
md5_path = './offline/md5.txt'

# chroma
chroma_name = 'knowledge_base'
chroma_path = './offline/chroma_db'
chroma_embedding_model = 'text-embedding-v4'

# splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_len = 1000

# retriever
top_k = 1

# model
chat_model = 'qwen3.7-max'

# history
history_path = './online/chat_history'

# session_id
session_config = {
    'configurable':{
        "session_id": 'user_001'
    }
}
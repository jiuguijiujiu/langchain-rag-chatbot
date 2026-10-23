# 导包
from langchain_community.chat_models.tongyi import ChatTongyi
import config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from knowledge_base import KnowledgeBase
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_store_history import get_history

# 输出提示词
def print_prompt(prompt):
    print('=' * 50)
    print(prompt.to_string())
    print('=' * 50)
    return prompt

# Rag
class RagService:
    def __init__(self):
        self.chat_model = ChatTongyi(model=config.chat_model)
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system", "并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder('history'),
                ("user", "请回答用户提问：{input}")
            ]
        )
        self.retriever = KnowledgeBase().get_retriever()
        self.chain = self.__get_chain()

    def __get_chain(self):
        def format_for_retriever(input_dict:dict)->str:
            return input_dict['input']

        def format_documents(docs:list[Document])->str:
            if not docs:
                return "无相关参考资料"

            formatted_docs = ""
            for doc in docs:
                formatted_docs += f'文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n'
            return formatted_docs

        def format_for_prompt_template(input_dict)->dict:
            new_dict = {}
            new_dict['input'] = input_dict['input']['input']
            new_dict['context'] = input_dict['context']
            new_dict['history'] = input_dict['input']['history']
            return new_dict

        chain = ({'input':RunnablePassthrough(), 'context':RunnableLambda(format_for_retriever) | self.retriever | RunnableLambda(format_documents)}
                 | RunnableLambda(format_for_prompt_template) | self.prompt_template | RunnableLambda(print_prompt) |self.chat_model | StrOutputParser()
        )

        new_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=get_history,
            input_messages_key='input',
            history_messages_key='history'
        )

        return new_chain
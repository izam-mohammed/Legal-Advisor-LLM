from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import prompt_template
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")


embeddings = download_hugging_face_embeddings()
index_name = "llm-chatbot"

# Initializing the Pinecone
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)


PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}

current_dir = os.getcwd()
llm = CTransformers(
    model=os.path.join(current_dir, "saved_models/llama-2-7b-chat.ggmlv3.q4_0.bin"),
    model_type="llama",
    streaming=True,
    config={"max_new_tokens": 256, "temperature": 0.6, "context_length": -1},
)


qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs,
    verbose=True,
)


def llama_call(input):
    result = qa.invoke({"query": input})
    return str(result["result"])


if __name__ == "__main__":
    msg = "If a previous owner of a land had allowed a neighbour or neighbour to walk or drive over his land in a shortcut and this has been going on for say a decade or so can I as the new owner stop them now from using the shortcut?"
    print(f"response: {llama_call(msg)}")

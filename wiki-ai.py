from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import os

load_dotenv()

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))


def session():
    try:
        llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', verbose=False)
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
        retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

        while True:
            query = input("\nEnter a query: ")
            if query == "exit":
                break

            # Get the answer from the chain
            res = qa(query)
            answer, docs = res['result'], res['source_documents']

            # Print the result
            print("\n\n> Question:")
            print(query)
            print("\n> Answer:")
            print(answer)

            for document in docs:
                print("\n> " + document.metadata["source"] + ":")
                print(document.page_content)
    except Exception as e:
        raise e


if __name__ == "__main__":
    session()

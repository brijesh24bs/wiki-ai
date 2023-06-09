import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from constants import CHROMA_SETTINGS
import wikipediaapi

from dotenv import load_dotenv
load_dotenv()

persist_directory = os.environ.get('PERSIST_DIRECTORY')
embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')


def download(query: str):
    try:
        wiki = wikipediaapi.Wikipedia('en')
        page = wiki.page(query)
        if page.exists():
            text = page.text
            with open(f"data/data.txt", "w") as f:
                f.write(text)
                f.close()
        else:
            raise Exception("Page does not exist")

    except Exception as e:
        raise e


def ingest(data_path: str):
    try:
        loader = TextLoader(data_path, autodetect_encoding=True)
        document = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = splitter.split_documents(document)
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

        db = Chroma.from_documents(documents, embeddings, persist_directory=persist_directory,
                                   client_settings=CHROMA_SETTINGS)
        db.persist()
        db = None
    except Exception as e:
        raise e


if __name__ == '__main__':
    topic = input("Enter a topic: ")
    download(topic)
    ingest('data/data.txt')


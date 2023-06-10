import os
import glob
from typing import List
from pathlib import Path
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from constants import CHROMA_SETTINGS
import wikipediaapi
import numpy as np
from dotenv import load_dotenv

load_dotenv()

source_directory = os.environ.get('SOURCE_DIRECTORY')
persist_directory = os.environ.get('PERSIST_DIRECTORY')
embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')


def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads documents from a source directory
    """
    documents = glob.glob(os.path.join(source_dir, f"**/*.txt"), recursive=True)
    texts = []  # List of Documents
    for file in documents:
        if not (file in ignored_files):
            loader = TextLoader(file, autodetect_encoding=True)
            text = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts.extend(splitter.split_documents(text))
    return texts


def does_vectorstore_exist(persist_directory: str) -> bool:
    """
    Checks if vectorstore exists
    """
    if os.path.exists(os.path.join(persist_directory, 'index')):
        if os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet')) and os.path.exists(
                os.path.join(persist_directory, 'chroma-embeddings.parquet')):
            list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
            list_index_files += glob.glob(os.path.join(persist_directory, 'index/*.pkl'))
            # At least 3 documents are needed in a working vectorstore
            if len(list_index_files) > 3:
                return True
    return False


class Ingest:
    def __init__(self, topic: str):
        self.query = topic
        self.data_dir = f"data/"
        self.model_dir = f"models/"
        self.db_dir = f"db/"

    def create_directories(self):
        # Create folders if they don't exist
        os.makedirs(Path(self.data_dir), exist_ok=True)
        os.makedirs(Path(self.model_dir), exist_ok=True)
        os.makedirs(Path(self.db_dir), exist_ok=True)

    def download(self):
        try:
            wiki = wikipediaapi.Wikipedia('en')
            page = wiki.page(self.query)
            if page.exists():
                text = page.text
                with open(self.data_dir + f"{self.query}.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                    f.close()
            else:
                raise Exception("Page does not exist")

        except Exception as e:
            raise e

    def ingest(self):
        if not does_vectorstore_exist(persist_directory=persist_directory):
            try:
                loader = TextLoader(self.data_dir + f"{self.query}.txt", autodetect_encoding=True)
                document = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                documents = splitter.split_documents(document)
                embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

                db = Chroma.from_documents(documents, embeddings, persist_directory=persist_directory,
                                           client_settings=CHROMA_SETTINGS)
                
                print("Data ingested successfully !!!! now you can run wiki-ai.py")
            except Exception as e:
                raise e
        else:
            print(f"Appending to existing vectorstore at {persist_directory}")
            embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
            db = Chroma(persist_directory=persist_directory, embedding_function=embeddings,
                        client_settings=CHROMA_SETTINGS)
            collection = db.get()
            ignored_files = list(set([metadata['source'] for metadata in collection['metadatas']]))
            for file in ignored_files:
                print(f"Found embeddings for {file}")
            documents = load_documents(source_dir=source_directory, ignored_files=ignored_files)
            db.add_documents(documents)
        db.persist()
        db = None

    def run(self):
        self.create_directories()
        self.download()
        self.ingest()


if __name__ == '__main__':
    query = input("Enter a topic: ")
    query = query.replace(" ", "_")
    ingest = Ingest(query)
    ingest.run()

##Python (programming language)
##Hunter x Hunter
##Artificial general intelligence

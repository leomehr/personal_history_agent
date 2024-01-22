import os

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

DATA_DIR = './data'
PERSIST_DIR = './storage'


if __name__ == '__main__':
    if os.path.exists(PERSIST_DIR):
        print(f'{PERSIST_DIR} Already exists -- overwriting')

    # load the documents and create the index
    documents = SimpleDirectoryReader(DATA_DIR, recursive=True).load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print('✅ Done')
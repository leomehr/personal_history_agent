import os

from llama_index import (
    StorageContext,
    load_index_from_storage,
)

from create_vector_store import PERSIST_DIR

if not os.path.exists(PERSIST_DIR):
    print(f'{PERSIST_DIR} missing -- please run create_vector_store.py first')

# load the existing index
print('loading index...')
storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
index = load_index_from_storage(storage_context)

# either way we can now query the index
query_engine = index.as_query_engine()

if __name__ == '__main__':
    query = 'What is my personality like based on my texts?'
    print('>', query)
    while query is not None:
        print('loading...')
        response = query_engine.query(query)
        print(response.response)
        # print(response.source_nodes)  # uncomment to see which nodes are used as context
        print()
        query = input('Enter a query:\n> ')

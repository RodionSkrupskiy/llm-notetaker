import sys

__import__("pysqlite3")  # Hack for running chromadb
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import chromadb


class DB:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient()
        collection_name = "personal_assistant"
        # self.chroma_client.delete_collection(collection_name)
        self.chroma_client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    def get_collection(self, collection_name):
        return self.chroma_client.get_collection(name=collection_name)

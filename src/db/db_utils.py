import datetime
import uuid


def add_data(collection, note, username):
    # all-MiniLM-L6-v2 for creating embeddings by default
    collection.add(
        documents=note,  # Write fix for too large notes
        metadatas={
            "username": username,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        },
        ids=uuid.uuid4().hex,
    )


def get_data(collection, message, username):
    notes = collection.query(
        query_texts=message,
        where={"username": username},
        n_results=5,
    )
    return notes


def get_recent(collection, N, username):
    # No inbuilt functionality to get results from the end or get only the ids to filter by them
    if N <= 0:
        return []
    recent = collection.get(
        where={"username": username},
        include=["documents"],
    )["documents"]
    return recent[-N:]

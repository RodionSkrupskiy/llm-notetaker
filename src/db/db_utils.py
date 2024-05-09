import datetime
import time


def add_data(collection, note, username):
    collection.add(
        documents=note,  # Write fix for too large notes
        metadatas={
            "username": username,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        },
        ids=f"{time.time()}",  # Write fix for id generation
    )


def get_data(collection, message, username):
    notes = collection.query(
        query_texts=message,
        where={"username": username},
        n_results=5,
        # include=["documents"],
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


# def remove_punctuation(text):
#     punct_str = string.punctuation
#     punct_str = punct_str.replace("'", "")
#     return text.translate(str.maketrans("", "", punct_str))

# def remove_stopwords(text):
#     text = ' '.join(word for word in text.split(' ') if word not in stop_words)
#     return text

# def search_cleaner(text):
#     new_text = text.lower()
#     new_text = remove_stopwords(new_text)
#     new_text = remove_punctuation(new_text)
#     return new_text

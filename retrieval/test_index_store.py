from retrieval.index_store import ensure_index

vs, chunks = ensure_index("data/docs")
print("INDEX OK")
print("CHUNKS:", len(chunks))

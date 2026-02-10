from retrieval.loader import load_and_chunk

chunks = load_and_chunk("data/docs")
print("chunks:", len(chunks))
print("example metadata:", chunks[0].metadata)
print("example text preview:", chunks[0].page_content[:120])

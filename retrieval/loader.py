from __future__ import annotations

import os
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


SUPPORTED_EXTS = {".txt", ".md"}  # keep it simple for now (we can add pdf later)


def load_raw_documents(docs_dir: str = "data/docs") -> List[Document]:
    """
    Loads raw documents from data/docs.
    For now: supports .txt only.
    Returns LangChain Documents with metadata for traceability.
    """
    base = Path(docs_dir)
    if not base.exists():
        raise FileNotFoundError(f"Docs folder not found: {docs_dir}")

    docs: List[Document] = []

    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTS:
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if not text:
                continue

            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "source_path": str(path).replace("\\", "/"),
                        "source_name": path.name,
                        "file_ext": path.suffix.lower(),
                    },
                )
            )

    return docs


def chunk_documents(
    docs: List[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> List[Document]:
    """
    Splits documents into chunks and attaches chunk-level metadata.
    This metadata is what we will later turn into citations.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    chunked: List[Document] = []
    for doc in docs:
        splits = splitter.split_documents([doc])

        for i, s in enumerate(splits):
            # add chunk identifiers
            s.metadata = dict(s.metadata)  # ensure it's a plain dict
            s.metadata["chunk_id"] = i

            # stable-ish id for citations
            # e.g. "doc:company_overview.txt#chunk_0"
            s.metadata["source_id"] = f"doc:{s.metadata.get('source_name')}#chunk_{i}"

            chunked.append(s)

    return chunked


def load_and_chunk(docs_dir: str = "data/docs") -> List[Document]:
    """
    Convenience function used by the index builder:
    load raw docs -> chunk them -> return chunks.
    """
    raw = load_raw_documents(docs_dir=docs_dir)
    return chunk_documents(raw)

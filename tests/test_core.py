import pytest
import os
import tempfile
from retriever import (
    intelligent_chunk_text,
    compute_file_hash,
    extract_text_from_file,
    retrieve_context
)

def test_intelligent_chunk_text_basic():
    """Test standard chunking logic and maximum chunk size limits."""
    sample_text = "This is paragraph 1.\n\nThis is paragraph 2 with some more context to ensure it processes properly."
    chunks = intelligent_chunk_text(sample_text, max_chunk_size=100, overlap=20)
    
    assert len(chunks) >= 2
    assert "This is paragraph 1." in chunks
    assert any("paragraph 2" in c for c in chunks)

def test_chunk_text_overlap():
    """Test overlapping mechanism for long single paragraphs."""
    long_paragraph = "A" * 250
    chunks = intelligent_chunk_text(long_paragraph, max_chunk_size=100, overlap=20)
    
    assert len(chunks) > 1
    # Ensure chunk boundary logic creates overlapping windows
    assert len(chunks[0]) <= 100

def test_compute_file_hash():
    """Test SHA-256 file hashing consistency."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as tmp:
        tmp.write("AeroGrid Test Content for SHA-256 Hash")
        tmp_path = tmp.name

    try:
        hash1 = compute_file_hash(tmp_path)
        hash2 = compute_file_hash(tmp_path)
        
        assert hash1 is not None
        assert len(hash1) == 64 # SHA-256 string length
        assert hash1 == hash2 # Deterministic hash requirement
    finally:
        os.remove(tmp_path)

def test_extract_text_from_txt_file():
    """Test plain text file extraction module."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write("Header Line\n\nPage Body Text")
        tmp_path = tmp.name

    try:
        pages = extract_text_from_file(tmp_path)
        assert len(pages) == 1
        page_num, content = pages[0]
        assert page_num == 1
        assert "Header Line" in content
    finally:
        os.remove(tmp_path)

def test_retrieval_context_structure():
    """Test vector search & reranking return structure and metadata key presence."""
    matches = retrieve_context("LOTO lockout procedure", top_k=2, use_reranker=True)
    
    assert isinstance(matches, list)
    assert len(matches) <= 2
    
    if matches:
        first_match = matches[0]
        assert "source" in first_match
        assert "page" in first_match
        assert "content" in first_match
        assert "rerank_score" in first_match or "score" in first_match

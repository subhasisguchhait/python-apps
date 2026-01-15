
def chunk_text(text, chunk_size=500, overlap=50):
    # Split text into words
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        # Create chunk with overlap
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap # move back by overlap

    return chunks
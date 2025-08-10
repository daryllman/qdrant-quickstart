# Qdrant Quickstart Tutorial

Welcome to the Qdrant Quickstart Tutorial! This guide will walk you through setting up and using Qdrant, a powerful vector database for similarity search and AI applications.

## What is Qdrant?

Qdrant is a vector similarity search engine that allows you to:
- Store and search high-dimensional vectors
- Perform similarity searches for AI/ML applications
- Build recommendation systems
- Create semantic search engines
- Power AI applications with efficient vector operations

## Prerequisites

Before starting, make sure you have:
- Python 3.8 or higher
- **uv (recommended)** or pip (Python package installer)
- Docker (optional, for running Qdrant in a container)

**Note:** We recommend using [uv](https://github.com/astral-sh/uv) for faster dependency management and better virtual environment handling.

### Installing uv

If you don't have uv installed, you can install it with:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip
pip install uv
```

## Installation Options

### Option 1: Using Docker (Recommended)

The easiest way to get started is using Docker:

```bash
# Pull and run Qdrant
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

This will:
- Start Qdrant on port 6333 (HTTP API) and 6334 (gRPC)
- Create a persistent storage volume
- Make Qdrant accessible at `http://localhost:6333`

### Option 2: Using pip (Python client only)

If you only need the Python client:

```bash
pip install qdrant-client
```

### Option 3: Building from source

For advanced users who want to build from source, visit the [Qdrant GitHub repository](https://github.com/qdrant/qdrant).

## Running and Testing the Examples

This repository includes comprehensive examples and tests to help you learn Qdrant. Here's how to run them:

### Quick Start - Run All Examples

The easiest way to test everything is using the main runner script:

#### Using uv (Recommended)

**Option 1: Automatic (Recommended)**
```bash
# uv run automatically creates venv and installs dependencies
uv run python run_examples.py
```

**Option 2: Manual (for more control)**
```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt

# Run all examples
uv run python run_examples.py
```

Or even simpler, run everything in one command:
```bash
uv run python run_examples.py
```

#### Using pip

```bash
# Install dependencies and run all examples
python run_examples.py
```

This script will:
- Check if Qdrant is running and offer to start it with Docker
- Install all required Python dependencies (if not using uv)
- Run all example scripts with proper error handling
- Execute the test suite
- Clean up resources when done

### Manual Setup and Testing

If you prefer to run things manually:

1. **Start Qdrant:**
   ```bash
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

2. **Install dependencies:**

   **Using uv (Recommended):**
   
   **Automatic (recommended for quick testing):**
   ```bash
   uv run python examples/basic_example.py  # Automatically handles venv and dependencies
   ```
   
   **Manual (for development work):**
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

   **Using pip:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run individual examples:**

   **Using uv:**
   ```bash
   # Basic functionality
   uv run python examples/basic_example.py
   
   # Document search system
   uv run python examples/document_search.py
   
   # Advanced features (filtering, batch operations)
   uv run python examples/advanced_features.py
   ```

   **Using pip:**
   ```bash
   # Basic functionality
   python examples/basic_example.py
   
   # Document search system
   python examples/document_search.py
   
   # Advanced features (filtering, batch operations)
   python examples/advanced_features.py
   ```

4. **Run tests:**

   **Using uv:**
   ```bash
   uv run pytest tests/ -v
   ```

   **Using pip:**
   ```bash
   pytest tests/ -v
   ```

### Example Scripts Overview

- **`examples/basic_example.py`**: Demonstrates core Qdrant functionality (connection, collections, search)
- **`examples/document_search.py`**: Complete document search system with multiple queries
- **`examples/advanced_features.py`**: Advanced features like filtering, batch operations, and collection management
- **`tests/test_qdrant_basics.py`**: Automated tests to verify functionality

### Testing Individual Components

You can also test specific functionality:

**Using uv:**
```bash
# Test connection and basic operations
uv run python -c "
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)
print('✅ Connected successfully!')
collections = client.get_collections()
print(f'Available collections: {len(collections.collections)}')
"
```

**Using pip:**
```bash
# Test connection and basic operations
python -c "
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)
print('✅ Connected successfully!')
collections = client.get_collections()
print(f'Available collections: {len(collections.collections)}')
"
```

## Quick Start Guide

### Step 1: Install the Python Client

**Using uv (Recommended):**
```bash
uv venv
uv pip install qdrant-client
```

**Using pip:**
```bash
pip install qdrant-client
```

### Step 2: Connect to Qdrant

Create a Python script to connect to your Qdrant instance:

```python
from qdrant_client import QdrantClient

# Connect to Qdrant (assuming it's running on localhost:6333)
client = QdrantClient("localhost", port=6333)

# Or connect to a remote instance
# client = QdrantClient("your-qdrant-host", port=6333)
```

### Step 3: Create a Collection

Collections in Qdrant are similar to tables in traditional databases:

```python
from qdrant_client.models import Distance, VectorParams

# Create a collection for storing document embeddings
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)
```

### Step 4: Insert Data

Add some sample data to your collection:

```python
from qdrant_client.models import PointStruct
import numpy as np

# Generate some sample vectors (in real applications, these would be embeddings from your data)
vectors = np.random.rand(100, 384).tolist()  # 100 documents with 384-dimensional vectors

# Create points with IDs and payload (metadata)
points = [
    PointStruct(
        id=i,
        vector=vector,
        payload={"text": f"Document {i}", "category": "sample"}
    )
    for i, vector in enumerate(vectors)
]

# Insert the points into the collection
client.upsert(
    collection_name="documents",
    points=points
)
```

### Step 5: Perform Similarity Search

Search for similar vectors:

```python
# Generate a query vector (in real applications, this would be an embedding of your search query)
query_vector = np.random.rand(384).tolist()

# Search for similar vectors
search_result = client.search(
    collection_name="documents",
    query_vector=query_vector,
    limit=5  # Return top 5 most similar vectors
)

print("Search results:")
for result in search_result:
    print(f"ID: {result.id}, Score: {result.score}, Payload: {result.payload}")
```

## Complete Example: Document Search System

Here's a complete example that demonstrates a simple document search system:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np

# Connect to Qdrant
client = QdrantClient("localhost", port=6333)

# Sample documents
documents = [
    "The quick brown fox jumps over the lazy dog",
    "A quick brown dog jumps over the lazy fox",
    "The lazy fox sleeps while the quick brown dog watches",
    "A brown fox and a lazy dog are friends",
    "The quick dog runs fast and jumps high"
]

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Generate simple embeddings (in practice, use a proper embedding model)
def simple_embedding(text):
    # This is a simplified embedding - use proper models like sentence-transformers
    return np.random.rand(384).tolist()

# Insert documents
points = []
for i, doc in enumerate(documents):
    points.append(
        PointStruct(
            id=i,
            vector=simple_embedding(doc),
            payload={"text": doc, "doc_id": i}
        )
    )

client.upsert(collection_name="documents", points=points)

# Search for similar documents
query = "quick brown fox"
query_vector = simple_embedding(query)

results = client.search(
    collection_name="documents",
    query_vector=query_vector,
    limit=3
)

print(f"Search results for: '{query}'")
for result in results:
    print(f"Score: {result.score:.4f} - {result.payload['text']}")
```

## Advanced Features

### Filtering

You can filter search results based on payload attributes:

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Search with filter
results = client.search(
    collection_name="documents",
    query_vector=query_vector,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="category",
                match=MatchValue(value="sample")
            )
        ]
    ),
    limit=5
)
```

### Batch Operations

For better performance with large datasets:

```python
# Batch upsert
client.upsert(
    collection_name="documents",
    points=points,
    batch_size=100  # Process in batches of 100
)
```

### Collection Management

```python
# List all collections
collections = client.get_collections()
print("Available collections:", [col.name for col in collections.collections])

# Get collection info
collection_info = client.get_collection("documents")
print("Collection info:", collection_info)

# Delete collection
# client.delete_collection("documents")
```

## Using Real Embeddings

For production applications, use proper embedding models:

**Using uv (Recommended):**
```bash
uv pip install sentence-transformers
```

**Using pip:**
```bash
pip install sentence-transformers
```

```python
from sentence_transformers import SentenceTransformer

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate real embeddings
texts = ["Hello world", "How are you?", "Good morning"]
embeddings = model.encode(texts).tolist()

# Use these embeddings with Qdrant
```

## Web UI

Qdrant provides a web interface for managing your data:

1. Start Qdrant with Docker (as shown above)
2. Open your browser and go to `http://localhost:6333/dashboard`
3. Explore your collections, view data, and perform searches visually

## Best Practices

1. **Choose the right distance metric**: Use COSINE for normalized vectors, EUCLIDEAN for raw vectors
2. **Optimize vector size**: Smaller vectors are faster but may lose information
3. **Use filters**: Combine vector search with metadata filtering for better results
4. **Batch operations**: Use batch operations for better performance with large datasets
5. **Index optimization**: Consider using HNSW index for better search performance

## Troubleshooting

### Common Issues

1. **Connection refused**: Make sure Qdrant is running and the port is correct
2. **Collection not found**: Create the collection before inserting data
3. **Vector size mismatch**: Ensure all vectors have the same dimension as specified in the collection
4. **Dependency issues**: If you encounter dependency conflicts, try using `uv` instead of `pip` for better dependency resolution

### Getting Help

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant GitHub](https://github.com/qdrant/qdrant)
- [Qdrant Discord](https://discord.gg/tdtYvXjC4h)

## Next Steps

Now that you have the basics, you can:

1. Build a recommendation system
2. Create a semantic search engine
3. Implement image similarity search
4. Build an AI-powered chatbot
5. Create a content recommendation system

Happy vector searching! 🚀 
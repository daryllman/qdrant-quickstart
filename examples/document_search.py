#!/usr/bin/env python3
"""
Document Search Example
This script demonstrates a complete document search system using Qdrant.
"""

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

def simple_embedding(text):
    """Generate a simple embedding for demonstration purposes.
    In production, use proper embedding models like sentence-transformers."""
    # Create a deterministic embedding based on text content
    np.random.seed(hash(text) % 2**32)
    return np.random.rand(384).tolist()

def main():
    """Main function to demonstrate document search."""
    print("📚 Starting Document Search Example")
    
    # Connect to Qdrant
    try:
        client = QdrantClient("localhost", port=6333)
        print("✅ Connected to Qdrant successfully")
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")
        print("Make sure Qdrant is running with: docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
        return
    
    # Sample documents
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "A quick brown dog jumps over the lazy fox",
        "The lazy fox sleeps while the quick brown dog watches",
        "A brown fox and a lazy dog are friends",
        "The quick dog runs fast and jumps high",
        "A lazy cat sleeps on the windowsill",
        "The brown cat chases the quick mouse",
        "A quick mouse escapes from the brown cat"
    ]
    
    collection_name = "documents"
    
    # Create collection
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"✅ Created collection: {collection_name}")
    except Exception as e:
        print(f"⚠️  Collection might already exist: {e}")
    
    # Insert documents
    print("📝 Inserting documents...")
    points = []
    for i, doc in enumerate(documents):
        points.append(
            PointStruct(
                id=i,
                vector=simple_embedding(doc),
                payload={"text": doc, "doc_id": i, "length": len(doc)}
            )
        )
    
    try:
        client.upsert(collection_name=collection_name, points=points)
        print(f"✅ Inserted {len(points)} documents")
    except Exception as e:
        print(f"❌ Failed to insert documents: {e}")
        return
    
    # Test different search queries
    test_queries = [
        "quick brown fox",
        "lazy dog",
        "cat mouse",
        "sleeping animals"
    ]
    
    print("\n🔍 Testing different search queries:")
    for query in test_queries:
        print(f"\n--- Searching for: '{query}' ---")
        query_vector = simple_embedding(query)
        
        try:
            results = client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=3
            )
            
            for i, result in enumerate(results, 1):
                print(f"{i}. Score: {result.score:.4f} - {result.payload['text']}")
                
        except Exception as e:
            print(f"❌ Search failed: {e}")
    
    # Clean up
    try:
        client.delete_collection(collection_name)
        print(f"\n🧹 Cleaned up collection: {collection_name}")
    except Exception as e:
        print(f"⚠️  Could not delete collection: {e}")
    
    print("🎉 Document search example completed!")

if __name__ == "__main__":
    main() 
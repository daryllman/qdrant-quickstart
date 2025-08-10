#!/usr/bin/env python3
"""
Basic Qdrant Example
This script demonstrates the core functionality of Qdrant vector database.
"""

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

def main():
    """Main function to demonstrate Qdrant basics."""
    print("🚀 Starting Qdrant Basic Example")
    
    # Connect to Qdrant
    try:
        client = QdrantClient("localhost", port=6333)
        print("✅ Connected to Qdrant successfully")
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")
        print("Make sure Qdrant is running with: docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
        return
    
    # Create a collection
    collection_name = "test_collection"
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"✅ Created collection: {collection_name}")
    except Exception as e:
        print(f"⚠️  Collection might already exist: {e}")
    
    # Generate sample data
    print("📊 Generating sample data...")
    vectors = np.random.rand(10, 384).tolist()  # 10 documents with 384-dimensional vectors
    
    # Create points with IDs and payload
    points = [
        PointStruct(
            id=i,
            vector=vector,
            payload={"text": f"Document {i}", "category": "sample", "index": i}
        )
        for i, vector in enumerate(vectors)
    ]
    
    # Insert the points
    try:
        client.upsert(collection_name=collection_name, points=points)
        print(f"✅ Inserted {len(points)} points into collection")
    except Exception as e:
        print(f"❌ Failed to insert points: {e}")
        return
    
    # Perform similarity search
    print("🔍 Performing similarity search...")
    query_vector = np.random.rand(384).tolist()
    
    try:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=3
        )
        
        print("\n📋 Search Results:")
        for i, result in enumerate(search_result, 1):
            print(f"{i}. ID: {result.id}, Score: {result.score:.4f}, Payload: {result.payload}")
            
    except Exception as e:
        print(f"❌ Search failed: {e}")
    
    # Clean up
    try:
        client.delete_collection(collection_name)
        print(f"🧹 Cleaned up collection: {collection_name}")
    except Exception as e:
        print(f"⚠️  Could not delete collection: {e}")
    
    print("🎉 Basic example completed!")

if __name__ == "__main__":
    main() 
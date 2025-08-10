#!/usr/bin/env python3
"""
Advanced Features Example
This script demonstrates advanced Qdrant features like filtering, batch operations, and collection management.
"""

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, 
    Filter, FieldCondition, MatchValue, Range
)

def main():
    """Main function to demonstrate advanced Qdrant features."""
    print("🚀 Starting Advanced Features Example")
    
    # Connect to Qdrant
    try:
        client = QdrantClient("localhost", port=6333)
        print("✅ Connected to Qdrant successfully")
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")
        print("Make sure Qdrant is running with: docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
        return
    
    collection_name = "advanced_demo"
    
    # Create collection
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"✅ Created collection: {collection_name}")
    except Exception as e:
        print(f"⚠️  Collection might already exist: {e}")
    
    # Generate sample data with different categories and metadata
    print("📊 Generating sample data with metadata...")
    categories = ["tech", "science", "history", "fiction"]
    points = []
    
    for i in range(50):
        vector = np.random.rand(384).tolist()
        category = categories[i % len(categories)]
        year = 2020 + (i % 5)  # Years 2020-2024
        
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={
                    "text": f"Document {i} about {category}",
                    "category": category,
                    "year": year,
                    "length": len(f"Document {i} about {category}"),
                    "tags": [category, f"year_{year}", f"doc_{i}"]
                }
            )
        )
    
    # Batch insert with progress
    print("📝 Inserting data in batches...")
    batch_size = 10
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        try:
            client.upsert(collection_name=collection_name, points=batch)
            print(f"✅ Inserted batch {i//batch_size + 1}/{(len(points) + batch_size - 1)//batch_size}")
        except Exception as e:
            print(f"❌ Failed to insert batch: {e}")
            return
    
    # Demonstrate filtering
    print("\n🔍 Demonstrating filtering capabilities:")
    
    # 1. Filter by category
    print("\n--- Filtering by category 'tech' ---")
    try:
        tech_results = client.search(
            collection_name=collection_name,
            query_vector=np.random.rand(384).tolist(),
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value="tech")
                    )
                ]
            ),
            limit=5
        )
        
        for i, result in enumerate(tech_results, 1):
            print(f"{i}. Score: {result.score:.4f} - {result.payload['text']} (Year: {result.payload['year']})")
            
    except Exception as e:
        print(f"❌ Category filter failed: {e}")
    
    # 2. Filter by year range
    print("\n--- Filtering by year range (2022-2024) ---")
    try:
        year_results = client.search(
            collection_name=collection_name,
            query_vector=np.random.rand(384).tolist(),
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="year",
                        range=Range(gte=2022, lte=2024)
                    )
                ]
            ),
            limit=5
        )
        
        for i, result in enumerate(year_results, 1):
            print(f"{i}. Score: {result.score:.4f} - {result.payload['text']} (Year: {result.payload['year']})")
            
    except Exception as e:
        print(f"❌ Year filter failed: {e}")
    
    # 3. Complex filter (category AND year)
    print("\n--- Complex filter: science documents from 2023 ---")
    try:
        complex_results = client.search(
            collection_name=collection_name,
            query_vector=np.random.rand(384).tolist(),
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value="science")
                    ),
                    FieldCondition(
                        key="year",
                        match=MatchValue(value=2023)
                    )
                ]
            ),
            limit=5
        )
        
        for i, result in enumerate(complex_results, 1):
            print(f"{i}. Score: {result.score:.4f} - {result.payload['text']} (Year: {result.payload['year']})")
            
    except Exception as e:
        print(f"❌ Complex filter failed: {e}")
    
    # Collection management
    print("\n📋 Collection Management:")
    
    # List all collections
    try:
        collections = client.get_collections()
        print(f"Available collections: {[col.name for col in collections.collections]}")
    except Exception as e:
        print(f"❌ Failed to list collections: {e}")
    
    # Get collection info
    try:
        collection_info = client.get_collection(collection_name)
        print(f"Collection '{collection_name}' info:")
        print(f"  - Vector size: {collection_info.config.params.vectors.size}")
        print(f"  - Distance: {collection_info.config.params.vectors.distance}")
        print(f"  - Points count: {collection_info.points_count}")
    except Exception as e:
        print(f"❌ Failed to get collection info: {e}")
    
    # Clean up
    try:
        client.delete_collection(collection_name)
        print(f"\n🧹 Cleaned up collection: {collection_name}")
    except Exception as e:
        print(f"⚠️  Could not delete collection: {e}")
    
    print("🎉 Advanced features example completed!")

if __name__ == "__main__":
    main() 
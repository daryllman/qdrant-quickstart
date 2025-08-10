#!/usr/bin/env python3
"""
Test suite for Qdrant basics
"""

import pytest
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class TestQdrantBasics:
    """Test class for basic Qdrant functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup Qdrant client for each test."""
        self.client = QdrantClient("localhost", port=6333)
        self.collection_name = "test_collection"
        yield
        # Cleanup after each test
        try:
            self.client.delete_collection(self.collection_name)
        except:
            pass
    
    def test_connection(self):
        """Test that we can connect to Qdrant."""
        # This test will fail if Qdrant is not running
        collections = self.client.get_collections()
        assert isinstance(collections.collections, list)
    
    def test_create_collection(self):
        """Test creating a collection."""
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        
        # Verify collection exists
        collection_info = self.client.get_collection(self.collection_name)
        assert collection_info.config.params.vectors.size == 384
        assert collection_info.config.params.vectors.distance == Distance.COSINE
    
    def test_insert_and_search(self):
        """Test inserting data and performing search."""
        # Create collection
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        
        # Insert test data
        vectors = np.random.rand(5, 384).tolist()
        points = [
            PointStruct(
                id=i,
                vector=vector,
                payload={"text": f"Test document {i}"}
            )
            for i, vector in enumerate(vectors)
        ]
        
        self.client.upsert(collection_name=self.collection_name, points=points)
        
        # Perform search
        query_vector = np.random.rand(384).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=3
        )
        
        # Verify results
        assert len(results) > 0
        assert all(hasattr(result, 'id') for result in results)
        assert all(hasattr(result, 'score') for result in results)
        assert all(hasattr(result, 'payload') for result in results)
    
    def test_collection_operations(self):
        """Test collection management operations."""
        # Create collection
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        
        # List collections
        collections = self.client.get_collections()
        collection_names = [col.name for col in collections.collections]
        assert self.collection_name in collection_names
        
        # Get collection info
        collection_info = self.client.get_collection(self.collection_name)
        assert collection_info.config.params.vectors.size == 384
        assert collection_info.points_count == 0  # Empty collection

if __name__ == "__main__":
    pytest.main([__file__]) 
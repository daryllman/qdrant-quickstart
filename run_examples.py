#!/usr/bin/env python3
"""
Main script to run Qdrant examples and tests
"""

import sys
import subprocess
import os
from pathlib import Path

def check_qdrant_running():
    """Check if Qdrant is running on localhost:6333."""
    try:
        import requests
        response = requests.get("http://localhost:6333/collections", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_qdrant():
    """Start Qdrant using Docker."""
    print("🐳 Starting Qdrant with Docker...")
    try:
        # First, try to stop and remove any existing container
        try:
            subprocess.run(["docker", "stop", "qdrant-quickstart"], check=False)
            subprocess.run(["docker", "rm", "qdrant-quickstart"], check=False)
        except:
            pass
        
        # Start new container
        subprocess.run([
            "docker", "run", "-d", "--name", "qdrant-quickstart",
            "-p", "6333:6333", "-p", "6334:6334",
            "-v", f"{os.getcwd()}/qdrant_storage:/qdrant/storage:z",
            "qdrant/qdrant"
        ], check=True)
        print("✅ Qdrant started successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Qdrant: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker first.")
        return False

def stop_qdrant():
    """Stop Qdrant Docker container."""
    try:
        subprocess.run(["docker", "stop", "qdrant-quickstart"], check=True)
        subprocess.run(["docker", "rm", "qdrant-quickstart"], check=True)
        print("🧹 Qdrant stopped and cleaned up.")
    except:
        pass

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    try:
        # Use uv instead of pip
        subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_example(example_name, script_path):
    """Run a specific example script."""
    print(f"\n{'='*50}")
    print(f"🚀 Running {example_name}")
    print(f"{'='*50}")
    
    try:
        # Use uv run directly instead of uv run python
        result = subprocess.run(["uv", "run", script_path], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Example completed successfully!")
            print(result.stdout)
        else:
            print("❌ Example failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Example timed out after 60 seconds")
    except Exception as e:
        print(f"❌ Error running example: {e}")

def run_tests():
    """Run the test suite."""
    print(f"\n{'='*50}")
    print("🧪 Running Tests")
    print(f"{'='*50}")
    
    try:
        # Use uv run directly instead of uv run python
        result = subprocess.run(["uv", "run", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True, timeout=120)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            
    except subprocess.TimeoutExpired:
        print("⏰ Tests timed out after 120 seconds")
    except Exception as e:
        print(f"❌ Error running tests: {e}")

def main():
    """Main function to orchestrate the examples and tests."""
    print("🎯 Qdrant Quickstart - Example Runner")
    print("=" * 50)
    
    # Check if Qdrant is running
    if not check_qdrant_running():
        print("⚠️  Qdrant is not running.")
        response = input("Would you like to start Qdrant with Docker? (y/n): ")
        if response.lower() == 'y':
            if not start_qdrant():
                print("❌ Cannot proceed without Qdrant running.")
                return
        else:
            print("❌ Please start Qdrant manually and try again.")
            print("Command: docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
            return
    else:
        print("✅ Qdrant is running!")
    
    # Skip dependency installation if running with uv (uv run handles this automatically)
    # Check if we're running with uv by looking at the Python executable path
    python_executable = sys.executable
    if "uv" in python_executable or "UV_RUNNING_DIR" in os.environ:
        print("✅ Using uv - dependencies will be handled automatically!")
    else:
        # Install dependencies only if not using uv
        if not install_dependencies():
            print("❌ Cannot proceed without dependencies.")
            return
    
    # Run examples
    examples = [
        ("Basic Example", "examples/basic_example.py"),
        ("Document Search", "examples/document_search.py"),
        ("Advanced Features", "examples/advanced_features.py")
    ]
    
    for name, path in examples:
        if os.path.exists(path):
            run_example(name, path)
        else:
            print(f"⚠️  Example file not found: {path}")
    
    # Run tests
    if os.path.exists("tests/"):
        run_tests()
    else:
        print("⚠️  Tests directory not found.")
    
    print(f"\n{'='*50}")
    print("🎉 All examples and tests completed!")
    print("=" * 50)
    
    # Ask if user wants to stop Qdrant
    response = input("\nWould you like to stop the Qdrant container? (y/n): ")
    if response.lower() == 'y':
        stop_qdrant()

if __name__ == "__main__":
    main() 
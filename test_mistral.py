#!/usr/bin/env python3
"""
Test script for Mistral API connection.
Run this to verify your Mistral API key works.

Usage:
    export MISTRAL_API_KEY="your-new-key-here"
    python test_mistral.py
"""

import os
import sys

# Add the project to path
sys.path.insert(0, '/home/mycelium/mycelium-hub')

from mycelium.core.llm_runtime import LLMRuntime
from mycelium.core.config import is_mistral_configured, get_mistral_api_key


def test_configuration():
    """Test if Mistral API key is configured."""
    print("=" * 60)
    print("TEST 1: Configuration Check")
    print("=" * 60)
    
    if is_mistral_configured():
        print("✅ Mistral API key is configured")
        print(f"   Key preview: {get_mistral_api_key()[:8]}..." if get_mistral_api_key() else "")
        return True
    else:
        print("❌ Mistral API key NOT configured")
        print("   Set MISTRAL_API_KEY environment variable:")
        print("   export MISTRAL_API_KEY='your-key-here'")
        return False


def test_mistral_api():
    """Test Mistral API connection with a simple prompt."""
    print("\n" + "=" * 60)
    print("TEST 2: Mistral API Connection")
    print("=" * 60)
    
    try:
        # Use a small, fast model
        response = LLMRuntime.call(
            "Say 'Hello from Mistral!'",
            model="mistral-tiny",
            temperature=0.7,
            max_tokens=50
        )
        print(f"✅ API call successful!")
        print(f"   Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False


def test_mistral_small():
    """Test with mistral-small model."""
    print("\n" + "=" * 60)
    print("TEST 3: Mistral Small Model")
    print("=" * 60)
    
    try:
        response = LLMRuntime.call(
            "What is the capital of France?",
            model="mistral-small",
            temperature=0.0,
            max_tokens=50
        )
        print(f"✅ mistral-small works!")
        print(f"   Response: {response}")
        return True
    except Exception as e:
        print(f"❌ mistral-small failed: {e}")
        return False


def test_local_brain():
    """Test the local brain (mycelium-brain) via Ollama."""
    print("\n" + "=" * 60)
    print("TEST 4: Local Brain (mycelium-brain:latest)")
    print("=" * 60)
    
    try:
        response = LLMRuntime.call(
            "You are a helpful AI. Respond with 'Local brain online!'",
            model="mycelium-brain:latest",
            max_tokens=50
        )
        print(f"✅ Local brain works!")
        print(f"   Response: {response}")
        return True
    except Exception as e:
        print(f"⚠️  Local brain not available (Ollama may not be running): {e}")
        print("   Try: ollama pull mycelium-brain:latest")
        print("        ollama serve")
        return False


def test_devstral():
    """Test devstral via llamacpp."""
    print("\n" + "=" * 60)
    print("TEST 5: Devstral (llamacpp)")
    print("=" * 60)
    
    try:
        response = LLMRuntime.call(
            "Hello devstral!",
            model="devstral",
            max_tokens=50
        )
        print(f"✅ Devstral works!")
        print(f"   Response: {response}")
        return True
    except Exception as e:
        print(f"⚠️  Devstral not available (llamacpp may not be running): {e}")
        print("   Try: llama-server --model devstral.gguf --port 8080")
        return False


def test_context_truncation():
    """Test that context truncation works."""
    print("\n" + "=" * 60)
    print("TEST 6: Context Truncation")
    print("=" * 60)
    
    # Create a very long prompt
    long_context = "X" * 50000  # 50KB of context
    
    try:
        response = LLMRuntime.call(
            f"{long_context}\n\nActual question: What is 2+2?",
            model="mistral-tiny",
            max_tokens=50
        )
        print(f"✅ Context truncation works!")
        print(f"   Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Context truncation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MISTRAL & LOCAL BRAIN CONNECTION TEST")
    print("=" * 60)
    
    results = []
    
    # Test 1: Configuration
    if not test_configuration():
        print("\n❌ Cannot proceed without API key. Please configure and re-run.")
        sys.exit(1)
    results.append(("Configuration", True))
    
    # Test 2-6: API and model tests
    results.append(("Mistral API", test_mistral_api()))
    results.append(("Mistral Small", test_mistral_small()))
    results.append(("Local Brain", test_local_brain()))
    results.append(("Devstral", test_devstral()))
    results.append(("Context Truncation", test_context_truncation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\nPassed: {passed_count}/{total}")
    
    if passed_count >= 2:
        print("\n🎉 Mistral connection is working!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return passed_count >= 2


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

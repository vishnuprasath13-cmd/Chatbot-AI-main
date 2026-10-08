#!/usr/bin/env python3
"""
Test script for Chatbot-Using-Langchain
Tests all components and API connectivity
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test all required imports"""
    print("\n" + "=" * 70)
    print("TEST 1: Checking Imports")
    print("=" * 70)
    try:
        from langchain_openai import OpenAI
        import streamlit as st
        import langchain
        print("[PASS] All imports successful")
        print(f"  - LangChain version: {langchain.__version__}")
        print(f"  - Streamlit version: {st.__version__}")
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False

def test_api_key():
    """Test API key loading"""
    print("\n" + "=" * 70)
    print("TEST 2: Checking API Key")
    print("=" * 70)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        print("[PASS] API Key loaded successfully")
        print(f"  Key: {api_key[:30]}...")
        return True
    else:
        print("[FAIL] API Key not found or invalid")
        print("  Make sure .env file has: OPENAI_API_KEY = your-key-here")
        return False

def test_openai_init():
    """Test OpenAI initialization"""
    print("\n" + "=" * 70)
    print("TEST 3: Initializing OpenAI Client")
    print("=" * 70)
    try:
        from langchain_openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5, api_key=api_key)
        print("[PASS] OpenAI client initialized")
        print("  - Model: gpt-3.5-turbo")
        print("  - Temperature: 0.5")
        return llm
    except Exception as e:
        print(f"[FAIL] Initialization error: {e}")
        return None

def test_api_call(llm):
    """Test actual API call"""
    print("\n" + "=" * 70)
    print("TEST 4: Testing API Call")
    print("=" * 70)

    if llm is None:
        print("[SKIP] Skipping (OpenAI not initialized)")
        return False

    print("Sending test request to OpenAI (this may take 5-10 seconds)...")
    try:
        response = llm.invoke("Say 'Chatbot is working!' in one sentence.")
        print("[PASS] API call successful!")
        print(f"Response: {response.strip()}")
        return True
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg:
            print("[FAIL] Quota/Billing Issue")
            print("  Your OpenAI account has exceeded its quota.")
            print("  Please fix your billing: https://platform.openai.com/account/billing/overview")
            print("  See BILLING_FIX_GUIDE.md for detailed instructions")
            return False
        elif "rate_limit" in error_msg:
            print("[FAIL] Rate limit exceeded")
            print("  Try again in 30 seconds")
            return False
        else:
            print(f"[FAIL] API Error: {error_msg[:200]}")
            return False

def print_summary(results):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    tests = [
        ("Imports", results[0]),
        ("API Key", results[1]),
        ("OpenAI Init", results[2]),
        ("API Call", results[3])
    ]

    passed = sum(1 for _, result in tests if result)
    total = len(tests)

    for name, result in tests:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")

    print("\n" + "-" * 70)
    print(f"Result: {passed}/{total} tests passed")

    if passed == total:
        print("\nAll systems GO! Ready to run the chatbot:")
        print("  cd \"D:\\Chatbot AI\\repo\"")
        print("  .\\venv\\Scripts\\Activate.ps1")
        print("  streamlit run app.py")
        print("\nThen open: http://localhost:8501")
    elif passed == 3:
        print("\nBilling issue detected. See BILLING_FIX_GUIDE.md for help.")
    else:
        print("\nSome tests failed. Check errors above.")

    print("=" * 70 + "\n")

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("CHATBOT TEST SUITE")
    print("=" * 70)

    # Run tests
    result_imports = test_imports()
    result_api_key = test_api_key()
    llm = test_openai_init()
    result_llm_init = llm is not None
    result_api_call = test_api_call(llm)

    # Print summary
    print_summary([result_imports, result_api_key, result_llm_init, result_api_call])

    # Exit with appropriate code
    sys.exit(0 if (result_imports and result_api_key and result_llm_init and result_api_call) else 1)

if __name__ == "__main__":
    main()

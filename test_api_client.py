"""
Example client script to test the Multi-Agent Decision Making API.
"""

import asyncio
import httpx
import sys


BASE_URL = "http://localhost:8000"


async def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")


async def test_mermaid():
    """Test the mermaid diagram endpoint."""
    print("Testing mermaid diagram endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/graph/mermaid")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Mermaid code length: {len(data['mermaid_code'])} characters\n")


async def test_sync_decision(query: str):
    """Test synchronous decision making."""
    print(f"Testing synchronous decision with query: '{query}'...")
    print("This may take a while...\n")
    
    async with httpx.AsyncClient(timeout=300.0) as client:  # 5 minute timeout
        try:
            response = await client.post(
                f"{BASE_URL}/decision/run",
                json={"decision_query": query}
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("\n" + "="*60)
                print("DECISION RESULTS")
                print("="*60)
                print(f"\nSelected Decision:\n{data['selected_decision']}\n")
                print(f"Comment:\n{data['selected_decision_comment']}\n")
                print(f"\nBest Alternative:\n{data['alternative_decision']}\n")
                print(f"Comment:\n{data['alternative_decision_comment']}\n")
                print("="*60 + "\n")
            else:
                print(f"Error: {response.text}\n")
        except Exception as e:
            print(f"Error occurred: {str(e)}\n")


async def test_async_decision(query: str):
    """Test asynchronous decision making."""
    print(f"Testing asynchronous decision with query: '{query}'...")
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            # Start the process
            print("Starting decision process...")
            response = await client.post(
                f"{BASE_URL}/decision/start",
                json={"decision_query": query}
            )
            
            if response.status_code != 200:
                print(f"Error starting process: {response.text}\n")
                return
            
            data = response.json()
            process_id = data["process_id"]
            print(f"Process ID: {process_id}")
            print("Polling for completion...\n")
            
            # Poll for completion
            poll_count = 0
            while True:
                await asyncio.sleep(3)  # Wait 3 seconds between polls
                poll_count += 1
                
                status_response = await client.get(
                    f"{BASE_URL}/decision/status/{process_id}"
                )
                status_data = status_response.json()
                
                print(f"Poll #{poll_count}: Status = {status_data['status']}")
                
                if status_data["status"] == "completed":
                    print("\n" + "="*60)
                    print("DECISION RESULTS")
                    print("="*60)
                    result = status_data["result"]
                    print(f"\nSelected Decision:\n{result['selected_decision']}\n")
                    print(f"Comment:\n{result['selected_decision_comment']}\n")
                    print(f"\nBest Alternative:\n{result['alternative_decision']}\n")
                    print(f"Comment:\n{result['alternative_decision_comment']}\n")
                    print("="*60 + "\n")
                    break
                elif status_data["status"] == "failed":
                    print(f"\nProcess failed: {status_data.get('error', 'Unknown error')}\n")
                    break
                
                # Safety limit
                if poll_count > 100:
                    print("\nPolling limit reached. Process may still be running.\n")
                    break
        except Exception as e:
            print(f"Error occurred: {str(e)}\n")


async def test_cli_decision(query: str):
    """Test CLI mode decision making."""
    print(f"Testing CLI mode decision with query: '{query}'...")
    print("This may take a while...\n")
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/decision/cli",
                json={"decision_query": query}
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("\n" + "="*60)
                print("CLI MODE RESULTS")
                print("="*60)
                print(f"\nStatus: {data['status']}")
                print(f"\nPersistence file: {data['persistence_file']}")
                print(f"\nExecution history ({len(data['execution_history'])} steps):")
                for i, step in enumerate(data['execution_history'], 1):
                    print(f"  {i}. {step}")
                
                final_state = data['final_state']
                print(f"\nSelected Decision:\n{final_state['selected_decision']}\n")
                print(f"Comment:\n{final_state['selected_decision_comment']}\n")
                print("="*60 + "\n")
            else:
                print(f"Error: {response.text}\n")
        except Exception as e:
            print(f"Error occurred: {str(e)}\n")


async def main():
    """Main test runner."""
    print("\n" + "="*60)
    print("Multi-Agent Decision Making API - Test Client")
    print("="*60 + "\n")
    
    if len(sys.argv) < 2:
        print("Usage: python test_api_client.py <test_type> [decision_query]")
        print("\nTest types:")
        print("  health      - Test health endpoint")
        print("  mermaid     - Test mermaid diagram endpoint")
        print("  sync        - Test synchronous decision (requires query)")
        print("  async       - Test asynchronous decision (requires query)")
        print("  cli         - Test CLI mode decision (requires query)")
        print("  all         - Run all basic tests (health, mermaid)")
        print("\nExamples:")
        print('  python test_api_client.py health')
        print('  python test_api_client.py sync "Should I invest in AI?"')
        print('  python test_api_client.py async "Should I hire more staff?"')
        return
    
    test_type = sys.argv[1].lower()
    decision_query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
    
    try:
        if test_type == "health":
            await test_health()
        
        elif test_type == "mermaid":
            await test_mermaid()
        
        elif test_type == "sync":
            if not decision_query:
                print("Error: Decision query required for sync test")
                print('Example: python test_api_client.py sync "Should I invest in AI?"')
                return
            await test_sync_decision(decision_query)
        
        elif test_type == "async":
            if not decision_query:
                print("Error: Decision query required for async test")
                print('Example: python test_api_client.py async "Should I hire more staff?"')
                return
            await test_async_decision(decision_query)
        
        elif test_type == "cli":
            if not decision_query:
                print("Error: Decision query required for CLI test")
                print('Example: python test_api_client.py cli "Should I expand internationally?"')
                return
            await test_cli_decision(decision_query)
        
        elif test_type == "all":
            await test_health()
            await test_mermaid()
        
        else:
            print(f"Unknown test type: {test_type}")
            print("Valid types: health, mermaid, sync, async, cli, all")
    
    except httpx.ConnectError:
        print("\n" + "="*60)
        print("ERROR: Could not connect to API server")
        print("="*60)
        print("\nMake sure the API server is running:")
        print("  uv run uvicorn src.app:app --reload")
        print("  or")
        print("  uv run python src/run_app.py")
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())

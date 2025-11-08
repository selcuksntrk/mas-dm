"""
Test Client for Backend API

This script tests all endpoints of the new backend API to verify functionality.
Can be used to compare responses with the old API.
"""

import asyncio
import time
from typing import Optional

import httpx


class APITestClient:
    """Client for testing the Multi-Agent Decision Making API"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=300.0)  # 5 minute timeout
    
    def test_root(self):
        """Test root endpoint"""
        print("\n" + "=" * 60)
        print("TEST: Root Endpoint (GET /)")
        print("=" * 60)
        
        response = self.client.get(f"{self.base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    
    def test_health(self):
        """Test health check endpoint"""
        print("\n" + "=" * 60)
        print("TEST: Health Check (GET /health)")
        print("=" * 60)
        
        response = self.client.get(f"{self.base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    
    def test_graph_mermaid(self):
        """Test mermaid diagram endpoint"""
        print("\n" + "=" * 60)
        print("TEST: Mermaid Diagram (GET /graph/mermaid)")
        print("=" * 60)
        
        response = self.client.get(f"{self.base_url}/graph/mermaid")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Mermaid code length: {len(data.get('mermaid_code', ''))}")
        print(f"First 200 chars: {data.get('mermaid_code', '')[:200]}...")
        return response.status_code == 200
    
    def test_graph_structure(self):
        """Test graph structure endpoint"""
        print("\n" + "=" * 60)
        print("TEST: Graph Structure (GET /graph/structure)")
        print("=" * 60)
        
        response = self.client.get(f"{self.base_url}/graph/structure")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total nodes: {data.get('total_nodes')}")
        print(f"Agent nodes: {data.get('agent_nodes')}")
        print(f"Evaluator nodes: {data.get('evaluator_nodes')}")
        return response.status_code == 200
    
    def test_decision_sync(self, query: str = "Should I learn Python or JavaScript first?"):
        """Test synchronous decision endpoint"""
        print("\n" + "=" * 60)
        print("TEST: Synchronous Decision (POST /decisions/run)")
        print("=" * 60)
        print(f"Query: {query}")
        print("This may take several minutes...")
        
        start_time = time.time()
        response = self.client.post(
            f"{self.base_url}/decisions/run",
            json={"decision_query": query}
        )
        elapsed = time.time() - start_time
        
        print(f"Status: {response.status_code}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nSelected Decision: {data.get('selected_decision', '')[:200]}...")
            print(f"\nAlternative: {data.get('alternative_decision', '')[:200]}...")
            print(f"\nTrigger: {data.get('trigger', '')[:100]}...")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    
    def test_decision_async(self, query: str = "Should I invest in renewable energy?"):
        """Test asynchronous decision endpoint"""
        print("\n" + "=" * 60)
        print("TEST: Asynchronous Decision (POST /decisions/start)")
        print("=" * 60)
        print(f"Query: {query}")
        
        # Start the process
        response = self.client.post(
            f"{self.base_url}/decisions/start",
            json={"decision_query": query}
        )
        
        print(f"Start Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return False
        
        data = response.json()
        process_id = data.get("process_id")
        print(f"Process ID: {process_id}")
        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        
        # Poll for completion (max 5 minutes)
        print("\nPolling for completion...")
        max_attempts = 60  # 5 minutes
        attempt = 0
        
        while attempt < max_attempts:
            time.sleep(5)  # Wait 5 seconds between checks
            attempt += 1
            
            status_response = self.client.get(
                f"{self.base_url}/decisions/status/{process_id}"
            )
            
            if status_response.status_code != 200:
                print(f"Error checking status: {status_response.text}")
                return False
            
            status_data = status_response.json()
            current_status = status_data.get("status")
            print(f"Attempt {attempt}: Status = {current_status}")
            
            if current_status == "completed":
                print("\n✅ Process completed!")
                result = status_data.get("result", {})
                print(f"Selected Decision: {result.get('selected_decision', '')[:200]}...")
                return True
            
            elif current_status == "failed":
                print(f"\n❌ Process failed: {status_data.get('error')}")
                return False
        
        print("\n⏱️ Timeout: Process did not complete in 5 minutes")
        return False
    
    def test_processes_list(self):
        """Test list processes endpoint"""
        print("\n" + "=" * 60)
        print("TEST: List Processes (GET /decisions/processes)")
        print("=" * 60)
        
        response = self.client.get(f"{self.base_url}/decisions/processes")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Stats: {data.get('stats')}")
            print(f"Total processes: {len(data.get('processes', []))}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    
    def test_cleanup(self):
        """Test cleanup endpoint"""
        print("\n" + "=" * 60)
        print("TEST: Cleanup Processes (DELETE /decisions/cleanup)")
        print("=" * 60)
        
        response = self.client.delete(f"{self.base_url}/decisions/cleanup")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Message: {data.get('message')}")
            print(f"Remaining: {data.get('remaining_processes')}")
            print(f"Stats: {data.get('stats')}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    
    def run_quick_tests(self):
        """Run quick tests (no decision execution)"""
        print("\n" + "🚀 " * 20)
        print("RUNNING QUICK TESTS (No AI execution)")
        print("🚀 " * 20)
        
        results = {
            "Root": self.test_root(),
            "Health": self.test_health(),
            "Graph Mermaid": self.test_graph_mermaid(),
            "Graph Structure": self.test_graph_structure(),
            "List Processes": self.test_processes_list(),
            "Cleanup": self.test_cleanup(),
        }
        
        self._print_summary(results)
        return results
    
    def run_full_tests(self, test_async: bool = False):
        """Run full tests including decision execution"""
        print("\n" + "🚀 " * 20)
        print("RUNNING FULL TESTS (Including AI execution)")
        print("🚀 " * 20)
        
        results = {
            "Root": self.test_root(),
            "Health": self.test_health(),
            "Graph Mermaid": self.test_graph_mermaid(),
            "Graph Structure": self.test_graph_structure(),
            "Synchronous Decision": self.test_decision_sync(),
        }
        
        if test_async:
            results["Asynchronous Decision"] = self.test_decision_async()
        
        results["List Processes"] = self.test_processes_list()
        results["Cleanup"] = self.test_cleanup()
        
        self._print_summary(results)
        return results
    
    def _print_summary(self, results: dict):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, passed_test in results.items():
            status = "✅ PASS" if passed_test else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print("-" * 60)
        print(f"Results: {passed}/{total} tests passed")
        print("=" * 60)
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {total - passed} test(s) failed")
    
    def close(self):
        """Close the HTTP client"""
        self.client.close()


def main():
    """Main test function"""
    import sys
    
    # Parse command line arguments
    test_type = sys.argv[1] if len(sys.argv) > 1 else "quick"
    base_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8001"
    
    print(f"Testing API at: {base_url}")
    
    client = APITestClient(base_url)
    
    try:
        if test_type == "full":
            client.run_full_tests(test_async=False)
        elif test_type == "full-async":
            client.run_full_tests(test_async=True)
        else:
            client.run_quick_tests()
    
    finally:
        client.close()


if __name__ == "__main__":
    main()

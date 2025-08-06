"""
NewsCheckr Test Examples
Sample data and test cases for testing the API
"""

import requests
import json
from typing import List, Dict

# Test URLs for different news sources and content types
TEST_URLS = [
    # High credibility sources
    "https://www.reuters.com/business/finance/",
    "https://apnews.com/",
    "https://www.bbc.com/news",
    
    # Various bias examples (these are example URLs - replace with real ones for testing)
    "https://www.cnn.com/politics",
    "https://www.foxnews.com/politics", 
    "https://www.npr.org/sections/news/",
]

# Sample article texts for testing without URLs
SAMPLE_ARTICLES = {
    "high_credibility": """
    The Federal Reserve announced today a 0.25 percentage point increase in the federal funds rate, 
    bringing it to a range of 5.25% to 5.5%, the highest level in 22 years. The decision was 
    unanimous among voting members of the Federal Open Market Committee. Chair Jerome Powell 
    stated in a press conference that the move reflects the committee's commitment to returning 
    inflation to the 2% target over time. Economic data released earlier this month showed 
    core inflation remains above the Fed's target, though it has moderated from peak levels 
    seen last year. The central bank will continue to assess incoming data to determine future 
    policy actions, Powell noted.
    """,
    
    "medium_credibility": """
    Sources close to the administration suggest that major policy changes could be announced 
    as early as next week, though no official confirmation has been provided. Industry experts 
    believe the potential changes could significantly impact the technology sector, with some 
    analysts predicting both positive and negative outcomes depending on implementation details. 
    While some stakeholders have expressed cautious optimism, others remain skeptical about 
    the timing and scope of any potential reforms. The White House press secretary declined 
    to comment on the speculation during yesterday's briefing.
    """,
    
    "low_credibility": """
    SHOCKING REVELATION!!! Government officials HATE this one simple trick that EVERYONE 
    needs to know! Leaked documents reveal the TRUTH they don't want you to see! Anonymous 
    sources confirm what we've suspected all along - the CONSPIRACY runs deeper than anyone 
    imagined! Click here to learn the secrets THEY don't want you to know! This will 
    change EVERYTHING you thought you knew about politics! Share this before it gets DELETED!
    """,
    
    "left_bias": """
    Progressive advocacy groups celebrated today's announcement of new climate initiatives 
    designed to accelerate the transition to renewable energy and create thousands of 
    green jobs. The comprehensive plan includes significant investments in solar and wind 
    infrastructure, as well as support for disadvantaged communities disproportionately 
    affected by pollution. Environmental justice advocates praised the administration's 
    commitment to addressing systemic inequalities while tackling the climate crisis. 
    The initiative represents a major step forward in fulfilling campaign promises to 
    prioritize environmental protection and social equity.
    """,
    
    "right_bias": """
    Conservative lawmakers voiced strong opposition to the proposed tax increases, arguing 
    they would burden hardworking families and small businesses already struggling with 
    inflation. The legislation threatens to undermine economic growth and job creation 
    by imposing excessive regulatory compliance costs on entrepreneurs and investors. 
    Free market advocates emphasize that reducing government spending and cutting red tape 
    would be more effective approaches to stimulating the economy. Traditional values 
    supporters also expressed concerns about provisions that could infringe on religious 
    liberty and parental rights.
    """,
    
    "center_bias": """
    The bipartisan infrastructure committee released its final report today, presenting 
    a balanced analysis of both the benefits and challenges associated with the proposed 
    legislation. Committee members from both parties acknowledged the complexity of funding 
    mechanisms while recognizing the critical need for infrastructure improvements. The 
    report includes input from various stakeholders, including business leaders, labor 
    unions, and community organizations, reflecting diverse perspectives on implementation 
    priorities. Independent economic analysis suggests the plan could generate both costs 
    and benefits that will vary across different regions and sectors.
    """
}


def test_api_with_url(url: str, api_endpoint: str = "http://localhost:5000/analyze"):
    """Test the API with a real URL."""
    try:
        payload = {"url": url}
        response = requests.post(
            api_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}


def test_api_with_text(text: str, source: str = "test", api_endpoint: str = "http://localhost:5000/test"):
    """Test the API with sample text."""
    try:
        payload = {"text": text, "source": source}
        response = requests.post(
            api_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}


def run_all_tests():
    """Run comprehensive tests of the NewsCheckr API."""
    
    print("=" * 60)
    print("NewsCheckr API Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check failed: {str(e)}")
    
    # Test 2: Text analysis with sample articles
    print("\n2. Testing text analysis with sample articles...")
    for article_type, text in SAMPLE_ARTICLES.items():
        print(f"\nTesting {article_type}:")
        result = test_api_with_text(text, article_type)
        
        if "error" not in result:
            print(f"✓ Source: {result['source']}")
            print(f"✓ Credibility Score: {result['credibility_score']}")
            print(f"✓ Bias: {result['bias']}")
            print(f"✓ Summary: {result['summary'][:100]}...")
            print(f"✓ Labels: {result['labels']}")
        else:
            print(f"✗ Error: {result['error']}")
    
    # Test 3: Known sources endpoint
    print("\n3. Testing known sources endpoint...")
    try:
        response = requests.get("http://localhost:5000/sources")
        if response.status_code == 200:
            sources_data = response.json()
            print(f"✓ Found {sources_data['total_sources']} known sources")
            print("Sample sources:")
            for source, data in list(sources_data['known_sources'].items())[:3]:
                print(f"  {source}: Credibility={data['credibility']}, Bias={data['bias']}")
        else:
            print(f"✗ Sources endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Sources endpoint failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)


def generate_sample_requests():
    """Generate sample request examples for documentation."""
    
    samples = {
        "analyze_url": {
            "method": "POST",
            "endpoint": "/analyze",
            "headers": {"Content-Type": "application/json"},
            "body": {"url": "https://www.reuters.com/business/finance/fed-raises-rates-2023-07-26/"}
        },
        "test_text": {
            "method": "POST", 
            "endpoint": "/test",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "text": "The Federal Reserve announced a rate increase today...",
                "source": "example.com"
            }
        },
        "health_check": {
            "method": "GET",
            "endpoint": "/",
            "headers": {},
            "body": {}
        },
        "list_sources": {
            "method": "GET",
            "endpoint": "/sources", 
            "headers": {},
            "body": {}
        }
    }
    
    print("Sample API Requests:")
    print("=" * 40)
    
    for name, request in samples.items():
        print(f"\n{name.upper()}:")
        print(f"Method: {request['method']}")
        print(f"Endpoint: {request['endpoint']}")
        if request['body']:
            print(f"Body: {json.dumps(request['body'], indent=2)}")
        
        # Generate curl command
        if request['method'] == 'GET':
            curl_cmd = f"curl -X GET http://localhost:5000{request['endpoint']}"
        else:
            curl_cmd = f"""curl -X POST http://localhost:5000{request['endpoint']} \\
     -H "Content-Type: application/json" \\
     -d '{json.dumps(request['body'])}'"""
        
        print(f"Curl: {curl_cmd}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            run_all_tests()
        elif sys.argv[1] == "samples":
            generate_sample_requests()
        elif sys.argv[1] == "url" and len(sys.argv) > 2:
            result = test_api_with_url(sys.argv[2])
            print(json.dumps(result, indent=2))
        else:
            print("Usage:")
            print("  python test_examples.py test      # Run all tests")
            print("  python test_examples.py samples   # Show sample requests")
            print("  python test_examples.py url <URL> # Test specific URL")
    else:
        print("NewsCheckr Test Examples")
        print("Available sample articles:")
        for key in SAMPLE_ARTICLES.keys():
            print(f"  - {key}")
        print("\nRun with 'test' argument to execute tests")
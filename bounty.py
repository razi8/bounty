import requests
import json
import argparse
import base64

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-hu', '--hackerone-username', required=True, help='HackerOne API username')
parser.add_argument('-ht', '--hackerone-token', required=True, help='HackerOne API token')
parser.add_argument('-it', '--inspectiv-token', required=True, help='Inspectiv API token')
args = parser.parse_args()

# Set up authentication headers with the base64-encoded HackerOne API username and token
hu_auth = base64.b64encode(f"{args.hackerone_username}:{args.hackerone_token}".encode('ascii')).decode('ascii')
hu_headers = {
    'Authorization': f'Basic {hu_auth}',
    'Content-Type': 'application/json',
}

# Set up authentication headers with the Inspectiv API token
it_headers = {
    'Authorization': f'Token {args.inspectiv_token}',
    'Content-Type': 'application/json',
}

# Set up initial variables
hu_earnings_total = 0
hu_next_page_url = 'https://api.hackerone.com/v1/hackers/payments/earnings'
it_url = 'https://api.inspectiv.io/cesppa/api/accounts/researcher-dashboard/'

# Loop through all pages of earnings data for HackerOne
while hu_next_page_url:
    # Make a request to the HackerOne API to retrieve the earnings data for the current page
    hu_response = requests.get(hu_next_page_url, headers=hu_headers)

    # Parse the response as JSON
    hu_data = json.loads(hu_response.text)

    # Loop through the data and track the total earnings for HackerOne
    for earning in hu_data['data']:
        hu_earnings_total += earning['attributes']['amount']

    # Check if there are more pages of data to retrieve for HackerOne
    if 'next' in hu_data['links']:
        hu_next_page_url = hu_data['links']['next']
    else:
        hu_next_page_url = None

# Make a request to the Inspectiv API to retrieve the earnings data
it_response = requests.get(it_url, headers=it_headers)

# Parse the response as JSON
it_data = json.loads(it_response.text)

# Retrieve the total earnings for Inspectiv
it_earnings_total = it_data['payment_stats']['earned']

# Print the total earnings for both HackerOne and Inspectiv
print(f'Total earnings from HackerOne: ${hu_earnings_total:.2f}')
print(f'Total earnings from Inspectiv: ${it_earnings_total:.2f}')
print(f'Combined total earnings: ${(hu_earnings_total + it_earnings_total):.2f}')


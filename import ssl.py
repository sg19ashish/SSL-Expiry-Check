import ssl
import socket
from datetime import datetime
import csv

def get_certificate_expiry_date(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            return expiry_date

# Define the file paths
input_file_path = 'C:\\<dir>\\<dir>\\urls.txt'   ## Provide the path to the text file containing the URLs
output_file_path = 'C:\\<dir>\\<dir>\\certificate_expiry_dates.csv'  ## Provide the path to the CSV file to write the results

# Read URLs from the text file
with open(input_file_path, 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Prepare the CSV file to write the results
with open(output_file_path, 'w', newline='') as csvfile:
    fieldnames = ['URL', 'Expiry Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Check the certificate expiry date for each URL and write to CSV
    for url in urls:
        try:
            # Remove the protocol (http:// or https://) if present
            hostname = url.replace("https://", "").replace("http://", "").split('/')[0]
            expiry_date = get_certificate_expiry_date(hostname)
            writer.writerow({'URL': url, 'Expiry Date': expiry_date})
        except Exception as e:
            writer.writerow({'URL': url, 'Expiry Date': f"Error: {e}"})
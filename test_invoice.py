import requests
import json
import os
from datetime import datetime
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Test DF-Accountant invoice generation')
parser.add_argument('--url', default='http://localhost:5000/api/v1/getInvoice', 
                    help='API endpoint URL (default: http://localhost:5000/api/v1/getInvoice)')
parser.add_argument('--output', default=None, 
                    help='Output PDF filename (default: auto-generated)')
args = parser.parse_args()

# API endpoint from args
API_URL = args.url

print(f"Using API endpoint: {API_URL}")

# Test data matching the expected format
test_data = {
  "autoSchool": {
    "name": "DiamondAuto",
    "website": "https://diamondauto.ro",
    "phone": "+40723111222",
    "email": "office@diamondauto.ro"
  },
  "student": {
    "firstName": "Ioana",
    "lastName": "Marin",
    "email": "ioana.marin@student.ro",
    "phone": "0734567890"
  },
  "file": {
    "scholarshipStartDate": "2025-01-10",
    "criminalRecordExpiryDate": "2026-01-10",
    "medicalRecordExpiryDate": "2025-07-10",
    "status": "completed"
  },
  "teachingCategory": {
    "type": "B",
    "sessionCost": 150,
    "sessionDuration": 120,
    "scholarshipPrice": 2250,
    "minDrivingLessonsReq": 15
  },
  "vehicle": {
    "licensePlateNumber": "CJ-456-ABC",
    "transmissionType": "M",
    "color": "blue",
    "licenseType": "B"
  },
  "instructor": {
    "fullName": "Andrei Popescu"
  },
  "payment": {
    "sessionsPayed": 30,
    "scholarshipBasePayment": true
  }
}

def test_generate_invoice():
    """
    Test the invoice generation endpoint
    """
    print(f"Testing invoice generation at {API_URL}...")
    
    try:
        # Send POST request to generate invoice
        response = requests.post(
            API_URL,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Check response status
        if response.status_code == 200:
            # Save the PDF
            if args.output:
                filename = args.output
            else:
                filename = f"test_invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print(f"Success! Invoice generated and saved as {filename}")
            print(f"File size: {os.path.getsize(filename)} bytes")
            return True
        else:
            print(f"Error: HTTP {response.status_code}")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_generate_invoice() 
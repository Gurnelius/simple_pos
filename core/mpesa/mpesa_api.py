import base64
import requests
from django.conf import settings
from datetime import datetime

class Mpesa:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY  
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.api_url = "https://sandbox.safaricom.co.ke"  
        self.business_shortcode = settings.MPESA_BUSINESS_SHORTCODE
        self.lipa_na_mpesa_online_passkey = settings.MPESA_PASSKEY

    def get_access_token(self):
        """
        Get the access token required for API calls.
        """
        auth_url = f"{self.api_url}/oauth/v1/generate?grant_type=client_credentials"
        auth_response = requests.get(auth_url, auth=(self.consumer_key, self.consumer_secret))
        access_token = auth_response.json().get('access_token')
        return access_token

    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """
        Initiates an STK Push (Lipa na MPesa Online Payment)
        """
        access_token = self.get_access_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{self.business_shortcode}{self.lipa_na_mpesa_online_passkey}{timestamp}".encode()
        ).decode("utf-8")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,  # The phone number of the customer making the payment
            "PartyB": self.business_shortcode,  # Your Business ShortCode
            "PhoneNumber": phone_number,
            "CallBackURL": settings.MPESA_CALLBACK_URL,  # URL to receive the payment confirmation
            "AccountReference": account_reference,  # Order or Invoice Number
            "TransactionDesc": transaction_desc  # Description of the transaction
        }
        
        stk_push_url = f"{self.api_url}/mpesa/stkpush/v1/processrequest"
        response = requests.post(stk_push_url, json=payload, headers=headers)
        return response.json()

    def handle_callback(self, request):
        """
        Handle the payment callback from Safaricom's API.
        """
        # Parse the callback response and update the order status
        callback_data = request.body
        print("Callback received:", callback_data)
        # Process callback data here (e.g., check if payment was successful, update DB)
        return callback_data

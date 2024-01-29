from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from decimal import Decimal as D, ROUND_HALF_UP
from redsys.constants import EUR, STANDARD_PAYMENT
from redsys.client import RedirectClient
from django.views.decorators.csrf import csrf_exempt
import base64
import json
import hmac
from Crypto.Cipher import DES3
import hashlib
from typing import Any
from typing import Dict
from django.http import JsonResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def success(request):
    template = loader.get_template("redsys/successful_payment.html")
    context = {
        "payment_id": "123",
    }
    return HttpResponse(template.render(context, request))

def sign_hmac256(encrypted_order: bytes, merchant_parameters: bytes) -> bytes:
    """
    Generates the encrypted signature using the 3DES-encrypted order
    and base64-encoded merchant parameters
    """
    signature = hmac.new(encrypted_order, merchant_parameters, hashlib.sha256).digest()
    return base64.b64encode(signature)

def encode_parameters(parameters: Dict[str, Any]) -> bytes:
    return base64.b64encode(json.dumps(parameters).encode())


@csrf_exempt
def make_payment(request):
    # secret_key = "f77UMdYa/fMjOamg1rTtttL/6PsYDrQP"
    secret_key = "sq7HjrUOBfKmC576ILgskD5srU870gJ7"
    parameters = {
        "Ds_Merchant_MerchantCode": "014407381",
        "Ds_Merchant_MerchantName": "MillonApp",
        "Ds_Merchant_Terminal": "2",
        "Ds_Merchant_TransactionType": "0",
        "Ds_Merchant_Currency": 978,
        "Ds_Merchant_Order": "000000000015",
        "Ds_Merchant_Amount": 2000,
    }


    merchant_parameters = encode_parameters(parameters)

    cipher = DES3.new(base64.b64decode(secret_key), DES3.MODE_CBC, IV=b"\0\0\0\0\0\0\0\0")
    encrypted_order = cipher.encrypt(parameters["Ds_Merchant_Order"].encode().ljust(16, b"\0"))
    signature = base64.b64encode(hmac.new(encrypted_order, merchant_parameters, hashlib.sha256).digest())

    return JsonResponse({
        "Ds_SignatureVersion": "HMAC_SHA256_V1",
        "Ds_MerchantParameters": merchant_parameters.decode("utf-8") ,
        "Ds_Signature": signature.decode("utf-8"),
    })

    parameters = {
        "merchant_code": "999008881",
        "terminal": "002",
        "transaction_type": STANDARD_PAYMENT,
        "currency": EUR,
        "order": "000000000012",
        "amount": D("20.00").quantize(D(".01"), ROUND_HALF_UP),
        # "merchant_data": "test merchant data",
        # "merchant_name": "MillonApp",
        # "merchant_identifier": "REQUIRED",
        # "titular": "John Doe",    
        # "product_description": "Prueba para guardar tarjeta",
        # "merchant_url": "https://example.com/redsys/response",
        # "url_ok": "https://google.com",
        # "url_ko": "https://nba.com"
    }

    client = RedirectClient(secret_key)
    args = client.prepare_request(parameters)
    return JsonResponse({
        "Ds_SignatureVersion": "HMAC_SHA256_V1",
        "Ds_MerchantParameters": args['Ds_MerchantParameters'].decode("utf-8"),
        "Ds_Signature": args['Ds_Signature'].decode("utf-8"),
    })

    return HttpResponse()
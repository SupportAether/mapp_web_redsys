# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from sermepa.forms import SermepaPaymentForm
from sermepa.signals import payment_was_successful, payment_was_error, signature_error
from sermepa.models import SermepaIdTPV
from django.template import loader

def form(request, trans_type='0'):
    amount = int(5.50 * 100) # El precio es en céntimos de euro

    merchant_parameters = {
        "Ds_Merchant_Titular": 'John Doe',
        "Ds_Merchant_MerchantData": 12345, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
        "Ds_Merchant_MerchantName": 'ACME',
        "Ds_Merchant_ProductDescription": 'petardos',
        "Ds_Merchant_Amount": amount,
        "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
        "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
        "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
        "Ds_Merchant_MerchantURL": "http://%s%s" % (settings.SERMEPA_SITE_DOMAIN, reverse('sermepa_ipn')),
        "Ds_Merchant_UrlOK": "http://%s%s" % (settings.SERMEPA_SITE_DOMAIN, reverse('end')),
        "Ds_Merchant_UrlKO": "http://%s%s" % (settings.SERMEPA_SITE_DOMAIN, reverse('end')),
    }

    if True: #Compra puntual
        # order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        merchant_parameters.update({
            "Ds_Merchant_Order": "000000000013",
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'L': #Compra recurrente por fichero. Cobro inicial
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'M': #Compra recurrente por fichero. Cobros sucesivos
        # order = suscripcion.idtpv #Primer idtpv, 10 dígitos
        order = ''
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0': #Compra recurrente por Referencia. Cobro inicial
        order = 'REQUIRED'
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0': #Compra recurrente por Referencia. Cobros sucesivos
        # order = suscripcion.idreferencia #Primer idtpv, 10 dígitos
        order = ''
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '3': #Devolución
        # order = suscripcion.idreferencia #Primer idtpv, 10 dígitos
        order = ''
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
            #"Ds_Merchant_AuthorisationCode": pedido.Ds_AuthorisationCode, #Este valor sale
            "Ds_Merchant_AuthorisationCode": '',
            # de la SermepaResponse obtenida del cobro que se quiere devolver.
        })

    form = SermepaPaymentForm(merchant_parameters)
    template = loader.get_template("sermepa-test/form.html")
    return HttpResponse(template.render({'form': form, 'debug': settings.DEBUG}, request))
    
def end(request):
    return render(request, 'end.html', {})
    
def payment_ok(sender, **kwargs):
    pass

def payment_ko(sender, **kwargs):
    pass

def sermepa_ipn_error(sender, **kwargs):
    pass

payment_was_successful.connect(payment_ok)
payment_was_error.connect(payment_ko)
signature_error.connect(sermepa_ipn_error)

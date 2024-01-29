# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from .utils import redsys_generate_request

class SermepaPaymentForm(forms.Form):
    Ds_SignatureVersion = forms.IntegerField(widget=forms.HiddenInput())
    Ds_MerchantParameters = forms.IntegerField(widget=forms.HiddenInput())
    Ds_Signature = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        merchant_parameters = kwargs.pop('merchant_parameters', None)
        super(SermepaPaymentForm, self).__init__(*args, **kwargs)

        if merchant_parameters:
            # Generate needed parameters using 256 signature Redsys method
            Ds_MerchantParameters, Ds_Signature = redsys_generate_request(merchant_parameters)

            # Parameters to send to RedSys
            self.initial['Ds_SignatureVersion'] = settings.SERMEPA_SIGNATURE_VERSION
            self.initial['Ds_MerchantParameters'] = Ds_MerchantParameters
            self.initial['Ds_Signature'] = Ds_Signature

    def render(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="submit" name="submit" alt="%s" value="%s"/>
        </form>""" % (settings.SERMEPA_URL_PRO, self.as_p(), settings.SERMEPA_BUTTON_TEXT,
                      settings.SERMEPA_BUTTON_TEXT))

    def sandbox(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            <input type="text" name="Ds_SignaturaVersion" value="%s" />
            <input type="text" name="Ds_MerchantParameters" value="%s" />
            <input type="text" name="Ds_Signature" value="%s" />
            <input type="submit" name="submit" alt="%s" value="%s"/>
        </form>""" % (settings.SERMEPA_URL_TEST, settings.SERMEPA_SIGNATURE_VERSION, "eyJEc19NZXJjaGFudF9BbW91bnQiOiAiMjAwMCIsICJEc19NZXJjaGFudF9DdXJyZW5jeSI6ICI5NzgiLCAiRHNfTWVyY2hhbnRfTWVyY2hhbnRDb2RlIjogIjk5OTAwODg4MSIsICJEc19NZXJjaGFudF9PcmRlciI6ICIwMDAwMDAwMDAwMTIiLCAiRHNfTWVyY2hhbnRfVGVybWluYWwiOiAiMSIsICJEc19NZXJjaGFudF9UcmFuc2FjdGlvblR5cGUiOiAiMCIsICJEc19NZXJjaGFudF9EaXJlY3RQYXltZW50IjogInRydWUiLCAiRHNfTWVyY2hhbnRfSWRlbnRpZmllciI6ICJSRVFVSVJFRCIsICJEc19NZXJjaGFudF9VcmxPSyI6ICJodHRwczovL2dvb2dsZS5jb20iLCAiRHNfTWVyY2hhbnRfVXJsS08iOiAiaHR0cHM6Ly9uYmEuY29tIn0=", "0Nc58VQyOTfsLHOgWXSdMKes1ntZMUdjYS+oy6gdjBg=", settings.SERMEPA_BUTTON_TEXT,
                      settings.SERMEPA_BUTTON_TEXT))


class SermepaResponseForm(forms.Form):
    Ds_SignatureVersion = forms.CharField(max_length=256)
    Ds_Signature = forms.CharField(max_length=256)
    Ds_MerchantParameters = forms.CharField(max_length=2048)

    Ds_Date = forms.DateField(required=False, input_formats=('%d/%m/%Y',))
    Ds_Hour = forms.TimeField(required=False, input_formats=('%H:%M',))

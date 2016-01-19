# coding: utf-8


from django import forms


class EmailInput(forms.TextInput):
    input_type = "email"


class PhoneInput(forms.TextInput):
    input_type = "tel"

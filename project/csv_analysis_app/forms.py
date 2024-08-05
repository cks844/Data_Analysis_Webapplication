from django import forms

# Django form for handling file uploads
class UploadFileForm(forms.Form):
    file = forms.FileField()

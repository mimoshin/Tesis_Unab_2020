from django import forms


class pruebaForm(forms.Form):
    firstName= forms.CharField(label='nombre',max_length=100)
    lastName = forms.CharField(label='apellido',max_length=100)

class otroForm(forms.Form):
    fecha = forms.DateField()
    fecha2 = forms.DateTimeField()

    
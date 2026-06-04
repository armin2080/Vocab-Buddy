from django import forms


class ReviewForm(forms.Form):
    correct = forms.BooleanField(required=False, initial=False)

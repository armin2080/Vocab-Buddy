from django import forms


class ReviewForm(forms.Form):
    correct = forms.BooleanField(required=False, initial=False)


class QuizAnswerForm(forms.Form):
    answer = forms.CharField(max_length=200)

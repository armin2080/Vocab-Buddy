from django import forms


class PracticeMessageForm(forms.Form):
    message = forms.CharField(
        label='Your message',
        max_length=5000,
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Write your German paragraph here...',
            'class': (
                'w-full rounded-xl border border-input bg-input-background px-4 py-3 '
                'text-foreground focus:outline-none focus:ring-2 focus:ring-primary'
            ),
        }),
    )

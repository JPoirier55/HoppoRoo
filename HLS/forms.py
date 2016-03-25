from django import forms


class PostForm(forms.Form):
    """
    We dont actually need this but im leaving it here incase
    """
    name = forms.CharField(max_length=256)
    question = forms.CharField()
    choice_1 = forms.CharField()
    choice_2 = forms.CharField()
    choice_3 = forms.CharField()
    choice_4 = forms.CharField()



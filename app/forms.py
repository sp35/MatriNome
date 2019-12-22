from django import forms
from users import data
from users.models import InterestChoice


class FilterForm(forms.Form):
	age = forms.IntegerField(label="Age", required=False)
	state = forms.ChoiceField(choices = [(None, 'Select')] + data.STATE_CHOICES, required=False)
	interests = forms.ModelMultipleChoiceField(queryset=InterestChoice.objects.all(),
				widget = forms.CheckboxSelectMultiple, required=False)


class SearchForm(forms.Form):
	query = forms.CharField(max_length=50, required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Search by name'}))
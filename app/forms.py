from django import forms


class FilterForm(forms.Form):
	gender = forms.ChoiceField(
		choices=[(None, "Select"), ('M', 'Guys'), ('F', 'Girls')], 
		label="Looking for")
	show_matched = forms.ChoiceField(
		choices=[(None, "Select"), (True, 'Matched Profiles'), (False, 'Unmatched')], label="Show")


class SearchForm(forms.Form):
	query = forms.CharField(max_length=50, required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Search by name'}))
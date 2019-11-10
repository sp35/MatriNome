from django import forms


class FilterForm(forms.Form):
	gender = forms.ChoiceField(
		choices=[(None, "Select"), ('M', 'Guys'), ('F', 'Girls')], 
		label="Looking for")
	show_matched = forms.ChoiceField(
		choices=[(None, "Select"), (True, 'Matched Profiles'), (False, 'Unmatched')], label="Show")
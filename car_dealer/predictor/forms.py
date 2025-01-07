from django import forms

class PredictionForm(forms.Form):
    age = forms.FloatField(
        label="Age",
        min_value=18,
        max_value=84,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter age', 'class': 'form-control'})
    )
    sexe = forms.ChoiceField(
        label="Sex",
        choices=[(0, 'Female'), (1, 'Male')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    taux = forms.FloatField(
        label="Taux",
        min_value=20,
        max_value=74185,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter taux', 'class': 'form-control'})
    )
    situationFamiliale = forms.ChoiceField(
        label="Situation Familiale",
        choices=[(0, 'Single'), (1, 'In Couple')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nbEnfantsAcharge = forms.IntegerField(
        label="Number of Children",
        min_value=0,
        max_value=4,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter number of children', 'class': 'form-control'})
    )
    deuxieme_voiture = forms.ChoiceField(
        label="2nd Car",
        choices=[(0, 'No'), (1, 'Yes')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

from django import forms

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        tag_breakfast = cleaned_data.get('tag_breakfast')
        tag_lunch = cleaned_data.get('tag_lunch')
        tag_dinner = cleaned_data.get('tag_dinner')

        if not (tag_breakfast or tag_lunch or tag_dinner):
            msg = 'Выберите хотя бы один тег'
            self.add_error('tag_breakfast', msg)
        return cleaned_data

    class Meta:
        model = Recipe
        exclude = ('slug', 'author', )
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input'},),
            'time': forms.TextInput(
                attrs={'class': 'form__input'}, ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': 8,}),
            'tag_breakfast': forms.CheckboxInput(
                attrs={'class': 'tags__checkbox tags__checkbox_style_orange'}),
            'tag_lunch': forms.CheckboxInput(
                attrs={'class': 'tags__checkbox tags__checkbox_style_green'}),
            'tag_dinner': forms.CheckboxInput(
                attrs={'class': 'tags__checkbox tags__checkbox_style_purple'}),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form__file'}),
        }

from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        tag_breakfast = cleaned_data.get('tag_breakfast')
        tag_lunch = cleaned_data.get('tag_lunch')
        tag_dinner = cleaned_data.get('tag_dinner')

        if not (tag_breakfast or tag_lunch or tag_dinner):
            text_error = 'Необходимо выбрать хотя бы один тег'
            self.add_error('tag_breakfast', text_error)
        error_ingredient = True
        for key in self.data.keys():
            if 'nameIngredient' in key:
                error_ingredient = False
        if error_ingredient:
            text_error = 'Вы забыли добавить ингридиенты'
            self.add_error('tag_lunch', text_error)
        return cleaned_data

    class Meta:
        image = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'class': 'form__file'})
        )

        model = Recipe
        fields = (
            'title', 'tag_breakfast', 'tag_lunch', 'tag_dinner',
            'time_cooking', 'text', 'image'
        )

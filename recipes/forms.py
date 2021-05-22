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
        if not cleaned_data.get('nameIngredient_1'):
            text_error = 'Вы забыли добавить ингридиенты'
            self.add_error('tag_lunch', text_error)
        return cleaned_data


    class Meta:
        model = Recipe
        fields = (
            'title', 'tag_breakfast', 'tag_lunch', 'tag_dinner',
            'time_cooking', 'text', 'image'
        )

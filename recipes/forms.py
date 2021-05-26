from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    def clean(self):
        # Проверка наличия тега
        cleaned_data = super().clean()
        tag_breakfast = cleaned_data.get('tag_breakfast')
        tag_lunch = cleaned_data.get('tag_lunch')
        tag_dinner = cleaned_data.get('tag_dinner')
        if not (tag_breakfast or tag_lunch or tag_dinner):
            text_error = 'Необходимо выбрать хотя бы один тег'
            self.add_error('tag_breakfast', text_error)
        error_ingredient = True

        # Проверка наличия ингредиента и его количества

        for key in self.data.keys():
            if 'nameIngredient' in key:
                error_ingredient = False
                break
        for key in self.data.keys():
            if 'valueIngredient' in key and int(self.data[key]) == 0:
                text_error = 'Кол-во ингредиента не может быть меньше 1'
                self.add_error('tag_lunch', text_error)
                break
        if error_ingredient:
            text_error = 'Вы забыли добавить ингредиенты'
            self.add_error('tag_lunch', text_error)

        # Проверка наличия ингредиента
        time_cooking = cleaned_data.get('time_cooking')
        if time_cooking == 0:
            text_error = 'Время приготовления не может быть меньше 1 минуты'
            self.add_error('time_cooking', text_error)

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

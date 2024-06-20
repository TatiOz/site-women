from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255, min_length=5,
    #                         label="Заголовок",
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         validators=[
    #                             RussianValidator(),
    #                         ],
    #                         error_messages={
    #                             'min_length': 'Слишком короткий заголовок',
    #                             'required': 'Без заголовка никак',
    #                         })
    # slug = forms.SlugField(max_length=255, label="URL",
    #                        validators=[
    #                            MinLengthValidator(5, message="Минимум 5 символов"),
    #                            MaxLengthValidator(100, message="Максимум 100 символов"),
    #                        ])
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    # is_published = forms.BooleanField(required=False, initial=True, label="Статус")


    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", required=False, label="Муж")

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")
    #
    #     return title


    class Meta:
        model = Women
        # fields = '__all__'
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            # 'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title'] #вся вееденная дата заголовка
        if len(title)>50:
            raise ValidationError('Длинна превышвет 50 смиволов')
        return title

class UploadFileForm(forms.Form):
    # file = forms.FileField(label="Файл")
    file = forms.ImageField(label="Файл")



from django import forms

from content.models import Content


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})


class ContentForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = Content
        fields = ('title', 'text', 'image')


class ManagerContentForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = Content
        fields = ('publish',)

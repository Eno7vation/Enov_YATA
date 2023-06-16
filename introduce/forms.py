import os.path

from django import forms

from introduce.models import Apply, DriverApply


class ApplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campus'].required = True
        self.fields['apply_part'].required = True
        self.fields['level'].required = True
        self.fields['phone_number'].required = True
        self.fields['grade'].required = True

    def clean_file(self):
        file = self.cleaned_data.get("grade", None)
        if file:
            extension = os.path.splitext(file.name)[-1].lower()
            if extension not in (".png", ".jpg", ".pdf"):
                raise forms.ValidationError("파일을 업로드해주세요.")
        return file

    class Meta:
        model = Apply
        fields = ['campus', 'apply_part', 'level', 'caption', 'phone_number', 'grade']
        widgets = {

        }
class DriverApplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['caption'].required = True
        self.fields['phone_number'].required = True
        self.fields['campus'].required = True
        self.fields['apply_part'].required = True
        self.fields['driver_license'].required = True

    def clean_photo(self):
        driver_license = self.cleaned_data.get("driver_license", None)
        if driver_license:
            extension = os.path.splitext(driver_license.name)[-1].lower()
            if extension not in (".png", ".jpg", ".pdf"):
                raise forms.ValidationError("파일을 업로드해주세요.")
        return driver_license

    def clean_file(self):
        file = self.cleaned_data.get("file", None)
        if file:
            extension = os.path.splitext(file.name)[-1].lower()
            if extension not in (".png", ".jpg", ".pdf"):
                raise forms.ValidationError("파일을 업로드해주세요.")
        return file

    class Meta:
        model = DriverApply
        fields = ['campus', 'apply_part', 'caption', 'phone_number', 'driver_license', 'file']
        widgets = {

        }
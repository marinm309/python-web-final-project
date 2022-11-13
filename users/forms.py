from django.forms import ModelForm
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserCreationForm(ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'
from django.forms import ModelForm
from .models import CustomUser


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        type = cleaned_data.get("type")
        sending_address = cleaned_data.get("sending_address")
        receiving_address = cleaned_data.get("receiving_address")

        if type in ["Отправитель", "Отправитель и Получатель"] and not sending_address:
            self.add_error("sending_address", "Укажите хотя бы один адрес отправки")
        if type in ["Получатель", "Отправитель и Получатель"] and not receiving_address:
            self.add_error("receiving_address", "Укажите хотя бы один адрес доставки")
        if type in ["Отправитель"] and receiving_address:
            self.add_error("receiving_address", "Укажите только адрес отправки")
        if type in ["Получатель"] and sending_address:
            self.add_error("sending_address", "Укажите только адрес доставки")

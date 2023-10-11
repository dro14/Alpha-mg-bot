from django.forms import ModelForm
from .models import CustomUser, Truck


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        type = cleaned_data.get("type")
        sender_address = cleaned_data.get("sender_address")
        receiver_address = cleaned_data.get("receiver_address")

        if type in ["Отправитель", "Отправитель и Получатель"] and not sender_address:
            self.add_error(
                "sender_address",
                "Укажите адрес отправителя",
            )
        if type in ["Получатель", "Отправитель и Получатель"] and not receiver_address:
            self.add_error(
                "receiver_address",
                "Укажите адрес получателя",
            )

        if type in ["Отправитель"] and receiver_address:
            self.add_error(
                "receiver_address",
                "У отправителя адрес получателя должен быть пустым",
            )
        if type in ["Получатель"] and sender_address:
            self.add_error(
                "sender_address",
                "У получателя адрес отправителя должен быть пустым",
            )


class TruckForm(ModelForm):
    class Meta:
        model = Truck
        fields = ("number",)

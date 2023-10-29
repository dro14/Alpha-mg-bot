from django.forms import ModelForm
from .models import CustomUser, Truck


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "phone_number",
            "type",
            "sender_address",
            "receiver_address",
        )

    def clean(self):
        cleaned_data = super().clean()

        type_ = cleaned_data.get("type")
        sender_address = cleaned_data.get("sender_address")
        receiver_address = cleaned_data.get("receiver_address")

        if type_ in ["Отправитель", "Отправитель и Получатель"] and not sender_address:
            self.add_error(
                "sender_address",
                "Укажите адрес отправителя",
            )
        if type_ in ["Получатель", "Отправитель и Получатель"] and not receiver_address:
            self.add_error(
                "receiver_address",
                "Укажите адрес получателя",
            )

        if type_ in ["Отправитель"] and receiver_address:
            self.add_error(
                "receiver_address",
                "У отправителя адрес получателя должен быть пустым",
            )
        if type_ in ["Получатель"] and sender_address:
            self.add_error(
                "sender_address",
                "У получателя адрес отправителя должен быть пустым",
            )

        username = cleaned_data.get("username")
        phone_number = cleaned_data.get("phone_number")

        if not username and not phone_number:
            self.add_error(
                "username",
                "Укажите либо имя пользователя, либо номер телефона Телеграм аккаунта",
            )
            self.add_error(
                "phone_number",
                "Укажите либо имя пользователя, либо номер телефона Телеграм аккаунта",
            )


class TruckForm(ModelForm):
    class Meta:
        model = Truck
        fields = ("number", "status")

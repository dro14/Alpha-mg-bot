from .filters import registered, sender, receiver
from pyrogram import Client, filters
from .receiver_flow import *
from .sender_flow import *


@Client.on_callback_query(registered & (sender | receiver))
def handle_callback_query(client, query):
    user_data = get_dict(f"sender:{query.from_user.id}")
    match user_data["current"]:
        case "cargo_type":
            cargo_type(client, query, user_data)
        case "transport_type":
            transport_type(client, query, user_data)
        case "transport_number":
            transport_number1(client, query, user_data)
        case "photo_2" | "photo_3":
            photo_2_3(client, query, user_data)
        case "receiver_address":
            receiver_address(client, query, user_data)
        case "end":
            end(client, query, user_data)
        case "not_found":
            user_data = get_dict(f"receiver:{query.from_user.id}:{query.data}")
            match user_data["current"]:
                case "confirm_delivery":
                    confirm_delivery(client, query, user_data)
                case "not_found":
                    user_data = get_dict(f"receiver:{query.from_user.id}")
                    match user_data["current"]:
                        case "complete_delivery":
                            complete_delivery(client, query, user_data)


@Client.on_message(filters.regex(r"^\d+$") & registered & (sender | receiver))
def handle_numbers(client, message):
    user_data = get_dict(f"sender:{message.from_user.id}")
    match user_data["current"]:
        case "transport_number":
            transport_number2(client, message, user_data)
        case "weight":
            weight(client, message, user_data)


@Client.on_message(filters.photo & registered & (sender | receiver))
def handle_photos(client, message):
    user_data = get_dict(f"sender:{message.from_user.id}")
    match user_data["current"]:
        case "photo_1" | "photo_2":
            photo_1_2(client, message, user_data)
        case "photo_3":
            photo_3(client, message, user_data)
        case "not_found":
            user_data = get_dict(f"receiver:{message.from_user.id}")
            match user_data["current"]:
                case "complete_delivery":
                    receive_comment(client, message, user_data, True)


@Client.on_message(registered & (sender | receiver))
def handle_text(client, message):
    user_data = get_dict(f"receiver:{message.from_user.id}")
    match user_data["current"]:
        case "complete_delivery":
            receive_comment(client, message, user_data, False)

def create_message(message: dict):
    from app.persitence.models import Message
    Message(message).save()


def get_all_messages_for_user(user_id):
    from app.persitence.models import Message
    return Message.find(receiver=user_id)


def get_message_by_id(message_id):
    from app.persitence.models import Message
    return Message.find(_id=message_id).first_or_none()


def get_unread_msg_count(user_id):
    from app.persitence.models import Message
    return len(Message.find(receiver=user_id, read=False))
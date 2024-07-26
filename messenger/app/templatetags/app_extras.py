from django import template

from app.models import Chat

register = template.Library()


@register.simple_tag
def chat(request):
    user = request.user
    chats = Chat.objects.filter(participants=user)
    chat_data = []
    for chat in chats:
        other_participants = chat.participants.exclude(id=user.id)
        chat_data.append({
            'chat': chat,
            'other_participants': other_participants
        })
    return chat_data
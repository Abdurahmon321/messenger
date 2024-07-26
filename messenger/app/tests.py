from django.test import TestCase
from .models import Chat, Message
# Create your tests here.
chats = Chat.objects.all()
for chat in chats:
    print(chat.encryption_key)
    print(len(chat.encryption_key))  # Bu 44 bo'lishi kerak

messages = Message.objects.all()
for message in messages:
    print(f"Message ID: {message.id}")
    print(f"Content: {message.content}")
    print(f"Chat Encryption Key: {message.chat.encryption_key}")
    print(f"Content Length: {len(message.content)}")
    print(f"Encryption Key Length: {len(message.chat.encryption_key)}")

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import random
import string
from django.utils.text import slugify
from cryptography.fernet import Fernet
import base64


def generate_slug():
    return str(uuid.uuid4())


def generate_key():
    return Fernet.generate_key().decode('utf-8')


def encrypt_message(key, message):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode('utf-8'))


def decrypt_message(key, encrypted_message):
    if type(encrypted_message) == str:
        encrypted_message = encrypted_message.split("'")[1].encode('utf-8')
    fernet = Fernet(key.encode('utf-8'))
    try:
        decrypted_bytes = fernet.decrypt(encrypted_message)
        decrypted_message = decrypted_bytes.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        decrypted_message = "[Decryption error]"
    return decrypted_message


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=5))


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, default=generate_verification_code, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 180


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class UserProfileImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='profile_images/')
    created = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='chats')
    encryption_key = models.CharField(max_length=100, default=generate_key)
    slug = models.SlugField(unique=True, default=generate_slug, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(generate_slug())
        super(Chat, self).save(*args, **kwargs)

    def __str__(self):
        return f"Chat id {self.id} with participants {', '.join([user.username for user in self.participants.all()])}"



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.content = encrypt_message(self.chat.encryption_key, self.content)
        super(Message, self).save(*args, **kwargs)

    @property
    def decrypted_content(self):
        return decrypt_message(self.chat.encryption_key, self.content)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
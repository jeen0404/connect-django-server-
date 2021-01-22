import random

import requests
from django.core.exceptions import ObjectDoesNotExist
from faker import Faker
from faker.providers import internet

from accounts.models import UserDetails
from post.models import *
from connections.models import *
from chat.models import *

fake = Faker('en_In')
fake.add_provider(internet)
#
#
# # generate mobile no
# def gen_phone(self):
#     first = str(random.randint(600, 999))
#     second = str(random.randint(1, 888)).zfill(3)
#
#     last = (str(random.randint(1, 9998)).zfill(4))
#     while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
#         last = (str(random.randint(1, 9998)).zfill(4))
#     return "+91" + first + second + last
#
#
# # create users
# x = 0
# for i in range(0):
#     try:
#         x += 1
#         print('user', x)
#         name = fake.name()
#         user = User()
#         user.user_id = str(uuid.uuid4())
#         user.phone_number = self.gen_phone()
#         user.save()
#         user_details = UserDetails()
#         user_details.username = name.replace(" ", '')
#         user_details.name = name
#         user_details.profession = fake.job()
#         user_details.user = user
#         user_details.profile_image = requests.get("https://picsum.photos/400").url
#         user_details.bio = fake.sentence()
#         user_details.save()
#     except Exception as e:
#         pass
#
# users = User.objects.all()
#
# # user details fix
# x = 0
# for i in []:
#     x += 1
#     print('user_details_fix', x)
#     try:
#         user = UserDetails.objects.get(user_id=i)
#     except ObjectDoesNotExist as e:
#         print(i.user_id, e)
#         user_details = UserDetails()
#         user_details.username = fake.name().replace(" ", '')
#         user_details.name = fake.name()
#         user_details.user = i
#         user_details.profile_image = requests.get("https://picsum.photos/400").url
#         user_details.bio = fake.sentence()
#         user_details.save()
#
# # follow request
# x = 0
# for i in []:
#     x += 1
#     y = 0
#     print("for user", x)
#     low = random.randint(0, len(users))
#     high = random.randint(low, len(users))
#     for k in range(low, high):
#         y += 1
#         print("to user", y)
#         try:
#             conn = Connection()
#             conn.follower = i
#             conn.following = users[k]
#             conn.save()
#         except Exception as e:
#             pass
#
# x = 0
# # generate chats
# for i in []:
#     x += 1
#     y = 0
#     print("chat user", x)
#     low = random.randint(0, len(users) - 30)
#     for k in range(low, low + 20):
#         y += 1
#         print("char", y)
#         conversation = Conversation()
#         conversation.sender = UserDetails.objects.get(user=i)
#         conversation.recipient = UserDetails.objects.get(user=users[k])
#         conversation.save()
#         for x in range(random.randint(2, 50)):
#             message = Messages()
#             message.conversation_id = conversation
#             message.message = fake.sentence()
#             message.sender_id = i.user_id
#             message.recipient_id = users[k].user_id
#             message.save()
#             replay = Messages()
#             replay.conversation_id = conversation
#             replay.message = fake.sentence()
#             replay.recipient_id = i.user_id
#             replay.sender_id = users[k].user_id
#             replay.save()
#
# # generating posts
# x = 0
# for i in []:
#     y = 0
#     x += 1
#     print("post for user", x)
#     for j in range(random.randint(0, 25)):
#         y += 1
#         print("post no", y)
#         post = Post()
#         post.post_id = str(uuid.uuid4())
#         post.user_id = i
#         post.save()
#         low = random.randint(0, len(users))
#         high = random.randint(low, len(users))
#         for k in range(low, high):
#             like = Like()
#             like.user_id = users[k]
#             like.post_id = post
#             like.save()
#         low = random.randint(0, len(users))
#         high = random.randint(low, len(users))
#         for k in range(low, high):
#             comment = Comment()
#             comment.post_id = post
#             comment.user_id = users[k]
#             comment.comment = fake.sentence()
#             comment.save()
#         for l in range(random.randint(1, 4)):
#             image = Image()
#             image.post_id = post
#             image.user_id = i
#             image.url = requests.get("https://picsum.photos/400").url
#             image.height = 400
#             image.width = 400
#             image.ratio = 1
#             image.save()

posts = Post.objects.all()

for i in posts:
    images = Image.objects.filter(post_id=i)
    if len(images) == 0:
        print("fix", i.user_id)
        image = Image()
        image.post_id = i
        image.user_id = i.user_id
        image.url = requests.get("https://picsum.photos/400").url
        image.height = 400
        image.width = 400
        image.ratio = 1
        image.save()

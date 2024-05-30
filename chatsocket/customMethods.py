

class CustomMethods():
    def set_channel(username, channel_name):
        from user.models import UserModel
        user = UserModel.objects.get(username=username)
        user.channel_name = channel_name
        user.save()

        print("client channel_name is updated")
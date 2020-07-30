import random

class default():
    def __init__(self, bot):
        self.bot = bot

    def ping(self):
        print("Pong!")
        self.bot.sendMessage(self.bot.DefaultChat, "Pong!")
        return

    def randomNumber(self, high, low=0):
        integer = random.randint(low,high+1)
        print(f"The random integer is: {integer}")
        self.bot.sendMessage(self.bot.DefaultChat)
        return


def setup(bot):
    bot.add_extension(default(bot))
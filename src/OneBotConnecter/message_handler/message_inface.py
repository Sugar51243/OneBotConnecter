from OneBotConnecter.connecter.connecter import connecter

class message_inface:

    inface: connecter


    def __init__(self, inface):
        self.inface = inface

    def get_bot_acc(self):
        acc = None
        ...
        return acc
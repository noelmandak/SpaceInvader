from abc import abstractmethod
from kink.inject import inject

from SpaceInvader.email_sender import EmailSender

class Message:
    pass

class Observer:
    def __init__(self,email_sender_ : EmailSender):
        self.email_sender = email_sender_


    @abstractmethod
    def update(self, message: Message):
        pass

class Subject:
    def __init__(self) -> None:
        self.observers = {}

    @abstractmethod
    def attach(self, observername ,observer: Observer):
        self.observers[observername] = observer

    @abstractmethod
    def defach(self, observername, observer: Observer):
        if observername in self.observers:
            del self.observers[observername]

    @abstractmethod
    def notify_update(self, msg: Message):
        pass


class FirstRankMessange(Message):
    def __init__(self,firstrank,firstrank_email):
        self.firstrank = firstrank
        self.firstrank_email = firstrank_email

@inject
class FirstRankChangeObserver(Observer):
    def __init__(self, email_sender_: EmailSender):
        super().__init__(email_sender_)
        self.firstrank = None
        self.firstrank_email = None

    def set_firstrank(self,username,email):
        self.firstrank = username
        self.firstrank_email = email

    def send_email(self,firstrank_before,email_firstrank_before):
        header = "Your rank is down"

        body = f"""Dear {firstrank_before},
Recently, there is a player with the username {self.firstrank} who can beat your highest score.
your rank dropped to rank 2.

let's play space invader again and get the first rank again.

Regards,
Space Invader Operators
"""     
        self.email_sender.send(email_firstrank_before,header,body)

    
    def notify_update(self, message: Message):
        if  isinstance(message,FirstRankMessange):
            if message.firstrank != self.firstrank:
                firstrank_before = self.firstrank
                email_firstrank_before = self.firstrank_email
                self.firstrank = message.firstrank
                self.firstrank_email = message.firstrank_email
                if firstrank_before != None:
                    self.send_email(firstrank_before,email_firstrank_before)


@inject
class NoteNewScoreSubject(Subject):
    def __init__(self,first_rank_change_observer : FirstRankChangeObserver):
        super().__init__()
        self.attach("first rank change observer",first_rank_change_observer)

    def first_rank_setup(self, firstrank, firstrank_email):
        self.observers["first rank change observer"].set_firstrank(firstrank,firstrank_email)

    def notify_update(self, msg: Message):
        for o in self.observers:
            self.observers[o].notify_update(msg)

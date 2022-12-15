class WrongChatID(Exception):
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        super().__init__()

    def __str__(self) -> str:
        return f'Got an unexpected chat id: {self.chat_id}.'

from settings import Settings
from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from pyrogram.client import Client as T_client


class Worker:

    def __init__(self, settings: Settings) -> None:
        self.settings: Settings = settings()
        self.status: bool = True
    
    def app_getter(self) -> Client:
        return Client('my_account', self.settings.api_id, self.settings.api_hash)
    
    async def _set_status(self, arg: bool=False):
        # will be change to logging
        self.status = arg if isinstance(arg, bool) else print("TypeError")

    async def check_command(self, chat_id, text: str):
        if chat_id == self.settings.self_chat_id:
            hash_command = {
                "стоп": lambda s = False: self._set_status(s),
                "старт": lambda s = True: self._set_status(s)
            }
            try:
                await hash_command.get(text.lower())()
            except TypeError as e:
                # will be change to logging
                print(f"Error: {e}")

    def __call__(self):
        app: Client = self.app_getter()

        @app.on_message(filters.private)
        async def my_handler(client: T_client, message: Message):
            try:
                if (l := len(message.text)) >= 4 and l <= 5:
                    await self.check_command(chat_id=message.chat.id, text=message.text)
            except TypeError as e:
                print(f"Error: {e}")

            if self.status and message.from_user.id != client.me.id:
                await app.send_message(chat_id=message.chat.id, text=self.settings.message_answer)

        app.run()


if __name__ == "__main__":
    worker: Worker = Worker(Settings)()

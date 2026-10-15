class TasksService:
    @classmethod
    async def send_magic_link_email(cls, user_email: str, link: str):
        print(user_email, link)

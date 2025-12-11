import asyncio
from bot import bot
from bot.helper.utils import new_task_id
from pyrogram.errors import FloodWait, MessageNotModified

# Key: GID | Value: Task Object
active_tasks = {}

class Task:
    def __init__(self, chat_id, message_id):
        self.chat_id = chat_id
        self.message_id = message_id
        self.progress = 0
        self.status_text = "Initializing..."
        self.asyncio_task = None 
        self.gid = new_task_id()
        
        while self.gid in active_tasks:
            self.gid = new_task_id()
            
        active_tasks[self.gid] = self

    def update(self, progress, text):
        self.progress = progress
        self.status_text = text

    async def cancel(self):
        if self.asyncio_task:
            self.asyncio_task.cancel()
        
        if self.gid in active_tasks:
            del active_tasks[self.gid]
            
        try:
            await bot.edit_message_text(
                self.chat_id, 
                self.message_id, 
                f"🚫 **Task Cancelled** (GID: `{self.gid}`)"
            )
        except:
            pass

async def status_loop():
    while True:
        await asyncio.sleep(15)
        current_tasks = list(active_tasks.values())
        
        if not current_tasks:
            continue

        for task in current_tasks:
            try:
                filled = int(task.progress / 10)
                bar = "▓" * filled + "░" * (10 - filled)
                msg_text = (
                    f"**🤖 Working...** (GID: `{task.gid}`)\n"
                    f"{task.status_text}\n"
                    f"[{bar}] {task.progress}%"
                )
                await bot.edit_message_text(task.chat_id, task.message_id, msg_text)
            except (MessageNotModified, Exception):
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
            
            await asyncio.sleep(0.5)
          

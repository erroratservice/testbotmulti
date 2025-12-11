from bot import bot, Config
from pyrogram import filters
from bot.helper.status import active_tasks

@bot.on_message(filters.command("status"))
async def status_command(client, message):
    user_id = message.chat.id
    
    if user_id == Config.OWNER_ID and len(message.command) > 1 and message.command[1] == "all":
        target_tasks = list(active_tasks.values())
        header = f"**🚨 GLOBAL SERVER STATUS ({len(target_tasks)})**\n\n"
    else:
        target_tasks = [t for t in active_tasks.values() if t.chat_id == user_id]
        header = f"**👤 Your Active Tasks ({len(target_tasks)})**\n\n"

    if not target_tasks:
        return await message.reply("💤 No active tasks found.")

    text = header
    for task in target_tasks:
        filled = int(task.progress / 10)
        bar = "▓" * filled + "░" * (10 - filled)
        text += (
            f"🆔 `{task.gid}`\n"
            f"📝 {task.status_text}\n"
            f"[{bar}] {task.progress}%\n\n"
        )
    await message.reply(text)
  

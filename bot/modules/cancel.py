from bot import bot, Config
from pyrogram import filters
from bot.helper.status import active_tasks

@bot.on_message(filters.command("cancel"))
async def cancel_command(client, message):
    user_id = message.chat.id
    args = message.command
    
    if len(args) > 1:
        gid = args[1]
        if gid in active_tasks:
            task = active_tasks[gid]
            if user_id != task.chat_id and user_id != Config.OWNER_ID:
                await message.reply("❌ This is not your task!")
                return
            await message.reply(f"🛑 Stopping task `{gid}`...")
            await task.cancel()
        else:
            await message.reply("❌ Invalid GID.")
        return

    user_tasks = [t for t in active_tasks.values() if t.chat_id == user_id]
    
    if len(user_tasks) == 0:
        await message.reply("💤 No active tasks.")
    elif len(user_tasks) == 1:
        task = user_tasks[0]
        await message.reply(f"🛑 Stopping task `{task.gid}`...")
        await task.cancel()
    else:
        text = "⚠️ **Multiple active tasks:**\n"
        for t in user_tasks:
            text += f"• `{t.gid}`: {t.status_text}\n"
        await message.reply(text + "\nUse `/cancel GID`")
      

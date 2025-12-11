import asyncio
from bot import bot, Config
from pyrogram import filters
from bot.helper.listeners import get_user_input
from bot.helper.status import Task, active_tasks
from bot.helper.worker import start_counting_worker
from bot.helper.db import db
from bot.helper.utils import get_readable_file_size

@bot.on_message(filters.command("count") & filters.private)
async def count_command(client, message):
    user_id = message.chat.id
    
    try:
        child_token = await db.get_user_token(user_id)
        if not child_token:
            await message.reply_text("⚠️ No Child Bot connected.")
            child_token = await get_user_input(user_id, "Send your **Child Bot Token**:")
            if ":" not in child_token:
                return await message.reply("❌ Invalid token.")
            await db.update_user_token(user_id, child_token)
            await message.reply_text("✅ Token saved.")

        target_input = await get_user_input(user_id, "Send **Channel ID** or **Username**:")
        try:
            target_channel = int(target_input) if target_input.startswith("-100") else target_input
        except:
            target_channel = target_input

    except asyncio.CancelledError:
        return await message.reply("❌ Command Cancelled.")

    status_msg = await message.reply("⚡ Initializing Worker...")
    task = Task(user_id, status_msg.id)
    task.api_id = Config.API_ID
    task.api_hash = Config.API_HASH
    
    await status_msg.edit(f"🆔 **GID:** `{task.gid}`\n🚀 Connecting to Telegram...")

    worker_coroutine = start_counting_worker(child_token, target_channel, task)
    bg_task = asyncio.create_task(worker_coroutine)
    task.asyncio_task = bg_task

    try:
        result = await bg_task
        if "error" in result:
            await status_msg.edit(f"❌ **Failed:**\n{result['error']}")
        else:
            readable_size = get_readable_file_size(result['total_size'])
            await status_msg.edit(
                f"✅ **Scan Complete**\n\n"
                f"🆔 GID: `{task.gid}`\n"
                f"📂 Files: {result['total_files']}\n"
                f"💬 Messages: {result['total_msgs']}\n"
                f"📦 Size: {readable_size}"
            )
    except asyncio.CancelledError:
        pass
    finally:
        if task.gid in active_tasks:
            del active_tasks[task.gid]
          

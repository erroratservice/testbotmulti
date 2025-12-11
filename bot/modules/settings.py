from bot import bot
from pyrogram import filters
from bot.helper.db import db
from bot.helper.listeners import get_user_input

@bot.on_message(filters.command("set_token") & filters.private)
async def set_token_command(client, message):
    user_id = message.chat.id
    new_token = await get_user_input(user_id, "Send me your new **Child Bot Token**:")
    
    if ":" not in new_token:
        return await message.reply("❌ Invalid token format.")
        
    await db.update_user_token(user_id, new_token)
    await message.reply("✅ Token updated.")

@bot.on_message(filters.command("my_info") & filters.private)
async def my_info_command(client, message):
    user_id = message.chat.id
    token = await db.get_user_token(user_id)
    token_display = f"`{token[:10]}...`" if token else "Not Set"
    await message.reply(f"👤 **User:** `{user_id}`\n🤖 **Bot Token:** {token_display}")
  

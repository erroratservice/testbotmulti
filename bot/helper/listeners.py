import asyncio
from pyrogram import filters
from bot import bot

input_listeners = {}

async def get_user_input(chat_id, text):
    sent = await bot.send_message(chat_id, text)
    future = asyncio.Future()
    input_listeners[chat_id] = future
    
    try:
        result_msg = await future
        if result_msg.text == "/cancel":
            raise asyncio.CancelledError("User cancelled input")
        return result_msg.text
    finally:
        if chat_id in input_listeners:
            del input_listeners[chat_id]

@bot.on_message(filters.text & filters.private, group=1)
async def check_user_input(client, message):
    if message.chat.id in input_listeners:
        input_listeners[message.chat.id].set_result(message)
        message.stop_propagation()
      

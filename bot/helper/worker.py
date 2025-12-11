import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait

async def start_counting_worker(child_token, target_chat_id, task):
    temp_bot = Client(
        name=f"temp_{task.gid}",
        api_id=task.api_id,
        api_hash=task.api_hash,
        bot_token=child_token,
        in_memory=True,
        no_updates=True
    )

    try:
        await temp_bot.start()
        task.update(0, "Worker started... Connecting to channel.")

        try:
            chat = await temp_bot.get_chat(target_chat_id)
            task.update(0, f"Connected to {chat.title}. Starting scan...")
        except Exception as e:
            return {"error": f"Cannot access chat. Is the bot Admin?\nError: {e}"}

        total_messages = 0
        total_size = 0
        file_count = 0
        
        async for message in temp_bot.get_chat_history(target_chat_id):
            total_messages += 1
            if message.document or message.video or message.audio:
                file_count += 1
                size = getattr(message.document or message.video or message.audio, "file_size", 0)
                total_size += size
            
            if total_messages % 100 == 0:
                task.update(0, f"Scanned {total_messages} messages...")

        return {
            "total_msgs": total_messages,
            "total_files": file_count,
            "total_size": total_size
        }

    except asyncio.CancelledError:
        raise 
    except FloodWait as e:
        await asyncio.sleep(e.value + 5)
        return {"error": f"Hit FloodWait. Try again."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if temp_bot.is_connected:
            await temp_bot.stop()
          

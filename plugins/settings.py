from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.pyromod import ListenerTimeout
from config import OWNER_ID
import humanize

@Client.on_callback_query(filters.regex("^settings$"))
async def settings(client, query):
    msg = f"""<blockquote><b>Settings of @{client.username}:</b></blockquote>
<b>Force Sub Channels:</b> `{len(client.fsub_dict)}`
<b>Auto Delete Timer:</b> `{client.auto_del}`
<b>Protect Content:</b> `{'True' if client.protect else 'False'}`
<b>Disable Button:</b> `{'True' if client.disable_btn else 'False'}`
<b>Reply Text:</b> `{client.reply_text if client.reply_text else 'None'}`
<b>Admins:</b> `{len(client.admins)}`
<b>Start Message:</b>
<pre>{client.messages.get('START', 'Empty')}</pre>
<b>Start Image:</b> `{bool(client.messages.get('START_PHOTO', ''))}`
<b>Force Sub Message:</b>
<pre>{client.messages.get('FSUB', 'Empty')}</pre>
<b>Force Sub Image:</b> `{bool(client.messages.get('FSUB_PHOTO', ''))}`
<b>About Message:</b>
<pre>{client.messages.get('ABOUT', 'Empty')}</pre>
<b>Reply Message:</b>
<pre>{client.reply_text}</pre>
    """
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ꜰꜱᴜʙ ᴄʜᴀɴɴᴇʟꜱ', 'fsub'), InlineKeyboardButton('ᴀᴅᴍɪɴꜱ', 'admins')],
        [InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ', 'auto_del'), InlineKeyboardButton('ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ', 'protect')],
        [InlineKeyboardButton('ᴘʜᴏᴛᴏꜱ', 'photos'), InlineKeyboardButton('ᴛᴇxᴛꜱ', 'texts')],
        [InlineKeyboardButton('ʜᴏᴍᴇ', 'home')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

@Client.on_callback_query(filters.regex("^fsub$"))
async def fsub(client, query):
    msg = f"""<blockquote><b>Force Subscription Settings:</b></blockquote>
<b>Force Subscribe Channel IDs:</b> `{set(client.fsub_dict.keys())}`

Use the appropriate button below to add or remove a force subscription channel based on your needs.
"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ', 'add_fsub'), InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ', 'rm_fsub')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

@Client.on_callback_query(filters.regex("^admins$"))
async def admins(client, query):
    if query.from_user.id != OWNER_ID:
        return await query.answer('This can only be used by the owner.')

    msg = f"""<blockquote><b>Admin Settings:</b></blockquote>
<b>Admin User IDs:</b> {', '.join(f'`{a}`' for a in client.admins)}

Use the appropriate button below to add or remove an admin based on your needs.
"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ᴀᴅᴅ ᴀᴅᴍɪɴ', 'add_admin'), InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ', 'rm_admin')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

@Client.on_callback_query(filters.regex("^photos$"))
async def photos(client, query):
    msg = f"""<blockquote><b>Photo Settings:</b></blockquote>
<b>Start Photo:</b> `{client.messages.get("START_PHOTO", "None")}`
<b>Force Sub Photo:</b> `{client.messages.get('FSUB_PHOTO', 'None')}`

Use the appropriate buttons below to update photo settings.
"""
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                ('ꜱᴇᴛ' if not client.messages.get("START_PHOTO") else 'ᴄʜᴀɴɢᴇ') + ' ꜱᴛᴀʀᴛ ᴘʜᴏᴛᴏ',
                callback_data='add_start_photo'
            ),
            InlineKeyboardButton(
                ('ꜱᴇᴛ' if not client.messages.get("FSUB_PHOTO") else 'ᴄʜᴀɴɢᴇ') + ' ꜰꜱᴜʙ ᴘʜᴏᴛᴏ',
                callback_data='add_fsub_photo'
            )
        ],
        [
            InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ ꜱᴛᴀʀᴛ ᴘʜᴏᴛᴏ', callback_data='rm_start_photo'),
            InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ ꜰꜱᴜʙ ᴘʜᴏᴛᴏ', callback_data='rm_fsub_photo')
        ],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', callback_data='settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return 

@Client.on_callback_query(filters.regex("^protect$"))
async def protect(client, query):
    client.protect = not client.protect
    await settings(client, query)

@Client.on_callback_query(filters.regex("^auto_del$"))
async def auto_del(client, query):
    msg = f"""<blockquote><b>Change Auto Delete Time:</b></blockquote>
<b>Current Timer:</b> `{client.auto_del}`

Enter a new integer value for auto delete time:
- 0 to disable
- -1 to keep unchanged
- Wait 60 seconds for timeout
"""
    await query.answer()
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        timer = res.text.strip()
        if timer.isdigit() or (timer.startswith(('+', '-')) and timer[1:].isdigit()):
            timer = int(timer)
            if timer >= 0:
                client.auto_del = timer
                await query.message.edit_text(f'**Auto Delete timer updated to {timer} seconds.**', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
            else:
                await query.message.edit_text("**No changes made to Auto Delete timer.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
        else:
            await query.message.edit_text("**Invalid input. Please enter a valid integer.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
    except ListenerTimeout:
        await query.message.edit_text("**Timeout, try again.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))

@Client.on_callback_query(filters.regex("^texts$"))
async def texts(client, query):
    msg = f"""<blockquote><b>Text Configuration:</b></blockquote>
<b>Start Message:</b>
<pre>{client.messages.get('START', 'Empty')}</pre>
<b>Force Sub Message:</b>
<pre>{client.messages.get('FSUB', 'Empty')}</pre>
<b>About Message:</b>
<pre>{client.messages.get('ABOUT', 'Empty')}</pre>
<b>Reply Message:</b>
<pre>{client.reply_text}</pre>
    """
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ꜱᴛᴀʀᴛ ᴛᴇxᴛ', 'start_txt'), InlineKeyboardButton('ꜰꜱᴜʙ ᴛᴇxᴛ', 'fsub_txt')],
        [InlineKeyboardButton('ʀᴇᴘʟʏ ᴛᴇxᴛ', 'reply_txt'), InlineKeyboardButton('ᴀʙᴏᴜᴛ ᴛᴇxᴛ', 'about_txt')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

@Client.on_callback_query(filters.regex('^rm_start_photo$'))
async def rm_start_photo(client, query):
    client.messages['START_PHOTO'] = ''
    await query.answer()
    await photos(client, query)

@Client.on_callback_query(filters.regex('^rm_fsub_photo$'))
async def rm_fsub_photo(client, query):
    client.messages['FSUB_PHOTO'] = ''
    await query.answer()
    await photos(client, query)

@Client.on_callback_query(filters.regex("^add_start_photo$"))
async def add_start_photo(client, query):
    msg = f"""<blockquote>**Change Start Image:**</blockquote>
**Current Start Image:** `{client.messages.get('START_PHOTO', '')}`

__Enter new link of start image or send the photo, or wait for 60 second timeout to be comoleted!__
"""
    await query.answer()
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=(filters.text|filters.photo), timeout=60)
        if res.text and res.text.startswith('https://' or 'http://'):
            client.messages['START_PHOTO'] = res.text
            return await query.message.edit_text("**This link has been set at the place of start photo!!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        elif res.photo:
            loc = await res.download()
            client.messages['START_PHOTO'] = loc
            return await query.message.edit_text("**This image has been set as the starting image!!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        else:
            return await query.message.edit_text("**Invalid Photo or Link format!!**\n__If you're sending the link of any image it must starts with either 'http' or 'https'!__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**Timeout, try again!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))

@Client.on_callback_query(filters.regex("^add_fsub_photo$"))
async def add_fsub_photo(client, query):
    msg = f"""<blockquote>**Change Force Sub Image:**</blockquote>
**Current Force Sub Image:** `{client.messages.get('FSUB_PHOTO', '')}`

__Enter new link of fsub image or send the photo, or wait for 60 second timeout to be comoleted!__
"""
    await query.answer()
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=(filters.text|filters.photo), timeout=60)
        if res.text and res.text.startswith('https://' or 'http://'):
            client.messages['FSUB_PHOTO'] = res.text
            return await query.message.edit_text("**This link has been set at the place of fsub photo!!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        elif res.photo:
            loc = await res.download()
            client.messages['FSUB_PHOTO'] = loc
            return await query.message.edit_text("**This image has been set as the force sub image!!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        else:
            return await query.message.edit_text("**Invalid Photo or Link format!!**\n__If you're sending the link of any image it must starts with either 'http' or 'https'!__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**Timeout, try again!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))

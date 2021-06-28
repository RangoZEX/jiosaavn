from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.text & filters.incoming & filters.private & ~filters.regex('.*http.*'))
async def search(c, m):
    send_msg = await m.reply_text('__**Processing... ⏳**__', quote=True)

    api_url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': 1,
        'q': m.text,
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 10,
        '__call': 'search.getResults'
    }
    data = await req(api_url, params)

    total_results = data['total']
    buttons = []
    for result in data['results']:
        title = result['title'] if 'title' in result else ''
        id = result['id'] if 'id' in result else None
        if result['type'] == 'song':
            album = ''
            if 'more_info' in result:
                album = result['title'] if 'album' in result['more_info'] else ''
            buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])

    if total_results > 10:
        buttons.append([InlineKeyboardButton("➡️", callback_data="nxt+2")])

    await send_msg.edit(f'**📈 Total Results:** {total_results}\n\n**🔍 Search Query:** {m.text}', reply_markup=InlineKeyboardMarkup(buttons))
    print(data)



@Client.on_callback_query(filters.regex('^nxt\+[0-9]*$'))
async def nxt_cb(c, m):
    page = int(m.data.split('+')[1])
    query = m.message.reply_to_message
    
    api_url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': page,
        'q': query.text,
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 10,
        '__call': 'search.getResults'
    }
    data = await req(api_url, params)

    total_results = data['total']
    buttons = []
    for result in data['results']:
        title = result['title'] if 'title' in result else ''
        id = result['id'] if 'id' in result else None
        if result['type'] == 'song':
            album = ''
            if 'more_info' in result:
                album = result['title'] if 'album' in result['more_info'] else ''
            buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])

    nxt_btn = []
    if total_results > 10:
        nxt_btn.append(InlineKeyboardButton("➡️", callback_data=f"nxt+{page+1}"))
    if page != 1:
        nxt_btn.append(InlineKeyboardButton("⬅️", callback_data=f"nxt+{page-1}"))
    buttons.append(nxt_btn)

    await m.message.edit(f'**📈 Total Results:** {total_results}\n\n**🔍 Search Query:** {m.text}', reply_markup=InlineKeyboardMarkup(buttons))
    print(data)

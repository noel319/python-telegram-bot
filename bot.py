
import asyncio
import logging
import logging
import os
import io

from uuid import uuid4
from telegram import BotCommandScopeAllGroupChats, Update, constants
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle
from telegram import InputTextMessageContent, BotCommand
from telegram.error import RetryAfter, TimedOut, BadRequest
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, \
    filters, InlineQueryHandler, CallbackQueryHandler, Application, ContextTypes, CallbackContext

from pydub import AudioSegment
from PIL import Image

from utils import is_group_chat, get_thread_id, message_text, wrap_with_indicator, split_into_chunks, \
    edit_message_with_retry, get_stream_cutoff_values, is_allowed, get_remaining_budget, is_admin, is_within_budget, \
    get_reply_to_message_id, add_chat_request_to_usage_tracker, error_handler, is_direct_result, handle_direct_result, \
    cleanup_intermediate_files
from openai_helper import OpenAIHelper, localized_text
from usage_tracker import UsageTracker

class TelegramBot:
    # Class  Test Telegram bot.
    def __init__(self, config:dict, openai:OpenAIHelper) -> None:
        # Initialize the bot with the given configuration and GPT bot object.
        self.config = config
        self.openai = openai
        bot_language = self.config['bot_language']
        self.commands = [
            BotCommand(command='start', description=localized_text('start_description', bot_language)),
            BotCommand(command='help', description=localized_text('help_description', bot_language)),
            BotCommand(command='echo', description=localized_text('echo_description', bot_language)),
            BotCommand(command='photo', description=localized_text('photo_description', bot_language)),
            BotCommand(command='register', description=localized_text('register_description', bot_language)),
            BotCommand(command='task', description=localized_text('task_description', bot_language)),            
        ]
        self.group_commands = [BotCommand(
            command='chat', description=localized_text('chat_description', bot_language)
        )] + self.commands
        self.disallowed_message = localized_text('disallowed', bot_language)
        self.budget_limit_message = localized_text('budget_limit', bot_language)
        self.usage = {}
        self.last_message = {}
        self.inline_queries_cache = {}

    async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        # Shows the help menu.
        commands = self.group_commands if is_group_chat(update) else self.commands
        commands_description = [f'/{commands.command} - {commands.description}' for command in commands]
        bot_language = self.config['bot_language']
        help_text = (
            localized_text('help_text', bot_language)[0] +
            '\n\n' +
            '\n'.join(commands_description) +
            '\n\n' +
            localized_text('help_text', bot_language)[1] +
            '\n\n' +
            localized_text('help_text', bot_language)[2]
        )
        await update.message.reply_text(help_text, disable_web_page_preview=True)

    async def start(self, update:Update, context:ContextTypes.DEFAULT_TYPE):
        # Shows data if Start command
        bot_language =self. config['bot_language']
        start_text =(localized_text('start_text'), bot_language)
        await update.message.reply_text(start_text, disable_web_page_preview=True)
    async def photo(self, update:Update, context: ContextTypes.DEFAULT_TYPE):
        # Generates an image or reply when image input.
        image_query = message_text(update.message)
        if image_query == '':
            await update.effective_message.reply_text(message_thread_id= get_thread_id(update), 
                text=localized_text('image_no_prompt', self.config['bot_language'])                                          
            )
            return
        logging.info(f'New image generation request received from user {update.message.from_user.name} '
                    f'(id: {update.message.from_user.id})')
            
    
    async def echo(self, update:Update, context: ContextTypes.DEFAULT_TYPE):
        # relpy user message
        user_message = ' '.join(context.args)
        await update.message.reply_text(user_message)
    
    def button(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # response query
        query = update.callback_query
        query.answer()
        choice = query.data

        if choice == '1':
            query.edit_message_text(text='You have selected Choice 1')
        elif choice == '2':
            query.edit_message_text(text='You have selected Choice 2')

    async def choice(self, update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
         # Select inline buttons
        keyboard = [
            [
                InlineKeyboardButton("Choice 1", callback_data='1'),
                InlineKeyboardButton("Choice 2", callback_data='2')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('please, choose:', reply_markup=reply_markup)

    
    
            

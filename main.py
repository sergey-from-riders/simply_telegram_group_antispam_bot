"""
This module implements an anti-spam bot for Telegram groups.
It checks new members and restricts them if they don't confirm they're not spammers.
"""

import os
import asyncio
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters


class AntiSpamBot:
    """
    A class to represent an anti-spam bot for Telegram groups.

    Attributes:
        TOKEN (str): Telegram Bot API token.
        WELCOME_MESSAGE (str): Message to greet new members.
        BUTTON_TEXT (str): Text for the confirmation button.
        VERIFIED_MESSAGE (str): Message sent when a user is verified.
        RESTRICTED_MESSAGES (list): List of messages for restricted users.
        BUTTON_PRESS_TIMEOUT (int): Timeout for button press in seconds.
        new_members (dict): Dictionary to store information about new members.
    """

    def __init__(self):
        """Initialize the AntiSpamBot with configuration and state."""
        load_dotenv()
        self.TOKEN = os.getenv('TOKEN')

        self.WELCOME_MESSAGE = "Привет, {full_name}! Спамер?"
        self.BUTTON_TEXT = "Не, я не спамер"
        self.VERIFIED_MESSAGE = "Добро пожаловать, {full_name}! Приятного общения в группе!"

        self.RESTRICTED_MESSAGES = [
            "{full_name}, вы похожи на спамера, если за 10 минут не нажали на кнопку.",
            "{full_name}, если вы не спамер, свяжитесь с администратором группы.",
        ]

        self.BUTTON_PRESS_TIMEOUT = 600  # 10 minutes
        self.new_members = {}

    async def handle_new_member(self, update: Update, context):
        """
        Handle new member join events.

        Args:
            update (Update): The incoming update.
            context (ContextTypes.DEFAULT_TYPE): The context object for the update.
        """
        if update.message.new_chat_members:
            for new_member in update.message.new_chat_members:
                user_id = new_member.id
                chat_id = update.message.chat_id
                join_message_id = update.message.message_id

                keyboard = [[InlineKeyboardButton(self.BUTTON_TEXT, callback_data=f'not_spam_{user_id}')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                welcome_message = await context.bot.send_message(
                    chat_id=chat_id,
                    text=self.WELCOME_MESSAGE.format(full_name=new_member.full_name),
                    reply_markup=reply_markup,
                    reply_to_message_id=join_message_id
                )
                
                self.new_members[user_id] = {
                    'chat_id': chat_id,
                    'join_message_id': join_message_id,
                    'welcome_message_id': welcome_message.message_id,
                    'full_name': new_member.full_name,
                    'expiry_time': datetime.now() + timedelta(seconds=self.BUTTON_PRESS_TIMEOUT)
                }
                
                context.job_queue.run_once(self.check_button_press, self.BUTTON_PRESS_TIMEOUT, data={'user_id': user_id, 'chat_id': chat_id})

    async def check_button_press(self, context):
        """
        Check if the user pressed the button within the time limit.

        Args:
            context (ContextTypes.DEFAULT_TYPE): The context object for the job.
        """
        user_id = context.job.data['user_id']
        chat_id = context.job.data['chat_id']
        
        if user_id in self.new_members:
            try:
                await context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions={}
                )
                
                restricted_message = random.choice(self.RESTRICTED_MESSAGES)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=restricted_message.format(full_name=self.new_members[user_id]['full_name']),
                    reply_to_message_id=self.new_members[user_id]['join_message_id']
                )
                
                await context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=self.new_members[user_id]['welcome_message_id']
                )
            except Exception as error:
                print(f"Error restricting user or sending restriction message: {error}")
            finally:
                del self.new_members[user_id]

    async def button_callback(self, update: Update, context):
        """
        Handle button press callback.

        Args:
            update (Update): The incoming update.
            context (ContextTypes.DEFAULT_TYPE): The context object for the update.
        """
        query = update.callback_query
        user_id = int(query.data.split('_')[2])
        
        if user_id in self.new_members:
            chat_id = self.new_members[user_id]['chat_id']
            join_message_id = self.new_members[user_id]['join_message_id']
            welcome_message_id = self.new_members[user_id]['welcome_message_id']
            
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=self.VERIFIED_MESSAGE.format(full_name=self.new_members[user_id]['full_name']),
                    reply_to_message_id=join_message_id
                )
                
                await context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=welcome_message_id
                )
            except Exception as error:
                print(f"Error deleting message or sending welcome message: {error}")
            finally:
                del self.new_members[user_id]
        
        await query.answer()

    def run(self):
        """Run the bot."""
        application = Application.builder().token(self.TOKEN).build()
        
        application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_member))
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    bot = AntiSpamBot()
    bot.run()
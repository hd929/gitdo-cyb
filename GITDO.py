from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler, CallbackQueryHandler
from Response import send_notification, handle_message, load_user_ids, start, user_info, tkb
from telegram import Update
from Environment import TOKEN

def main():
    load_user_ids()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tb", send_notification))
    application.add_handler(CommandHandler("user", user_info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(tkb))
    application.run_polling()
if __name__ == '__main__':
    main()

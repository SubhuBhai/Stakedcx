import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from keep_alive import keep_alive
keep_alive()
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# States
ASK_ACTIVATE, ASK_CODE, ASK_SEED, ASK_MINES, ASK_AMOUNT, ASK_FEEDBACK = range(6)

# Hardcoded valid code
VALID_CODE = "668dtvsd23678dgfu"
IMAGE_PATH = "D:/mines/pos.png"  # Replace with your actual image path

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Do you want Mines Bomb Locator to get activated?")
    return ASK_ACTIVATE

async def ask_activate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = update.message.text.lower()
    if response == "yes":
        await update.message.reply_text(
            "Please visit this link to purchase the PDF containing the code: https://sxbhu.gumroad.com/l/stakedcx\n\nOnce you have purchased the PDF, please enter the code from it:"
        )
        return ASK_CODE
    else:
        await update.message.reply_text("Okay, activation cancelled.")
        return ConversationHandler.END

async def ask_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    code = update.message.text.strip()
    if code == VALID_CODE:
        await update.message.reply_text("Code is valid!")
        await update.message.reply_text("Enter Stake Seed:")
        return ASK_SEED
    else:
        await update.message.reply_text("Invalid code. Please check the PDF and try again.")
        return ASK_CODE

async def ask_seed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['seed'] = update.message.text.strip()
    await update.message.reply_text("Enter number of mines:")
    return ASK_MINES

async def ask_mines(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        mines = int(update.message.text.strip())
        if mines > 24:
            await update.message.reply_text("Mines can't be more than 24. Please enter again:")
            return ASK_MINES
        context.user_data['mines'] = mines
        await update.message.reply_text("Enter bet amount (RS. 20, 30, 50, or 100):")
        return ASK_AMOUNT
    except ValueError:
        await update.message.reply_text("Please enter a valid number:")
        return ASK_MINES

async def ask_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    amount = update.message.text.strip()
    context.user_data['amount'] = amount

    await update.message.reply_text("Click on Bet")

    # Send image from local path
    try:
        with open(IMAGE_PATH, 'rb') as photo:
            await update.message.reply_photo(photo=InputFile(photo))
    except Exception as e:
        logger.error(f"Failed to send image: {e}")

    await update.message.reply_text("Worked Right? Drop a Feedback?")
    return ASK_FEEDBACK

async def ask_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    feedback = update.message.text.strip()
    logger.info(f"Feedback received: {feedback}")
    await update.message.reply_text("Thanks for your feedback!")
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token("8125490160:AAHWNSn16apD8BaaaNrYgVxvmVypnuNzh3Y").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_ACTIVATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_activate)],
            ASK_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_code)],
            ASK_SEED: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_seed)],
            ASK_MINES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_mines)],
            ASK_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_amount)],
            ASK_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_feedback)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

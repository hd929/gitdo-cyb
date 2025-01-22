from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
)
from telegram.ext import ContextTypes
from fuzzywuzzy import fuzz

import os
import time
import random

start_time = time.time()

thathinh_file = open("./thathinh.txt", "r")
thathinh_list = thathinh_file.read().split("\n")
thathinh_list.pop()

casual_responses_file = open("./casual_responses.txt", "r")
casual_responses = casual_responses_file.read().split("\n")
casual_responses.pop()

chao_files = open("./chao.txt", "r")
chao = chao_files.read().split("\n")
chao.pop()

user_ids = set()
ADMIN_USER_ID = 5889848203
USER_DATA_FILE = "user_ids.txt"


def save_user_id(user_id: int):
    if str(user_id) not in user_ids:
        user_ids.add(str(user_id))
        with open(USER_DATA_FILE, "a") as f:
            f.write(f"{user_id}\n")


def load_user_ids():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            user_ids.update(f.read().splitlines())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.from_user:
        user_id = update.message.from_user.id
        save_user_id(user_id)
        await update.message.reply_text("Hế lô :))")
        await update.message.reply_text("// Chào Mừng Bạn Đến Với GitDo! //")


def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uptime_seconds = time.time() - start_time
    uptime_hours = int(uptime_seconds // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    uptime_seconds = int(uptime_seconds % 60)
    return [
        f"Thời gian hoạt động: {uptime_hours} giờ {uptime_minutes} phút {uptime_seconds} giây"
    ]


async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return
    if user_ids:
        user_list = []
        for user_id in user_ids:
            try:
                user = await context.bot.get_chat(user_id)
                username = user.full_name if user.full_name else "Không rõ tên"
                user_list.append(f"{user_id} - {username}")
            except Exception as e:
                user_list.append(f"{user_id} - Không thể lấy thông tin ({str(e)})")
        user_info_str = "\n".join(user_list)
        await update.message.reply_text(f"Danh sách người dùng GitDo:\n{user_info_str}")
    else:
        await update.message.reply_text("Chưa có người dùng nào tương tác với bot.")


async def send_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id != ADMIN_USER_ID:
        await update.message.reply_text("Bạn không có quyền gửi thông báo.")
        return
    notification_text = " ".join(update.message.text.split()[1:])
    if not notification_text:
        await update.message.reply_text("Bạn cần nhập nội dung thông báo.")
        return
    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=notification_text)
        except Exception as e:
            print(f"Không thể gửi thông báo đến người dùng {user_id}: {e}")
    await update.message.reply_text("Đã gửi thông báo đến tất cả người dùng.")


def thathinh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    response_list = []
    thathinh_message = random.choice(thathinh_list)

    response_list.append("Ok :))")
    response_list.append(thathinh_message)

    return response_list


def handle_response(text: str, update, context) -> str:
    processed: str = text.lower()

    def message(s, ans):
        if fuzz.partial_ratio(processed, s) > 70:
            return ans
        return None

    responses = [
        ("ping", status(update, context)),
        ("thả thính", thathinh(update, context)),
        ("hello", [random.choice(chao)]),
    ]

    for s, ans in responses:
        res = message(s, ans)
        if res:
            return res
    return [random.choice(casual_responses)]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response_list = handle_response(user_message, update, context)

    if user_message.lower() == "tkb":
        pass
    else:
        for response in response_list:
            await update.message.reply_text(response)


async def tkb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Khối 10", callback_data="10")],
        [InlineKeyboardButton("Khối 11", callback_data="11")],
        [InlineKeyboardButton("Khối 12", callback_data="12")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bạn muốn lấy thời khóa biểu khôi nào?",
        reply_markup=reply_markup,  # Display the initial prompt
    )


async def tkb_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler for inline buttons."""

    query = update.callback_query
    data = query.data
    await query.answer()

    tkb10ti = open("./tkb/10ti.jpg", "rb")
    tkb10t = open("./tkb/10t.jpg", "rb")
    tkb10sd = open("./tkb/10sd.jpg", "rb")

    match data:
        case "10":
            keyboard = [
                [
                    InlineKeyboardButton("Tin", callback_data="10ti"),
                    InlineKeyboardButton("Toán", callback_data="10t"),
                    InlineKeyboardButton("Sử - Địa", callback_data="10sd"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "Chọn lớp 10 chuyên:",
                reply_markup=reply_markup,
            )

    # Respond based on user selection
    match data:
        case "10ti":
            await query.edit_message_media(InputMediaPhoto(media=tkb10ti))
        case "10t":
            await query.edit_message_media(InputMediaPhoto(media=tkb10t))
        case "10sd":
            await query.edit_message_media(InputMediaPhoto(media=tkb10sd))

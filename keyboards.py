from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


markup = ReplyKeyboardMarkup(resize_keyboard=True)

markup.row("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng - 🇺🇿 Uzb", "🇷🇺 Rus - 🇺🇿 Uzb")
markup.row("🇺🇿 Uzb - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng", "🇺🇿 Uzb - 🇷🇺 Rus")
markup.row("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng - 🇷🇺 Rus", "🇷🇺 Rus - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Eng")

speech_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎙 Audio tinglash", callback_data="audio")]
])

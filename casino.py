
import customtkinter as ctk
import random

# =========================================================
# НАСТРОЙКИ
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎰 CASINO DELUXE")
app.geometry("1100x700")
app.minsize(900, 600)

# =========================================================
# СОСТОЯНИЕ ИГРЫ
# =========================================================

START_BALANCE = 100
MAX_CREDIT = 1_000_000
CREDIT_PERCENT = 0.20
CREDIT_TURNS = 5

chips = START_BALANCE
debt = 0
turns_left = 0
game_round = 1

wins = 0
losses = 0

history = []

# =========================================================
# ЦВЕТА РУЛЕТКИ
# =========================================================

RED = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

BLACK = {
    2, 4, 6, 8, 10, 11, 13, 15, 17,
    20, 22, 24, 26, 28, 29, 31, 33, 35
}

SLOT_SYMBOLS = ["🍒", "🍋", "🍊", "💎", "7️⃣"]

# =========================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================================================

def money(value):
    return f"{value:,}".replace(",", " ")


def update_balance():
    balance_label.configure(text=f"🪙 {money(chips)}")
    debt_label.configure(text=f"💳 Борг: {money(debt)} 🪙")
    timer_label.configure(text=f"⏳ Ходів: {turns_left}")
    round_label.configure(text=f"🔄 Раунд: {game_round}")


def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


def add_history(text):
    history.insert(0, text)

    if len(history) > 10:
        history.pop()


def change_balance(amount):
    global chips
    chips += amount
    update_balance()


def parse_bet(entry):
    try:
        amount = int(entry.get().replace(" ", ""))

        if amount <= 0:
            return None, "❌ Ставка должна быть больше 0."

        if amount > chips:
            return None, "❌ Недостаточно монет."

        return amount, None

    except ValueError:
        return None, "❌ Введите целое число."


def make_turn():
    global turns_left

    if debt <= 0:
        return

    turns_left -= 1
    update_balance()

    if turns_left <= 0:
        app.after(500, collector)


# =========================================================
# ГЛАВНАЯ
# =========================================================

def show_home():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎰 CASINO DELUXE",
        font=("Arial", 42, "bold"),
        text_color="gold"
    ).pack(pady=60)

    ctk.CTkLabel(
        content_frame,
        text="Добро пожаловать!",
        font=("Arial", 28)
    ).pack(pady=10)

    ctk.CTkLabel(
        content_frame,
        text="Выберите игру или функцию слева",
        font=("Arial", 18),
        text_color="gray"
    ).pack(pady=10)

    stats = ctk.CTkFrame(content_frame)
    stats.pack(pady=40)

    ctk.CTkLabel(
        stats,
        text=f"🪙 Баланс: {money(chips)}",
        font=("Arial", 20, "bold"),
        text_color="gold"
    ).pack(padx=30, pady=10)

    ctk.CTkLabel(
        stats,
        text=f"🏆 Победы: {wins}     💀 Поражения: {losses}",
        font=("Arial", 18)
    ).pack(padx=30, pady=10)


# =========================================================
# БАРАБАНЫ
# =========================================================

def show_slots():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎰 БАРАБАНЫ",
        font=("Arial", 36, "bold"),
        text_color="gold"
    ).pack(pady=30)

    slot_label = ctk.CTkLabel(
        content_frame,
        text="🍒   🍋   🍒",
        font=("Arial", 60)
    )
    slot_label.pack(pady=30)

    bet_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="💰 Ставка",
        width=280,
        height=50,
        font=("Arial", 17)
    )
    bet_entry.pack(pady=10)

    result = ctk.CTkLabel(
        content_frame,
        text="Сделайте ставку",
        font=("Arial", 20)
    )
    result.pack(pady=20)

    def spin():
        global chips, wins, losses

        amount, error = parse_bet(bet_entry)

        if error:
            result.configure(
                text=error,
                text_color="red"
            )
            return

        chips -= amount

        symbols = [
            random.choice(SLOT_SYMBOLS)
            for _ in range(3)
        ]

        a, b, c = symbols

        slot_label.configure(
            text=f"{a}   {b}   {c}"
        )

        if a == b == c:
            win = amount * 10
            chips += win
            wins += 1

            result.configure(
                text=f"🎉 ДЖЕКПОТ! +{money(win)} 🪙",
                text_color="gold"
            )

            add_history(
                f"🎰 Джекпот +{money(win)}"
            )

        elif a == b or b == c or a == c:
            win = amount * 2
            chips += win
            wins += 1

            result.configure(
                text=f"🎉 ВЫИГРЫШ! +{money(win)} 🪙",
                text_color="lime"
            )

            add_history(
                f"🎰 Выигрыш +{money(win)}"
            )

        else:
            losses += 1

            result.configure(
                text=f"😢 ПРОИГРЫШ! -{money(amount)} 🪙",
                text_color="red"
            )

            add_history(
                f"🎰 Проигрыш -{money(amount)}"
            )

        make_turn()
        update_balance()

    ctk.CTkButton(
        content_frame,
        text="🎰 КРУТИТЬ БАРАБАНЫ",
        width=320,
        height=55,
        font=("Arial", 18, "bold"),
        command=spin
    ).pack(pady=10)


# =========================================================
# РУЛЕТКА
# =========================================================

def show_roulette():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎡 РУЛЕТКА",
        font=("Arial", 36, "bold"),
        text_color="gold"
    ).pack(pady=25)

    wheel = ctk.CTkLabel(
        content_frame,
        text="🟢 0",
        font=("Arial", 65, "bold")
    )
    wheel.pack(pady=25)

    bet_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="💰 Ставка",
        width=280,
        height=50
    )
    bet_entry.pack(pady=10)

    choice = ctk.StringVar(value="Красное")

    ctk.CTkOptionMenu(
        content_frame,
        variable=choice,
        values=[
            "Красное",
            "Чёрное",
            "Парное",
            "Непарное"
        ],
        width=280,
        height=45
    ).pack(pady=10)

    result = ctk.CTkLabel(
        content_frame,
        text="Сделайте ставку",
        font=("Arial", 20)
    )
    result.pack(pady=20)

    def spin():
        global chips, wins, losses

        amount, error = parse_bet(bet_entry)

        if error:
            result.configure(
                text=error,
                text_color="red"
            )
            return

        chips -= amount

        number = random.randint(0, 36)

        if number == 0:
            icon = "🟢"
        elif number in RED:
            icon = "🔴"
        else:
            icon = "⚫"

        wheel.configure(
            text=f"{icon} {number}"
        )

        selected = choice.get()

        if selected == "Красное":
            won = number in RED

        elif selected == "Чёрное":
            won = number in BLACK

        elif selected == "Парное":
            won = number != 0 and number % 2 == 0

        else:
            won = number % 2 == 1

        if won:
            win = amount * 2
            chips += win
            wins += 1

            result.configure(
                text=f"🎉 ВЫИГРЫШ! +{money(win)} 🪙",
                text_color="lime"
            )

            add_history(
                f"🎡 Рулетка: +{money(win)}"
            )

        else:
            losses += 1

            result.configure(
                text=f"💀 ПРОИГРЫШ! -{money(amount)} 🪙",
                text_color="red"
            )

            add_history(
                f"🎡 Рулетка: -{money(amount)}"
            )

        make_turn()
        update_balance()

    ctk.CTkButton(
        content_frame,
        text="🎡 КРУТИТЬ РУЛЕТКУ",
        width=320,
        height=55,
        fg_color="#A00000",
        hover_color="#D00000",
        font=("Arial", 18, "bold"),
        command=spin
    ).pack(pady=10)


# =========================================================
# КРЕДИТ
# =========================================================

def show_credit():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="💳 КРЕДИТНЫЙ ЦЕНТР",
        font=("Arial", 36, "bold"),
        text_color="orange"
    ).pack(pady=30)

    ctk.CTkLabel(
        content_frame,
        text=f"Максимальный кредит: {money(MAX_CREDIT)} 🪙",
        font=("Arial", 21)
    ).pack(pady=10)

    credit_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="Введите сумму кредита",
        width=320,
        height=50,
        font=("Arial", 17)
    )
    credit_entry.pack(pady=20)

    ctk.CTkLabel(
        content_frame,
        text="📈 Процент: 20%\n⏳ Срок: 5 ходов",
        font=("Arial", 18),
        text_color="yellow"
    ).pack(pady=10)

    info = ctk.CTkLabel(
        content_frame,
        text="Введите сумму от 1 до 1 000 000",
        font=("Arial", 16)
    )
    info.pack(pady=15)

    def take_credit():
        global chips, debt, turns_left

        if debt > 0:
            info.configure(
                text="❌ Сначала погасите текущий кредит.",
                text_color="red"
            )
            return

        try:
            amount = int(
                credit_entry.get().replace(" ", "")
            )
        except ValueError:
            info.configure(
                text="❌ Введите целое число.",
                text_color="red"
            )
            return

        if amount <= 0:
            info.configure(
                text="❌ Сумма должна быть больше 0.",
                text_color="red"
            )
            return

        if amount > MAX_CREDIT:
            info.configure(
                text="❌ Максимум — 1 000 000 🪙",
                text_color="red"
            )
            return

        debt = int(
            amount * (1 + CREDIT_PERCENT)
        )

        chips += amount
        turns_left = CREDIT_TURNS

        update_balance()

        info.configure(
            text=(
                f"💰 Получено: {money(amount)} 🪙\n"
                f"💳 Вернуть: {money(debt)} 🪙"
            ),
            text_color="lime"
        )

        add_history(
            f"💳 Взят кредит {money(amount)}"
        )

    ctk.CTkButton(
        content_frame,
        text="💳 ВЗЯТЬ КРЕДИТ",
        width=320,
        height=55,
        font=("Arial", 18, "bold"),
        fg_color="#8B0000",
        hover_color="#B00000",
        command=take_credit
    ).pack(pady=20)


# =========================================================
# ПОГАШЕНИЕ КРЕДИТА
# =========================================================

def show_repay():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="💰 ПОГАШЕНИЕ КРЕДИТА",
        font=("Arial", 34, "bold"),
        text_color="lime"
    ).pack(pady=40)

    if debt <= 0:
        ctk.CTkLabel(
            content_frame,
            text="✅ У вас нет задолженности!",
            font=("Arial", 25),
            text_color="lime"
        ).pack(pady=50)

        return

    ctk.CTkLabel(
        content_frame,
        text=f"💳 Текущий долг:\n{money(debt)} 🪙",
        font=("Arial", 28, "bold"),
        text_color="orange"
    ).pack(pady=20)

    ctk.CTkLabel(
        content_frame,
        text=f"🪙 На балансе: {money(chips)}",
        font=("Arial", 20)
    ).pack(pady=10)

    def repay():
        global chips, debt, turns_left, game_round

        if chips < debt:
            show_insufficient()
            return

        chips -= debt
        debt = 0
        turns_left = 0
        game_round += 1

        add_history("💰 Кредит полностью погашен")

        update_balance()
        show_repay()

    ctk.CTkButton(
        content_frame,
        text=f"💰 ПОГАСИТЬ {money(debt)} 🪙",
        width=350,
        height=55,
        font=("Arial", 18, "bold"),
        fg_color="green",
        hover_color="darkgreen",
        command=repay
    ).pack(pady=30)


def show_insufficient():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="❌ НЕДОСТАТОЧНО МОНЕТ",
        font=("Arial", 30, "bold"),
        text_color="red"
    ).pack(pady=80)

    ctk.CTkLabel(
        content_frame,
        text=(
            f"Нужно: {money(debt)} 🪙\n"
            f"Есть: {money(chips)} 🪙"
        ),
        font=("Arial", 22)
    ).pack(pady=20)


# =========================================================
# КОЛЛЕКТОР
# =========================================================

def collector():
    global chips, debt, turns_left, game_round

    if debt <= 0:
        return

    penalty = min(chips, 100)

    chips -= penalty
    debt = 0
    turns_left = 0
    game_round += 1

    add_history(
        f"🚨 Коллектор забрал {money(penalty)}"
    )

    update_balance()

    win = ctk.CTkToplevel(app)
    win.title("🚨 КОЛЛЕКТОР")
    win.geometry("500x400")
    win.grab_set()

    ctk.CTkLabel(
        win,
        text="🚨 КОЛЛЕКТОР",
        font=("Arial", 36, "bold"),
        text_color="red"
    ).pack(pady=30)

    ctk.CTkLabel(
        win,
        text="Срок кредита закончился!",
        font=("Arial", 20)
    ).pack(pady=10)

    ctk.CTkLabel(
        win,
        text=f"💸 Штраф: -{money(penalty)} 🪙",
        font=("Arial", 24, "bold"),
        text_color="orange"
    ).pack(pady=20)

    ctk.CTkButton(
        win,
        text="🔄 ПРОДОЛЖИТЬ",
        width=250,
        height=50,
        command=win.destroy
    ).pack(pady=20)


# =========================================================
# ИСТОРИЯ
# =========================================================

def show_history():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="📜 ИСТОРИЯ ИГР",
        font=("Arial", 36, "bold"),
        text_color="cyan"
    ).pack(pady=30)

    if not history:
        ctk.CTkLabel(
            content_frame,
            text="История пока пустая.",
            font=("Arial", 20),
            text_color="gray"
        ).pack(pady=50)

        return

    box = ctk.CTkTextbox(
        content_frame,
        width=600,
        height=400,
        font=("Arial", 17)
    )
    box.pack(pady=20)

    for index, item in enumerate(history, 1):
        box.insert(
            "end",
            f"{index}. {item}\n"
        )

    box.configure(state="disabled")


# =========================================================
# СТАТИСТИКА
# =========================================================

def show_stats():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="📊 СТАТИСТИКА",
        font=("Arial", 36, "bold"),
        text_color="cyan"
    ).pack(pady=40)

    ctk.CTkLabel(
        content_frame,
        text=f"🏆 Победы: {wins}",
        font=("Arial", 24),
        text_color="lime"
    ).pack(pady=10)

    ctk.CTkLabel(
        content_frame,
        text=f"💀 Поражения: {losses}",
        font=("Arial", 24),
        text_color="red"
    ).pack(pady=10)

    ctk.CTkLabel(
        content_frame,
        text=f"🪙 Баланс: {money(chips)}",
        font=("Arial", 24),
        text_color="gold"
    ).pack(pady=10)

    ctk.CTkLabel(
        content_frame,
        text=f"🔄 Раунд: {game_round}",
        font=("Arial", 24)
    ).pack(pady=10)


# =========================================================
# ИНТЕРФЕЙС
# =========================================================

def show_interface():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎨 ИНТЕРФЕЙС",
        font=("Arial", 36, "bold"),
        text_color="cyan"
    ).pack(pady=50)

    ctk.CTkButton(
        content_frame,
        text="🌙 Тёмная тема",
        width=250,
        height=45,
        command=lambda: ctk.set_appearance_mode("dark")
    ).pack(pady=10)

    ctk.CTkButton(
        content_frame,
        text="☀️ Светлая тема",
        width=250,
        height=45,
        command=lambda: ctk.set_appearance_mode("light")
    ).pack(pady=10)


# =========================================================
# СБРОС ИГРЫ
# =========================================================

def reset_game():
    global chips, debt, turns_left, game_round
    global wins, losses, history

    chips = START_BALANCE
    debt = 0
    turns_left = 0
    game_round = 1

    wins = 0
    losses = 0
    history = []

    update_balance()
    show_home()


# =========================================================
# ОСНОВНОЙ ИНТЕРФЕЙС
# =========================================================

main_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
main_frame.pack(
    fill="both",
    expand=True
)

# =========================================================
# ЛЕВОЕ МЕНЮ
# =========================================================

menu_frame = ctk.CTkFrame(
    main_frame,
    width=240,
    corner_radius=0,
    fg_color="#151515"
)

menu_frame.pack(
    side="left",
    fill="y"
)

menu_frame.pack_propagate(False)

ctk.CTkLabel(
    menu_frame,
    text="🎰\nCASINO",
    font=("Arial", 28, "bold"),
    text_color="gold"
).pack(pady=25)


def menu_button(text, command):
    ctk.CTkButton(
        menu_frame,
        text=text,
        height=42,
        command=command
    ).pack(
        fill="x",
        padx=15,
        pady=4
    )


menu_button("🏠 Главная", show_home)
menu_button("🎡 Рулетка", show_roulette)
menu_button("🎰 Барабаны", show_slots)
menu_button("💳 Кредит", show_credit)
menu_button("💰 Погасить кредит", show_repay)
menu_button("📜 История", show_history)
menu_button("📊 Статистика", show_stats)
menu_button("🎨 Интерфейс", show_interface)

ctk.CTkFrame(
    menu_frame,
    height=2,
    fg_color="#444444"
).pack(
    fill="x",
    padx=15,
    pady=15
)

balance_label = ctk.CTkLabel(
    menu_frame,
    text="🪙 100",
    font=("Arial", 21, "bold"),
    text_color="gold"
)
balance_label.pack(pady=4)

debt_label = ctk.CTkLabel(
    menu_frame,
    text="💳 Борг: 0 🪙",
    font=("Arial", 14)
)
debt_label.pack(pady=4)

timer_label = ctk.CTkLabel(
    menu_frame,
    text="⏳ Ходів: 0",
    font=("Arial", 14)
)
timer_label.pack(pady=4)

round_label = ctk.CTkLabel(
    menu_frame,
    text="🔄 Раунд: 1",
    font=("Arial", 14),
    text_color="cyan"
)
round_label.pack(pady=4)

ctk.CTkButton(
    menu_frame,
    text="🔄 НОВА ИГРА",
    height=40,
    fg_color="#8B0000",
    hover_color="#B00000",
    command=reset_game
).pack(
    fill="x",
    padx=15,
    pady=20
)

# =========================================================
# ПРАВАЯ ЧАСТЬ
# =========================================================

content_frame = ctk.CTkFrame(
    main_frame,
    corner_radius=0,
    fg_color="#202020"
)

content_frame.pack(
    side="right",
    fill="both",
    expand=True
)

# =========================================================
# ЗАПУСК
# =========================================================

update_balance()
show_home()

app.mainloop()


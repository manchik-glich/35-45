import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎰 КАЗИНО DELUXE")
app.geometry("700x850")

# =========================
# СТАН ГРИ
# =========================

chips = 100
debt = 0
interest = 0.20
turns_left = 0
game_round = 1
spinning = False


# =========================
# РУЛЕТКА
# =========================

RED = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

BLACK = {
    2, 4, 6, 8, 10, 11, 13, 15, 17,
    20, 22, 24, 26, 28, 29, 31, 33, 35
}


def number_color(number):
    if number == 0:
        return "🟢"
    if number in RED:
        return "🔴"
    return "⚫"


# =========================
# ОНОВЛЕННЯ ІНФОРМАЦІЇ
# =========================

def update_ui():
    balance.configure(text=f"🪙 КРЕДИТИ: {chips}")
    debt_label.configure(
        text=f"💳 БОРГ: {debt} 🪙"
    )
    timer_label.configure(
        text=f"⏳ ДО ТЕРМІНУ: {turns_left} ХОДІВ"
    )
    round_label.configure(
        text=f"🔄 РАУНД: {game_round}"
    )

    if debt > 0:
        debt_label.configure(text_color="orange")
    else:
        debt_label.configure(text_color="white")


# =========================
# КРЕДИТ
# =========================

def take_credit():
    global chips, debt, turns_left

    if debt > 0:
        result.configure(
            text="❌ У тебе вже є непогашений кредит!",
            text_color="red"
        )
        return

    amount = 500

    chips += amount
    debt = amount
    turns_left = 5

    update_ui()

    result.configure(
        text=(
            f"💳 Ти взяв кредит {amount} 🪙\n"
            f"Повернути треба {int(amount * (1 + interest))} 🪙"
        ),
        text_color="orange"
    )


def repay_credit():
    global chips, debt, turns_left, game_round

    if debt <= 0:
        result.configure(
            text="ℹ️ У тебе немає боргу"
        )
        return

    if chips < debt:
        result.configure(
            text=f"❌ Потрібно {debt} 🪙",
            text_color="red"
        )
        return

    chips -= debt
    debt = 0
    turns_left = 0

    game_round += 1

    result.configure(
        text="✅ Кредит повністю погашено!",
        text_color="lime"
    )

    update_ui()


# =========================
# КОЛЕКТОР
# =========================

def collector():
    global chips, debt, turns_left, game_round

    penalty = min(chips, 100)

    chips -= penalty

    debt = 0
    turns_left = 0
    game_round += 1

    win = ctk.CTkToplevel(app)
    win.title("🚨 КОЛЕКТОР")
    win.geometry("500x400")
    win.grab_set()

    ctk.CTkLabel(
        win,
        text="🚨 КОЛЕКТОР ПРИЇХАВ!",
        font=("Arial", 32, "bold"),
        text_color="red"
    ).pack(pady=30)

    ctk.CTkLabel(
        win,
        text=(
            "— ГРОШІ Є?\n"
            "— Немає...\n"
            "— Ну тоді забираємо штраф 😈"
        ),
        font=("Arial", 20)
    ).pack(pady=20)

    ctk.CTkLabel(
        win,
        text=f"💸 Штраф: -{penalty} 🪙",
        font=("Arial", 20, "bold"),
        text_color="orange"
    ).pack(pady=10)

    def restart():
        win.destroy()

        result.configure(
            text="🔄 НОВИЙ РАУНД! Починай спочатку.",
            text_color="cyan"
        )

        update_ui()

    ctk.CTkButton(
        win,
        text="🔄 НОВИЙ РАУНД",
        width=250,
        height=50,
        command=restart
    ).pack(pady=20)

    update_ui()


# =========================
# ХІД
# =========================

def make_turn():
    global turns_left

    if debt <= 0:
        return

    turns_left -= 1

    if turns_left <= 0:
        update_ui()

        app.after(
            500,
            collector
        )
    else:
        update_ui()


# =========================
# СЛОТИ
# =========================

def slots():
    global chips

    try:
        bet = int(bet_entry.get())
    except ValueError:
        result.configure(
            text="❌ Введи ставку"
        )
        return

    if bet <= 0:
        result.configure(
            text="❌ Ставка має бути більше 0"
        )
        return

    if bet > chips:
        result.configure(
            text="❌ Недостатньо кредитів"
        )
        return

    chips -= bet

    symbols = [
        "🍒",
        "🍋",
        "🍊",
        "💎",
        "7️⃣"
    ]

    a, b, c = [
        random.choice(symbols)
        for _ in range(3)
    ]

    slot.configure(
        text=f"{a}   {b}   {c}"
    )

    if a == b == c:
        win = bet * 10
        chips += win

        result.configure(
            text=f"🎰 ДЖЕКПОТ! +{win} 🪙",
            text_color="gold"
        )

    elif a == b or b == c or a == c:
        win = bet * 2
        chips += win

        result.configure(
            text=f"🎉 ВИГРАШ! +{win} 🪙",
            text_color="lime"
        )

    else:
        result.configure(
            text=f"😢 ПРОГРАШ! -{bet} 🪙",
            text_color="red"
        )

    make_turn()
    update_ui()


# =========================
# РУЛЕТКА
# =========================

def roulette():
    global chips, spinning

    if spinning:
        return

    try:
        bet = int(bet_entry.get())
    except ValueError:
        result.configure(
            text="❌ Введи ставку"
        )
        return

    if bet <= 0 or bet > chips:
        result.configure(
            text="❌ Недостатньо кредитів"
        )
        return

    chips -= bet

    spinning = True

    result.configure(
        text="🎡 РУЛЕТКА ОБЕРТАЄТЬСЯ...",
        text_color="yellow"
    )

    spin_animation(0, bet)


def spin_animation(step, bet):
    global spinning

    number = random.randint(0, 36)

    wheel.configure(
        text=f"{number_color(number)} {number}"
    )

    if step < 35:
        delay = 40 + step * 7

        app.after(
            delay,
            lambda: spin_animation(
                step + 1,
                bet
            )
        )
    else:
        finish_roulette(bet)


def finish_roulette(bet):
    global chips, spinning

    number = random.randint(0, 36)
    choice = roulette_choice.get()

    wheel.configure(
        text=f"{number_color(number)} {number}"
    )

    won = False

    if choice == "Червоне":
        won = number in RED

    elif choice == "Чорне":
        won = number in BLACK

    elif choice == "Парне":
        won = number != 0 and number % 2 == 0

    elif choice == "Непарне":
        won = number % 2 == 1

    if won:
        win = bet * 2
        chips += win

        result.configure(
            text=f"🎉 ВИГРАШ! Випало {number} +{win} 🪙",
            text_color="lime"
        )
    else:
        result.configure(
            text=f"💀 ПРОГРАШ! Випало {number} -{bet} 🪙",
            text_color="red"
        )

    spinning = False

    make_turn()
    update_ui()


# =========================
# ФЕЙКОВЕ ПОПОВНЕННЯ
# =========================

def deposit():
    win = ctk.CTkToplevel(app)

    win.title("💳 ТУТ ПРОДАЮТЬСЯ ГРОШІ!!!")
    win.geometry("450x600")
    win.grab_set()

    ctk.CTkLabel(
        win,
        text="💳 ТУТ ПРОДАЮТЬСЯ ГРОШІ!!!",
        font=("Arial", 24, "bold"),
        text_color="gold"
    ).pack(pady=25)

    ctk.CTkLabel(
        win,
        text="⚠️ DEMO — реальних платежів немає",
        text_color="orange"
    ).pack(pady=5)

    ctk.CTkLabel(
        win,
        text="💳 Тестовий номер"
    ).pack(pady=(20, 5))

    card = ctk.CTkEntry(
        win,
        placeholder_text="0000 0000 0000 0000",
        width=300
    )
    card.pack()

    ctk.CTkLabel(
        win,
        text="🌐 Фейковий IP"
    ).pack(pady=(20, 5))

    fake_ip = (
        f"192.168."
        f"{random.randint(0,255)}."
        f"{random.randint(1,254)}"
    )

    ctk.CTkLabel(
        win,
        text=fake_ip,
        font=("Consolas", 18),
        text_color="cyan"
    ).pack()

    ctk.CTkLabel(
        win,
        text="🔐 Тестовий код"
    ).pack(pady=(20, 5))

    cvv = ctk.CTkEntry(
        win,
        placeholder_text="123",
        show="*",
        width=150
    )
    cvv.pack()

    package = ctk.StringVar(
        value="50 грн → 20 кредитів"
    )

    ctk.CTkOptionMenu(
        win,
        variable=package,
        values=[
            "50 грн → 20 кредитів",
            "100 грн → 45 кредитів",
            "200 грн → 100 кредитів",
            "500 грн → 300 кредитів"
        ]
    ).pack(pady=25)

    def add_money():
        global chips

        rewards = {
            "50 грн → 20 кредитів": 20,
            "100 грн → 45 кредитів": 45,
            "200 грн → 100 кредитів": 100,
            "500 грн → 300 кредитів": 300
        }

        if not card.get() or not cvv.get():
            status.configure(
                text="❌ Введи тестові дані",
                text_color="red"
            )
            return

        amount = rewards[package.get()]

        chips += amount

        update_ui()

        status.configure(
            text=f"💰 +{amount} кредитів!",
            text_color="lime"
        )

    ctk.CTkButton(
        win,
        text="💸 КУПИТИ КРЕДИТИ",
        width=280,
        height=50,
        fg_color="green",
        hover_color="darkgreen",
        command=add_money
    ).pack()

    status = ctk.CTkLabel(
        win,
        text="Очікування..."
    )
    status.pack(pady=20)


# =========================
# ІНТЕРФЕЙС
# =========================

ctk.CTkLabel(
    app,
    text="🎰 КАЗИНО DELUXE",
    font=("Arial", 38, "bold"),
    text_color="gold"
).pack(pady=20)

round_label = ctk.CTkLabel(
    app,
    text="🔄 РАУНД: 1",
    font=("Arial", 16)
)
round_label.pack()

balance = ctk.CTkLabel(
    app,
    text="🪙 КРЕДИТИ: 100",
    font=("Arial", 25, "bold"),
    text_color="gold"
)
balance.pack(pady=10)

debt_label = ctk.CTkLabel(
    app,
    text="💳 БОРГ: 0 🪙",
    font=("Arial", 20)
)
debt_label.pack()

timer_label = ctk.CTkLabel(
    app,
    text="⏳ ДО ТЕРМІНУ: 0 ХОДІВ",
    font=("Arial", 17)
)
timer_label.pack(pady=5)


# =========================
# КНОПКИ КРЕДИТУ
# =========================

ctk.CTkButton(
    app,
    text="💳 ВЗЯТИ КРЕДИТ 500 🪙",
    width=300,
    height=45,
    fg_color="#8B0000",
    hover_color="#B00000",
    command=take_credit
).pack(pady=8)

ctk.CTkButton(
    app,
    text="💰 ПОГАСИТИ КРЕДИТ",
    width=300,
    command=repay_credit
).pack(pady=5)

ctk.CTkButton(
    app,
    text="💳 ТУТ ПРОДАЮТЬСЯ ГРОШІ!!!",
    width=300,
    command=deposit
).pack(pady=5)


# =========================
# СТАВКА
# =========================

bet_entry = ctk.CTkEntry(
    app,
    placeholder_text="💰 Сума ставки",
    width=250,
    height=40
)
bet_entry.pack(pady=20)


# =========================
# СЛОТИ
# =========================

ctk.CTkLabel(
    app,
    text="🎰 СЛОТИ",
    font=("Arial", 22, "bold")
).pack()

slot = ctk.CTkLabel(
    app,
    text="🍒   🍋   🍒",
    font=("Arial", 45)
)
slot.pack(pady=10)

ctk.CTkButton(
    app,
    text="🎰 КРУТИТИ СЛОТИ",
    width=250,
    height=45,
    command=slots
).pack()


# =========================
# РУЛЕТКА
# =========================

ctk.CTkLabel(
    app,
    text="🎡 РУЛЕТКА",
    font=("Arial", 22, "bold")
).pack(pady=(25, 5))

wheel = ctk.CTkLabel(
    app,
    text="🟢 0",
    font=("Arial", 45, "bold")
)
wheel.pack(pady=10)

roulette_choice = ctk.StringVar(
    value="Червоне"
)

ctk.CTkOptionMenu(
    app,
    variable=roulette_choice,
    values=[
        "Червоне",
        "Чорне",
        "Парне",
        "Непарне"
    ],
    width=220
).pack(pady=5)

ctk.CTkButton(
    app,
    text="🎡 ЗАПУСТИТИ РУЛЕТКУ",
    width=280,
    height=50,
    fg_color="#A00000",
    hover_color="#D00000",
    font=("Arial", 17, "bold"),
    command=roulette
).pack(pady=10)


# =========================
# РЕЗУЛЬТАТ
# =========================

result = ctk.CTkLabel(
    app,
    text="Зроби ставку 😈",
    font=("Arial", 18, "bold")
)
result.pack(pady=20)

ctk.CTkLabel(
    app,
    text="⚠️ DEMO • Віртуальні кредити • Реальних платежів немає",
    font=("Arial", 11),
    text_color="gray"
).pack(side="bottom", pady=12)

app.mainloop()
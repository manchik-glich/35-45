import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎰 КАЗИНО DELUXE")
app.geometry("1000x700")
app.minsize(850, 600)

# ==========================================
# СТАН ГРИ
# ==========================================

chips = 100
debt = 0
interest = 0.20
turns_left = 0
game_round = 1
spinning = False


# ==========================================
# РУЛЕТКА
# ==========================================

RED = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

BLACK = {
    2, 4, 6, 8, 10, 11, 13, 15, 17,
    20, 22, 24, 26, 28, 29, 31, 33, 35
}


# ==========================================
# ОНОВЛЕННЯ
# ==========================================

def update_balance():
    balance_label.configure(
        text=f"🪙 {chips}"
    )

    debt_label.configure(
        text=f"💳 Борг: {debt} 🪙"
    )

    timer_label.configure(
        text=f"⏳ Ходів: {turns_left}"
    )

    round_label.configure(
        text=f"🔄 Раунд: {game_round}"
    )


# ==========================================
# ОЧИЩЕННЯ ЦЕНТРАЛЬНОЇ ОБЛАСТІ
# ==========================================

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


# ==========================================
# ГОЛОВНИЙ ЕКРАН
# ==========================================

def show_home():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎰 КАЗИНО DELUXE",
        font=("Arial", 42, "bold"),
        text_color="gold"
    ).pack(pady=80)

    ctk.CTkLabel(
        content_frame,
        text="Ласкаво просимо!",
        font=("Arial", 24)
    ).pack(pady=10)

    ctk.CTkLabel(
        content_frame,
        text="Обери гру або функцію в меню зліва 👈",
        font=("Arial", 18),
        text_color="gray"
    ).pack(pady=10)


# ==========================================
# КРЕДИТ
# ==========================================

def show_credit():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="💳 КРЕДИТ",
        font=("Arial", 36, "bold"),
        text_color="orange"
    ).pack(pady=40)

    ctk.CTkLabel(
        content_frame,
        text="Отримай 500 🪙 зараз\n"
             "та поверни з відсотками.",
        font=("Arial", 20)
    ).pack(pady=20)

    ctk.CTkLabel(
        content_frame,
        text="500 🪙 → 600 🪙\n"
             "Термін: 5 ходів",
        font=("Arial", 22, "bold"),
        text_color="yellow"
    ).pack(pady=20)

    ctk.CTkButton(
        content_frame,
        text="💳 ВЗЯТИ КРЕДИТ",
        width=300,
        height=55,
        font=("Arial", 18, "bold"),
        fg_color="#8B0000",
        hover_color="#B00000",
        command=take_credit
    ).pack(pady=20)


def take_credit():
    global chips, debt, turns_left

    if debt > 0:
        show_message(
            "❌ У тебе вже є кредит!"
        )
        return

    chips += 500
    debt = 600
    turns_left = 5

    update_balance()

    show_message(
        "💳 Кредит отримано!\n"
        "Тепер потрібно повернути 600 🪙"
    )


# ==========================================
# ПОГАШЕННЯ
# ==========================================

def show_repay():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="💰 ПОГАШЕННЯ КРЕДИТУ",
        font=("Arial", 32, "bold"),
        text_color="lime"
    ).pack(pady=40)

    if debt <= 0:

        ctk.CTkLabel(
            content_frame,
            text="✅ У тебе немає боргу!",
            font=("Arial", 24),
            text_color="lime"
        ).pack(pady=50)

        return

    ctk.CTkLabel(
        content_frame,
        text=f"Поточний борг: {debt} 🪙",
        font=("Arial", 25, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        content_frame,
        text=f"На руках: {chips} 🪙",
        font=("Arial", 20)
    ).pack(pady=10)

    ctk.CTkButton(
        content_frame,
        text=f"💰 ПОГАСИТИ {debt} 🪙",
        width=300,
        height=55,
        fg_color="green",
        hover_color="darkgreen",
        command=repay_credit
    ).pack(pady=30)


def repay_credit():
    global chips, debt, turns_left, game_round

    if debt <= 0:
        return

    if chips < debt:
        show_message(
            f"❌ Недостатньо кредитів!\n"
            f"Потрібно: {debt} 🪙"
        )
        return

    chips -= debt
    debt = 0
    turns_left = 0
    game_round += 1

    update_balance()

    show_repay()


# ==========================================
# БАРАБАНИ
# ==========================================

def show_slots():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎰 БАРАБАНИ",
        font=("Arial", 36, "bold"),
        text_color="gold"
    ).pack(pady=35)

    slot_label = ctk.CTkLabel(
        content_frame,
        text="🍒   🍋   🍒",
        font=("Arial", 55)
    )

    slot_label.pack(pady=40)

    bet = ctk.CTkEntry(
        content_frame,
        placeholder_text="💰 Ставка",
        width=250,
        height=45
    )

    bet.pack(pady=10)

    result = ctk.CTkLabel(
        content_frame,
        text="Зроби ставку",
        font=("Arial", 18)
    )

    result.pack(pady=20)

    def spin():

        global chips

        try:
            amount = int(bet.get())
        except ValueError:
            result.configure(
                text="❌ Введи число"
            )
            return

        if amount <= 0:
            result.configure(
                text="❌ Неправильна ставка"
            )
            return

        if amount > chips:
            result.configure(
                text="❌ Недостатньо 🪙"
            )
            return

        chips -= amount

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

        slot_label.configure(
            text=f"{a}   {b}   {c}"
        )

        if a == b == c:

            win = amount * 10
            chips += win

            result.configure(
                text=f"🎉 ДЖЕКПОТ +{win} 🪙",
                text_color="gold"
            )

        elif a == b or b == c or a == c:

            win = amount * 2
            chips += win

            result.configure(
                text=f"🎉 ВИГРАШ +{win} 🪙",
                text_color="lime"
            )

        else:

            result.configure(
                text=f"😢 ПРОГРАШ -{amount} 🪙",
                text_color="red"
            )

        make_turn()
        update_balance()

    ctk.CTkButton(
        content_frame,
        text="🎰 КРУТИТИ БАРАБАНИ",
        width=300,
        height=55,
        font=("Arial", 18, "bold"),
        command=spin
    ).pack(pady=10)


# ==========================================
# РУЛЕТКА
# ==========================================

def show_roulette():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎡 РУЛЕТКА",
        font=("Arial", 36, "bold"),
        text_color="gold"
    ).pack(pady=30)

    wheel = ctk.CTkLabel(
        content_frame,
        text="🟢 0",
        font=("Arial", 60, "bold")
    )

    wheel.pack(pady=30)

    bet = ctk.CTkEntry(
        content_frame,
        placeholder_text="💰 Ставка",
        width=250,
        height=45
    )

    bet.pack(pady=10)

    choice = ctk.StringVar(
        value="Червоне"
    )

    ctk.CTkOptionMenu(
        content_frame,
        variable=choice,
        values=[
            "Червоне",
            "Чорне",
            "Парне",
            "Непарне"
        ],
        width=250
    ).pack(pady=10)

    result = ctk.CTkLabel(
        content_frame,
        text="Зроби ставку",
        font=("Arial", 18)
    )

    result.pack(pady=20)

    def spin():

        global chips

        try:
            amount = int(bet.get())
        except ValueError:
            result.configure(
                text="❌ Введи число"
            )
            return

        if amount <= 0 or amount > chips:
            result.configure(
                text="❌ Недостатньо 🪙"
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

        won = False

        if selected == "Червоне":
            won = number in RED

        elif selected == "Чорне":
            won = number in BLACK

        elif selected == "Парне":
            won = number != 0 and number % 2 == 0

        elif selected == "Непарне":
            won = number % 2 == 1

        if won:

            win = amount * 2
            chips += win

            result.configure(
                text=f"🎉 ВИГРАШ +{win} 🪙",
                text_color="lime"
            )

        else:

            result.configure(
                text=f"💀 ПРОГРАШ -{amount} 🪙",
                text_color="red"
            )

        make_turn()
        update_balance()

    ctk.CTkButton(
        content_frame,
        text="🎡 КРУТИТИ РУЛЕТКУ",
        width=300,
        height=55,
        fg_color="#A00000",
        hover_color="#D00000",
        font=("Arial", 18, "bold"),
        command=spin
    ).pack(pady=15)


# ==========================================
# ХІД КРЕДИТУ
# ==========================================

def make_turn():

    global turns_left

    if debt <= 0:
        return

    turns_left -= 1

    if turns_left <= 0:
        update_balance()

        app.after(
            400,
            collector
        )

    update_balance()


# ==========================================
# КОЛЕКТОР
# ==========================================

def collector():

    global chips, debt, turns_left, game_round

    penalty = min(chips, 100)

    chips -= penalty

    debt = 0
    turns_left = 0
    game_round += 1

    update_balance()

    win = ctk.CTkToplevel(app)
    win.title("🚨 КОЛЕКТОР")
    win.geometry("500x400")

    ctk.CTkLabel(
        win,
        text="🚨 КОЛЕКТОР",
        font=("Arial", 36, "bold"),
        text_color="red"
    ).pack(pady=30)

    ctk.CTkLabel(
        win,
        text="Термін кредиту закінчився!",
        font=("Arial", 20)
    ).pack(pady=10)

    ctk.CTkLabel(
        win,
        text=f"💸 Штраф: -{penalty} 🪙",
        font=("Arial", 24, "bold"),
        text_color="orange"
    ).pack(pady=20)

    ctk.CTkLabel(
        win,
        text="🔄 Починається новий раунд",
        font=("Arial", 18),
        text_color="cyan"
    ).pack(pady=10)

    ctk.CTkButton(
        win,
        text="🔄 ПРОДОВЖИТИ",
        width=250,
        height=50,
        command=win.destroy
    ).pack(pady=20)


# ==========================================
# ПОВІДОМЛЕННЯ
# ==========================================

def show_message(text):

    clear_content()

    ctk.CTkLabel(
        content_frame,
        text=text,
        font=("Arial", 25, "bold"),
        justify="center"
    ).pack(
        expand=True
    )


# ==========================================
# ІНТЕРФЕЙС
# ==========================================

def show_interface():

    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="🎨 ІНТЕРФЕЙС",
        font=("Arial", 36, "bold"),
        text_color="cyan"
    ).pack(pady=50)

    ctk.CTkLabel(
        content_frame,
        text="Тема оформлення",
        font=("Arial", 20)
    ).pack(pady=15)

    def dark():
        ctk.set_appearance_mode("dark")

    def light():
        ctk.set_appearance_mode("light")

    ctk.CTkButton(
        content_frame,
        text="🌙 Темна тема",
        width=250,
        command=dark
    ).pack(pady=10)

    ctk.CTkButton(
        content_frame,
        text="☀️ Світла тема",
        width=250,
        command=light
    ).pack(pady=10)


# ==========================================
# ГОЛОВНИЙ КОНТЕЙНЕР
# ==========================================

main_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

main_frame.pack(
    fill="both",
    expand=True
)


# ==========================================
# ЛІВЕ МЕНЮ
# ==========================================

menu_frame = ctk.CTkFrame(
    main_frame,
    width=220,
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
    text="🎰\nКАЗИНО",
    font=("Arial", 27, "bold"),
    text_color="gold"
).pack(pady=30)


ctk.CTkButton(
    menu_frame,
    text="🏠 Головна",
    height=45,
    command=show_home
).pack(
    fill="x",
    padx=15,
    pady=5
)

ctk.CTkButton(
    menu_frame,
    text="💳 Кредит",
    height=45,
    command=show_credit
).pack(
    fill="x",
    padx=15,
    pady=5
)

ctk.CTkButton(
    menu_frame,
    text="🎡 Рулетка",
    height=45,
    command=show_roulette
).pack(
    fill="x",
    padx=15,
    pady=5
)

ctk.CTkButton(
    menu_frame,
    text="🎰 Барабани",
    height=45,
    command=show_slots
).pack(
    fill="x",
    padx=15,
    pady=5
)

ctk.CTkButton(
    menu_frame,
    text="💰 Погасити кредит",
    height=45,
    command=show_repay
).pack(
    fill="x",
    padx=15,
    pady=5
)

ctk.CTkButton(
    menu_frame,
    text="🎨 Інтерфейс",
    height=45,
    command=show_interface
).pack(
    fill="x",
    padx=15,
    pady=5
)


# ==========================================
# НИЖНЯ ІНФОРМАЦІЯ
# ==========================================

ctk.CTkFrame(
    menu_frame,
    height=2,
    fg_color="#444444"
).pack(
    fill="x",
    padx=15,
    pady=20
)

balance_label = ctk.CTkLabel(
    menu_frame,
    text="🪙 100",
    font=("Arial", 22, "bold"),
    text_color="gold"
)

balance_label.pack(pady=5)

debt_label = ctk.CTkLabel(
    menu_frame,
    text="💳 Борг: 0 🪙",
    font=("Arial", 15)
)

debt_label.pack(pady=5)

timer_label = ctk.CTkLabel(
    menu_frame,
    text="⏳ Ходів: 0",
    font=("Arial", 15)
)

timer_label.pack(pady=5)

round_label = ctk.CTkLabel(
    menu_frame,
    text="🔄 Раунд: 1",
    font=("Arial", 15),
    text_color="cyan"
)

round_label.pack(pady=5)


# ==========================================
# ПРАВА ЧАСТИНА
# ==========================================

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



update_balance()
show_home()

app.mainloop()
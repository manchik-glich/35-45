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


# ==========================================
# КОЛЬОРИ РУЛЕТКИ
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
# ОНОВЛЕННЯ ІНФОРМАЦІЇ
# ==========================================

def update_balance():
    balance_label.configure(
        text=f"🪙 {chips:,}".replace(",", " ")
    )

    debt_label.configure(
        text=f"💳 Борг: {debt:,} 🪙".replace(",", " ")
    )

    timer_label.configure(
        text=f"⏳ Ходів: {turns_left}"
    )

    round_label.configure(
        text=f"🔄 Раунд: {game_round}"
    )


# ==========================================
# ОЧИСТИТИ ЦЕНТР
# ==========================================

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


# ==========================================
# ГОЛОВНА
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
        font=("Arial", 26)
    ).pack(pady=10)

    ctk.CTkLabel(
        content_frame,
        text="Обери гру або функцію з меню зліва 👈",
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
        text="💳 КРЕДИТНИЙ ЦЕНТР",
        font=("Arial", 36, "bold"),
        text_color="orange"
    ).pack(pady=35)

    ctk.CTkLabel(
        content_frame,
        text="Максимальний кредит",
        font=("Arial", 20)
    ).pack(pady=5)

    ctk.CTkLabel(
        content_frame,
        text="1 000 000 🪙",
        font=("Arial", 32, "bold"),
        text_color="gold"
    ).pack(pady=10)

    credit_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="Введи суму кредиту",
        width=320,
        height=50,
        font=("Arial", 17)
    )

    credit_entry.pack(pady=20)

    ctk.CTkLabel(
        content_frame,
        text="📈 Відсоток: 20%\n⏳ Термін: 5 ходів",
        font=("Arial", 18),
        text_color="yellow"
    ).pack(pady=10)

    info = ctk.CTkLabel(
        content_frame,
        text="Введи суму від 1 до 1 000 000",
        font=("Arial", 16)
    )

    info.pack(pady=15)

    def take_custom_credit():

        global chips
        global debt
        global turns_left

        if debt > 0:
            info.configure(
                text="❌ Спочатку погаси поточний кредит!",
                text_color="red"
            )
            return

        try:
            amount = int(
                credit_entry.get().replace(" ", "")
            )
        except ValueError:
            info.configure(
                text="❌ Введи ціле число",
                text_color="red"
            )
            return

        if amount <= 0:
            info.configure(
                text="❌ Сума має бути більше 0",
                text_color="red"
            )
            return

        if amount > 1_000_000:
            info.configure(
                text="❌ Максимум — 1 000 000 🪙",
                text_color="red"
            )
            return

        # Відсотки
        debt = int(
            amount * (1 + interest)
        )

        chips += amount
        turns_left = 5

        update_balance()

        info.configure(
            text=(
                f"💰 Отримано: "
                f"{amount:,} 🪙\n"
                f"💳 Повернути: "
                f"{debt:,} 🪙"
            ).replace(",", " "),
            text_color="lime"
        )

    ctk.CTkButton(
        content_frame,
        text="💳 ВЗЯТИ КРЕДИТ",
        width=320,
        height=55,
        font=("Arial", 18, "bold"),
        fg_color="#8B0000",
        hover_color="#B00000",
        command=take_custom_credit
    ).pack(pady=20)


# ==========================================
# ПОГАШЕННЯ КРЕДИТУ
# ==========================================

def show_repay():
    clear_content()

    ctk.CTkLabel(
        content_frame,
        text="💰 ПОГАШЕННЯ КРЕДИТУ",
        font=("Arial", 34, "bold"),
        text_color="lime"
    ).pack(pady=45)

    if debt <= 0:

        ctk.CTkLabel(
            content_frame,
            text="✅ У тебе немає боргу!",
            font=("Arial", 25),
            text_color="lime"
        ).pack(pady=50)

        return

    ctk.CTkLabel(
        content_frame,
        text=(
            f"💳 Поточний борг:\n"
            f"{debt:,} 🪙"
        ).replace(",", " "),
        font=("Arial", 28, "bold"),
        text_color="orange"
    ).pack(pady=20)

    ctk.CTkLabel(
        content_frame,
        text=(
            f"🪙 На балансі: "
            f"{chips:,} 🪙"
        ).replace(",", " "),
        font=("Arial", 20)
    ).pack(pady=10)

    ctk.CTkButton(
        content_frame,
        text=f"💰 ПОГАСИТИ {debt:,} 🪙".replace(",", " "),
        width=350,
        height=55,
        font=("Arial", 18, "bold"),
        fg_color="green",
        hover_color="darkgreen",
        command=repay_credit
    ).pack(pady=30)


def repay_credit():

    global chips
    global debt
    global turns_left
    global game_round

    if debt <= 0:
        return

    if chips < debt:

        clear_content()

        ctk.CTkLabel(
            content_frame,
            text="❌ НЕДОСТАТНЬО КРЕДИТІВ",
            font=("Arial", 30, "bold"),
            text_color="red"
        ).pack(pady=100)

        ctk.CTkLabel(
            content_frame,
            text=(
                f"Потрібно: {debt:,} 🪙\n"
                f"Є: {chips:,} 🪙"
            ).replace(",", " "),
            font=("Arial", 22)
        ).pack(pady=20)

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
            amount = int(
                bet.get().replace(" ", "")
            )
        except ValueError:

            result.configure(
                text="❌ Введи число",
                text_color="red"
            )

            return

        if amount <= 0:

            result.configure(
                text="❌ Ставка має бути більше 0",
                text_color="red"
            )

            return

        if amount > chips:

            result.configure(
                text="❌ Недостатньо 🪙",
                text_color="red"
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
                text=f"🎉 ДЖЕКПОТ! +{win:,} 🪙".replace(",", " "),
                text_color="gold"
            )

        elif a == b or b == c or a == c:

            win = amount * 2
            chips += win

            result.configure(
                text=f"🎉 ВИГРАШ! +{win:,} 🪙".replace(",", " "),
                text_color="lime"
            )

        else:

            result.configure(
                text=f"😢 ПРОГРАШ! -{amount:,} 🪙".replace(",", " "),
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
            amount = int(
                bet.get().replace(" ", "")
            )
        except ValueError:

            result.configure(
                text="❌ Введи число",
                text_color="red"
            )

            return

        if amount <= 0 or amount > chips:

            result.configure(
                text="❌ Недостатньо 🪙",
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

        won = False

        if selected == "Червоне":
            won = number in RED

        elif selected == "Чорне":
            won = number in BLACK

        elif selected == "Парне":
            won = (
                number != 0
                and number % 2 == 0
            )

        elif selected == "Непарне":
            won = number % 2 == 1

        if won:

            win = amount * 2
            chips += win

            result.configure(
                text=f"🎉 ВИГРАШ! +{win:,} 🪙".replace(",", " "),
                text_color="lime"
            )

        else:

            result.configure(
                text=f"💀 ПРОГРАШ! -{amount:,} 🪙".replace(",", " "),
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

    update_balance()

    if turns_left <= 0:

        app.after(
            500,
            collector
        )


# ==========================================
# КОЛЕКТОР
# ==========================================

def collector():

    global chips
    global debt
    global turns_left
    global game_round

    penalty = min(chips, 100)

    chips -= penalty

    debt = 0
    turns_left = 0
    game_round += 1

    update_balance()

    win = ctk.CTkToplevel(app)

    win.title("🚨 КОЛЕКТОР")
    win.geometry("500x400")
    win.grab_set()

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
        text=f"💸 Штраф: -{penalty:,} 🪙".replace(",", " "),
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

    ctk.CTkButton(
        content_frame,
        text="🌙 Темна тема",
        width=250,
        command=lambda: ctk.set_appearance_mode("dark")
    ).pack(pady=10)

    ctk.CTkButton(
        content_frame,
        text="☀️ Світла тема",
        width=250,
        command=lambda: ctk.set_appearance_mode("light")
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
    width=230,
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
    font=("Arial", 28, "bold"),
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
# ІНФОРМАЦІЯ В МЕНЮ
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


# ==========================================
# ЗАПУСК
# ==========================================

update_balance()
show_home()

app.mainloop()
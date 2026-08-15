import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("600x700")
chips = 100
spin = False

def update():
    bal.configure(text=f"🪙 {chips}")

def roulette():
    global chips, spin
    if spin: return
    try: bet = int(bet_in.get())
    except: return msg.configure(text="Введи ставку")

    if bet <= 0 or bet > chips:
        return msg.configure(text="Недостатньо фішок")

    chips -= bet
    update()
    spin = True
    n = random.randint(0, 36)
    animate(0, n, bet)

def animate(i, n, bet):
    global spin, chips

    if i < 25:
        wheel.configure(text=f"🎡 {random.randint(0,36)}")
        app.after(50, animate, i + 1, n, bet)
        return

    wheel.configure(text=f"🎡 {n}")
    choice = pick.get()
    win = (
        choice == "Червоне" and n != 0 and n % 2 == 1 or
        choice == "Чорне" and n != 0 and n % 2 == 0 or
        choice == "Парне" and n != 0 and n % 2 == 0 or
        choice == "Непарне" and n % 2 == 1
    )

    if choice == "Число":
        try: win = int(num_in.get()) == n
        except: win = False

    if win:
        x = 36 if choice == "Число" else 2
        chips += bet * x
        msg.configure(text=f"🎉 Виграш +{bet*x} 🪙", text_color="lime")
    else:
        msg.configure(text=f"😢 Випало {n}", text_color="red")

    update()
    spin = False

def deposit():
    w = ctk.CTkToplevel(app)
    w.title("Поповнення")
    w.geometry("350x400")

    ctk.CTkLabel(w, text="💳 Поповнення", font=("Arial", 24)).pack(pady=20)

    card = ctk.CTkEntry(w, placeholder_text="Тестовий номер")
    card.pack(pady=7)

    cvv = ctk.CTkEntry(w, placeholder_text="Тестовий код", show="*")
    cvv.pack(pady=7)

    p = ctk.StringVar(value="50 грн → 20 🪙")
    ctk.CTkOptionMenu(
        w, variable=p,
        values=["50 грн → 20 🪙", "100 грн → 45 🪙",
                "200 грн → 100 🪙", "500 грн → 300 🪙"]
    ).pack(pady=15)

    def add():
        global chips
        if not card.get() or not cvv.get(): return
        chips += int(p.get().split("→")[1].split()[0])
        update()
        ctk.CTkLabel(w, text="✅ Фішки додано!", text_color="lime").pack()

    ctk.CTkButton(w, text="🪙 ПОПОВНИТИ", command=add).pack(pady=10)


ctk.CTkLabel(
    app, text="🎡 РУЛЕТКА",
    font=("Arial", 36, "bold")
).pack(pady=20)

ctk.CTkButton(
    app, text="🪙 ПОПОВНИТИ ФІШКИ",
    command=deposit
).pack()

bal = ctk.CTkLabel(app, text=f"🪙 {chips}", font=("Arial", 25))
bal.pack(pady=15)

wheel = ctk.CTkLabel(app, text="🎡", font=("Arial", 60))
wheel.pack(pady=20)

bet_in = ctk.CTkEntry(app, placeholder_text="Ставка")
bet_in.pack(pady=5)

pick = ctk.CTkOptionMenu(
    app,
    values=["Червоне", "Чорне", "Парне", "Непарне", "Число"]
)
pick.pack(pady=5)

num_in = ctk.CTkEntry(app, placeholder_text="Число 0-36")
num_in.pack(pady=5)

ctk.CTkButton(
    app, text="🎡 КРУТИТИ",
    width=250, height=50,
    command=roulette
).pack(pady=15)

msg = ctk.CTkLabel(app, text="Зроби ставку", font=("Arial", 18))
msg.pack()

app.mainloop()
import customtkinter as ctk
from PIL import Image
import webbrowser
import json
import os

# ================= APP SETTINGS =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SAFAR – Mumbai Transport")
app.geometry("430x660")
app.resizable(False, False)

current_frame = None
FAV_FILE = "favorites.json"

# ================= BASIC FUNCTIONS =================
def show(frame):
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = frame
    frame.pack(fill="both", expand=True)

def load_favorites():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r") as f:
            return json.load(f)
    return []

def save_favorites(data):
    with open(FAV_FILE, "w") as f:
        json.dump(data, f)

favorites = load_favorites()

# ================= TOP BAR =================
def top_bar(parent, title, back=None):
    bar = ctk.CTkFrame(parent, height=60, fg_color="#0b132b")
    bar.pack(fill="x")

    if back:
        ctk.CTkButton(
            bar, text="⬅",
            width=40, height=35,
            fg_color="#1c2541",
            command=back
        ).pack(side="left", padx=10, pady=12)

    ctk.CTkLabel(
        bar, text=title,
        font=("Arial", 18, "bold"),
        text_color="#eaeaea"
    ).pack(pady=16)

# ================= SPLASH =================
def splash():
    frame = ctk.CTkFrame(app)

    bg = ctk.CTkImage(Image.open("train_back image.jpg"), size=(430, 760))
    ctk.CTkLabel(frame, image=bg, text="").place(relwidth=1, relheight=1)

    ctk.CTkLabel(
        frame, text="🚇 SAFAR",
        font=("Arial", 80, "bold"),
        text_color="#0a9ae3"
    ).place(relx=0.5, rely=0.35, anchor="center")

    ctk.CTkLabel(frame, text="Mumbai Train Navigation", font=("Arial", 30)).pack()

    ctk.CTkButton(
        frame, text="Get Started",
        width=290, height=75,
        font=("Arial", 40, "bold"),
        fg_color="#00bbf9",
        hover_color="#0096c7",
        command=home
    ).place(relx=0.5, rely=0.55, anchor="center")

    show(frame)

# ================= HOME =================
def home():
    frame = ctk.CTkFrame(app)
    top_bar(frame, "Mumbai")

    if favorites:
        ctk.CTkLabel(frame, text="⭐ Favorites", font=("Arial", 16, "bold")).pack(pady=5)
        for st in favorites:
            ctk.CTkButton(
                frame, text=f"🚉 {st}",
                fg_color="#ff6b6b",
                command=lambda s=st: station_options(s)
            ).pack(padx=30, pady=4, fill="x")

    buttons = [
        ("🚆 Local", local_lines),
        ("🚇 Metro", metro),
        ("🚄 Express", express),
        ("🗺 Map", open_map)
    ]

    for txt, cmd in buttons:
        ctk.CTkButton(
            frame, text=txt, height=60,
            fg_color="#3a86ff",
            hover_color="#8338ec",
            command=cmd
        ).pack(pady=12, padx=30, fill="x")

    show(frame)

# ================= SHOW STATIONS =================
def show_stations(title, stations, back_func):
    frame = ctk.CTkFrame(app)
    top_bar(frame, title, back_func)

    search_var = ctk.StringVar()

    ctk.CTkEntry(
        frame,
        placeholder_text="Search station...",
        textvariable=search_var
    ).pack(padx=18, pady=10, fill="x")

    buttons = []

    def filter_list(*args):
        text = search_var.get().lower()
        for b in buttons:
            b.pack_forget()
            if text in b.station.lower():
                b.pack(fill="x", padx=18, pady=6)

    search_var.trace_add("write", filter_list)

    for s in stations:
        btn = ctk.CTkButton(
            frame,
            text="🚉 " + s,
            anchor="w",
            fg_color="#1b4965",
            hover_color="#d58505",
            command=lambda st=s: station_options(st)
        )
        btn.station = s
        btn.pack(fill="x", padx=18, pady=6)
        buttons.append(btn)

    show(frame)

# ================= LOCAL =================
def local_lines():
    frame = ctk.CTkFrame(app)
    top_bar(frame, "Local Lines", home)

    data = {
        "Western": ["Churchgate", "Dadar", "Andheri", "Borivali", "Virar"],
        "Central": ["CSMT", "Dadar", "Kurla", "Thane", "Kalyan"],
        "Harbour": ["CSMT", "Wadala", "Kurla", "Vashi", "Panvel"]
    }

    for name, stations in data.items():
        ctk.CTkButton(
            frame, text=name,
            fg_color="#0e3de6",
            hover_color="#022aa0",
            command=lambda s=stations, t=name: show_stations(t, s, local_lines)
        ).pack(pady=8, padx=25, fill="x")

    show(frame)

# ================= METRO =================
def metro():
    frame = ctk.CTkFrame(app)
    top_bar(frame, "Metro", home)

    metro_lines = {
        "Line 1": ["Ghatkopar", "Andheri", "Versova"],
        "Line 2": ["DN Nagar", "Lower Andheri", "CSMT"]
    }

    for name, stations in metro_lines.items():
        ctk.CTkButton(
            frame, text=name,
            fg_color="#ff006e",
            hover_color="#ff5c8d",
            command=lambda s=stations, t=name: show_stations(t, s, metro)
        ).pack(pady=8, padx=25, fill="x")

    show(frame)

# ================= EXPRESS =================
def express():
    frame = ctk.CTkFrame(app)
    top_bar(frame, "Express Trains", home)

    trains = {
        "Rajdhani Express": ["Mumbai", "Surat", "Vadodara", "Delhi"],
        "Shatabdi Express": ["Mumbai", "Vadodara", "Ahmedabad"],
        "Duronto Express": ["Mumbai", "Nagpur", "Delhi"]
    }

    for t, route in trains.items():
        ctk.CTkButton(
            frame, text=t,
            fg_color="#ffbe0b",
            hover_color="#fb5607",
            command=lambda tr=t, r=route: express_info(tr, r)
        ).pack(pady=8, padx=25, fill="x")

    show(frame)

def express_info(name, route):
    frame = ctk.CTkFrame(app)
    top_bar(frame, name, express)

    txt = f"{name}\n\nStops:\n" + "\n".join(f"🚉 {s}" for s in route)
    ctk.CTkLabel(frame, text=txt, font=("Arial", 15), justify="left").pack(pady=20)

    show(frame)

# ================= STATION OPTIONS =================
def station_options(st):
    frame = ctk.CTkFrame(app)
    top_bar(frame, st, home)

    fav_text = "💛 Remove Favorite" if st in favorites else "🤍 Add Favorite"

    def toggle_fav():
        if st in favorites:
            favorites.remove(st)
        else:
            favorites.append(st)
        save_favorites(favorites)
        home()

    options = [
        (fav_text, toggle_fav),
        ("📍 Station Info", lambda: station_info(st)),
        ("➡️ Go From Here", lambda: route_from(st)),
        ("⬅️ Go To Here", lambda: route_to(st)),
        ("⏱ Next Train", lambda: next_train(st))
    ]

    for txt, cmd in options:
        ctk.CTkButton(
            frame, text=txt,
            fg_color="#4ea8de",
            hover_color="#5390d9",
            height=55,
            command=cmd
        ).pack(padx=30, pady=8, fill="x")

    show(frame)

# ================= STATION INFO =================
def station_info(st):
    frame = ctk.CTkFrame(app)
    top_bar(frame, f"{st} Info", lambda: station_options(st))

    info = f"""{st} Station

🚻 Washroom
🅿️ Parking
♿ Accessible
🛒 Shops
🚪 Lift
"""
    ctk.CTkLabel(frame, text=info, font=("Arial", 15), justify="left").pack(pady=20)
    show(frame)

def next_train(st):
    frame = ctk.CTkFrame(app)
    top_bar(frame, "Next Trains", lambda: station_options(st))

    for t in ["5 min", "12 min", "20 min"]:
        ctk.CTkLabel(frame, text=f"🚆 Train in {t}", font=("Arial", 15)).pack(pady=10)

    show(frame)

# ================= MAP =================
def route_from(st):
    webbrowser.open(f"https://www.google.com/maps/search/{st}+station")

def route_to(st):
    webbrowser.open(f"https://www.google.com/maps/dir//{st}+station")

def open_map():
    webbrowser.open("https://www.google.com/maps/@19.0760,72.8777,12z")

# ================= START =================
splash()
app.mainloop()

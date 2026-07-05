"""
TripGenie - Premium Travel Booking GUI
Built with Python Tkinter
Author: (Connect to your existing backend/MySQL later)

STRUCTURE:
- App class: Root window, sidebar, page container
- Each page is a Frame subclass
- Sidebar navigation switches between pages
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import random


import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="Harman@03",
    database="TripGenie"
)

# ─────────────────────────────────────────────
#  COLOUR & STYLE TOKENS
# ─────────────────────────────────────────────
COLORS = {
    # Sidebar
    "sidebar_bg":    "#1A1A2E",
    "sidebar_hover": "#16213E",
    "sidebar_active":"#45B2E9",
    "sidebar_text":  "#A8B2D8",
    "sidebar_text_active": "#FFFFFF",

    # Main background
    "bg_main":       "#0F3460",
    "bg_card":       "#16213E",
    "bg_card2":      "#1A1A2E",
    "bg_input":      "#1E2A4A",

    # Accent / CTA
    "accent":        "#459FE9",
    "accent2":       "#F5A623",
    "accent3":       "#4ECDC4",
    "success":       "#2ECC71",
    "warning":       "#F39C12",

    # Text
    "text_primary":  "#FFFFFF",
    "text_secondary":"#A8B2D8",
    "text_muted":    "#6B7DB3",

    # Gradient substitute (top banner)
    "banner_top":    "#1B25B0",
    "banner_bottom": "#0F3460",
}

FONTS = {
    "title":    ("Segoe UI", 100, "bold"),
    "subtitle": ("Segoe UI", 26, "bold"),
    "heading":  ("Segoe UI", 20, "bold"),
    "body":     ("Segoe UI", 15),
    "body_sm":  ("Segoe UI", 15),
    "nav":      ("Segoe UI", 14, "bold"),
    "hero":     ("Segoe UI", 32, "bold"),
    "badge":    ("Segoe UI", 15, "bold"),
    "big":      ("Segoe UI", 22, "bold"),
    "mono":     ("Courier New", 11),
}

# Sidebar nav items: (label, icon_emoji, page_key)
NAV_ITEMS = [
    ("🏠  Home",              "home"),
    ("👤  Customer Login",    "login"),
    ("🌍  Region Selection",  "region"),
    ("📍  Destinations",      "destination"),
    ("🏨  Hotel Booking",     "hotel"),
    ("🚌  Transport",         "transport"),
    ("🧾  Bill Summary",      "bill"),
    ("💬  Feedback",          "feedback"),
    ("❓  Help & Support",    "help"),
    ("🔐  Owner Login",       "owner"),
    ("📊  Dashboard",         "dashboard"),
]


# ─────────────────────────────────────────────
#  HELPER WIDGETS
# ─────────────────────────────────────────────

def make_card(parent, **kwargs):
    """Return a styled 'card' frame."""
    defaults = dict(bg=COLORS["bg_card"], relief="flat", bd=0,
                    padx=20, pady=20)
    defaults.update(kwargs)
    return tk.Frame(parent, **defaults)


def label(parent, text, style="body", fg=None, bg=None, **kwargs):
    """Shorthand for a styled Label."""
    return tk.Label(
        parent,
        text=text,
        font=FONTS.get(style, FONTS["body"]),
        fg=fg or COLORS["text_primary"],
        bg=bg or COLORS["bg_card"],
        **kwargs
    )


def entry_field(parent, placeholder="", width=30):
    """Styled entry with placeholder behaviour."""
    e = tk.Entry(
        parent,
        font=FONTS["body"],
        fg=COLORS["text_secondary"],
        bg=COLORS["bg_input"],
        insertbackground=COLORS["text_primary"],
        relief="flat",
        bd=0,
        width=width,
    )
    e.insert(0, placeholder)

    def on_focus_in(event):
        if e.get() == placeholder:
            e.delete(0, tk.END)
            e.config(fg=COLORS["text_primary"])

    def on_focus_out(event):
        if e.get() == "":
            e.insert(0, placeholder)
            e.config(fg=COLORS["text_secondary"])

    e.bind("<FocusIn>", on_focus_in)
    e.bind("<FocusOut>", on_focus_out)
    return e


def accent_button(parent, text, command=None, color=None, width=18):
    """Pill-shaped accent button."""
    c = color or COLORS["accent"]
    btn = tk.Button(
        parent,
        text=text,
        font=FONTS["heading"],
        fg="#FFFFFF",
        bg=c,
        activebackground=COLORS["bg_card2"],
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        width=width,
        command=command,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["bg_card2"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=c))
    return btn


def section_title(parent, text, bg=None):
    """Big section title with accent underline stripe."""
    bg = bg or COLORS["bg_main"]
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=text, font=FONTS["subtitle"],
             fg=COLORS["text_primary"], bg=bg).pack(anchor="w")
    tk.Frame(f, bg=COLORS["accent"], height=3, width=60).pack(anchor="w", pady=(2, 0))
    return f


def scrollable_frame(parent, bg=None):
    """Returns (outer_frame, inner_canvas_frame) for scrollable content."""
    bg = bg or COLORS["bg_main"]
    outer = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(outer, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    return outer, inner


# ─────────────────────────────────────────────
#  SHARED APP STATE  (connect to your backend)
# ─────────────────────────────────────────────
class AppState:
    def __init__(self, root):
        self.customer_name = tk.StringVar(root)
        self.customer_phone = tk.StringVar(root)
        self.customer_email = tk.StringVar(root)
        self.customer_city = tk.StringVar(root)

        self.selected_region = tk.StringVar(root)
        self.selected_place = tk.StringVar(root)
        self.selected_hotel = tk.StringVar(root)

        self.hotel_fare = tk.DoubleVar(root, value=0)
        self.selected_transport = tk.StringVar(root)
        self.transport_fare = tk.DoubleVar(root, value=0)

        self.members = tk.IntVar(root, value=1)


# ─────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────
class HomePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        # ── Hero Banner ──
        hero = tk.Frame(self, bg=COLORS["accent"], padx=40, pady=40)
        hero.pack(fill="x")

        tk.Label(hero, text="✈️  TripGenie",
                 font=FONTS["hero"], fg="#FFFFFF", bg=COLORS["accent"]).pack(anchor="w")
        tk.Label(hero, text="Your Smart Travel Companion  🌍",
                 font=FONTS["subtitle"], fg="#FFEEF2", bg=COLORS["accent"]).pack(anchor="w")
        tk.Label(hero, text="Book destinations, hotels & transport — all in one place.",
                 font=FONTS["body"], fg="#FFEEF2", bg=COLORS["accent"]).pack(anchor="w", pady=(6, 0))

        accent_button(hero, "  Book Now  →",
                      command=lambda: self.app.show_page("login"),
                      color="#1A1A2E", width=14).pack(anchor="w", pady=(20, 0))

        # ── Stats Strip ──
        stats_bar = tk.Frame(self, bg=COLORS["bg_card2"], pady=16)
        stats_bar.pack(fill="x")
        stats = [("20+", "Destinations"), ("5", "Room Types"),
                 ("3", "Transport Modes"), ("1000+", "Happy Travellers")]
        for i, (num, desc) in enumerate(stats):
            col = tk.Frame(stats_bar, bg=COLORS["bg_card2"])
            col.pack(side="left", expand=True)
            tk.Label(col, text=num, font=FONTS["big"],
                     fg=COLORS["accent2"], bg=COLORS["bg_card2"]).pack()
            tk.Label(col, text=desc, font=FONTS["body_sm"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card2"]).pack()
            if i < len(stats)-1:
                tk.Frame(stats_bar, bg=COLORS["text_muted"],
                         width=1).pack(side="left", fill="y", padx=10)

        # ── Featured Destinations ──
        body_outer, body = scrollable_frame(self)
        body_outer.pack(fill="both", expand=True, padx=30, pady=20)

        section_title(body, "🔥  Featured Destinations", bg=COLORS["bg_main"]).pack(
            anchor="w", pady=(0, 12))

        destinations = [
            ("🏔️ Manali", "Himachal Pradesh", "From ₹8,500", "#4ECDC4"),
            ("🌊 Goa", "West India", "From ₹6,200", "#E94560"),
            ("🏯 Udaipur", "Rajasthan", "From ₹7,800", "#F5A623"),
            ("🍃 Munnar", "Kerala", "From ₹7,100", "#2ECC71"),
            ("🗻 Darjeeling", "West Bengal", "From ₹5,900", "#9B59B6"),
            ("🏖️ Puri", "Odisha", "From ₹5,400", "#E67E22"),
        ]

        row_f = None
        for idx, (name, region, price, col) in enumerate(destinations):
            if idx % 3 == 0:
                row_f = tk.Frame(body, bg=COLORS["bg_main"])
                row_f.pack(fill="x", pady=6)
            card = make_card(row_f, bg=COLORS["bg_card"], padx=100, pady=40)
            card.pack(side="left", expand=True, fill="both", padx=6)

            tk.Label(card, text=name, font=FONTS["heading"],
                     fg=col, bg=COLORS["bg_card"]).pack(anchor="w")
            tk.Label(card, text=region, font=FONTS["body_sm"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(anchor="w")
            tk.Label(card, text=price, font=("Segoe UI", 12, "bold"),
                     fg=COLORS["accent2"], bg=COLORS["bg_card"]).pack(anchor="w", pady=(8, 0))

            accent_button(card, "Explore →",
                          command=lambda: self.app.show_page("destination"),
                          color=col, width=10).pack(anchor="w", pady=(8, 0))

        # ── Why TripGenie ──
        tk.Frame(body, bg=COLORS["text_muted"], height=1).pack(
            fill="x", pady=20)
        section_title(body, "💡  Why TripGenie?", bg=COLORS["bg_main"]).pack(
            anchor="w", pady=(0, 12))

        reasons = [
            ("🔒", "Secure Booking", "Your data is always safe with us."),
            ("💰", "Best Prices", "Guaranteed lowest fares every season."),
            ("📞", "24/7 Support", "We're always here when you need us."),
        ]
        reason_row = tk.Frame(body, bg=COLORS["bg_main"])
        reason_row.pack(fill="x")
        for icon, title, desc in reasons:
            rf = make_card(reason_row, bg=COLORS["bg_card2"], padx=20, pady=20)
            rf.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(rf, text=icon, font=("Segoe UI", 28),
                     bg=COLORS["bg_card2"]).pack()
            tk.Label(rf, text=title, font=FONTS["heading"],
                     fg=COLORS["accent3"], bg=COLORS["bg_card2"]).pack(pady=(4, 0))
            tk.Label(rf, text=desc, font=FONTS["body_sm"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card2"],
                     wraplength=180, justify="center").pack()


# ─────────────────────────────────────────────
#  PAGE: CUSTOMER LOGIN
# ─────────────────────────────────────────────
class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        # Banner
        tk.Frame(self, bg=COLORS["accent"], height=8).pack(fill="x")

        center = tk.Frame(self, bg=COLORS["bg_main"])
        center.pack(expand=True, fill="both", padx=60, pady=30)

        section_title(center, "👤  Customer Login", bg=COLORS["bg_main"]).pack(
            anchor="w", pady=(0, 4))
        tk.Label(center, text="Fill in your details to start booking.",
                 font=FONTS["body"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_main"]).pack(anchor="w", pady=(0, 24))

        card = make_card(center, bg=COLORS["bg_card"], padx=40, pady=36)
        card.pack(fill="x")

        # Form grid
        fields = [
            ("Full Name", self.app.state.customer_name, "e.g. Harmandeep Kaur"),
            ("Phone Number", self.app.state.customer_phone, "e.g. 9876543210"),
            ("Email", self.app.state.customer_email, "e.g. abc@gmail.com"),
            ("City", self.app.state.customer_city, "e.g. Ambala"),
        ]
        for row_idx, (lbl_text, var, hint) in enumerate(fields):
            row = tk.Frame(card, bg=COLORS["bg_card"])
            row.pack(fill="x", pady=10)

            tk.Label(row, text=lbl_text, font=FONTS["heading"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                     width=16, anchor="w").pack(side="left")

            wrapper = tk.Frame(row, bg=COLORS["bg_input"], pady=2, padx=6)
            wrapper.pack(side="left", fill="x", expand=True)

            e = tk.Entry(wrapper, textvariable=var,
                         font=FONTS["body"],
                         fg=COLORS["text_primary"],
                         bg=COLORS["bg_input"],
                         insertbackground=COLORS["text_primary"],
                         relief="flat", bd=0, width=36)
            e.pack(fill="x")

            tk.Label(row, text=hint, font=FONTS["body_sm"],
                     fg=COLORS["text_muted"], bg=COLORS["bg_card"]).pack(
                side="left", padx=(10, 0))

        # Members spinner
        mem_row = tk.Frame(card, bg=COLORS["bg_card"])
        mem_row.pack(fill="x", pady=10)
        tk.Label(mem_row, text="No. of Members", font=FONTS["heading"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                 width=16, anchor="w").pack(side="left")

        spin_wrapper = tk.Frame(mem_row, bg=COLORS["bg_input"], pady=2, padx=6)
        spin_wrapper.pack(side="left")
        tk.Spinbox(spin_wrapper, from_=1, to=20,textvariable=self.app.state.members,
                   font=FONTS["body"], fg=COLORS["text_primary"],
                   bg=COLORS["bg_input"], buttonbackground=COLORS["bg_card2"],
                   relief="flat", width=6).pack()

        # Buttons
        btn_row = tk.Frame(card, bg=COLORS["bg_card"])
        btn_row.pack(pady=(24, 0))
        

        accent_button(btn_row, "Save & Continue →",
                      command=self._save,
                      color=COLORS["accent"], width=18).pack(side="left", padx=8)
        accent_button(btn_row, "Clear Form",
                      command=self._clear,
                      color=COLORS["text_muted"], width=12).pack(side="left", padx=8)
        
    def _clear(self):
        self.app.state.customer_name.set("")
        self.app.state.customer_phone.set("")
        self.app.state.customer_email.set("")
        self.app.state.customer_city.set("")
        self.app.state.members.set(1)

    def _save(self):
        try:
            name = self.app.state.customer_name.get().strip()
            phone = self.app.state.customer_phone.get().strip()
            email = self.app.state.customer_email.get().strip()
            city = self.app.state.customer_city.get().strip()

        # ── VALIDATION ──
            if not name or not phone or not email or not city:
                messagebox.showwarning("Missing Info", "Please fill all fields.")
                return

            if "@" not in email:
                messagebox.showwarning("Invalid Email", "Email must contain @")
                return

        # ── INSERT BOOKING ──
            self.app.cursor.execute("""
                INSERT INTO bookings (name, phone, email, city, booking_type, booking_number)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, phone, email, city, "GENERAL", 1))

            db.commit()

            self.app.cursor.execute("SELECT MAX(id) FROM bookings")
            booking_id = self.app.cursor.fetchone()[0]

        # 🔥 SAFE BOOKING ID FETCH (100% WORKING)
            self.app.cursor.execute("SELECT MAX(id) FROM bookings")
            booking_id = self.app.cursor.fetchone()[0]

            self.app.state.booking_id = booking_id

            print("DEBUG booking_id SET =", booking_id)

            messagebox.showinfo(
                "Saved",
                f"Customer saved successfully!\nBooking ID: {booking_id}"
            )

            self.app.show_page("region")

        except Exception as e:
            messagebox.showerror("DB Error", str(e))

# ─────────────────────────────────────────────
#  PAGE: REGION SELECTION
# ─────────────────────────────────────────────
class RegionPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, bg=COLORS["accent3"], height=8).pack(fill="x")

        top = tk.Frame(self, bg=COLORS["bg_main"], padx=40, pady=24)
        top.pack(fill="x")
        section_title(top, "🗺️  Select Your Region", bg=COLORS["bg_main"]).pack(anchor="w")
        tk.Label(top, text="Choose the part of India you want to explore.",
                 font=FONTS["body"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_main"]).pack(anchor="w", pady=(4, 0))

        regions = [
            ("🏔️  North India", "north", "#4ECDC4",
             "Amritsar · Shimla · Manali\nDharamshala · Srinagar"),
            ("🌴  South India", "south", "#E94560",
             "Ooty · Munnar · Coorg\nMysore · Kodaikanal"),
            ("🐅  East India", "east", "#F5A623",
             "Darjeeling · Gangtok · Puri\nShillong · Kaziranga"),
            ("🏜️  West India", "west", "#9B59B6",
             "Goa · Udaipur · Jaisalmer\nMount Abu · Mumbai"),
        ]

        grid = tk.Frame(self, bg=COLORS["bg_main"], padx=40)
        grid.pack(fill="both", expand=True, pady=10)

        for i, (name, key, color, desc) in enumerate(regions):
            card = make_card(grid, bg=COLORS["bg_card"], padx=28, pady=28)
            card.grid(row=i//2, column=i%2, padx=14, pady=14, sticky="nsew")
            grid.columnconfigure(i%2, weight=1)
            grid.rowconfigure(i//2, weight=1)

            tk.Label(card, text=name, font=("Segoe UI", 18, "bold"),
                     fg=color, bg=COLORS["bg_card"]).pack(anchor="w")
            tk.Label(card, text=desc, font=FONTS["body"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                     justify="left").pack(anchor="w", pady=(10, 16))

            def select(k=key, n=name, c=color):
                self.app.state.selected_region.set(n)
                messagebox.showinfo("Region Selected", f"You selected {n}!")
                self.app.show_page("destination")

            accent_button(card, "Select Region →", command=select,
                          color=color, width=16).pack(anchor="w")


# ─────────────────────────────────────────────
#  PAGE: DESTINATION SELECTION
# ─────────────────────────────────────────────
class DestinationPage(tk.Frame):
    PLACES = {
        "North": [("Amritsar","✨"), ("Shimla","❄️"), ("Dharamshala","🏔️"),
                  ("Manali","🏕️"), ("Srinagar","🌸")],
        "South": [("Ooty","🍵"), ("Munnar","🌿"), ("Coorg","☕"),
                  ("Mysore","🏯"), ("Kodaikanal","🌄")],
        "East":  [("Darjeeling","🍃"), ("Gangtok","🎋"), ("Puri","🌊"),
                  ("Shillong","🌧️"), ("Kaziranga","🦏")],
        "West":  [("Goa","🏖️"), ("Udaipur","💎"), ("Jaisalmer","🐪"),
                  ("Mount Abu","🌅"), ("Mumbai","🌆")],
    }

    COLORS_MAP = ["#4ECDC4","#E94560","#F5A623","#2ECC71","#9B59B6"]

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, bg=COLORS["accent2"], height=8).pack(fill="x")

        top = tk.Frame(self, bg=COLORS["bg_main"], padx=40, pady=20)
        top.pack(fill="x")

        section_title(top, "📍 Choose Your Destination",
                      bg=COLORS["bg_main"]).pack(anchor="w")

        tk.Label(
            top,
            text="20 handpicked destinations across India.",
            font=FONTS["body"],
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_main"]
        ).pack(anchor="w", pady=(4, 0))

        outer, inner = scrollable_frame(self)
        outer.pack(fill="both", expand=True, padx=40, pady=10)

        for region, places in self.PLACES.items():

            grp_label = tk.Frame(inner, bg=COLORS["bg_main"])
            grp_label.pack(fill="x", pady=(16, 4))

            tk.Label(
                grp_label,
                text=f"── {region} India",
                font=FONTS["heading"],
                fg=COLORS["text_muted"],
                bg=COLORS["bg_main"]
            ).pack(anchor="w", padx=6)

            row_f = tk.Frame(inner, bg=COLORS["bg_main"])
            row_f.pack(fill="x", pady=4)

            for idx, (place, emoji) in enumerate(places):

                col = self.COLORS_MAP[idx % len(self.COLORS_MAP)]

                card = make_card(row_f, bg=COLORS["bg_card"], padx=16, pady=16)
                card.pack(side="left", expand=True, fill="both", padx=6)

                tk.Label(card, text=emoji, font=("Segoe UI", 28),
                         bg=COLORS["bg_card"]).pack()

                tk.Label(card, text=place, font=FONTS["heading"],
                         fg=col, bg=COLORS["bg_card"]).pack(pady=(4, 0))

                tk.Label(card, text=f"{region} India",
                         font=FONTS["body_sm"],
                         fg=COLORS["text_muted"],
                         bg=COLORS["bg_card"]).pack()

                # ⭐ IMPORTANT FIX: BUTTON INSIDE LOOP
                def book(p=place):

                    try:
                        if not self.app.state.booking_id:
                            messagebox.showerror(
                                "Error",
                                "Booking ID missing. Please login first."
                            )
                            return

                        self.app.state.selected_place.set(p)

                        self.app.cursor.execute("""
                            INSERT INTO place_booking
                            (booking_id, place_name, place_fare)
                            VALUES (%s, %s, %s)
                        """, (
                            self.app.state.booking_id,
                            p,
                            0
                        ))

                        db.commit()

                        messagebox.showinfo(
                            "Success",
                            f"{p} selected successfully!"
                        )

                        self.app.show_page("hotel")

                    except Exception as e:
                        messagebox.showerror("DB Error", str(e))

                accent_button(
                    card,
                    "Select →",
                    command=book,
                    color=col,
                    width=10
                ).pack(pady=(10, 0))
# ─────────────────────────────────────────────
#  PAGE: HOTEL BOOKING
# ─────────────────────────────────────────────
class HotelPage(tk.Frame):
    ROOMS = [
        ("Family Room", "👨‍👩‍👧‍👦", 2500, "#4ECDC4",
         "Spacious room for families up to 6 guests. Twin + double beds."),
        ("Couple Room", "❤️", 2200, "#E94560",
         "Romantic setup with king bed, mood lighting & breakfast."),
        ("Single Room", "🧳", 1800, "#F5A623",
         "Compact yet cozy. Perfect for solo travellers."),
        ("AC Premium Room", "⭐", 3000, "#9B59B6",
         "Premium AC suite with city view & complimentary spa."),
        ("Non-AC Room", "🌿", 2000, "#2ECC71",
         "Budget-friendly eco room with natural ventilation."),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, bg=COLORS["accent"], height=8).pack(fill="x")

        top = tk.Frame(self, bg=COLORS["bg_main"], padx=40, pady=20)
        top.pack(fill="x")

        section_title(top, "🏨  Hotel Booking", bg=COLORS["bg_main"]).pack(anchor="w")

        self.dest_lbl = tk.Label(
            top,
            text=f"Destination: {self.app.state.selected_place.get() or '—'}",
            font=FONTS["body"],
            fg=COLORS["accent2"],
            bg=COLORS["bg_main"]
        )
        self.dest_lbl.pack(anchor="w", pady=(4, 0))

        outer, inner = scrollable_frame(self)
        outer.pack(fill="both", expand=True, padx=30, pady=10)

        for name, emoji, fare, color, desc in self.ROOMS:
            card = make_card(inner, bg=COLORS["bg_card"], padx=20, pady=18)
            card.pack(fill="x", pady=8)

            left = tk.Frame(card, bg=COLORS["bg_card"])
            left.pack(side="left", fill="both", expand=True)

            tk.Label(left, text=f"{emoji}  {name}",
                     font=("Segoe UI", 14, "bold"),
                     fg=color, bg=COLORS["bg_card"]).pack(anchor="w")

            tk.Label(left, text=desc,
                     font=FONTS["body"],
                     fg=COLORS["text_secondary"],
                     bg=COLORS["bg_card"],
                     wraplength=400,
                     justify="left").pack(anchor="w", pady=(4, 0))

            right = tk.Frame(card, bg=COLORS["bg_card"])
            right.pack(side="right", padx=12)

            tk.Label(right, text=f"₹{fare:,}/night",
                     font=FONTS["big"],
                     fg=COLORS["accent2"],
                     bg=COLORS["bg_card"]).pack()

            tk.Label(right, text="per person",
                     font=FONTS["body_sm"],
                     fg=COLORS["text_muted"],
                     bg=COLORS["bg_card"]).pack()

            # ✅ IMPORTANT: button inside loop
            def select(n=name, f=fare):
                try:
                    members = self.app.state.members.get()
                    total = f * members

                    self.app.state.selected_hotel.set(n)
                    self.app.state.hotel_fare.set(total)

                    self.app.cursor.execute("""
                    INSERT INTO hotel_booking (booking_id,customer_name, room_type, room_fare)
                    VALUES (%s, %s, %s,%s)
                    """, (
                        self.app.state.booking_id,
                        name,
                        n,
                        total
                    ))

                    db.commit()

                    messagebox.showinfo(
                        "🏨 Room Selected",
                        f"{n} booked successfully!\nTotal: ₹{total}"
                    )

                    self.app.show_page("transport")

                except Exception as e:
                    messagebox.showerror("DB Error", str(e))

            accent_button(
                right,
                "Select Room",
                command=select,
                color=color,
                width=12
            ).pack(pady=(8, 0))


# ─────────────────────────────────────────────
#  PAGE: TRANSPORT BOOKING
# ─────────────────────────────────────────────
class TransportPage(tk.Frame):
    MODES = [
        ("🚌  Bus",   "Bus",   800,  "#4ECDC4",
         "Comfortable AC sleeper bus. Departs daily 8 PM."),
        ("🚆  Train", "Train", 600,  "#F5A623",
         "Express rail travel. Rajdhani/Shatabdi available."),
        ("🚕  Cab",   "Cab",   3500, "#E94560",
         "Private cab door-to-door. AC, GPS tracked."),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, bg=COLORS["accent2"], height=8).pack(fill="x")

        top = tk.Frame(self, bg=COLORS["bg_main"], padx=40, pady=24)
        top.pack(fill="x")

        section_title(top, "🚌  Transport Booking", bg=COLORS["bg_main"]).pack(anchor="w")

        tk.Label(
            top,
            text="Select how you'd like to travel to your destination.",
            font=FONTS["body"],
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_main"]
        ).pack(anchor="w", pady=(4, 0))

        body = tk.Frame(self, bg=COLORS["bg_main"], padx=40)
        body.pack(fill="both", expand=True, pady=16)

        for emoji_name, key, fare, color, desc in self.MODES:
            card = make_card(body, bg=COLORS["bg_card"], padx=24, pady=24)
            card.pack(fill="x", pady=10)

            lft = tk.Frame(card, bg=COLORS["bg_card"])
            lft.pack(side="left", fill="both", expand=True)

            tk.Label(
                lft,
                text=emoji_name,
                font=("Segoe UI", 18, "bold"),
                fg=color,
                bg=COLORS["bg_card"]
            ).pack(anchor="w")

            tk.Label(
                lft,
                text=desc,
                font=FONTS["body"],
                fg=COLORS["text_secondary"],
                bg=COLORS["bg_card"]
            ).pack(anchor="w", pady=(6, 0))

            rgt = tk.Frame(card, bg=COLORS["bg_card"])
            rgt.pack(side="right")

            members = self.app.state.members.get()
            total = fare * members

            tk.Label(
                rgt,
                text=f"₹{fare}/person",
                font=FONTS["heading"],
                fg=COLORS["text_secondary"],
                bg=COLORS["bg_card"]
            ).pack()

            tk.Label(
                rgt,
                text=f"₹{total:,} total",
                font=FONTS["big"],
                fg=COLORS["accent2"],
                bg=COLORS["bg_card"]
            ).pack()

            # ✅ FIXED: proper closure + safe DB handling
            def choose(mode=key, fare_per_person=fare):
                try:
                    members = self.app.state.members.get()
                    total = fare_per_person * members

                    name = self.app.state.customer_name.get()

                    if not name:
                        messagebox.showwarning("Missing", "Please enter customer details first.")
                        return

                    self.app.state.selected_transport.set(mode)
                    self.app.state.transport_fare.set(total)

                    self.app.cursor.execute("""
                        INSERT INTO transport_booking (booking_id,customer_name, transport_type, transport_fare)
                        VALUES (%s, %s, %s,%s)
                    """, (
                        self.app.state.booking_id,
                        name,
                        mode,
                        total
                    ))

                    db.commit()

                    messagebox.showinfo(
                        "🚌 Transport Booked",
                        f"{mode} selected successfully!\nTotal: ₹{total}"
                    )

                    self.app.show_page("bill")

                except Exception as e:
                    messagebox.showerror("DB Error", str(e))

            accent_button(
                rgt,
                "Book Now →",
                command=choose,
                color=color,
                width=12
            ).pack(pady=(8, 0))


# ─────────────────────────────────────────────
#  PAGE: BILL SUMMARY
# ─────────────────────────────────────────────
class BillPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, bg=COLORS["success"], height=8).pack(fill="x")

        top = tk.Frame(self, bg=COLORS["bg_main"], padx=40, pady=20)
        top.pack(fill="x")
        section_title(top, "🧾  Bill Summary", bg=COLORS["bg_main"]).pack(anchor="w")

        body = tk.Frame(self, bg=COLORS["bg_main"], padx=80)
        body.pack(expand=True, fill="both", pady=20)

        # Receipt card
        receipt = make_card(body, bg=COLORS["bg_card"], padx=40, pady=36)
        receipt.pack(fill="x")

        # Header
        tk.Label(receipt, text="TRIPGENIE", font=("Segoe UI", 22, "bold"),
                 fg=COLORS["accent"], bg=COLORS["bg_card"]).pack()
        tk.Label(receipt, text="Official Booking Receipt",
                 font=FONTS["body_sm"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_card"]).pack(pady=(0, 16))

        tk.Frame(receipt, bg=COLORS["text_muted"], height=1).pack(fill="x")

        def bill_row(left, right, bold=False, color=None):
            r = tk.Frame(receipt, bg=COLORS["bg_card"])
            r.pack(fill="x", pady=5)
            fnt = FONTS["heading"] if bold else FONTS["body"]
            clr = color or COLORS["text_primary"]
            tk.Label(r, text=left, font=fnt, fg=COLORS["text_secondary"],
                     bg=COLORS["bg_card"], anchor="w").pack(side="left")
            tk.Label(r, text=right, font=fnt, fg=clr,
                     bg=COLORS["bg_card"], anchor="e").pack(side="right")

        def refresh_bill():
            for w in receipt.winfo_children()[:]:
                w.destroy()

            hotel  = self.app.state.hotel_fare.get()
            trans  = self.app.state.transport_fare.get()
            subtotal = hotel + trans
            gst    = subtotal * 0.18
            final  = subtotal + gst

            bill_row("Customer",    self.app.state.customer_name.get() or "—")
            bill_row("Phone",       self.app.state.customer_phone.get() or "—")
            bill_row("City",        self.app.state.customer_city.get() or "—")
            bill_row("Destination", self.app.state.selected_place.get() or "—")
            bill_row("Members",     str(self.app.state.members.get()))
            bill_row("Room Type",   self.app.state.selected_hotel.get() or "—")
            bill_row("Transport",   self.app.state.selected_transport.get() or "—")

            tk.Frame(receipt, bg=COLORS["text_muted"],
                     height=1).pack(fill="x", pady=8)

            bill_row("Hotel Fare",      f"₹{hotel:,.0f}")
            bill_row("Transport Fare",  f"₹{trans:,.0f}")
            bill_row("Subtotal",        f"₹{subtotal:,.0f}")
            bill_row("GST (18%)",       f"₹{gst:,.0f}", color=COLORS["warning"])

            tk.Frame(receipt, bg=COLORS["accent"],
                     height=2).pack(fill="x", pady=8)

            bill_row("GRAND TOTAL", f"₹{final:,.0f}",
                     bold=True, color=COLORS["accent2"])

            tk.Frame(receipt, bg=COLORS["text_muted"],
                     height=1).pack(fill="x", pady=12)

            thanks = tk.Label(receipt, text="🎉  Thank you for booking with TripGenie!",
                              font=FONTS["heading"], fg=COLORS["accent3"],
                              bg=COLORS["bg_card"])
            thanks.pack(pady=(0, 4))

            btn_row = tk.Frame(receipt, bg=COLORS["bg_card"])
            btn_row.pack(pady=10)
            accent_button(btn_row, "🔄  Refresh Bill",
                          command=refresh_bill,
                          color=COLORS["accent3"], width=14).pack(side="left", padx=6)
            accent_button(btn_row, "🏠  Back to Home",
                          command=lambda: self.app.show_page("home"),
                          color=COLORS["text_muted"], width=14).pack(side="left", padx=6)

        refresh_bill()

        # Auto-refresh when shown
        self.bind("<Visibility>", lambda e: refresh_bill())


# ─────────────────────────────────────────────
#  PAGE: FEEDBACK
# ─────────────────────────────────────────────
class FeedbackPage(tk.Frame):
    SAMPLE_REVIEWS = [
        ("Priya Sharma",    5, "Amazing experience! Manali was breathtaking."),
        ("Rahul Mehta",     4, "Hotel was cosy, transport was on time. Will book again."),
        ("Anika Verma",     5, "TripGenie made everything hassle-free. Loved it!"),
        ("Deepak Kumar",    3, "Good service but could improve cab availability."),
        ("Sneha Reddy",     5, "Goa trip was perfect. Budget-friendly and fun!"),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _stars(self, n):
        return "⭐" * n + "☆" * (5 - n)

    def _build(self):
        tk.Frame(self, bg=COLORS["accent2"], height=8).pack(fill="x")

        outer, inner = scrollable_frame(self)
        outer.pack(fill="both", expand=True, padx=40, pady=20)

        section_title(inner, "💬  Customer Feedback", bg=COLORS["bg_main"]).pack(
            anchor="w", pady=(0, 4))
        tk.Label(inner, text="What our travellers are saying 🌟",
                 font=FONTS["body"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_main"]).pack(anchor="w", pady=(0, 16))

        # Previous reviews
        for name, rating, review in self.SAMPLE_REVIEWS:
            rc = make_card(inner, bg=COLORS["bg_card"], padx=20, pady=16)
            rc.pack(fill="x", pady=6)
            hdr = tk.Frame(rc, bg=COLORS["bg_card"])
            hdr.pack(fill="x")
            tk.Label(hdr, text=name, font=FONTS["heading"],
                     fg=COLORS["accent3"], bg=COLORS["bg_card"]).pack(side="left")
            tk.Label(hdr, text=self._stars(rating), font=FONTS["body"],
                     fg=COLORS["accent2"], bg=COLORS["bg_card"]).pack(side="right")
            tk.Label(rc, text=f'"{review}"', font=FONTS["body"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                     wraplength=600, justify="left").pack(anchor="w", pady=(6, 0))

        # New review form
        tk.Frame(inner, bg=COLORS["text_muted"], height=1).pack(fill="x", pady=20)
        section_title(inner, "✍️  Leave Your Review", bg=COLORS["bg_main"]).pack(
            anchor="w", pady=(0, 12))

        form = make_card(inner, bg=COLORS["bg_card"], padx=30, pady=26)
        form.pack(fill="x")

        name_var = tk.StringVar()
        rating_var = tk.IntVar(value=5)
        review_var = tk.StringVar()

        def field_row(lbl, widget_fn):
            r = tk.Frame(form, bg=COLORS["bg_card"])
            r.pack(fill="x", pady=8)
            tk.Label(r, text=lbl, font=FONTS["heading"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                     width=14, anchor="w").pack(side="left")
            widget_fn(r)

        def name_widget(parent):
            wrapper = tk.Frame(parent, bg=COLORS["bg_input"], pady=2, padx=6)
            wrapper.pack(side="left", fill="x", expand=True)
            tk.Entry(wrapper, textvariable=name_var, font=FONTS["body"],
                     fg=COLORS["text_primary"], bg=COLORS["bg_input"],
                     insertbackground=COLORS["text_primary"],
                     relief="flat", bd=0, width=36).pack(fill="x")

        def rating_widget(parent):
            for i in range(1, 6):
                tk.Radiobutton(parent, text=f"{i}⭐", variable=rating_var, value=i,
                               font=FONTS["body"], fg=COLORS["accent2"],
                               bg=COLORS["bg_card"],
                               activebackground=COLORS["bg_card"],
                               selectcolor=COLORS["bg_input"],
                               relief="flat").pack(side="left", padx=4)

        def review_widget(parent):
            wrapper = tk.Frame(parent, bg=COLORS["bg_input"], pady=4, padx=6)
            wrapper.pack(side="left", fill="x", expand=True)
            t = tk.Text(wrapper, font=FONTS["body"], fg=COLORS["text_primary"],
                        bg=COLORS["bg_input"], insertbackground=COLORS["text_primary"],
                        relief="flat", bd=0, width=40, height=3)
            t.pack(fill="x")
            # Store text widget reference
            form.review_widget = t

        field_row("Your Name", name_widget)
        field_row("Rating", rating_widget)
        field_row("Review", review_widget)

        def submit():
            # Hook to your feedback() function later
            messagebox.showinfo("✅ Thank You!",
                                f"Thanks {name_var.get() or 'Traveller'}!\n"
                                "Your review has been submitted.")
            name_var.set("")
            rating_var.set(5)
            if hasattr(form, "review_widget"):
                form.review_widget.delete("1.0", tk.END)

        accent_button(form, "Submit Review ✅", command=submit,
                      color=COLORS["accent3"], width=18).pack(pady=(16, 0))


# ─────────────────────────────────────────────
#  PAGE: HELP & SUPPORT
# ─────────────────────────────────────────────
class HelpPage(tk.Frame):
    FAQ = [
        ("How do I cancel a booking?",
         "Contact us at tripgenie@gmail.com or call 9876543210. Cancellations are processed within 24 hours."),
        ("Is my payment secure?",
         "Yes! All transactions are encrypted and PCI-DSS compliant."),
        ("Can I change my destination after booking?",
         "Destination changes are allowed up to 48 hours before your travel date."),
        ("Do you offer group discounts?",
         "Groups of 10+ members get a 15% discount automatically."),
        ("How do I contact the driver/hotel?",
         "Contact details are shared via SMS & email after confirmation."),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, bg=COLORS["accent3"], height=8).pack(fill="x")

        outer, inner = scrollable_frame(self)
        outer.pack(fill="both", expand=True, padx=40, pady=20)

        section_title(inner, "❓  Help & Support", bg=COLORS["bg_main"]).pack(
            anchor="w", pady=(0, 4))

        # Contact card
        contact = make_card(inner, bg=COLORS["bg_card2"], padx=30, pady=24)
        contact.pack(fill="x", pady=(12, 0))

        tk.Label(contact, text="📞  Owner: Miss Harmandeep Kaur",
                 font=FONTS["heading"], fg=COLORS["accent2"],
                 bg=COLORS["bg_card2"]).pack(anchor="w")
        tk.Label(contact, text="📱  9876543210      ✉️  tripgenie@gmail.com",
                 font=FONTS["body"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_card2"]).pack(anchor="w", pady=(6, 0))

        # FAQ
        tk.Frame(inner, bg=COLORS["text_muted"], height=1).pack(fill="x", pady=20)
        section_title(inner, "🔍  Frequently Asked Questions",
                       bg=COLORS["bg_main"]).pack(anchor="w", pady=(0, 12))

        for q, a in self.FAQ:
            faq_card = make_card(inner, bg=COLORS["bg_card"], padx=20, pady=14)
            faq_card.pack(fill="x", pady=6)
            tk.Label(faq_card, text=f"Q: {q}", font=FONTS["heading"],
                     fg=COLORS["accent3"], bg=COLORS["bg_card"],
                     anchor="w", wraplength=700, justify="left").pack(anchor="w")
            tk.Label(faq_card, text=f"A: {a}", font=FONTS["body"],
                     fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
                     wraplength=700, justify="left").pack(anchor="w", pady=(4, 0))

        # Complaint form
        tk.Frame(inner, bg=COLORS["text_muted"], height=1).pack(fill="x", pady=20)
        section_title(inner, "📝  Raise a Complaint", bg=COLORS["bg_main"]).pack(
            anchor="w", pady=(0, 12))

        comp_card = make_card(inner, bg=COLORS["bg_card"], padx=30, pady=24)
        comp_card.pack(fill="x")

        wrapper = tk.Frame(comp_card, bg=COLORS["bg_input"], pady=4, padx=6)
        wrapper.pack(fill="x")
        comp_text = tk.Text(wrapper, font=FONTS["body"],
                            fg=COLORS["text_primary"],
                            bg=COLORS["bg_input"],
                            insertbackground=COLORS["text_primary"],
                            relief="flat", bd=0, height=4)
        comp_text.pack(fill="x")

        def submit_comp():
            # Hook to your help_section() complaint logic later
            text = comp_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Empty", "Please write your complaint.")
                return
            messagebox.showinfo("✅ Complaint Submitted",
                                "We'll get back to you within 24 hours.")
            comp_text.delete("1.0", tk.END)

        accent_button(comp_card, "Submit Complaint", command=submit_comp,
                      color=COLORS["accent"], width=18).pack(pady=(16, 0))


# ─────────────────────────────────────────────
#  PAGE: OWNER LOGIN
# ─────────────────────────────────────────────
class OwnerLoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, bg="#6C3483", height=8).pack(fill="x")

        center = tk.Frame(self, bg=COLORS["bg_main"])
        center.pack(expand=True)

        card = make_card(center, bg=COLORS["bg_card"], padx=60, pady=50)
        card.pack(padx=40, pady=40)

        tk.Label(card, text="🔐", font=("Segoe UI", 40),
                 bg=COLORS["bg_card"]).pack()
        tk.Label(card, text="Owner Portal", font=FONTS["subtitle"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(pady=(8, 0))
        tk.Label(card, text="Authorised personnel only.",
                 font=FONTS["body_sm"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_card"]).pack(pady=(2, 24))

        wrapper = tk.Frame(card, bg=COLORS["bg_input"], pady=4, padx=8)
        wrapper.pack(fill="x")
        self.pwd = tk.Entry(wrapper, show="●",
                            font=FONTS["body"],
                            fg=COLORS["text_primary"],
                            bg=COLORS["bg_input"],
                            insertbackground=COLORS["text_primary"],
                            relief="flat", bd=0, width=28)
        self.pwd.pack(fill="x")

        self.err_lbl = tk.Label(card, text="", font=FONTS["body_sm"],
                                fg=COLORS["accent"], bg=COLORS["bg_card"])
        self.err_lbl.pack(pady=(8, 0))

        accent_button(card, "🔓  Login as Owner",
                      command=self._login,
                      color="#6C3483", width=20).pack(pady=(16, 0))

    def _login(self):
        # Hook to your owner_login() function later
        pwd = self.pwd.get()
        if pwd == "Admin123":
            self.app.is_owner = True 
            self.err_lbl.config(text="")
             
            messagebox.showinfo("✅ Access Granted", "Welcome, Owner!")
            self.app.show_page("dashboard")
        else:
            self.err_lbl.config(text="❌ Incorrect password. Try again.")
            self.pwd.delete(0, tk.END)


# ─────────────────────────────────────────────
#  PAGE: CUSTOMER DETAILS DASHBOARD
# ─────────────────────────────────────────────
class DashboardPage(tk.Frame):
    
    def __init__(self, parent, app):
        self.cursor = app.cursor
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app

        self.records = []
        self._load_data()
        self._build()

    def _load_data(self):
        self.cursor.execute("""
        SELECT
            b.id,
            b.name,
            b.phone,
            COALESCE(p.place_name, 'None') AS place_name,
            COALESCE(h.room_type, 'None') AS room_type,
            COALESCE(t.transport_type, 'None') AS transport_type,
            b.city,
            (
                COALESCE(h.room_fare, 0) +
                COALESCE(t.transport_fare, 0) +
                COALESCE(p.place_fare, 0)
            ) AS total_cost
        FROM bookings b
        LEFT JOIN hotel_booking h ON b.id = h.booking_id
        LEFT JOIN transport_booking t ON b.id = t.booking_id
        LEFT JOIN place_booking p ON b.id = p.booking_id
        """)

        self.records = self.cursor.fetchall()
    
    def _calculate_kpis(self):
        total_bookings = len(self.records)

        total_revenue = sum(r[7] or 0 for r in self.records)
        avg_fare = total_revenue / total_bookings if total_bookings else 0

        return total_bookings, total_revenue, avg_fare

    def _build(self):
        tk.Frame(self, bg="#1ABC9C", height=8).pack(fill="x")

        top = tk.Frame(self, bg=COLORS["bg_main"], padx=40, pady=20)
        top.pack(fill="x")

        section_title(top, "📊 Customer Dashboard", bg=COLORS["bg_main"]).pack(anchor="w")

        
        total_bookings, total_revenue, avg_fare = self._calculate_kpis()

        kpis = [
            ("Total Bookings", str(total_bookings), "#4ECDC4"),
            ("Revenue (est.)", f"₹{total_revenue}", "#F5A623"),
            ("Destinations", "20+", "#E94560"),
            ("Avg. Fare", f"₹{round(avg_fare, 2)}", "#2ECC71"),
        ]
        tk.Label(
            top,
            text="All booking records (Owner View)",
            font=FONTS["body"],
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_main"]
        ).pack(anchor="w", pady=(4, 0))

        # KPI Cards
        kpi_row = tk.Frame(self, bg=COLORS["bg_main"], padx=40)
        kpi_row.pack(fill="x", pady=10)

        for title, val, col in kpis:
            kf = make_card(kpi_row, bg=COLORS["bg_card"], padx=20, pady=16)
            kf.pack(side="left", expand=True, fill="both", padx=6)

            tk.Label(kf, text=val, font=FONTS["big"], fg=col,
                     bg=COLORS["bg_card"]).pack()

            tk.Label(kf, text=title, font=FONTS["body_sm"],
                     fg=COLORS["text_secondary"],
                     bg=COLORS["bg_card"]).pack()

        # Table
        outer, inner = scrollable_frame(self)
        outer.pack(fill="both", expand=True, padx=40, pady=10)

        headers = [
            "ID", "Name", "Phone", "Place",
            "Room", "Transport", "City", "Total Cost"
        ]

        widths = [4, 18, 13, 14, 14, 12, 12, 12]

        col_colors = [
            "#A8B2D8", "#4ECDC4", "#A8B2D8", "#F5A623",
            "#E94560", "#9B59B6", "#A8B2D8", "#2ECC71"
        ]

        # Header row
        hdr_row = tk.Frame(inner, bg=COLORS["bg_card2"])
        hdr_row.pack(fill="x")

        for h, w, cc in zip(headers, widths, col_colors):
            tk.Label(
                hdr_row,
                text=h,
                font=FONTS["badge"],
                fg=cc,
                bg=COLORS["bg_card2"],
                width=w,
                anchor="w",
                padx=6,
                pady=8
            ).pack(side="left")

        tk.Frame(inner, bg=COLORS["accent"], height=2).pack(fill="x")

        # Data rows
        for i, row in enumerate(self.records):
            bg = COLORS["bg_card"] if i % 2 == 0 else COLORS["bg_card2"]

            data_row = tk.Frame(inner, bg=bg)
            data_row.pack(fill="x")

            for val, w, cc in zip(row, widths, col_colors):
                tk.Label(
                    data_row,
                    text=str(val),
                    font=FONTS["body_sm"],
                    fg=COLORS["text_primary"],
                    bg=bg,
                    width=w,
                    anchor="w",
                    padx=6,
                    pady=7
                ).pack(side="left")


# ─────────────────────────────────────────────
#  MAIN APP SHELL (Sidebar + Page Container)
# ─────────────────────────────────────────────
class TripGenieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TripGenie — Smart Travel Booking")
        self.root.geometry("1280x800")
        self.state = AppState(self.root)
        self.root.minsize(1100, 700)
        self.root.configure(bg=COLORS["bg_main"])
        self.is_owner = False
        self.cursor = db.cursor()

        self.pages = {}
        self.nav_buttons = {}
        self.current_page = None

        self._build_sidebar()
        self._build_content_area()
        self._register_pages()

        # Show home by default
        self.show_page("home")

    # ── SIDEBAR ──────────────────────────────
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=COLORS["sidebar_bg"],
                                width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=COLORS["sidebar_bg"],
                              pady=28)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="✈️", font=("Segoe UI", 28),
                 bg=COLORS["sidebar_bg"]).pack()
        tk.Label(logo_frame, text="TripGenie", font=("Segoe UI", 18, "bold"),
                 fg="#FFFFFF", bg=COLORS["sidebar_bg"]).pack()
        tk.Label(logo_frame, text="Smart Travel Booking",
                 font=FONTS["body_sm"], fg=COLORS["sidebar_text"],
                 bg=COLORS["sidebar_bg"]).pack()

        tk.Frame(self.sidebar, bg=COLORS["sidebar_active"],
                 height=1).pack(fill="x", padx=20)

        # Nav items
        for label_text, page_key in NAV_ITEMS:
            btn = tk.Button(
                self.sidebar,
                text=label_text,
                font=FONTS["nav"],
                fg=COLORS["sidebar_text"],
                bg=COLORS["sidebar_bg"],
                activebackground=COLORS["sidebar_hover"],
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                padx=24,
                pady=12,
                anchor="w",
                cursor="hand2",
                command=lambda k=page_key: self.show_page(k),
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: (
                b.config(bg=COLORS["sidebar_hover"],
                         fg="#FFFFFF") if b != self._active_btn() else None))
            btn.bind("<Leave>", lambda e, b=btn, k=page_key: (
                b.config(bg=COLORS["sidebar_bg"],
                         fg=COLORS["sidebar_text"])
                if self.current_page != k else None))
            self.nav_buttons[page_key] = btn

        # Footer
        tk.Frame(self.sidebar, bg=COLORS["sidebar_bg"]).pack(expand=True)
        tk.Label(self.sidebar, text="© 2026 TripGenie\nFinal Year Project",
                 font=FONTS["body_sm"], fg=COLORS["text_muted"],
                 bg=COLORS["sidebar_bg"], justify="center").pack(pady=16)

    def _active_btn(self):
        if self.current_page and self.current_page in self.nav_buttons:
            return self.nav_buttons[self.current_page]
        return None

    # ── CONTENT AREA ──────────────────────────
    def _build_content_area(self):
        self.container = tk.Frame(self.root, bg=COLORS["bg_main"])
        self.container.pack(side="right", fill="both", expand=True)

    # ── REGISTER PAGES ────────────────────────
    def _register_pages(self):
        page_classes = {
            "home":        HomePage,
            "login":       LoginPage,
            "region":      RegionPage,
            "destination": DestinationPage,
            "hotel":       HotelPage,
            "transport":   TransportPage,
            "bill":        BillPage,
            "feedback":    FeedbackPage,
            "help":        HelpPage,
            "owner":       OwnerLoginPage,
            "dashboard":   DashboardPage,
        }
        for key, cls in page_classes.items():
            page = cls(self.container, self)
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages[key] = page

    # ── PAGE SWITCHER ─────────────────────────
    def show_page(self, key):
        # Reset all nav buttons
        for k, btn in self.nav_buttons.items():
            btn.config(bg=COLORS["sidebar_bg"],
                       fg=COLORS["sidebar_text"])
        
        if key == "dashboard" and not self.is_owner:
            messagebox.showerror(
            "Access Denied",
            "Only Owner can access Dashboard."
            )
            return

        # Highlight active
        if key in self.nav_buttons:
            self.nav_buttons[key].config(
                bg=COLORS["sidebar_active"],
                fg=COLORS["sidebar_text_active"])

        self.current_page = key

        if key == "dashboard":
            page = self.pages["dashboard"]

         # Latest data DB se load karo
            page._load_data()

        # Purana UI remove karo
            for widget in page.winfo_children():
                widget.destroy()

         # Dashboard dobara build karo
            page._build()

        if key in self.pages:
            self.pages[key].lift()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main():
    root = tk.Tk()

    # Window icon (optional: replace with a real .ico file)
    try:
        root.iconbitmap("tripgenie.ico")
    except Exception:
        pass

    # DPI awareness (Windows)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = TripGenieApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
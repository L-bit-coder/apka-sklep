import customtkinter as ctk
from .views.products import get_products

# WYGLAD APLIKACJI
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# KOLORY
BACKGROUND = "#FFF8F5"
PINK = "#F3C4D0"
DARK_PINK = "#C77D98"
PURPLE = "#DCCFF0"
TEXT = "#51445B"
WHITE = "#FFFFFF"

# GLOWNE OKNO
app = ctk.CTk()
app.title("Crafty Corner")
app.geometry("1100x750")
app.minsize(850, 600)
app.configure(fg_color=BACKGROUND)

# UKLAD OKNA
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, weight=1)


# NAGLOWEK
header = ctk.CTkFrame(app, fg_color=PINK, corner_radius=0, height=85)
header.grid(row=0, column=0, columnspan=2, sticky="ew")
header.grid_columnconfigure(0, weight=1)

logo = ctk.CTkLabel(
    header, text="Crafty Corner", font=("Arial", 30, "bold"), text_color=TEXT
)
logo.grid(row=0, column=0, padx=30, pady=20, sticky="w")

subtitle = ctk.CTkLabel(
    header, text="Handmade with love", font=("Arial", 14, "italic"), text_color=TEXT
)
subtitle.grid(row=0, column=1, padx=30)


# MENU BOCZNE
sidebar = ctk.CTkFrame(app, width=210, fg_color=PURPLE, corner_radius=0)
sidebar.grid(row=1, column=0, sticky="ns")
sidebar.grid_propagate(False)

menu_title = ctk.CTkLabel(
    sidebar, text="MENU", font=("Arial", 20, "bold"), text_color=TEXT
)
menu_title.pack(pady=(30, 20))


menu_items = [
    ("Strona glowna", None),
    ("Wszystkie produkty", None),
    ("Obrazy", "Obrazy"),
    ("Glina", "Glina"),
    ("Druciki kreatywne", "Druciki kreatywne"),
    ("Zestawy DIY", "Zestawy DIY"),
]

for item, category in menu_items:
    button = ctk.CTkButton(
        sidebar,
        text=item,
        font=("Arial", 14),
        text_color=TEXT,
        fg_color="transparent",
        hover_color=PINK,
        anchor="w",
        command=lambda cat=category: show_products(cat),
    )

    button.pack(fill="x", padx=12, pady=8)

# GLOWNA CZESC SKLEPU
content = ctk.CTkFrame(app, fg_color=BACKGROUND)
content.grid(row=1, column=1, sticky="nsew", padx=25, pady=20)

content.grid_columnconfigure(0, weight=1)
content.grid_rowconfigure(1, weight=1)

heading = ctk.CTkLabel(
    content, text="Nasze produkty", font=("Arial", 27, "bold"), text_color=TEXT
)
heading.grid(row=0, column=0, sticky="w", pady=(5, 20))


# RAMKA Z PRODUKTAMI
products_frame = ctk.CTkScrollableFrame(
    content, fg_color=BACKGROUND, scrollbar_button_color=PINK
)
products_frame.grid(row=1, column=0, sticky="nsew")

for i in range(3):
    products_frame.grid_columnconfigure(i, weight=1)


# WYBOR IKONY PRODUKTU
def get_emoji(category):
    if category == "Obrazy":
        return "🎨"
    elif category == "Glina":
        return "🏺"
    elif category == "Druciki kreatywne":
        return "🌸"
    elif category == "Zestawy DIY":
        return "🎁"
    return "✨"


# WYSWIETLANIE PRODUKTOW


def show_products(category=None):

    # Usuwamy poprzednie produkty
    for widget in products_frame.winfo_children():
        widget.destroy()

    # Pobieramy produkty z MySQL
    products = get_products()

    # Filtrowanie kategorii
    if category is not None:
        products = [product for product in products if product["kategoria"] == category]

    # Sprawdzamy, czy znaleziono produkty
    if not products:
        message = ctk.CTkLabel(
            products_frame, text="Brak produktow w tej kategorii.", text_color=TEXT
        )
        message.grid(row=0, column=0, padx=20, pady=20)
        return

    # Wyswietlanie produktow
    for index, product in enumerate(products):

        row = index // 3
        column = index % 3

        card = ctk.CTkFrame(
            products_frame,
            fg_color=WHITE,
            corner_radius=15,
            border_width=1,
            border_color=PINK,
        )

        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        image_placeholder = ctk.CTkFrame(
            card, fg_color="#FFF0F3", height=110, corner_radius=10
        )
        image_placeholder.pack(fill="x", padx=10, pady=(10, 5))
        image_placeholder.pack_propagate(False)

        emoji = ctk.CTkLabel(
            image_placeholder, text=get_emoji(product["kategoria"]), font=("Arial", 45)
        )
        emoji.pack(expand=True)

        name = ctk.CTkLabel(
            card,
            text=product["nazwa"],
            font=("Arial", 16, "bold"),
            text_color=TEXT,
            wraplength=190,
        )
        name.pack(padx=10, pady=5)

        category_label = ctk.CTkLabel(
            card, text=product["kategoria"], font=("Arial", 12), text_color=DARK_PINK
        )
        category_label.pack(pady=2)

        description = ctk.CTkLabel(
            card,
            text=product["opis"],
            font=("Arial", 12),
            text_color=TEXT,
            wraplength=190,
        )
        description.pack(padx=10, pady=5)

        price = ctk.CTkLabel(
            card,
            text=f'{product["cena"]} zł',
            font=("Arial", 18, "bold"),
            text_color=DARK_PINK,
        )
        price.pack(pady=5)

        stock = ctk.CTkLabel(
            card,
            text=f'Dostepne sztuki: {product["ilosc"]}',
            font=("Arial", 11),
            text_color=TEXT,
        )
        stock.pack(pady=(0, 12))


# PRZYCISK ODSWIEZANIA


# FUNKCJA ODSWIEZANIA PRODUKTOW
def refresh_products():
    for widget in products_frame.winfo_children():
        widget.destroy()

    show_products()


# PRZYCISK ODSWIEZANIA
refresh_button = ctk.CTkButton(
    content,
    text="Odswiez produkty",
    fg_color=DARK_PINK,
    hover_color="#AD6681",
    command=refresh_products,
)

refresh_button.grid(row=2, column=0, sticky="e", pady=10)

refresh_button.grid(row=2, column=0, sticky="e", pady=10)


# URUCHOMIENIE PRODUKTOW
show_products()

# URUCHOMIENIE APLIKACJI
app.mainloop()

import customtkinter as ctk
from tkinter import messagebox
from database import (
    init_db,
    register_user,
    authenticate_user,
    add_item,
    fetch_filtered_items,
    delete_item,
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ItemCard(ctk.CTkFrame):
    def __init__(self, master, item_data, current_user_id, delete_callback):
        super().__init__(master, corner_radius=10, border_width=1)
        self.item_data = item_data
        self.current_user_id = current_user_id
        self.delete_callback = delete_callback

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(8, 2))

        ctk.CTkLabel(
            header_frame,
            text=f"[{item_data[4]}] {item_data[1]}",
            font=("Arial", 15, "bold"),
        ).pack(side="left")

        # Contextual ownership option rendered ONLY for the post creator
        if self.item_data[7] == self.current_user_id:
            self.menu = ctk.CTkOptionMenu(
                header_frame,
                values=["...", "Delete Post"],
                width=90,
                command=self.handle_action,
            )
            self.menu.pack(side="right")

        ctk.CTkLabel(
            self,
            text=f"Category: {item_data[2]}  |  Location: {item_data[5]}",
            font=("Arial", 12),
            text_color="gray35",
        ).pack(anchor="w", padx=12)

        ctk.CTkLabel(
            self,
            text=item_data[3],
            wraplength=560,
            justify="left",
            font=("Arial", 13),
        ).pack(anchor="w", padx=12, pady=4)

        ctk.CTkLabel(
            self,
            text=f"Contact: {item_data[6]}",
            font=("Arial", 11, "italic"),
        ).pack(anchor="w", padx=12, pady=(0, 8))

    def handle_action(self, choice):
        if choice == "Delete Post":
            if messagebox.askyesno(
                "Confirm Deletion", "Are you sure you want to remove this post?"
            ):
                self.delete_callback(self.item_data[0])
            else:
                self.menu.set("...")


class FindItApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FindIT - Campus Lost & Found Network")
        self.geometry("820x620")
        init_db()
        self.current_user_id = None
        self.current_username = None
        self.show_auth_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_auth_screen(self):
        self.clear_window()
        frame = ctk.CTkFrame(self, width=400, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            frame, text="FindIT", font=("Arial", 28, "bold")
        ).pack(pady=(25, 5), padx=40)
        ctk.CTkLabel(
            frame,
            text="Connecting Things to Their Rightful Owners",
            font=("Arial", 12),
            text_color="gray40",
        ).pack(pady=(0, 20), padx=30)

        self.username_entry = ctk.CTkEntry(
            frame, placeholder_text="Campus Username / ID", width=280
        )
        self.username_entry.pack(pady=8, padx=30)

        self.password_entry = ctk.CTkEntry(
            frame, placeholder_text="Password", show="*", width=280
        )
        self.password_entry.pack(pady=8, padx=30)

        ctk.CTkButton(
            frame, text="Login", width=280, command=self.handle_login
        ).pack(pady=(15, 6), padx=30)

        ctk.CTkButton(
            frame,
            text="Create New Account",
            width=280,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.handle_register,
        ).pack(pady=(0, 25), padx=30)

    def handle_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if not user.strip() or not pwd.strip():
            messagebox.showwarning("Input Required", "Please enter username and password.")
            return
        user_id = authenticate_user(user, pwd)
        if user_id:
            self.current_user_id = user_id
            self.current_username = user.strip()
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def handle_register(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if not user.strip() or not pwd.strip():
            messagebox.showwarning("Input Required", "Please enter username and password.")
            return
        user_id = register_user(user, pwd)
        if user_id:
            self.current_user_id = user_id
            self.current_username = user.strip()
            messagebox.showinfo(
                "Registration Successful", f"Welcome to FindIT, {self.current_username}!"
            )
            self.show_dashboard()
        else:
            messagebox.showerror("Registration Error", "Username already exists.")

    def show_dashboard(self):
        self.clear_window()

        # Top Navbar
        navbar = ctk.CTkFrame(self, height=55, corner_radius=0)
        navbar.pack(fill="x")
        ctk.CTkLabel(
            navbar, text="🔍 FindIT", font=("Arial", 20, "bold")
        ).pack(side="left", padx=20, pady=12)

        ctk.CTkButton(
            navbar,
            text="Logout",
            width=80,
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self.show_auth_screen,
        ).pack(side="right", padx=15)

        ctk.CTkButton(
            navbar,
            text="+ Report Lost / Found",
            command=self.open_post_modal,
        ).pack(side="right", padx=8)

        ctk.CTkLabel(
            navbar, text=f"User: {self.current_username}", font=("Arial", 12)
        ).pack(side="right", padx=12)

        # Filter Bar
        filter_bar = ctk.CTkFrame(self, fg_color="transparent")
        filter_bar.pack(fill="x", padx=20, pady=12)

        self.search_entry = ctk.CTkEntry(
            filter_bar, placeholder_text="Search by item name or description...", width=300
        )
        self.search_entry.pack(side="left", padx=(0, 8))

        self.category_var = ctk.StringVar(value="All")
        ctk.CTkOptionMenu(
            filter_bar,
            variable=self.category_var,
            values=["All", "ID Card / Documents", "Electronics", "Keys", "Books/Notes", "Water Bottle / Bag", "Other"],
            width=170,
        ).pack(side="left", padx=6)

        self.type_var = ctk.StringVar(value="All")
        ctk.CTkOptionMenu(
            filter_bar,
            variable=self.type_var,
            values=["All", "Lost", "Found"],
            width=100,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            filter_bar, text="Filter", width=80, command=self.refresh_feed
        ).pack(side="left", padx=6)

        # Feed Area
        self.feed_frame = ctk.CTkScrollableFrame(self)
        self.feed_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self.refresh_feed()

    def refresh_feed(self):
        for widget in self.feed_frame.winfo_children():
            widget.destroy()

        records = fetch_filtered_items(
            self.search_entry.get(), self.category_var.get(), self.type_var.get()
        )
        if not records:
            ctk.CTkLabel(
                self.feed_frame,
                text="No matching campus items found.",
                font=("Arial", 14),
                text_color="gray50",
            ).pack(pady=40)
            return

        for item in records:
            card = ItemCard(
                self.feed_frame, item, self.current_user_id, self.handle_delete_item
            )
            card.pack(fill="x", pady=6, padx=4)

    def handle_delete_item(self, item_id):
        delete_item(item_id, self.current_user_id)
        self.refresh_feed()

    def open_post_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Report Lost or Found Item")
        modal.geometry("420x470")
        modal.grab_set()

        ctk.CTkLabel(
            modal, text="Report Campus Item", font=("Arial", 18, "bold")
        ).pack(pady=(15, 10))

        type_var = ctk.StringVar(value="Found")
        ctk.CTkOptionMenu(
            modal, variable=type_var, values=["Found", "Lost"], width=320
        ).pack(pady=6)

        title_entry = ctk.CTkEntry(modal, placeholder_text="Item Title (e.g., ID Card)", width=320)
        title_entry.pack(pady=6)

        cat_var = ctk.StringVar(value="ID Card / Documents")
        ctk.CTkOptionMenu(
            modal,
            variable=cat_var,
            values=["ID Card / Documents", "Electronics", "Keys", "Books/Notes", "Water Bottle / Bag", "Other"],
            width=320,
        ).pack(pady=6)

        loc_entry = ctk.CTkEntry(modal, placeholder_text="Location (e.g., Lab 303, Canteen)", width=320)
        loc_entry.pack(pady=6)

        desc_entry = ctk.CTkEntry(modal, placeholder_text="Short Description", width=320)
        desc_entry.pack(pady=6)

        contact_entry = ctk.CTkEntry(modal, placeholder_text="Contact Info (Phone / Email)", width=320)
        contact_entry.pack(pady=6)

        def submit():
            if not all([
                title_entry.get().strip(),
                loc_entry.get().strip(),
                desc_entry.get().strip(),
                contact_entry.get().strip(),
            ]):
                messagebox.showwarning("Missing Fields", "Please fill in all fields.", parent=modal)
                return
            add_item(
                title_entry.get().strip(),
                cat_var.get(),
                desc_entry.get().strip(),
                type_var.get(),
                loc_entry.get().strip(),
                contact_entry.get().strip(),
                self.current_user_id,
            )
            modal.destroy()
            self.refresh_feed()

        ctk.CTkButton(modal, text="Submit Post", width=320, command=submit).pack(pady=18)


if __name__ == "__main__":
    app = FindItApp()
    app.mainloop()

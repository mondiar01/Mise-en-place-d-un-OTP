# src/gui/auth_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.auth_system import AuthSystem

class AuthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Système d'Authentification")
        self.auth_system = AuthSystem()
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        ttk.Button(self.root, text="S'inscrire", command=self.show_register_form).pack(pady=10)
        ttk.Button(self.root, text="Se connecter", command=self.show_login_form).pack(pady=10)

    def show_register_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        fields = {}
        for field in ['username', 'password', 'email', 'birth_date', 'address', 'postal_code']:
            ttk.Label(self.root, text=field.replace('_', ' ').title() + ':').pack()
            entry = ttk.Entry(self.root)
            entry.pack()
            fields[field] = entry

        ttk.Button(self.root, text="S'inscrire", 
                  command=lambda: self.handle_register(fields)).pack(pady=10)
        ttk.Button(self.root, text="Retour", command=self.show_main_menu).pack()

    def show_login_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Username:").pack()
        username_entry = ttk.Entry(self.root)
        username_entry.pack()

        ttk.Label(self.root, text="Password:").pack()
        password_entry = ttk.Entry(self.root, show="*")
        password_entry.pack()

        ttk.Button(self.root, text="Se connecter", 
                  command=lambda: self.handle_login(username_entry.get(), password_entry.get())).pack(pady=10)
        ttk.Button(self.root, text="Retour", command=self.show_main_menu).pack()

    def handle_register(self, fields):
        values = {field: entry.get() for field, entry in fields.items()}
        success, message = self.auth_system.register(**values)
        if success:
            messagebox.showinfo("Succès", message)
            self.show_main_menu()
        else:
            messagebox.showerror("Erreur", message)

    def handle_login(self, username, password):
        success, result = self.auth_system.login(username, password)
        if success:
            question, answer = self.auth_system.get_security_question(username)
            self.show_security_question(question, answer)
        else:
            messagebox.showerror("Erreur", result)

    def show_security_question(self, question, correct_answer):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text=question).pack()
        answer_entry = ttk.Entry(self.root)
        answer_entry.pack()

        def verify_answer():
            if answer_entry.get() == correct_answer:
                messagebox.showinfo("Succès", "Connexion réussie!")
                self.show_main_menu()
            else:
                messagebox.showerror("Erreur", "Réponse incorrecte")
                self.show_login_form()

        ttk.Button(self.root, text="Vérifier", command=verify_answer).pack(pady=10)
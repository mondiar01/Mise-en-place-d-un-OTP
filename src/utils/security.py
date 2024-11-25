# src/utils/security.py
import hashlib

class Security:
    @staticmethod
    def verify_password_strength(password):
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères"
        if not any(c.isupper() for c in password):
            return False, "Le mot de passe doit contenir au moins une majuscule"
        if not any(c.isdigit() for c in password):
            return False, "Le mot de passe doit contenir au moins un chiffre"
        if not any(c in "!@#$%^&*" for c in password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial"
        return True, "Mot de passe valide"

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(input_password, stored_password):
        return hashlib.sha256(input_password.encode()).hexdigest() == stored_password
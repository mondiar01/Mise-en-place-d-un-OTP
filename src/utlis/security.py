# src/utils/security.py
import hashlib
import secrets
import re
import pyotp

class Security:
    @staticmethod
    def validate_password(password):
        if len(password) < 12:
            return False, "Le mot de passe doit contenir au moins 12 caractères"
        if not re.search(r"[A-Z]", password):
            return False, "Le mot de passe doit contenir au moins une majuscule"
        if not re.search(r"[a-z]", password):
            return False, "Le mot de passe doit contenir au moins une minuscule"
        if not re.search(r"\d", password):
            return False, "Le mot de passe doit contenir au moins un chiffre"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial"
        return True, "Mot de passe valide"

    @staticmethod
    def generate_otp_secret():
        return pyotp.random_base32()

    @staticmethod
    def verify_otp(secret, code):
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
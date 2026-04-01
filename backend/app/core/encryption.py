"""
数据加密模块 - 医疗数据安全
"""
from cryptography.fernet import Fernet
import base64
import hashlib
from app.core.config import settings


class DataEncryption:
    """对称加密服务 - 用于医疗数据保护"""
    
    def __init__(self):
        key = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
        self.fernet = Fernet(base64.urlsafe_b64encode(key))
    
    def encrypt(self, data: str) -> str:
        """加密数据"""
        if not data:
            return ""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        if not encrypted_data:
            return ""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return ""


encryption_service = DataEncryption()


def mask_phone(phone: str) -> str:
    """手机号脱敏 138****1234"""
    if not phone or len(phone) < 11:
        return phone
    return f"{phone[:3]}****{phone[-4:]}"


def mask_id_card(id_card: str) -> str:
    """身份证号脱敏 310****1234"""
    if not id_card or len(id_card) < 18:
        return id_card
    return f"{id_card[:3]}****{id_card[-4:]}"


def mask_name(name: str) -> str:
    """姓名脱敏 张*"""
    if not name or len(name) < 2:
        return name
    return f"{name[0]}*"


def mask_email(email: str) -> str:
    """邮箱脱敏 a***@example.com"""
    if not email or "@" not in email:
        return email
    parts = email.split("@")
    username = parts[0]
    if len(username) <= 2:
        masked_username = username[0] + "*"
    else:
        masked_username = username[0] + "***" + username[-1]
    return f"{masked_username}@{parts[1]}"


def desensitize_user_data(data: dict) -> dict:
    """批量脱敏用户数据"""
    result = data.copy()
    if "phone" in result and result["phone"]:
        result["phone"] = mask_phone(result["phone"])
    if "id_card" in result and result["id_card"]:
        result["id_card"] = mask_id_card(result["id_card"])
    if "name" in result and result["name"]:
        result["name"] = mask_name(result["name"])
    if "email" in result and result["email"]:
        result["email"] = mask_email(result["email"])
    return result

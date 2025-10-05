# auth_manager.py
import param
import bcrypt
import secrets
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Conexão com MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017/')
db = client.daphi_stakeholders
users_collection = db.users
sessions_collection = db.sessions

class AuthManager(param.Parameterized):
    current_user = param.String(default="")
    is_logged_in = param.Boolean(default=False)
    session_token = param.String(default="")
    
    async def register_user(self, username, password):
        existing_user = await users_collection.find_one({"username": username})
        if existing_user:
            return False, "Usuário já existe"
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        
        result = await users_collection.insert_one(user_data)
        return True, f"Usuário {username} criado com sucesso"
    
    async def login_user(self, username, password):
        user = await users_collection.find_one({"username": username})
        if not user:
            return False, "Usuário não encontrado"
        
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            session_token = secrets.token_urlsafe(32)
            session_data = {
                "user_id": user['_id'],
                "username": username,
                "token": session_token,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=24)
            }
            
            await sessions_collection.insert_one(session_data)
            
            await users_collection.update_one(
                {"_id": user['_id']},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            
            self.current_user = username
            self.is_logged_in = True
            self.session_token = session_token
            
            return True, "Login bem-sucedido"
        else:
            return False, "Senha incorreta"
    
    async def logout_user(self):
        if self.session_token:
            await sessions_collection.delete_one({"token": self.session_token})
        
        self.current_user = ""
        self.is_logged_in = False
        self.session_token = ""
        return True, "Logout bem-sucedido"
    
    async def validate_session(self, token):
        if not token:
            return False
        
        session = await sessions_collection.find_one({"token": token})
        if session and session['expires_at'] > datetime.utcnow():
            self.current_user = session['username']
            self.is_logged_in = True
            self.session_token = token
            return True
        return False
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal, get_db
from app.schemas.user import UserCreate, UserOut, LoginOut, Login
from app.models.user import User as UserModel
from app.core.security import hash_password, create_access_token, verify_password
from app.dependencies.auth import admin_required, role_required, get_current_user

router_user = APIRouter(prefix="/users", tags=["users"])
router_auth = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------
# USERS
# ---------------------------

# Liste des utilisateurs (ADMIN ONLY)
@router_user.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(UserModel).all()

# Supprimer un utilisateur par ID (ADMIN ONLY)
@router_user.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with id {user_id} has been deleted"}

# Dashboard (que je rend accessible a admin et user)
@router_user.get("/dashboard")
def dashboard(current_user=Depends(role_required("admin", "user"))):
    return {"message": f"Hello {current_user.username}, welcome to your dashboard"}

# Mon profil (USER)
@router_user.get("/me", response_model=UserOut)
def me(current_user=Depends(role_required("user"))):
    return current_user

# ---------------------------
# AUTH
# ---------------------------

# Register (par défaut role=user)
@router_auth.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    us = UserModel(
        username=user.username,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        role="user"
    )
    db.add(us)
    db.commit()
    db.refresh(us)
    return us

# Login
@router_auth.post("/login", response_model=LoginOut)
def login(user: Login, db: Session = Depends(get_db)):
    us = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not us or not verify_password(user.password, us.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": us.username,
        "role": us.role
    })
    return {"access_token": access_token, "token_type": "bearer"}
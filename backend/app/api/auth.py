"""
认证API - 用户注册、登录、访客模式
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from app.core.database import get_db
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    get_current_user
)
from app.core.config import settings
from app.models.user import User, UserProfile, UserRole
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, UserUpdate,
    UserProfileUpdate, TokenResponse, UserProfileResponse,
    PrivacySettingsUpdate, VisitorRegisterResponse
)

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password),
        role=UserRole[user_data.role.value.upper()]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    profile = UserProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录"""
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )
    
    user.last_login = datetime.now()
    db.commit()
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)
    )


@router.post("/visitor", response_model=VisitorRegisterResponse)
async def register_visitor():
    """访客注册 - 无需登录即可使用部分功能"""
    visitor_id = str(uuid.uuid4())
    session_token = str(uuid.uuid4())
    
    return VisitorRegisterResponse(
        visitor_id=visitor_id,
        session_token=session_token,
        expires_in=3600 * 24
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """用户登出"""
    return {"message": "登出成功"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    if user_data.email:
        current_user.email = user_data.email
    if user_data.phone:
        current_user.phone = user_data.phone
    
    current_user.updated_at = datetime.now()
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户详细信息"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return UserProfileResponse.model_validate(profile)


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户详细信息"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    
    profile.updated_at = datetime.now()
    db.commit()
    db.refresh(profile)
    
    return UserProfileResponse.model_validate(profile)


@router.put("/privacy")
async def update_privacy_settings(
    settings_data: PrivacySettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新隐私设置"""
    if settings_data.data_encryption_enabled is not None:
        current_user.data_encryption_enabled = settings_data.data_encryption_enabled
    if settings_data.data_sharing_enabled is not None:
        current_user.data_sharing_enabled = settings_data.data_sharing_enabled
    
    db.commit()
    
    return {
        "message": "隐私设置已更新",
        "data_encryption_enabled": current_user.data_encryption_enabled,
        "data_sharing_enabled": current_user.data_sharing_enabled
    }


@router.delete("/account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """注销账户 - 删除所有个人数据"""
    user_id = current_user.id
    
    db.query(UserProfile).filter(UserProfile.user_id == user_id).delete()
    db.delete(current_user)
    db.commit()
    
    return {"message": "账户已注销，所有个人数据已删除"}

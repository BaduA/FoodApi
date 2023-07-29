from fastapi import status, HTTPException, Depends, APIRouter
import models
import schemas
import database
from sqlalchemy.orm import Session
from utlils import hash, verify
from . import oauth2

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_current_user(current_user=Depends(oauth2.get_current_user)):
    return current_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_pw = hash(user.password)
    user.password = hashed_pw
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/changePsw")
def change_psw(
    chg_psw: schemas.ChangePsw,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    isTrue = verify(chg_psw.old_psw, current_user.password)
    if isTrue:
        userQuery = db.query(models.User).filter(models.User.id == current_user.id)
        userQuery.update({"password": hash(chg_psw.new_psw)})
        db.commit()
        return "successfully changed password"
    else:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="old password not matching",
        )


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return user


@router.post("/{id}/friendrequest")
def friend_request(
    id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    req = models.UserFriendRequest(sender=current_user.id, taker=id)
    db.add(req)
    db.commit()
    return "Requested"


@router.post("/{id}/handlerequest")
def handle_friend_request(
    id: int,
    acc: bool,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    db.query(models.UserFriendRequest).filter(
        models.UserFriendRequest.sender == id
    ).filter(models.UserFriendRequest.taker == current_user.id).delete(
        synchronize_session=False
    )
    db.commit()
    if acc:
        friendship = models.UserFriend(user1_id=current_user.id, user2_id=id)
        db.add(friendship)
        return "Accepted"
    return "Denied"


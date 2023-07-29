from passlib.context import CryptContext

import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_psw, hashed_psw):
    return pwd_context.verify(plain_psw, hashed_psw)


def is_member(groupname, user, db):
    groupid = (
        db.query(models.Group).filter(models.Group.groupname == groupname).first().id
    )
    membership = (
        db.query(models.GroupMember)
        .filter(models.GroupMember.group_id == groupid)
        .filter(models.GroupMember.user_id == user.id)
        .first()
    )
    if not membership:
        return False
    else:
        return True

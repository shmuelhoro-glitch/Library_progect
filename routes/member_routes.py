from fastapi import FastAPI,APIRouter,HTTPException
from pydantic import BaseModel
from database.member_db import MemberDB


router = APIRouter()


class BaseMember(BaseModel):
    name : str
    email : str

class UpdateMember(BaseModel):
    name : str | None = None
    email : str | None = None
    is_active : bool | None = None
    total_borrows : int | None = None


member = MemberDB()



@router.post("",status_code=201)
def create_member(new:BaseMember):
    name = new.name
    email = new.email
    return member.create_member_in_db(name,email)


@router.get("")
def get_all_members():
    return member.get_all_members_in_db()

@router.get("/{id:int}")
def get_member_by_id(id):
    data = member.get_member_by_id_in_db(id)
    if data:
        return data
    else:
        raise HTTPException(404,"Member not found")

@router.patch("/{id:int}")
def update_member(id,update_data:UpdateMember):
    data = update_data.model_dump(exclude_unset=True)
    return member.update_member_in_db(id,data)

@router.patch("/{id:int}/deactivate")
def deactivate_member(id):
    return member.deactivate_member_in_db(id)



@router.patch("/{id:int}/activate")
def activate_member(id):
    return member.activate_member_in_db(id)
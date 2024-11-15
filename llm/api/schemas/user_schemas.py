from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    id: int = Field(..., json_schema_extra={"description" : "ユーザーIDの指定：必須", "example" : 1})
    name: str = Field(..., json_schema_extra={"description" : "ユーザー名の指定：必須", "example" : "John Smith"})
    
    model_config = ConfigDict(from_attributes=True)  # ORMモードを有効化

# class ItemBase(BaseModel):
#     title: str
#     description: Optional[str] = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True

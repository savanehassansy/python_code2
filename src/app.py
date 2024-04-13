from fastapi import FastAPI
from controllers.user_controller import router as UserRouter

app = FastAPI()
app.include_router(UserRouter, tags=["User"], prefix="/user")

# @app.get("/",tags=["Root"])
# async def read_root():
#     return{"message":"bienvenue sur mon app"}

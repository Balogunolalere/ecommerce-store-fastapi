from fastapi import Depends, FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAccessTokenInfo, FiefAsync, FiefUserInfo
from fief_client.integrations.fastapi import FiefAuth

fief = FiefAsync(  # !
    "https://yemzy.fief.dev",
    "YOUR_CLIENT_ID",
    "YOUR_CLIENT_SECRET",
)

scheme = OAuth2AuthorizationCodeBearer(  # !
    "https://yemzy.fief.dev/authorize",
    "https://yemzy.fief.dev/api/token",
    scopes={"openid": "openid", "offline_access": "offline_access"},

)

auth = FiefAuth(fief, scheme)  # !



app = FastAPI()


@app.get("/userinfo")
async def get_user_info(
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    userinfo: FiefUserInfo = Depends(auth.current_user())  # !
):
    return access_token_info, userinfo

@app.get("/user")
async def get_user(
    userinfo: FiefUserInfo = Depends(auth.current_user()),
):
    return userinfo



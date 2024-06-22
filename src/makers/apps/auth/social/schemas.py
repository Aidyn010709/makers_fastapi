from pydantic import BaseModel

class LikeRequest(BaseModel):
    user_id: int  # Идентификатор пользователя, которому устанавливается лайк

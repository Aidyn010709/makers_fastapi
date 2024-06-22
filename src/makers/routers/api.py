from fastapi import APIRouter

from makers.apps.auth.views.api import auth_router
from makers.apps.mentor.views.api import router as mentor_router
from makers.apps.mentor.profiles.views.api import router as profile_router
from makers.apps.courses.views.api import router as course_router
from makers.apps.auth.social.views.api import router as social_router


core_router = APIRouter()

# Auth user router
core_router.include_router(auth_router, prefix="/account", tags=["Accounts"])
# Mentor router
core_router.include_router(mentor_router, prefix='/mentor', tags=['Mentors'])

core_router.include_router(profile_router, prefix='/profile', tags=['Profile'])

core_router.include_router(course_router, prefix='/course', tags=['Course'])

core_router.include_router(social_router, prefix='/social', tags=['Social'])


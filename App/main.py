from fastapi import FastAPI, APIRouter

from . import Routers
################################################################################
# Main app instantiation
app = FastAPI()
# Include these routers to the MAIN app because we don't want them under the
# 'guilds/{guild_id}' context
app.include_router(Routers.Auth.router)
# app.include_router(App.Routers.Old.LoadAll.router)
app.include_router(Routers.Guilds.router)

################################################################################
# Router Inclusion
main_router = APIRouter(prefix="/guilds/{guild_id}")

# All other routers are included under the main_router to get the guild_id context
main_router.include_router(Routers.Embeds.router)
main_router.include_router(Routers.Forms.router)
main_router.include_router(Routers.Giveaways.router)
main_router.include_router(Routers.Glyphs.router)
main_router.include_router(Routers.Positions.router)
main_router.include_router(Routers.Profiles.router)
main_router.include_router(Routers.Raffles.router)
main_router.include_router(Routers.ReactionRoles.router)

# Hook this up at the end after adding all other routers
app.include_router(main_router)

################################################################################

from aiogram import Router

from . import (
    start,
    profile,
    events,
    admin,
    roles,
    settings,
    callbacks,
    profile_callbacks,
    game_end,
    parse_active_players
)

main_router = Router()

main_router.include_router(start.router)
main_router.include_router(profile.router)
main_router.include_router(events.router)
main_router.include_router(admin.router)
main_router.include_router(roles.router)
main_router.include_router(settings.router)
main_router.include_router(callbacks.router)
main_router.include_router(profile_callbacks.router)
main_router.include_router(game_end.router)
main_router.include_router(parse_active_players.router)

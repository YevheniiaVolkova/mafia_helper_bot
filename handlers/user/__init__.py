from . import profile

def setup_user_routes(router):
    router.include_router(profile.router)
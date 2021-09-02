TORTOISE_ORM = {
    "connections": {"default": "mysql://root:rxpad@127.0.0.1:3306/mvpuser"},
    "apps": {
        "models": {
            "models": ["USER_SERVICE_SYSTEM.domain.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
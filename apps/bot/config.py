from environs import Env

env = Env()
env.read_env()

with env.prefixed("BOT_APP_"):
    LOG_CONFIG = env.json("LOG_CONFIG")
    CONTENT_FILENAME = env.str("CONTENT_FILENAME")

    SCHEDULER_CONFIG = env.json("SCHEDULER_CONFIG")

    with env.prefixed("POSTGRES_"):
        POSTGRES_CONFIG = dict(
            host=env.str("HOST", "localhost"),
            port=env.int("PORT", 5432),
            user=env.str("USER"),
            password=env.str("PASSWORD"),
            database=env.str("DATABASE"),
            register_hstore=False,
            server_side_cursors=False,
            autorollback=True,
        )

    BOT_TOKEN = env.str("BOT_TOKEN")
    BOT_ADMINS = tuple(str(chat_id) for chat_id in env.list("BOT_ADMINS", []))

    BLOCK_REGISTRATION = env.bool("BLOCK_REGISTRATION", False)

    SHEET_URL_TEMPLATE = env.str(
        "SHEET_URL_TEMPLATE", "https://docs.google.com/spreadsheets/d/{sheet}"
    )

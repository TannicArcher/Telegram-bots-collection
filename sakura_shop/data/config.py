from environs import Env

env = Env()
env.read_env()

ADMINS = list(map(int, env.list("ADMINS")))
TOKEN = env.str("TOKEN")
API_KEY = env.str("API_KEY")

from create_bot import Bot, dp
from handlers import client, admin
import logging
from database import sqlliteClient, sqlliteAdmin
from aiogram.utils import executor


sqlliteClient.sql_start()
sqlliteAdmin.sql_start()

logging.info("Подпишись @END_SOFT")

client.register_handlers_client(dp)
admin.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True)




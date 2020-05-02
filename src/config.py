import os
import dotenv
dotenv.load_dotenv()

PORT = int(os.getenv("PORT"))
DB_ALMA = os.getenv("DB_ALMA")
SERV_ALMA=os.getenv("SERV_ALMA")

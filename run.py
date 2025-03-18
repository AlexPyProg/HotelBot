import asyncio
from app.handler import main
# from app.database.models import init_db
import logging


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
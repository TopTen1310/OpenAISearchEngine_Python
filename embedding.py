import asyncio
import asyncpg
import datetime
import os
from dotenv import load_dotenv
from utils import convert_records_to_string
from engine import Engine
from tqdm import tqdm
import pickle

# Record type ------------------------------
# # name
# # manufacturer
# # model
# # location
# # price
# # year
# # mileage
# # machine_condition
# # image
# # url
# # main_category
# # sub_category
# ------------------------------------------

load_dotenv()


async def main():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    engine = Engine()

    rows = await conn.fetch('SELECT * FROM machinelist WHERE embedding IS NULL')

    n = len(rows)
    batch_size = 8
    for i in tqdm(range(n // batch_size + 1)):
        st = i * batch_size
        en = st + batch_size
        if en >= n:
            en = n
        batch = rows[st:en]
        embeddings = engine.get_embedding(convert_records_to_string(batch))
        for j in range(en - st):
            id = batch[j]["id"]
            embedding = pickle.dumps(embeddings[j])
            await conn.execute(f'''
                UPDATE machinelist
                SET embedding = $1
                WHERE id = {id}
                ''',
                               embedding
                               )

    # Close the connection.
    await conn.close()

asyncio.get_event_loop().run_until_complete(main())

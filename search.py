import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from utils import calculate_similarity
from engine import Engine
from tqdm import tqdm
import pickle


load_dotenv()


async def main():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    engine = Engine()

    rows = await conn.fetch('SELECT * FROM machinelist')

    user_input = input("Input your search string...\n")

    user_embedding = engine.get_embedding([user_input])[0]

    similarities = list(map(lambda x: {
        "score": calculate_similarity(pickle.loads(x["embedding"]), user_embedding),
        "id": x["id"]
    }, rows))

    similarities = sorted(
        similarities, key=lambda x: x["score"], reverse=True)[:10]

    ids = list(map(lambda x: x["id"], similarities))

    results = await conn.fetch('SELECT name, manufacturer, model, location, price FROM machinelist WHERE id = ANY($1)', ids)

    print(results)
    # Close the connection.
    await conn.close()

asyncio.get_event_loop().run_until_complete(main())

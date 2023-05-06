from quart import Quart, render_template, websocket
from quart import request
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from utils import calculate_similarity
from engine import Engine
from tqdm import tqdm
import pickle

load_dotenv()

app = Quart(__name__)

@app.before_serving
async def startup():
    print("Start loading data from DB")
    conn = await asyncpg.connect(host="c.machinesearchdb.postgres.database.azure.com", user="citus", database="citus", password="FastSearchEngine123")
    global engine
    engine = Engine()
    global rows
    rows = await conn.fetch('SELECT * FROM machinelist WHERE embedding IS NOT NULL')
    await conn.close()
    print("Finish loading data from DB")

@app.route("/")
async def search():
    user_input = request.args.get("q")

    if user_input == None:
        return { "message": "No query provided." }

    user_embedding = engine.get_embedding([user_input])[0]

    similarities = list(map(lambda x: {
        "score": calculate_similarity(pickle.loads(x["embedding"]), user_embedding),
        "id": x["id"]
    }, rows))

    similarities = sorted(
        similarities, key=lambda x: x["score"], reverse=True)[:10]
    ids = list(map(lambda x: x["id"], similarities))

    conn = await asyncpg.connect(host="c.machinesearchdb.postgres.database.azure.com", user="citus", database="citus", password="FastSearchEngine123")
    results = await conn.fetch('SELECT name, manufacturer, model, location, price FROM machinelist WHERE id = ANY($1)', ids)

    # Close the connection.
    await conn.close()

    return results

if __name__ == "__main__":
    app.run()
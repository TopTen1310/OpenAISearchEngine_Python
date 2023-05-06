import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from utils import calculate_similarity
from engine import Engine
from tqdm import tqdm
import pickle
import csv 

fields = ["Id"] + [f'Feature_{i}' for i in range(1536)] 
    
# name of csv file 
filename = "embedding.csv"

async def main():
    conn = await asyncpg.connect(host="c.machinesearchdb.postgres.database.azure.com", user="citus", database="citus", password="FastSearchEngine123")

    rows = await conn.fetch('SELECT id, embedding FROM machinelist')

    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields)

        for row in tqdm(rows):
            id = row["id"]
            embedding = pickle.loads(row["embedding"])
            csvwriter.writerow([id] + embedding)
            

    await conn.close()

asyncio.get_event_loop().run_until_complete(main())
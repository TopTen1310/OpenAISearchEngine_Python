import numpy as np
from numpy.linalg import norm


def convert_record_to_string(record):
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

    return f'''
"name": {record["name"]}
"manufacturer": {record["manufacturer"]}
"model": {record["model"]}
"location": {record["location"]}
"price": {record["price"]}
"year": {record["year"]}
"mileage": {record["mileage"]}
"machine_condition": {record["machine_condition"]}
"image": {record["image"]}
"url": {record["url"]}
"main_category": {record["main_category"]}
"sub_category": {record["sub_category"]}
'''


def convert_records_to_string(records):
    return list(map(lambda x: convert_record_to_string(x).replace('\n', ' '), records))


def calculate_similarity(vector1, vector2):
    A = np.array(vector1)
    B = np.array(vector2)
    return np.dot(A, B) / (norm(A) * norm(B))

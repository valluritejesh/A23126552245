from fastapi import FastAPI
import requests
from scheduler import knapsack

app = FastAPI()

DEPOTS_URL = "http://4.224.186.213/evaluation-service/depots"
VEHICLES_URL = "http://4.224.186.213/evaluation-service/vehicles"

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJ2YWxsdXJpdGVqZXNoLjIzLmNzbUBhbml0cy5lZHUuaW4iLCJleHAiOjE3ODIxOTgwOTAsImlhdCI6MTc4MjE5NzE5MCwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6ImQ0ZDc3YzljLWFiMTctNGNhMi1iOTg3LWIzOTU4YmQ5YTU4MSIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6InZhbGx1cmkgdGVqZXNoIiwic3ViIjoiMjNjYjgwMDgtYzQ2My00OTY2LWE3MjUtM2M0YThkYzc3MWViIn0sImVtYWlsIjoidmFsbHVyaXRlamVzaC4yMy5jc21AYW5pdHMuZWR1LmluIiwibmFtZSI6InZhbGx1cmkgdGVqZXNoIiwicm9sbE5vIjoiYTIzMTI2NTUyMjQ1IiwiYWNjZXNzQ29kZSI6Ik1UcXhhciIsImNsaWVudElEIjoiMjNjYjgwMDgtYzQ2My00OTY2LWE3MjUtM2M0YThkYzc3MWViIiwiY2xpZW50U2VjcmV0Ijoia3JjWXJueERrZFJYeU1zaCJ9.jp9qnLu5lTpW-zo8fljMsNTe64DsWobco1auXSUygWw"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}


@app.get("/")
def home():
    return {"message": "Vehicle Scheduler API"}


@app.get("/schedule")
def schedule():

    depots_response = requests.get(
        DEPOTS_URL,
        headers=headers
    )

    vehicles_response = requests.get(
        VEHICLES_URL,
        headers=headers
    )

    depots = depots_response.json()["depots"]
    vehicles = vehicles_response.json()["vehicles"]

    result = []

    for depot in depots:

        max_score = knapsack(
            vehicles,
            depot["MechanicHours"]
        )

        result.append({
            "DepotID": depot["ID"],
            "MechanicHours": depot["MechanicHours"],
            "MaxImpact": max_score
        })

    return result
    
@app.get("/vehicles")
def get_vehicles():
    response = requests.get(
        VEHICLES_URL,
        headers=headers
    )
    return response.json()

@app.get("/depots")
def get_depots():
    response = requests.get(
        DEPOTS_URL,
        headers=headers
    )
    return response.json()

import requests
import datetime
import json
import os

from github import Github
from fastapi import FastAPI
from pytz import timezone

app = FastAPI()

eastern = timezone("US/Eastern")
token = os.environ.get("GITHUB_TOKEN")
g = Github(token)


@app.get("/")
async def home(track: str, level: str):
    # setup

    repo = g.get_repo("nanthony007/pct-decision-tool")

    # get current data inside file
    # is an array
    data = requests.get(
        "https://raw.githubusercontent.com/nanthony007/pct-decision-tool/main/data/records.json"
    ).json()

    # get sha val from last commit
    sha_val = (
        requests.get(
            "https://api.github.com/repos/nanthony007/pct-decision-tool/contents/data/records.json"
        )
        .json()
        .get("sha")
    )

    # generate new data
    new_data = {
        "track": track,
        "range": level,
        "timestamp": datetime.datetime.now(eastern),
    }
    data.append(new_data)

    # update file using PUT

    # dynamic commit message
    repo.update_file(
        path="data/records.json",
        message=f"Adding more data at {datetime.datetime.now(eastern)}",
        content=json.dumps(data),
        sha=sha_val,
    )
    return "Data successfully added."

from datetime import datetime
import asyncio
import json

from .api_requests import share_request


async def data_parsing():
    while True:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_response = share_request.response_data

        if share_request.selective_response_data[0][1] is not None:
            data = {"datetime": current_datetime, "data": current_response}

            with open("db/parsed_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f)

        await asyncio.sleep(10)

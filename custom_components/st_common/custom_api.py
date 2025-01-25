import logging
import aiohttp
import json
from homeassistant.util import ssl
import traceback

import json
import os

from pysmartthings import App

import traceback

_LOGGER = logging.getLogger(__name__)

BASE = "custom_components/st_common/"

async def async_get_app_info(app_id, token):

    path = BASE + app_id + ".json"

    app = App()
    try:
        # 파일이 있는지 먼저 확인
        if os.path.isfile(path):
            with open(path, "r") as f:
                data = json.load(f)
                app.apply_data(data)
                return app
        else:
            url = "https://api.smartthings.com/v1/apps/" + app_id
            custom_ssl_context = ssl.get_default_context()
            custom_ssl_context.options |= 0x00040000
            headers={"Authorization": "Bearer " + token}

            _LOGGER.error("call url " + str(url))
            connector = aiohttp.TCPConnector(ssl=custom_ssl_context)
            async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        raw_data = await response.read()
                        data = json.loads(raw_data)
                        app.apply_data(data)
                        with open(path, "w") as f:
                            json.dump(obj=data, fp=f, sort_keys=True, indent=4)
                        return app

    except Exception as e:
        _LOGGER.error("get_app_info failed - " + traceback.format_exc())

        

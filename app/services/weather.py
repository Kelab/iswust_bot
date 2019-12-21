from app.aio import requests
from app.aio.requests import AsyncResponse
from typing import Optional,List

class Weather:
    @classmethod
    async def get(cls, city_name: str, params: dict = {},
                  **kwargs: dict) -> str:

        # url = f"http://wttr.in/{city_name}?format=j1&m"
        url = f"http://wttr.in/{city_name}?format=%m%l:+%c%C+%F0%9F%8C%A1%EF%B8%8F%t+%F0%9F%92%A7%h"


        headers = {
            "Accept-Language": "zh-CN",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        }
        r: AsyncResponse = await requests.get(url,
                                        params=params,
                                        headers=headers,
                                        **kwargs)

        response = await r.text
        if not response:
            return "无法获取天气API，请稍后再试！"
        return response
        # current_condition_list: Optional[List[dict]] = response['current_condition']
        # if not current_condition_list:
        #     return "查询天气无结果，请重试！"
        # current_condition = current_condition_list[0]
        # FeelsLikeC = current_condition['FeelsLikeC']
        # cloudcover = current_condition['cloudcover'] # 云量
        # humidity = current_condition['humidity']
        # observation_time = current_condition['observation_time']
        # precipMM = current_condition['precipMM'] # 预测降雨量
        # pressure = current_condition['pressure']
        # temp_C = current_condition['temp_C']
        # uvIndex = current_condition['uvIndex'] # 紫外线指数
        # visibility = current_condition['visibility']
        # cloudcover = current_condition['cloudcover']
        # 我还是决定用一句话的辣个 api
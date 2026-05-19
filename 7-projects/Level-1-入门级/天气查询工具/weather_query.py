"""
天气查询工具 (Level 1)
功能：调用和风天气 API 查询城市天气
"""

import requests

# 配置
API_KEY = "YOUR_API_KEY"  # 替换为你的 API Key
URL_NOW = "https://devapi.qweather.com/v7/weather/now"
URL_CITY = "https://geoapi.qweather.com/v2/city/lookup"


def get_city_id(city_name: str) -> str:
    """通过城市名称获取城市 ID"""
    response = requests.get(URL_CITY, params={"location": city_name, "key": API_KEY})
    data = response.json()

    if data.get("code") != "200" or not data.get("location"):
        raise ValueError(f"找不到城市：{city_name}")

    return data["location"][0]["id"]


def get_weather(city_name: str) -> dict:
    """获取指定城市的当前天气"""
    try:
        city_id = get_city_id(city_name)

        response = requests.get(URL_NOW, params={"location": city_id, "key": API_KEY})
        data = response.json()

        if data.get("code") != "200":
            raise ValueError("天气数据获取失败")

        now = data["now"]
        return {
            "city": city_name,
            "temp": now["temp"],
            "feels_like": now["feelsLike"],
            "text": now["text"],
            "humidity": now["humidity"],
            "wind_dir": now["windDir"],
            "wind_scale": now["windScale"],
        }
    except Exception as e:
        print(f"查询 {city_name} 失败：{e}")
        return {}


def main():
    """主程序"""
    print("=== 天气查询工具 ===")
    while True:
        city = input("\n请输入城市名称 (输入 q 退出): ").strip()
        if city.lower() == "q":
            break
        if not city:
            continue

        weather = get_weather(city)
        if weather:
            print(f"当前天气: {weather['text']}")
            print(f"温度: {weather['temp']}°C (体感 {weather['feels_like']}°C)")
            print(f"湿度: {weather['humidity']}%")
            print(f"风向: {weather['wind_dir']} {weather['wind_scale']}级")


if __name__ == "__main__":
    main()

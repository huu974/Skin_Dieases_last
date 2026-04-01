"""
地图服务 - 周边皮肤科诊所查询
"""
import random
from typing import List, Dict, Optional


class MapService:
    """地图服务 - 获取周边医疗机构"""
    
    def __init__(self):
        pass
    
    async def search_nearby_clinics(
        self,
        latitude: float,
        longitude: float,
        radius: float = 5000,
        keyword: str = "皮肤科"
    ) -> List[Dict]:
        """
        搜索附近诊所
        TODO: 集成地图API（高德/百度/腾讯地图）
        """
        # TODO: 实际调用地图API
        # import requests
        # url = f"https://restapi.amap.com/v3/place/around"
        # params = {
        #     "key": settings.MAP_API_KEY,
        #     "location": f"{longitude},{latitude}",
        #     "keywords": keyword,
        #     "radius": radius,
        #     "types": "综合医院|专科医院"
        # }
        # response = requests.get(url, params=params)
        # return response.json()
        
        # 模拟返回附近诊所
        clinics = [
            {
                "name": "市第一人民医院皮肤科",
                "address": "XX区XX路123号",
                "distance": round(random.uniform(0.5, 5.0), 1),
                "phone": "010-12345678",
                "rating": round(random.uniform(4.0, 5.0), 1),
                "hours": "周一至周日 8:00-17:00"
            },
            {
                "name": "XX皮肤病专科医院",
                "address": "XX区XX大道456号",
                "distance": round(random.uniform(1.0, 8.0), 1),
                "phone": "010-87654321",
                "rating": round(random.uniform(4.2, 5.0), 1),
                "hours": "周一至周五 9:00-18:00"
            },
            {
                "name": "社区服务中心皮肤门诊",
                "address": "XX街道XX社区",
                "distance": round(random.uniform(0.3, 2.0), 1),
                "phone": "010-11112222",
                "rating": round(random.uniform(3.8, 4.8), 1),
                "hours": "周一至周六 8:30-16:30"
            }
        ]
        
        return sorted(clinics, key=lambda x: x["distance"])
    
    async def get_route_info(
        self,
        start_lat: float,
        start_lng: float,
        end_lat: float,
        end_lng: float
    ) -> Dict:
        """获取路线信息"""
        # TODO: 实际调用路线规划API
        return {
            "distance": round(random.uniform(0.5, 10.0), 1),
            "duration": round(random.uniform(5, 60), 0),
            "route_points": []
        }


map_service = MapService()

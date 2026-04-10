import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.weibo_apis import WeiboApis
from apis.weibo_mobile_apis import WeiboMobileApis

weiboMobileApis = WeiboMobileApis()
weiboapis = WeiboApis()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
    获取笔记的详细
    :param work_id: 你想要获取的笔记的id
    返回笔记的详细
"""
@app.post("/get_work_info")
async def get_work_info(data: dict):
    try:
        work_id = data["work_id"]
        success, msg, work_info = weiboMobileApis.getWorkInfo(work_id)
        data = {"work_info": work_info}
        if success:
            return {"code": 200, "message": msg, "data": data}
        else:
            return {"code": 400, "message": msg, "data": data}
    except Exception as e:
        return {"code": 500, "message": str(e)}

"""
    获取搜索笔记的结果
    :param query 搜索的关键词
    :param page 搜索的页数
    返回搜索的结果
"""
@app.post("/search_work")
async def search_work(data: dict):
    try:
        query = data["query"]
        page = data["page"]
        success, msg, works = weiboMobileApis.searchSome(query, page)
        data = {"works": works}
        if success:
            return {"code": 200, "message": msg, "data": data}
        else:
            return {"code": 400, "message": msg, "data": data}
    except Exception as e:
        return {"code": 500, "message": str(e)}

"""
    获取搜索笔记的结果
    :param query 搜索的关键词
    :param page 搜索的页数
    返回搜索的结果
"""
@app.post("/get_user_posted")
async def getUserPosted(data: dict):
    try:
        user_id = data["user_id"]
        page = data["page"]
        since_id = data["since_id"] if "since_id" in data else None
        cookies_str = data["cookies_str"]
        success, msg, res_json = weiboapis.getUserPosted(user_id, page, since_id, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": res_json}
        else:
            return {"code": 400, "message": msg, "data": res_json}
    except Exception as e:
        return {"code": 500, "message": str(e)}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999, forwarded_allow_ips='*')



























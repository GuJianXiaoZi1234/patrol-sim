"""后端 API 路由层。

只做参数校验和格式转换；仿真逻辑在 simulation/（具身智能维护），
地图唯一数据源在 pathplanning/grid_map.py（算法维护）。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from pathplanning.grid_map import H, OBSTACLES, W
from simulation.robot import Robot, back_checked, forward_checked

app = FastAPI(title="patrol-sim", version="0.1.0")

# 联调期允许所有来源；结业打包前可收紧
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局唯一的机器人实例（仿真状态在内存中）
robot = Robot(x=1, y=1, heading=90)

ERROR_MESSAGES = {
    "OUT_OF_BOUNDS": "目标越出地图边界，机器人保持原位",
    "OBSTACLE_BLOCKED": "前方是障碍物，机器人保持原位",
}


class MoveRequest(BaseModel):
    action: str


def robot_state() -> dict:
    return {
        "x": robot.x,
        "y": robot.y,
        "heading": robot.heading,
        "status": robot.status,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/map")
def get_map():
    return {"width": W, "height": H, "obstacles": [[x, y] for x, y in sorted(OBSTACLES)]}


@app.get("/api/robot")
def get_robot():
    return robot_state()


@app.post("/api/robot/move")
def move(req: MoveRequest):
    if req.action in ("turn_left", "turn_right"):
        robot.turn(req.action)
        return robot_state()

    if req.action not in ("forward", "back"):
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "INVALID_ACTION",
                    "message": f"不支持的指令：{req.action}（可选 forward/back/turn_left/turn_right）",
                }
            },
        )

    _, err = forward_checked(robot) if req.action == "forward" else back_checked(robot)
    if err:
        return JSONResponse(
            status_code=409,
            content={"error": {"code": err, "message": ERROR_MESSAGES[err]}},
        )
    return robot_state()


# 结业打包时（运维）在下面挂载前端静态产物，本地联调保持注释：
# from fastapi.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
@app.get("/api/sensor/front")
def read_front_sensor():
    return {"ok": True, "data": forward_checked(robot)}

@app.get("/api/sensor/back")
def read_back_sensor():
    return {"ok": True, "data": back_checked(robot)}
@app.get("/api/sensor/front_info")
def front_info():
    try:
        data = forward_checked(robot)
        if data is None:
            return {"ok": True, "blocked": False, "distance": None}
        min_dist = min(data)
        blocked = min_dist < 0.2
        return {"ok": True, "blocked": blocked, "distance": min_dist}
    except Exception as e:
        print("front sensor error:", e)
        return {"ok": True, "blocked": False, "distance": None}

@app.get("/api/sensor/back_info")
def back_info():
    try:
        data = back_checked(robot)
        if data is None:
            return {"ok": True, "blocked": False, "distance": None}
        min_dist = min(data)
        blocked = min_dist < 0.2
        return {"ok": True, "blocked": blocked, "distance": min_dist}
    except Exception as e:
        print("back sensor error:", e)
        return {"ok": True, "blocked": False, "distance": None}
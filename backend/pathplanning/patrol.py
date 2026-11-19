# -*- coding: utf-8 -*-
"""巡检调度（算法方向核心文件）。

状态：11.19 由具身智能临时放置最小可运行版（保证巡检路由今天可用）。
明天（11.20 20:30 前）由算法按任务包全文替换为完整实现并补 2 个测试：
  - plan_patrol: 依次串联巡检点（起点 -> 点1 -> 点2 ...），任一段不可达返回 None
  - patrol_progress: 返回进度对象 {"total", "current", "done"}
替换时本文件头注释整段删除，并保留函数签名不变（路由层依赖它）。
"""
from pathplanning.bfs import find_path


def plan_patrol(start, points):
    """依次串联巡检点：返回分段路径列表；某段不可达返回 None"""
    segs = []
    cur = start
    for pt in points:
        seg = find_path(cur, pt)
        if seg is None:
            return None
        segs.append(seg)
        cur = pt
    return segs


def patrol_progress(segs, walked):
    """进度对象：walked = 已走完的段数"""
    total = len(segs)
    return {"total": total, "current": walked + 1, "done": walked >= total}

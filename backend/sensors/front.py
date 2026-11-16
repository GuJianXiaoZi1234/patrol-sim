def probe(is_wall: bool):
    if is_wall:
        return 65
    else:
        return 900

if __name__ == "__main__":
    wall_val = probe(True)
    empty_val = probe(False)
    print("贴墙时传感器数值：", wall_val)
    print("无墙时传感器数值：", empty_val)
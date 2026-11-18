from pathplanning.patrol import plan_patrol


def test_normal_patrol():
    result = plan_patrol((1, 1), [(4, 4), (8, 8), (12, 10)])
    assert result is not None
    assert len(result) == 3
    assert result[0][0] == (1, 1)
    assert result[-1][-1] == (12, 10)


def test_unreachable_patrol_point():
    result = plan_patrol((1, 1), [(99, 99)])
    assert result is None

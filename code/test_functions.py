import projet_import

def test_in_wall():
    x1, x2 = 2, 5
    y1, y2 = 3, 7.5
    p1 = (3, 4.5)
    p2 = (3, 5)
    assert projet.in_wall(x1, y1, x2, y2, p1[0], p1[1])
    assert not projet.in_wall(x1, y1, x2, y2, p2[0], p2[1])


import unittest

from maze.grid import RectangularGrid, PolarGrid


class TestGridMethods(unittest.TestCase):

    def test_init(self):
        g = RectangularGrid(4, 4)
        self.assertEqual(g.get_cell(3, 2), g.grid[3][2])

        self.assertTrue(g.grid[2][2].north == g.grid[1][2])
        self.assertTrue(g.grid[2][2].south == g.grid[3][2])
        self.assertTrue(g.grid[2][2].east == g.grid[2][3])
        self.assertTrue(g.grid[2][2].west == g.grid[2][1])

        self.assertIsNone(g.grid[0][2].north)
        self.assertIsNone(g.grid[3][2].south)
        self.assertIsNone(g.grid[2][3].east)
        self.assertIsNone(g.grid[2][0].west)

        self.assertEqual(4, len(g.grid[1][1].neighbors()))
        n = g.grid[0][0].neighbors()
        self.assertEqual(2, len(n))
        self.assertIn(g.grid[0][1], n)
        self.assertIn(g.grid[1][0], n)

        self.assertFalse(g.grid[1][1].has_link(g.grid[1][2]))
        self.assertEqual(0, len(g.grid[1][1].links))
        g.grid[1][1].link(g.grid[1][2])
        self.assertTrue(g.grid[1][1].has_link(g.grid[1][2]))
        self.assertEqual(1, len(g.grid[1][1].links))

    def test_distances(self):
        g = RectangularGrid(4, 4)
        g.grid[0][0].link(g.grid[0][1])
        g.grid[0][1].link(g.grid[1][1])
        distances = g.grid[0][0].compute_distances()
        self.assertEqual(distances[g.grid[0][0]], 0)
        self.assertEqual(distances[g.grid[0][1]], 1)
        self.assertEqual(distances[g.grid[1][1]], 2)
        self.assertTrue(g.grid[2][3] not in distances.cells.keys())

    def test_polargrid(self):
        p = PolarGrid(8)

        self.assertEqual(len(p.grid), 8)
        self.assertEqual(len(p.grid[0]), 1)
        self.assertEqual(len(p.grid[1]), 6)
        self.assertEqual(len(p.grid[2]), 12)
        self.assertEqual(len(p.grid[3]), 12)
        self.assertEqual(len(p.grid[4]), 24)
        self.assertEqual(len(p.grid[5]), 24)
        self.assertEqual(len(p.grid[6]), 24)
        self.assertEqual(len(p.grid[7]), 24)
        c1 = p.get_cell(0, 0)
        self.assertIsNone(c1.cw)
        self.assertIsNone(c1.ccw)
        self.assertIsNone(c1.inward)
        self.assertTrue(len(c1.outwards) > 0)
        c2 = p.get_cell(1, 0)

        #self.assertEqual(c2.ccw, p.get_cell(1, 7))
        #self.assertIsNotNone(c2.ccw)
        self.assertEqual(c2.cw, p.get_cell(1, 1))
        self.assertIsNotNone(c2.cw)
        self.assertIsNotNone(c2.inward)
        self.assertEqual(c2.inward, p.get_cell(0, 0))
        self.assertTrue(len(c2.outwards) == 2)
        self.assertIn(p.get_cell(2, 0), c2.outwards)
        self.assertIn(p.get_cell(2, 1), c2.outwards)

if __name__ == '__main__':
    unittest.main()

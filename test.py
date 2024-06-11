import unittest

from a6 import search_direct_intermediate_nodes

class TestSearchDirectIntermediateNodes(unittest.TestCase):
    def test_1(self):
        graph = {
            'to': [('explore', 1.0), ('seek', 1.0), ('find', 3.0), ('kick', 1.0)],
            'explore': [('strange', 1.0)],
            'strange': [('new', 1.0)],
            'new': [('worlds', 1.0), ('life', 1.0), ('civilizations', 1.0)],
            'worlds': [('go', 1.0)],
            'go': [('to', 1.0), ('and', 1.0)],
            'seek': [('out', 1.0)],
            'out': [('new', 1.0), ('to', 3.0), ('go', 1.0)],
            'life': [('and', 1.0)],
            'and': [('new', 1.0), ('i', 1.0)],
            'civilizations': [('to', 1.0)],
            'find': [('out', 3.0)],
            'kick': [('out', 1.0)]
        }
        start_node = 'find'
        end_node = 'new'
        self.assertEqual(search_direct_intermediate_nodes(graph, start_node, end_node), "find和new之间的桥接词是out")

    def test_2(self):
        graph = {
            'to': [('explore', 1.0), ('seek', 1.0), ('find', 3.0), ('kick', 1.0)],
            'explore': [('strange', 1.0)],
            'strange': [('new', 1.0)],
            'new': [('worlds', 1.0), ('life', 1.0), ('civilizations', 1.0)],
            'worlds': [('go', 1.0)],
            'go': [('to', 1.0), ('and', 1.0)],
            'seek': [('out', 1.0)],
            'out': [('new', 1.0), ('to', 3.0), ('go', 1.0)],
            'life': [('and', 1.0)],
            'and': [('new', 1.0), ('i', 1.0)],
            'civilizations': [('to', 1.0)],
            'find': [('out', 3.0)],
            'kick': [('out', 1.0)]
        }
        start_node = '666'
        end_node = 'out'
        self.assertEqual(search_direct_intermediate_nodes(graph, start_node, end_node), '没有666或out')

    def test_3(self):
        graph = {
            'to': [('explore', 1.0), ('seek', 1.0), ('find', 3.0), ('kick', 1.0)],
            'explore': [('strange', 1.0)],
            'strange': [('new', 1.0)],
            'new': [('worlds', 1.0), ('life', 1.0), ('civilizations', 1.0)],
            'worlds': [('go', 1.0)],
            'go': [('to', 1.0), ('and', 1.0)],
            'seek': [('out', 1.0)],
            'out': [('new', 1.0), ('to', 3.0), ('go', 1.0)],
            'life': [('and', 1.0)],
            'and': [('new', 1.0), ('i', 1.0)],
            'civilizations': [('to', 1.0)],
            'find': [('out', 3.0)],
            'kick': [('out', 1.0)]
        }
        start_node = 'explore'
        end_node = 'i'
        self.assertEqual(search_direct_intermediate_nodes(graph, start_node, end_node), 'explore和i之间没有桥接词')

    def test_4(self):
        graph = {
            'to': [('explore', 1.0), ('seek', 1.0), ('find', 3.0), ('kick', 1.0)],
            'explore': [('strange', 1.0)],
            'strange': [('new', 1.0)],
            'new': [('worlds', 1.0), ('life', 1.0), ('civilizations', 1.0)],
            'worlds': [('go', 1.0)],
            'go': [('to', 1.0), ('and', 1.0)],
            'seek': [('out', 1.0)],
            'out': [('new', 1.0), ('to', 3.0), ('go', 1.0)],
            'life': [('and', 1.0)],
            'and': [('new', 1.0), ('i', 1.0)],
            'civilizations': [('to', 1.0)],
            'find': [('out', 3.0)],
            'kick': [('out', 1.0)]
        }
        start_node = 'to'
        end_node = 'find'
        self.assertEqual(search_direct_intermediate_nodes(graph, start_node, end_node), 'to和find之间没有桥接词')

if __name__ == '__main__':
    unittest.main()

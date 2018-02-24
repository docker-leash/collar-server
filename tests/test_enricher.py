# vim:set ts=4 sw=4 et:
"""
EnricherTest
============
"""


import unittest

from docker_collar.enricher import Enricher


class EnricherTests(unittest.TestCase):
    """Validation of :cls:`docker_collar.Enricher`
    """

    def test_add_host(self):
        """Add Host field
        """
        enricher = Enricher()
        payload = enricher.add_host({})
        self.assertIn('Host', payload)

import unittest2 as unittest
from nose.plugins.attrib import attr
from tempest import exceptions
from tempest import openstack
import tempest.config


class FlavorsTest(unittest.TestCase):

    release = tempest.config.TempestConfig().env.release_name

    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.flavors_client
        cls.config = cls.os.config
        cls.flavor_id = cls.config.env.flavor_ref

    @attr(type='smoke')
    def test_list_flavors(self):
        """List of all flavors should contain the expected flavor"""
        resp, flavors = self.client.list_flavors()
        resp, flavor = self.client.get_flavor_details(self.flavor_id)
        flavor_min_detail = {'id': flavor['id'], 'links': flavor['links'],
                             'name': flavor['name']}
        self.assertTrue(flavor_min_detail in flavors)

    @attr(type='smoke')
    def test_list_flavors_with_detail(self):
        """Detailed list of all flavors should contain the expected flavor"""
        resp, flavors = self.client.list_flavors_with_detail()
        resp, flavor = self.client.get_flavor_details(self.flavor_id)
        self.assertTrue(flavor in flavors)

    @attr(type='smoke')
    def test_get_flavor(self):
        """The expected flavor details should be returned"""
        resp, flavor = self.client.get_flavor_details(self.flavor_id)
        self.assertEqual(self.flavor_id, str(flavor['id']))

    @attr(type='negative')
    def test_get_non_existant_flavor(self):
        """flavor details are not returned for non existant flavors"""
        self.assertRaises(exceptions.NotFound, self.client.get_flavor_details,
                          999)

    @unittest.expectedFailure
    @attr(type='positive', bug='lp912922')
    def test_list_flavors_using_marker(self):
        """The list of flavors should start from the provided marker"""
        resp, flavors = self.client.list_flavors()
        flavor_id = flavors[0]['id']

        params = {'marker': flavor_id}
        resp, flavors = self.client.list_flavors(params)
        self.assertFalse(any([i for i in flavors if i['id'] == flavor_id]),
                        'The list of flavors did not start after the marker.')

    @unittest.expectedFailure
    @attr(type='positive', bug='lp912922')
    def test_list_flavors_detailed_using_marker(self):
        """The list of flavors should start from the provided marker"""
        resp, flavors = self.client.list_flavors_with_detail()
        flavor_id = flavors[0]['id']

        params = {'marker': flavor_id}
        resp, flavors = self.client.list_flavors_with_detail(params)
        self.assertFalse(any([i for i in flavors if i['id'] == flavor_id]),
                        'The list of flavors did not start after the marker.')

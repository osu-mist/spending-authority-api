import logging
import json
import unittest
import yaml
import utils


class integration_tests(unittest.TestCase):
    @classmethod
    def setup(cls, config_path, openapi_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
            cls.base_url = utils.setup_base_url(config)
            cls.session = utils.setup_session(config)
            cls.test_cases = config['test_cases']

        with open(openapi_path) as openapi_file:
            cls.openapi = yaml.load(openapi_file)

    @classmethod
    def cleanup(cls):
        cls.session.close()

    # Test case: GET /spendingauthority with valid authority onids
    def test_get_authority_onids(self, endpoint='/spendingauthority'):
        for onid in self.test_cases['valid_authority_onids']:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            spending_schema = utils.get_resource_schema(
                self, 'SpendingAuthorityResource'
            )
            utils.check_schema(self, response, spending_schema)
            response_data = response.json()['data']
            actual_onid = response_data['id']
            self.assertEqual(actual_onid.lower(), onid.lower())

    # Test case: GET /spendingauthority with invalid authority onids
    def test_get_non_authority_onids(self, endpoint='/spendingauthority'):
        for onid in self.test_cases['invalid_authority_onids']:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            spending_schema = []
            self.assertEqual(response.json()['data'], spending_schema)

    # Test case: GET /spendingauthority with bad request
    def test_error_response(self, endpoint='/spendingauthority'):
        for onid in self.test_cases['bad_request']:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 400, params=params)
            error_schema = utils.get_resource_schema(self, 'Error')
            utils.check_schema(self, response, error_schema)

    # Test case: GET /spendingauthority spending limits
    def test_spending_limits(self, endpoint='/spendingauthority'):
        # Checking that the lists of spending limits and indexes are unique
        # Checking valid onids with spending authority only
        for onid in self.test_cases['valid_authority_onids']:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            response_data = response.json()['data']
            attributes = response_data['attributes']
            limits = attributes['limits']
            spendingLimit = []
            index_array = []
            # Checking that each spending limit has at least one index
            for limit in limits:
                index_array = limit['indexes']
                spendingLimit.append(limit['spendingLimit'])
                self.assertGreater(len(limit['indexes']), 0)
            # Creating a dict indexes_list from indexes,
            # and compare it with the original array of indexes
            indexes_list = list(dict.fromkeys(index_array))
            self.assertEqual(index_array, indexes_list)
            # Creating a dict spendingLimit_list from spendingLimit,
            # and compare it with the original array of spendingLimit
            spendingLimit_list = list(dict.fromkeys(spendingLimit))
            self.assertEqual(spendingLimit, spendingLimit_list)


if __name__ == '__main__':
    arguments, argv = utils.parse_arguments()

    # Setup logging level
    if arguments.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    integration_tests.setup(arguments.config_path, arguments.openapi_path)
    unittest.main(argv=argv, exit=False)
    integration_tests.cleanup()

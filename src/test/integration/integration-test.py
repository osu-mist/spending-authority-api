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

    def test_get_authority_onids(self, endpoint='/spendingauthority'):
        for onid in self.test_cases['valid_authority_onids']:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            self.checking_response_schema(response, onid)
            self.checking_spending_limits(response)

    # Test case: GET /spendingauthority with valid authority onids
    def checking_response_schema(self, response, onid):
        spending_schema = utils.get_resource_schema(
            self, 'SpendingAuthorityResource'
        )
        utils.check_schema(self, response, spending_schema)
        response_data = response.json()['data']
        actual_onid = response_data['id']
        logging.debug(f'Request to made to {onid.lower()}')
        logging.debug(f'Response for {actual_onid.lower()}')
        self.assertEqual(actual_onid.lower(), onid.lower())

    # Test case: GET /spendingauthority spending limits
    def checking_spending_limits(self, response):
        # Checking that the lists of spending limits and indexes are unique
        # Checking valid onids with spending authority only
        # To make sure that attributes is not empty
        response_data = response.json()['data']
        attributes = response_data['attributes']
        self.assertTrue(attributes)
        limits = attributes['limits']
        # Checking that limits has at least one index
        logging.debug(f'limits: {len(limits)}')
        self.assertTrue(limits)
        spendinglimit = []
        index_array = []
        for limit in limits:
            for index in limit['indexes']:
                index_array.append(index)
            spendinglimit.append(limit['spendingLimit'])
            # Checking that each spending limit has at least one index
            logging.debug(f'spending limit has: {limit["indexes"]}')
            self.assertTrue(limit['indexes'])
        # Comparing the size of the list with the size of the set of that
        # list doublications will be removed in a the set
        logging.debug(f'index_array size: {len(index_array)}')
        logging.debug(f'index_array set size: {len(set(index_array))}')
        self.assertEqual(len(index_array), len(set(index_array)))
        logging.debug(f'index_array size:{len(spendinglimit)}')
        logging.debug(f'index_array set size:{len(set(spendinglimit))}')
        self.assertEqual(len(spendinglimit), len(set(spendinglimit)))

    # Test case: GET /spendingauthority with invalid authority onids
    def test_get_non_authority_onids(self, endpoint='/spendingauthority'):
        for onid in self.test_cases['invalid_authority_onids']:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            spending_schema = []
            self.assertEqual(response.json()['data'], spending_schema)

    # Test case: GET /spendingauthority with bad request
    def test_bad_request_response(self, endpoint='/spendingauthority'):
        bad_requests = ["", {}, []]
        for request in bad_requests:
            params = {'onid': request}
            response = utils.make_request(self, endpoint, 400, params=params)
            error_schema = utils.get_resource_schema(self, 'Error')
            utils.check_schema(self, response, error_schema)


if __name__ == '__main__':
    arguments, argv = utils.parse_arguments()

    # Setup logging level
    if arguments.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    integration_tests.setup(arguments.config_path, arguments.openapi_path)
    unittest.main(argv=argv)
    integration_tests.cleanup()

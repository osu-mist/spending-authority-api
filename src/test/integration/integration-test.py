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
            response_data = response.json()['data']
            # Test case: GET /spendingauthority with valid authority onids
            spending_schema = utils.get_resource_schema(
                self, 'SpendingAuthorityResource'
            )
            utils.check_schema(self, response, spending_schema)
            response_data = response.json()['data']
            actual_onid = response_data['id']
            logging.debug(f'Requested onid: {onid}')
            logging.debug(f'Received onid: {actual_onid}')
            self.assertEqual(actual_onid.lower(), onid.lower())
            self.checking_spending_limits(response_data['attributes'])

    # Test case: GET /spendingauthority spending limits
    def checking_spending_limits(self, attributes):
        # Checking that the lists of spending limits and indexes are unique
        # Checking valid onids with spending authority only
        # To make sure that attributes and index are not empty
        non_empty_list_dict = {
            'attributes': attributes,
            'limits': attributes['limits']
        }

        for key, non_empty_list in non_empty_list_dict.items():
            logging.debug(f'{key} size: {len(non_empty_list)}')
            self.assertTrue(non_empty_list)

        spending_limit = []

        try:
            for limit in non_empty_list_dict['limits']:
                index_array = [index for index in limit['indexes']]
                # Checking that each spending limit has at least one index
                logging.debug(f'spending limit size: {len(limit["indexes"])}')
                self.assertTrue(limit['indexes'])
                spending_limit.append(limit['spendingLimit'])
        except KeyError as error:
            logging.debug(f'{error} don\'t exist')
            self.fail(error)

        # Comparing the size of the list with the size of the set of that
        # list doublications will be removed in a the set
        equal_list_dict = {
            'index_array': index_array,
            'spending_limit': spending_limit
        }

        for equal_list in equal_list_dict.values():
            self.assertEqual(len(equal_list), len(set(equal_list)))

    # Test case: GET /spendingauthority with invalid authority onids
    def test_get_non_authority_onids(self, endpoint='/spendingauthority'):
        for onid in self.test_cases['invalid_authority_onids']:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            spending_schema = []
            self.assertEqual(response.json()['data'], spending_schema)

    # Test case: GET /spendingauthority with bad request
    def test_bad_request_response(self, endpoint='/spendingauthority'):
        bad_params = [{'onid': ''}, {}]
        for bad_param in bad_params:
            response = utils.make_request(
                self,
                endpoint,
                400,
                params=bad_param
                )
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

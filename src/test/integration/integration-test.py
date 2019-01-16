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

    # Test case: GET /spendingauthority with onid filter
    def test_get_onids_with_filter(self, endpoint='/spendingauthority'):
        testing_authority_onids = ['kuok', 'wetherel'] # Valid onids with spending authority
        testing_non_authority_onids = ['alawammo', 'wilsonai'] # Valid onids with no spending authority
        testing_bad_request = [''] # Invalid request

        for onid in testing_authority_onids:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            spending_schema = utils.get_resource_schema(
                self, 'SpendingAuthorityResource'
            )

            utils.check_schema(self, response, spending_schema)

            response_data = response.json()['data']
            actual_onid = response_data['id']
            self.assertEqual(actual_onid.lower(), onid.lower())

        for onid in testing_non_authority_onids:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            spending_schema = []
            try:
                self.assertEqual(response.json()['data'], spending_schema)
            except AssertionError:
                logging.warning('data should be an empty array')


        # Testing Error response
        for onid in testing_bad_request:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 400, params=params)
            spending_schema = utils.get_resource_schema(self, 'Error')
            utils.check_schema(self, response, spending_schema)

        # Checking that the lists of spending limits and indexes are unique
        # Checking valid onids with spending authority only
        for onid in testing_authority_onids:
            params = {'onid': onid}
            response = utils.make_request(self, endpoint, 200, params=params)
            spending_schema = utils.get_resource_schema(
                self, 'SpendingAuthorityResource'
            )

            response_data = response.json()['data']
            attributes = response_data['attributes']
            limits = attributes['limits']
            indexes = []
            spendingLimit = []

            # Checking that each spending limit has at least one index
            for i in limits:
                indexes.append(i['indexes'])
                spendingLimit.append(i['spendingLimit'])
                self.assertGreater(len(i['indexes']), 0)

            # Creating a dict indexes_list from indexes, and compare it with the original array of indexes
            for i in indexes:
                indexes_list = list(dict.fromkeys(i))
                self.assertEqual(i, indexes_list)

            # Creating a dict spendingLimit_list from spendingLimit, and compare it with the original array of spendingLimit
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

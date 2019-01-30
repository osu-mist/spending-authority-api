# Spending Authority API Integration Tests

This directory contains template files that run integration tests against the API.

## Configuration

### Test on local instance

1. Start the API which should be tested locally.
2. copy
[configuration-example.json](./configuration-example.json) as `configuration.json`  and modify it as necessary. For example:

    ```json
    "local_test": true,
    "api": {
        "local_base_url": "https://localhost:8080/api/v1",
        ...
    },
    "auth": {
        "basic_auth": {
            "username": <username>,
            "password": <password>
        },
        ...
    },
    ...
    ```
3. Replace the fields for test_cases with existing usernames:

 ```json
    "test_cases": {
    "valid_authority_onids": [ "Users with authority"],
    "invalid_authority_onids": ["Users with no authority"],
    "bad_request": [""]
    }
    ...
    ```
### Test on production environment

1. Register an application via [OSU Developer Portal](https://developer.oregonstate.edu/)
2. Get `client_id` and `client_secret` from your app, then copy
[configuration-example.json](./configuration-example.json) as `configuration.json` and modify it as necessary. For example:

    ```json
    "local_test": false,
    "api": {
        ...
        "base_url": "https://api.oregonstate.edu/v1"
    },
    "auth": {
        ...
        "oauth2": {
            "token_api_url": "https://api.oregonstate.edu/oauth2/token",
            "client_id": <client_id>,
            "client_secret": <client_secret>
        }
    },
    ...
    ```

## Usage

1. Install dependencies via pip:

    ```shell
    $ pip install -r requirements.txt
    ```

2. Run the integration test:

    ```shell
    $ python integration-test.py -v --config path/to/configuration.json --openapi path/to/openapi.yaml
    ```

## Docker

Use these commands to build and run the tests in a container. All you need installed is Docker. **Make sure you are in the root directory of the repository**.

```shell
$ docker build -f src/test/integration/Dockerfile -t spendingauthority-integration-test .
$ docker run --rm \
             -v "$PWD"/src/test/integration/configuration.json:/usr/src/app/configuration.json:ro \
             spendingauthority-integration-test
```

### Test on local instance from the Docker container

* Mac users: replace `localhost` with `host.docker.internal` in the `configuration.json`.
* Linux users: add `--network=host` flag when performing `docker run` command.

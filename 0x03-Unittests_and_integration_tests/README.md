# Unittests and Integration Tests

This project covers unit testing and integration testing in Python using the unittest framework.

## Files

- `utils.py`: Utility functions including `access_nested_map`, `get_json`, and `memoize` decorator.
- `client.py`: GithubOrgClient class for interacting with GitHub API.
- `fixtures.py`: Test fixtures for integration tests.
- `test_utils.py`: Unit tests for utils.py functions.
- `test_client.py`: Unit and integration tests for client.py.

## Requirements

- Python 3.7+
- unittest
- parameterized
- requests

## Running Tests

To run the tests:

```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

## Learning Objectives

- Difference between unit and integration tests
- Mocking, parametrization, and fixtures
- Testing patterns in Python

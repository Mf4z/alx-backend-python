# 0x03. Unittests and Integration Tests

This project covers **unit testing** and **integration testing** in Python using the `unittest` framework.

The key goals are:

- Understand the **difference** between unit tests and integration tests.
- Learn how to write effective tests using:
  - `unittest`
  - `unittest.mock`
  - `parameterized`
  - mocking HTTP calls
  - mocking properties
  - testing memoization
- Practice writing **isolated unit tests** using mocks.
- Implement **integration tests** that mock only external requests.

## Files

- `utils.py` — Helper functions provided by ALX.
- `client.py` — GitHub API client provided by ALX.
- `fixtures.py` — Example payloads for integration tests.
- `test_utils.py` — Unit tests for `utils.py`:
  - `access_nested_map`
  - `get_json`
  - `memoize`
- `test_client.py` — Unit & integration tests for `GithubOrgClient`:
  - `org`
  - `_public_repos_url`
  - `public_repos`
  - `has_license`
  - Integration tests with fixtures

## Running Tests

Use Python 3:

```bash
python3 -m unittest -v test_utils
python3 -m unittest -v test_client

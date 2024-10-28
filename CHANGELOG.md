# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [8.0.0-post.1] - 2024-10-28
### Changed
- Modernize package quality tooling and configuration
- Add support for Python 3.13

## [8.0.0] - 2024-09-04
### Changed
- Updated to simpler typing syntax for optional arguments and iterable types using `pyupgrade`
- Reformatted files constrained to Python 3.8+ syntax using `black`
- Updated documentation to prefer `tox` usage
- Updated documentation dependencies and removed upper bounds on their versions
- Add support for Python 3.12
- Remove upper bound on dependencies

### Removed
- apiron no longer supports Python 3.7, which reached end of life on 2023-06-27
- apiron no longer supports Python 3.8, which reaches end of life on 2024-10-31

## [7.1.0-post.3] - 2023-06-20
### Fixed
- Update permissions in publishing workflow to allow publishing of files to GitHub releases

## [7.1.0-post.2] - 2023-06-20
### Changed
- Use `package` and `wheel_build_env` to speed up tests as this is a pure Python package. See the [tox docs](https://tox.wiki/en/latest/upgrading.html#universal-wheels) for more detail.

## [7.1.0-post.1] - 2023-04-24
### Changed
- Use PyPI trusted publishing instead of manual token authentication

## [7.1.0] - 2023-04-19
### Added
- You can now configure `retry_spec` and `timeout_spec` at the endpoint level. Calls to endpoints may override the endpoint-level configuration when necessary.

## [7.0.0] - 2022-12-07
### Fixed
- Ensure `py.typed` files end up in binary wheel distribution, which may break type checking for consumers

### Added
- Run tests against Python 3.11
- Stop ignoring imports during type checking

## [6.1.0] - 2021-12-22
### Added
- Add `py.typed` file so mypy can check against package types in downstream applications

## [6.0.1] - 2021-10-12
### Changed
- Use interpolation for logging messages to avoid wasted computation

## [6.0.0-post.1] - 2021-06-21
### Changed
- Move from Travis CI to GitHub Actions for testing and publishing
- Use PEP 517 builds

## [6.0.0] - 2021-06-14
### Added
- Testing matrix and trove classifiers for Python 3.9
- Type hints for all classes, methods, and functions

### Removed
- Support for Python 3.6 has been removed due to its impending end of life and the desire to leverage features from 3.7

### Changed
- Remove Python 3.10 testing and support for now, as Travis CI only has Python 3.10.0a5 which isn't compatible with recent pytest-randomly releases
- Indicate (by renaming) that all functions in the `client` module are private, except for `call`

## [5.1.0] - 2020-07-14
### Added
- Ability to specify `proxies` for a `Service` definition so all calls to the service use the defined proxies
- Ability to specify `auth` for a `Service` definition so all calls to the service use the defined authentication
- Ability to specify `return_raw_response_object` at the endpoint level, overridden by any value specified at call time

### Maintenance
- Add [pre-commit](https://pre-commit.com/) configuration for earlier linting and formatting checks

## [5.0.0] - 2019-12-02
### Removed
- Support for Python 3.4 and 3.5 has been removed based on official Python support timelines and usage statistics

## [4.2.0] - 2019-09-09
### Added
- Ability to pass dict to `files` keyword argument for file-like-objects for multipart encoding upload

## [4.1.0] - 2019-08-05
### Added
- Ability to run linting and build docs using `tox`
- Ability to access raw response object when making a call using `return_raw_response_object=True`.
  Useful for accessing things like response cookies or headers.

### Changed
- Moved implementation to `src/` directory for improved end-to-end testing with packaging.

## [4.0.0] - 2019-07-18
### Added
- An `endpoints` attribute on `Service` classes returns a list of that service's configured endpoints
- `Endpoint` classes now have a useful `__repr__` implementation, e.g. `"JsonEndpoint(path='/foo')"`.

### Changed
- `StubEndpoint` now inherits from `Endpoint` and as a result does not accept arbitrary keyword arguments
- Use `setup.cfg` for most project metadata and tool configuration, aside from `black`.

## [3.0.0] - 2019-06-20
### Added
- More testing for the bug fixed in v2.6.1

### Changed
- Extract `ServiceCaller` behaviors to module level and remove class
- Remove `path_kwargs` argument from the `call` function (previously a `ServiceCaller` method)

## [2.6.1] - 2019-06-06
### Added
- Backwards compatibility to allow `ServiceCaller.call()` to use endpoints that live in an instantiated `Service`

## [2.6.0] - 2019-06-05
### Added
- Ability to pass optional parameter `allow_redirects` to enable/disable HTTP redirection when calling an endpoint

### Changed
- Move to the descriptor protocol from metaclassing under the hood for turning an endpoint into a callable

## [2.5.0] - 2019-04-18
### Added
- Ability to pass dict to `json` keyword argument for raw POST body instead of form-encoded data
- Ability to use regular keyword arguments when calling an endpoint (instead of `path_kwargs`)

### Changed
- `DiscoverableService` now inherits from `ServiceBase`, an ancestor common with `Service`, instead of `Service` itself

## [2.4.0] - 2019-04-09
### Changed
- Simplify imports so that all commonly-used classes can be imported with `from apiron import <class>`

### Fixed
- Error in calling a dynamic stub endpoint

## [2.3.0] - 2019-03-25
### Added
- `pytest.ini` for `pytest` configuration
- Syntax sugar for calling endpoints

### Changed
- Update tests to use `pytest`-style `assert`s and fixtures (`unittest.mock` usage is still in place, for now)
- Make `--cov=apiron` the default when running `pytest`
- Make test output terse by default (`-v` when running restores previous behavior; `-vv` gives explicit test list)
- An endpoint's `stub_response` can optionally be a callable, for returning dynamic values in response to parameters

### Fixed
- End PyPI server URL with a slash to avoid a redirect, allowing deployment of build artifacts during release

## [2.2.0] - 2019-02-04
### Added
- Automated release artifact deployment via Travis CI's `providers` feature

### Changed
- The `endpoint` module has been split up into a module for each endpoint type, still importable as before

### Fixed
- Added the missing `wheel` dependency to `dev-requirements.txt` for creating a wheel distribution during release

## [2.1.0] - 2019-01-31
### Added
- Added ability to create a `StubEndpoint` for stubs

## [2.0.0] - 2019-01-03
### Removed
- The `check_for_trailing_slash` argument and default behavior has been removed

### Changed
- Service domains and endpoint paths were previously joined per [IETF RCF 1808](https://tools.ietf.org/html/rfc1808.html),
  which has surprising edge cases.
  These are now always joined by appending the endpoint path;
  the previous behavior can be achieved with multiple services or endpoints as needed.

## [1.1.0] - 2018-12-03
### Added
- Exposed ability to explicitly set the response encoding
- Expose pass-through `auth` argument to `requests`

### Changed
- Moved all tests to a top-level `tests` package and switched to using the `pytest` runner
- Added missing parameter in docstring for `apiron.client.ServiceCaller.call`
- Removed unused imports from `apiron.client`

## [1.0.0] - 2018-08-01
### Added
- Initial open source release of this package!
- Documentation on use and development of this package
- Code of conduct, contribution guide, and issue templates for contributors

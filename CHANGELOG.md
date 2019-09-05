# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- Ability to pass dict to `files` keyword argument for file-like-objects for multipart encoding upload

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

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

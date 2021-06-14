# Contributing to apiron

Thanks for taking the time to contribute to `apiron`!
Before you submit your work, take some time to read through these guidelines.
You should also read and follow the [code of conduct](../CODE_OF_CONDUCT.md).


## Submitting a pull request

All `apiron` changes and releases are done with the `dev` branch.
As such, when developing, please cut a branch from `dev` and open your pull request against `dev`.
We squash commits when merging to `dev`, so it's okay if you have several commits within your pull request.
That being said, please make sure your commit messages are clear so we can tell what's happening!


## Commits

### Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to run checks on the code prior to a successful commit.
Installing pre-commit and using its hooks can ease your development by uncovering issues earlier in the development life cycle.

### Commit messages

We don't currently have a strict commit message convention, but here are a few guidelines:

- Use the imperative, present tense: `Add cat pictures` rather than `Added cat pictures` or `I added some cat pictures`
- No punctuation at the end of the message -- if you need to describe something at length, do it in the body of the commit message
- If addressing a specific, open issue in full, prefix the commit message with the issue number and a colon [e.g. `#12: Add even more cats`]


## Testing

`apiron` is thoroughly tested.
Its current scope has let us reach 100% code coverage with fairly low effort, which may not always be possible.
Nonetheless, when fixing a bug it is helpful to us that you add a failing test that your fix makes pass.
If adding a new feature, it should also be thoroughly tested.
This allows for easier refactoring to prove that nothing broke in transit!

To test `apiron`, check out the repository and:

```
$ cd /path/to/apiron/
$ pyenv virtualenv 3.7.10 apiron  # pick your favorite virtual environment tool
$ pyenv local apiron:3.10-dev:3.9.4:3.8.9:3.7.10  # use any Python versions you want to test
(apiron:3.10-dev:3.9.4:3.8.9:3.7.10) $ pip install -e .[test]
(apiron:3.10-dev:3.9.4:3.8.9:3.7.10) $ pytest
```

If you have `tox` installed, you may instead run `tox` to run the full matrix of tests across all Python versions.


## Code formatting

This project uses [`black`](https://github.com/ambv/black) for consistent code formatting.
Before opening a pull request, try to remember to run `black` on your code; the build will fail otherwise.
Note that `black` requires Python 3.6+ to run, although it supports formatting compatible with earlier versions of Python.


## Release process

### Setup

To participate in the release process, you'll need the following:

* Accounts registered on [Test PyPI](https://test.pypi.org) and [PyPI](https://pypi.org) and added as maintainers of the [apiron project](https://pypi.org/project/apiron)
* An account registered on [Read the Docs](https://readthedocs.org/) and added as a maintainer of the [apiron project](https://readthedocs.org/projects/apiron/)
* A virtual environment with `tox` installed, and any Python versions you want to test against available on your `$PATH`

### Preparing a release

1. Once all changes for a release are approved and incorporated into `dev`, update the `setup.cfg` file to a new semantic version. Update `CHANGELOG.md` to reflect the new version and make sure all changes are reflected (see link in `CHANGELOG.md` for formatting).
1. Open a pull request titled something like "v3.X.X release prep" and merge to `dev`
1. Tag the head of `dev` as a new GitHub release matching the version in `setup.cfg`, using the body of the version's changes from `CHANGELOG.md` as the release description
1. Monitor the resulting build on [Travis CI](https://travis-ci.com/github/ithaka/apiron) to make sure the build artifacts are uploaded to PyPI and the GitHub release
1. Smoke check the documentation build on Read the Docs

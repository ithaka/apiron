# Contributing to apiron

Thanks for taking the time to contribute to `apiron`!
Before you submit your work, take some time to read through these guidelines.
You should also read and follow the [code of conduct](../CODE_OF_CONDUCT.md).


## Submitting a pull request

`apiron` releases are developed on the `dev` branch and only merged to `master` when a new release is imminent.
As such, when developing, please cut a branch from `dev` and open your pull request against `dev`.
We squash commits when merging to `dev`, so it's okay if you have several commits within your pull request.
That being said, please make sure your commit messages are clear so we can tell what's happening!


## Commit messages

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
$ pyenv virtualenv 3.7.3 apiron  # pick your favorite virtual environment tool
$ pyenv local apiron:3.8-dev:3.7.3:3.6.8:3.5.7:3.4.3  # use any Python versions you want to test
(apiron:3.8-dev:3.7.3:3.6.8:3.5.7:3.4.3) $ pip install -e .[test]
(apiron:3.8-dev:3.7.3:3.6.8:3.5.7:3.4.3) $ pytest
```

If you have `tox` installed, you may instead run `tox` to run the full matrix of tests across all Python versions.

## Code formatting

This project uses [`black`](https://github.com/ambv/black) for consistent code formatting.
Before opening a pull request, try to remember to run `black` on your code; the build will fail otherwise.
Note that `black` requires Python 3.6+ to run, although it supports formatting compatible with earlier versions of Python.

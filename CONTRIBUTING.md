# MiniWoB++ Contribution Guidelines

We welcome:

- Bug reports
- Pull requests for bug fixes
- Documentation improvements

## Contributing to the codebase

### Coding

Contributing code is done through standard github methods:

1. Fork this repo
2. Commit your code
3. Submit a pull request. It will be reviewed by maintainers and they'll give feedback or make requests as applicable

### Considerations
- Make sure your new code is properly tested and fully-covered
- Any fixes to environments should include fixes to the appropriate documentation

### Git hooks
The CI will run several checks on the new code pushed to the MiniWoB++ repository. These checks can also be run locally without waiting for the CI by following the steps below:
1. [install `pre-commit`](https://pre-commit.com/#install),
2. install the Git hooks by running `pre-commit install`.

Once those two steps are done, the Git hooks will be run automatically at every new commit. The Git hooks can also be run manually with `pre-commit run --all-files`, and if needed they can be skipped (not recommended) with `git commit --no-verify`. **Note:** you may have to run `pre-commit run --all-files` manually a couple of times to make it pass when you commit, as each formatting tool will first format the code and fail the first time but should pass the second time.

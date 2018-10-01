# apiron

`apiron` helps you cook a tasty client for RESTful APIs. Just don't wash it with SOAP.

<img src="docs/_static/cast-iron-skillet.png" alt="Pie in a cast iron skillet" width="200">

Gathering data from multiple services has become a ubiquitous task for web application developers.
The complexity can grow quickly:
calling an API endpoint with multiple parameter sets,
calling multiple API endpoints,
calling multiple endpoints in multiple APIs.
While the business logic can get hairy,
the code to interact with those APIs doesn't have to.

`apiron` provides declarative, structured configuration of services and endpoints
with a unified interface for interacting with them.


## Defining a service

A service definition requires a domain
and one or more endpoints with which to interact:

```python
from apiron.service.base import Service
from apiron.endpoint import JsonEndpoint

class GitHub(Service):
    domain = 'https://api.github.com'
    user = JsonEndpoint(path='/users/{username}')
    repo = JsonEndpoint(path='/repos/{org}/{repo}')
```


## Interacting with a service

Once your service definition is in place, you can interact with its endpoints
using the `ServiceCaller`:

```python
from apiron.client import ServiceCaller

github = GitHub()

response = ServiceCaller.call(
    github,
    github.user,
    path_kwargs={'username': 'defunkt'},
)  # {"name": "Chris Wanstrath", ...}

response = ServiceCaller.call(
    github,
    github.repo,
    path_kwargs={'org': 'github', 'repo': 'hub'},
)  # {"description": "hub helps you win at git.", ...}
```

To learn more about building clients, head over to [the docs](docs/).


## Contributing

We are happy to consider contributions via pull request,
especially if they address an existing bug or vulnerability.
Please read our [contribution guidelines](.github/CONTRIBUTING.md) before getting started.

## License

This package is available under the MIT license.
For more information, [view the full license and copyright notice](LICENSE).

Copyright 2018 Ithaka Harbors, Inc.

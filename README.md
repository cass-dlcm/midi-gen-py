# midi-gen-py
> Generates music compositions (with optional lightshows) using randomness and predefined patterns

![Lint, Type Check, Test](https://github.com/cassdelacruzmunoz/midi-gen-py/workflows/Lint,%20Type%20Check,%20Test/badge.svg)
![Package Application with Pyinstaller](https://github.com/cassdelacruzmunoz/midi-gen-py/workflows/Package%20Application%20with%20Pyinstaller/badge.svg)
[![codecov](https://codecov.io/gh/cassdelacruzmunoz/midi-gen-py/branch/master/graph/badge.svg)](https://codecov.io/gh/cassdelacruzmunoz/midi-gen-py)

![License](https://www.gnu.org/graphics/gplv3-or-later.png)

## Installation

Just download a compatible build from the [GitHub actions](https://github.com/cassdelacruzmunoz/midi-gen-py/actions?query=workflow%3A%22Package+Application+with+Pyinstaller%22), or clone the source.

## Usage example

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Install dependencies, then run linter, static type checker, and tests with code coverage.
```sh
python -m pip install --upgrade pip
python -m pip install -r src/requirements.txt
flake8 && mypy src tests && pytest --cov=src tests
```

## Release History

no releases ... yet

## Meta

Cassandra de la Cruz-Munoz – cassandra.delacruzmunoz@gmail.com

Distributed under the GNU GPL 3 or later license. See ``LICENSE`` for more information.

[https://github.com/cassdelacruzmunoz/github-link](https://github.com/cassdelacruzmunoz/)

## Contributing

1. Fork it (<https://github.com/cassdelacruzmunoz/midi-gen-py/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

[wiki]: https://github.com/cassdelacruzmunoz/midi-gen-py/wiki

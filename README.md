# Timeseries

Python exercise

![Tests](https://github.com/rcbop/python-timeseries/actions/workflows/ci.yaml/badge.svg)[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries?ref=badge_shield)
&nbsp;&nbsp;[![codecov](https://codecov.io/gh/rcbop/timeseries-visualization/branch/main/graph/badge.svg?token=ijcD6RzE8L)](https://codecov.io/gh/rcbop/timeseries-visualization)&nbsp;&nbsp;[![CodeQL](https://github.com/rcbop/python-timeseries/workflows/CodeQL/badge.svg)](https://github.com/rcbop/python-timeseries/actions/workflows/github-code-scanning/codeql)

## Requirements

- [Pyenv](https://github.com/pyenv/pyenv)
- [Pyenv virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- `GNU make`

## Development

Run all tests with docker compose:

```
make test
```

Spin up development environment:

```
make compose-up
```

## Query String Filters

API endpoint with query string filters deep-object like:

```
?timestamp[gte]=2021-01-01T00:00:00&timestamp[lte]=2021-01-05T00:00:00&metadata.area=kitchen&limit=100"
```

will become mongo query:

```
{
    "timestamp": { $gte: ISODate("2021-01-01T00:00:00"), $lte: ISODate("2021-01-05T00:00:00") },
    "metadata": { "area": "kitchen" },
    "limit": 100
}
```

## Preview

Query result:

![query-result](./docs/query_result.png)

Dashboard:

![dashboard](./docs/dashboard.png)

## TODO

check usage of [mongo engine ORM](http://mongoengine.org/) with timeseries collection


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries?ref=badge_large)

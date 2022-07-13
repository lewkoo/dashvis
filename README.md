<p align="center">
  <a href="https://github.com/lewkoo/dashvis">
    <img src="https://github.com/lewkoo/dashvis/blob/main/readme_images/DashVis_Logo.png?raw=true" alt="vis.js logo" width="500" height="200">
  </a>
</p>

<h3 align="center">DashVis Component</h3>

<p align="center">
  Full implementation of vis.js network framework for Plotly Dash
  <br>
  <a href="https://visjs.github.io/vis-network/docs/network/">Explore the documentation</a>
  ·
  <a href="https://github.com/lewkoo/dashvis/issues/new?template=bug.md">Report a bug</a>
  ·
  <a href="https://github.com/lewkoo/dashvis/issues/new?template=feature.md">Request a feature</a>
  <br>
  <br>
  <img alt="GitHub Actions" src="https://github.com/facultyai/dash-bootstrap-components/workflows/Tests/badge.svg?branch=main">
  <img alt="GitHub" src="https://img.shields.io/github/license/lewkoo/dashvis">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/dashvis">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/dashvis">
</p>

A full implementation of [vis.js][visjs-homepage] Network component for [Dash Plotly][dash-homepage]. Useful for displaying dynamic, automatically organised, customizable network views.

## Table of contents

- [Table of contents](#table-of-contents)
- [Installation](#installation)
  - [PyPI](#pypi)
- [Quick start](#quick-start)
- [See how it is used](#see-how-it-is-used)
- [Contributing](#contributing)
- [Future work 🔨](#future-work-)

## Installation

### PyPI

You can install _dashvis_ with `pip`:

```sh
pip install dashvis
```

## Quick start

_dashvis_ exposes a single component, _DashNetwork_. Simply create one and include it in your Dash layout. Simplest example:

```python
import dash
from dashvis import DashNetwork

app = dash.Dash()
app.layout = html.Div([
    DashNetwork()
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

## See how it is used

<!-- # TODO: update usage.py -->

1. Run: 
```python
python -m venv dashvis-venv 
source dashvis-venv/bin/activate 
pip install -r requirements.txt
python usage.py
```
2. Visit <http://localhost:8050> in your web browser

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Future work 🔨

- [ ] Update `usage.py`
- [ ] Fix two disabled `vis.js` function calls
- [ ] Add tests and code coverage badges
- [ ] Update this README

[dash-homepage]: https://dash.plotly.com/
[visjs-homepage]: https://visjs.github.io/vis-network/docs/network/
[bug-report]: https://github.com/lewkoo/dashvis/issues/new?template=bug.md
[feature-request]: https://github.com/lewkoo/dashvis/issues/new?template=feature.md
[contribution-guide]: https://github.com/lewkoo/dashvis/blob/main/.github/CONTRIBUTING.md

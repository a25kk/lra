# lra.sitecontent

## Sitecontent package containing folderish content pages

* `Source code @ GitHub <https://github.com/potzenheimer/lra.sitecontent>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/lra.sitecontent>`_
* `Documentation @ ReadTheDocs <http://lrasitecontent.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/potzenheimer/lra.sitecontent>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

The generated Python package hold the necessary scaffold to add content types
via the 'contenttype' template and to add functionality.

In order to get productive you still need to generate a contenttype

```bash
$ cd lra.sitecontent/src/lra/sitecontent/
$ mrbob --config ~/.mrbob.ini -O example_type bobtemplates:contenttype

```


## Installation

To install `lra.sitecontent` you simply add ``lra.sitecontent``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `lra.sitecontent` using the Add-ons control panel.

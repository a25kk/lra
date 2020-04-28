# LRA
   
   ## Landratsamt Aichach Portal
   
   * `Source code @ GitHub <https://github.com/a25kk/lra>`_
   * `Releases @ PyPI <http://pypi.python.org/pypi/lra>`_
   * `Documentation @ ReadTheDocs <http://lra.readthedocs.org>`_
   * `Continuous Integration @ Travis-CI <http://travis-ci.org/kreativkombinat/lra>`_
   
   
   ## Installation
   
   This buildout is intended to be used via the development profile to provide
   a ready to work on setup. The relevant steps to get started with a new
   development environment would be:
   

Setup python mysql

   
   ``` bash
   $ virtualenv-2.7 lra
   $ cd ./lra
   $ git clone git@github.com:username/lra.git buildout.lra
   $ cd ./buildout.lra
   $ python bootstrap.py -c development.cfg
   $ bin/buildout -Nc development.cfg
   ```

# LRA
   
   ## Landratsamt Aichach Portal
   
   * `Source code @ GitHub <https://github.com/a25kk/lra>`_
   * `Releases @ PyPI <http://pypi.python.org/pypi/lra>`_
   * `Documentation @ ReadTheDocs <http://lra.readthedocs.org>`_
   * `Continuous Integration @ Travis-CI <http://travis-ci.org/kreativkombinat/lra>`_
   
   
   ## Installation
   
   This buildout is intended to be used via the development profile to provide
   a ready to work on setup. To get started with a new development environment
   clone the buildout to your local machine and initialize the buildout:
   
   ``` bash
   $ git clone git@git.team23.de/a25kk/lra.git
   $ cd ./lra
   $ b5 install
   ```
   
   We use the globally installed task runner `b5` for the project. The buildout is intended to be used with a docker setup that mirrors the production environment. Therefore the build requires a local docker and traefik installation.
   
   Alternatively you can use the provided installation script
   
   ```bash
   chmod 777 ./bootstrap.sh
   ./bootstrap.sh -c development.cfg
   ```

### Compatibility with OSX mariadb setup

```bash
brew unlink mariadb

brew install mariadb-connector-c
ln -s /usr/local/opt/mariadb-connector-c/bin/mariadb_config /usr/local/bin/mysql_config

pip install mysqlclient

rm /usr/local/bin/mysql_config
brew unlink mariadb-connector-c
brew link mariadb
```
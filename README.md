# Calls API - OList test 
This is a RESTFul API developed in Python that has two main features:
- Receives call detail records and store 
- Calculate monthly bills for a given telephone number.

## Built With
- [Python 3.7](https://docs.python.org/3/whatsnew/3.7.html)
- [Flask](http://flask.pocoo.org/)
- [Flask RestPlus](http://flask-restplus.readthedocs.io/)
- [Flask SQL Alchemy](http://flask-sqlalchemy.pocoo.org/)
- [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker](https://www.docker.com/)
- [PostGresSQL](https://www.postgresql.org/)

## How to **Run**

Don't forget to prepare and activate your virtual env, then install your environment:

```
make install
```

Make sure you run the local database:
```
make create_db_dev
```

Update your database running the migrations:
```
make apply_upgrade_dev 
```

Then, run the API:
```
make run_dev
```
> Observation: We use flake8 to standardize the code style. The `make run_dev` will give you errors if your code has problems.

## Database models
We use SQL Alchemy as ORM. 
After create a new database model(folder `app/db_models`), you have to generate the migrations file:
```
make generate_migrate
```

## How to **Test**

To run the tests and show the code coverage report, run the command below:

```
make test
```

# Work environment

## Operational System 

[Ubuntu 18.04.1 LTS (Bionic Beaver)
](http://releases.ubuntu.com/18.04/)

## IDE 

[VSCode](https://code.visualstudio.com/)

### Extensions in VSCode: 
``` 
dbaeumer.vscode-eslint
dracula-theme.theme-dracula
eamodio.gitlens
felipecaputo.git-project-manager
ms-python.python
PeterJausovec.vscode-docker
redhat.java
redhat.vscode-yaml
robertohuertasm.vscode-icons
Shan.code-settings-sync
VisualStudioExptTeam.vscodeintellicode
vscjava.vscode-java-debug
vscjava.vscode-java-pack
vscjava.vscode-java-test
vscjava.vscode-maven
yzhang.markdown-all-in-one
```
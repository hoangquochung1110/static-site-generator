Init virtual environment
```
pyenv virtualenv 3.10.1 <env_name>
pyenv shell <env_name>
pyenv local <env_name>
```

Install `pre-commit``

```
pip install pre-commit
pre-commit install
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

Install packages
```
pip install -r requirements.txt
````

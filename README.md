```bash
$ git clone https://shravankeshav@bitbucket.org/projexelmauritius/meteohub.datafeeder.git
```

##### Requirements
* Python 3
* Pip 3

```bash
$ brew install python3
```

Pip3 is installed with Python3

##### Setup Virtual Environment
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

##### Usage
```bash
$ virtualenv -p python3 <desired-path>
```

Activate the virtualenv:
```bash
$ source <desired-path>/bin/activate
```

Deactivate the virtualenv:
```bash
$ deactivate
```


##### Adding New Package
```bash
$ pip install <packagename>
$ pip freeze > requirements.txt
```

##### Restore Package
```bash
$ pip install -r requirements.txt
```


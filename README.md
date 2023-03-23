# CognitiveEquinox23

Soundtrack for news

## Development

### Faster development

To mount code as volume for faster development use next recipe.

```bash
cp docker-compose.override.yml{.tmpl,}
```

Edit your *docker-compose.override.yml* file for more custom modifications.

### Load data

Download dataset from https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019 and copy
to *api/resources* directory

``` bash
$ docker-compose run -it api /bin/bash
root@1835f1a2da0c:/code# PYTHONPATH="/code" python app/provisioning/parse_songs.py
root@1835f1a2da0c:/code# PYTHONPATH="/code" python app/provisioning/add_songs.py
```
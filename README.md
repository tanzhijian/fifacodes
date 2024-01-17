# fifacodes

FIFA country codes query and search.

A mapping of FIFA country codes to country names.

The default data is sourced from [Wikipedia](https://en.wikipedia.org/wiki/List_of_FIFA_country_codes).

## Installation

```
pip install fifacodes
```

## Usage

You can query like using dict：

```pycon
>>> from fifacodes import Counties
>>> counties = Counties()
>>> counties.get('ENG')
Country(code='ENG', name='England')
>>> len(counties)
211
>>> list(counties.items())[0]
('AFG', Country(code='AFG', name='Afghanistan'))
```

Query by name:

```pycon
>>> counties['England']
Country(code='ENG', name='England')
```

Search for a country by name or code, the search uses fuzzy string matching to find potential results.

```pycon
>>> counties.search('ARG')
[Country(code='ARG', name='Argentina'), Country(code='AFG', name='Afghanistan'), Country(code='ALG', name='Algeria')]
```

Results can be adjusted using parameters:

```pycon
>>> counties.search('Fran', limit=2, score_cutoff=70)
[Country(code='FRA', name='France'), Country(code='IRN', name='Iran')]
```

Search for a country by name or code and return the first result.

```pycon
>>> counties.search_one('Argent')
Country(code='ARG', name='Argentina')
```

## Data Update

To update `default.csv` run `scrape.py`, If there are codes corresponding to other country names, add them to `custom.csv`.

View source code for detailed usage.

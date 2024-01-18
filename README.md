# fifacodes

FIFA member associations codes query and search.

A mapping of FIFA member associations codes to member associations names.

The default data is sourced from [Wikipedia](https://en.wikipedia.org/wiki/List_of_FIFA_country_codes).

## Installation

```
pip install fifacodes
```

## Usage

You can query like using dict：

```pycon
>>> from fifacodes import Members
>>> members = Members()
>>> members.get('ENG')
Member(code='ENG', name='England')
>>> len(members)
211
>>> list(members.items())[0]
('AFG', Member(code='AFG', name='Afghanistan'))
```

Query by name:

```pycon
>>> members['England']
Member(code='ENG', name='England')
```

Search for a member by name or code, the search uses fuzzy string matching to find potential results.

```pycon
>>> members.search('argtl')
[Member(code='ARG', name='Argentina'), Member(code='ARM', name='Armenia'), Member(code='ARU', name='Aruba')]
```

Results can be adjusted using parameters:

```pycon
>>> members.search('Fran', limit=2, score_cutoff=70, case_sensitive=True)
[Member(code='FRA', name='France'), Member(code='IRN', name='Iran')]
```

Search for a member by name or code and return the first result.

```pycon
>>> members.search_one('Argent')
Member(code='ARG', name='Argentina')
```

## Data Update

To update `default.csv` run `scrape.py`, If there are codes corresponding to other member names, add them to `custom.csv`.

View source code for detailed usage.

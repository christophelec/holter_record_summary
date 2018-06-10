# Holter record summary

See [instructions](./instructions.md)

## How to use :

First, clone the repo and cd into it :

```bash
git clone git@github.com:christophelec/holter_record_summary.git
cd holter_record_summary
```

### General help :

```bash
python hrs.py -h
```

### Premature P waves and QRS complexes

```bash
python hrs.py prematures record.csv
```

### Mean heart rate

```bash
python hrs.py mean_heart_rate record.csv
```

### Min and max heart rate

Relative to the beginning :

```bash
python hrs.py min_max_hr record.csv
```

Relative to a date, for example now (input is a timestamp):

```
python hrs.py min_max_hr --start-timestamp `date +%s` record.csv
```

### Tests

```bash
pytest
```
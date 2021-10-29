# bmrb-query

This repository has an example on how to download all the NMR-STAR files for macromolecules in the
BMRB database and then perform a query on them, and then extract some data.

First, clone this project by opening a terminal and running: `git clone https://github.com/bmrb-io/query-bmrb.git`.

Next, run `setup_environment.sh` to download the BMRB entries and prepare a Python virtual environment
with the necessary dependencies.

Finally, run `source venv/bin/activate` once, and then you can run `./search.py` however many times you desire,
modifying it between runs if necessary.
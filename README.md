# Enron
This repository contains a Python project that builds email correspondences analytics for Enron email data. The current implementation of this project implements the following:

1. A .csv file with three columns---"person", "sent", "received"---where the final two columns contain
 the number of emails that person sent or received ordered by number of sent emails.

2. A PNG image visualizing the number of emails sent over time by some of the most prolific person
 , top-N senders in (1). 

3. A visualization that shows the [relative contact ratio](https://en.wikipedia.org/wiki/Relative_change_and_difference) for the same people in (2).


## Data

The [Enron event history](https://github.com/aidinhass/enron/blob/master/enron/data/raw/enron-event-history-all.csv) (.csv, adapted from the widely-used publicly available data set) is included in this repo. The columns contain:

* **time** - time is Unix time (in milliseconds)
* **message identifier**
* **sender**
* **recipients** - pipe-separated list of email recipients
* **topic** - always empty
* **mode** - always "email"

## Requirements
- python                3.6
- numpy                 1.15.1
- pandas                0.23.4 
- jupyter               1.0.0
- notebook              5.6.0
- nb_conda              2.2.1
- plotly                3.2.1
- plotly-orca           1.1.1
- psutil                5.4.7 

## Directory Structure

```
.
├── enro                <- source files used in this projectn.
│   ├── data
│   │   ├── ex          <- raw data utilized in this project.
│   │   └── raw         <- data files created in this project.
│   └── scripts         <- script files used in this project.
│      
├── images              <- Images for summary trend plots. 
└── notebooks           <- Ipython notebook files.
```
## Installation

Install python dependencies from  `conda-requirements.txt` using conda.
```bash
conda install --yes --file conda-requirements.txt
```

Or create a new conda environment `<new-env-name>` by importing a copy of a working conda environment `conda-enron.yml` at the project root directory :.
```bash
conda env create --name <new-env-name> -f conda-enron.yml
```
## Usage

```
Create summary of Enron email correspondences

optional arguments:
  -h, --help            show this help message and exit
  -t TOPN, --topn TOPN  Top-N sender. Default=`5`
  -s START, --start START
                        Start date in Year-Month. Default=1998-05
  -d END, --end END     End date in Year-Month. Default=2002-12

Example of use: `python -m enron.scripts.summarize --topn 5 --start 1998-05
--end 2002-12`

```

## To Do
- [ ] Add start/end date features

## License
MIT License


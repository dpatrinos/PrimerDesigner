# PrimerDesigner
[![GNU General Public License 3.0](https://img.shields.io/badge/license-GPLv3-blue)](https://github.com/dpatrinos/PrimerDesigner/blob/main/LICENSE)

A Python-based CLI that uses the NCBI mRatBN7.2 assembly to create nucleotide sequences for the designing of primers to target exon-exon splice junctions

## Installation

```sh
$ wget https://github.com/dpatrinos/PrimerDesigner/archive/refs/tags/v0.2.0.tar.gz
$ tar -xzf v0.2.0.tar.gz
$ pip install -e PrimerDesigner-0.2.0
```

## Usage

```sh
$ primerdesigner -h

### OUTPUT
# usage: primerdesigner [-h] (-c | -s) (-p | -m) [--chr CHR] [--start START] [--stop STOP] [--intron INTRON] [--sjPath SJPATH] [--left LEFT] [--right RIGHT]
#                       [--destination DESTINATION]
# usage: primerdesigner [-h] (-c | -s) (-p | -m) [--chr CHR] [--start START] [--stop STOP] [--intron INTRON] [--sjPath SJPATH] [--left LEFT] [--right RIGHT]
#                       [--destination DESTINATION]
# 
# Create sequence for design of primers to span an exon-exon junction
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -c, --coordinates     Create a sequence from a chromosome, start position, and stop position
#   -s, --sj              Create a sequence from a X-labeled splice junction dataset. See --sjPath for more information
#   -p, --plus            Intron is on the plus strand
#   -m, --minus           Intron is on the minus strand
#   --chr CHR             Chromosome number (e.g. 1)
#   --start START         Chromosome-relative coordinate of the start of the intron
#   --stop STOP           Chromosome-relative coordinate of the start of the intron
#   --intron INTRON       Intron X of the splice junction to use
#   --sjPath SJPATH       Path to the splice junction dataset: /path/to/sjdblist.csv or /path/to/sjdblist.tab. Note: the splice junction dataset must be in
#                         the format of Column 1: X; Column 2: Accession Version; Column 3: Start Position; Column 4: Stop Position
#   --left LEFT           Number of bases to the left of the start position to include. Default: 150bp
#   --right RIGHT         Number of bases to the right of the stop position to include. Default: 150bp
#   --destination DESTINATION
#                         Path to directory to save the sequence to /path/to/destination. Default: current working directory
```

## Examples

### Generate sequences from chromosome number and intron start and stop coordinates

```sh
$ primerdesigner -c -p --chr 1 --start 163310 --stop 163645

### OUTPUT
# Chromosome 1 sequence loaded
# 300bp sequence length constructed
# chr1_163310-163645.fasta created in /current/working/directory
# chr1_163310-163645.fasta created in /current/working/directory
```

### Generate sequences from an X-labeled splice junction dataset

```sh
$ primerdesigner -s -p --intron 1 --sjPath /path/to/sjdblist.csv

### OUTPUT
# Intron 1
# Intron 1
# NC_051336.1: 163310:163645
# Chromosome 1 sequence loaded
# 300bp sequence length constructed
# chr1_163310-163645.fasta created in /current/working/directory
# chr1_163310-163645.fasta created in /current/working/directory
```

The splice junction dataset needs to be a .csv or .tab file organized as follows:
 
![SJ table example](sj.png)

## Compatibility

PrimerDesigner has been tested on Ubuntu 20.04.6 using Python 3.8.12 and Windows 11 22621.1555 using Python 3.8.8. Installation and usage is shown only in Ubuntu, but can be done in Windows using the OS's equivalent commands.

## License

PrimerDesigner is released under an [GNU General Public License v3.0](https://github.com/dpatrinos/PrimerDesigner/blob/main/LICENSE) license.

## Acknowledgements

 - [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/10116/)
 - Jacob S. Roberts, Ron A. Perets, Kathryn S. Sarfert, John J. Bowman, Patrick A. Ozark, Gregg B. Whitworth, Sarah N. Blythe, and Natalia Toporikova, High-fat high-sugar diet induces polycystic ovary syndrome in a rodent model, *Biology of Reproduction*, Volume 96, Issue 3, March 2017, Pages 551–562, https://doi.org/10.1095/biolreprod.116.142786
 - Washington and Lee University Summer Research Scholars Program, Lexington, VA

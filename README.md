
# PrimerDesigner
[![GNU General Public License 3.0](https://img.shields.io/badge/license-GPLv3-blue)](https://github.com/dpatrinos/PrimerDesigner/blob/main/LICENSE)

A Python-based CLI that uses the NCBI mRatBN7.2 assembly to create nucleotide sequences for the designing of primers to target exon-exon splice junctions

## Installation

```sh
$ wget https://github.com/dpatrinos/PrimerDesigner/archive/refs/tags/v0.1.0.tar.gz
$ tar -xzf v0.1.0.tar.gz
$ pip install -e primerdesigner
```

## Usage

```sh
$ primerdesigner -h

### OUTPUT
# usage: primerdesigner [-h] (-c | -s) [--accessionVersion ACCESSIONVERSION | --chromosome CHROMOSOME]
#                       [--startPos STARTPOS] [--stopPos STOPPOS] [--intronX INTRONX] [--sjPath SJPATH]
#                       [--bpLeft BPLEFT] [--bpRight BPRIGHT] --destination DESTINATION
# 
# Create sequence for design of primers to span an exon-exon junction
# 
# optional arguments:
#   -h, --help                    show this help message and exit
#   -c, --coordinates             Create a sequence from a chromosome, start position, and stop position
#   -s, --sjDataset               Create a sequence from a X-labeled splice junction dataset. See --sjPath for more information
#   --accVersion ACCVERSION       Molecule name as accession.version (e.g. NC_000001.11)
#   --chromosome CHROMOSOME       Chromosome number (e.g. 1). Note: Either --accessionVersion or --chromosome must be specified, but not both
#   --startPos STARTPOS           Chromosome-relative coordinate of the start of the intron
#   --stopPos STOPPOS             Chromosome-relative coordinate of the start of the intron
#   --intronX INTRONX             Intron X of the splice junction to use
#   --sjPath SJPATH               Path to the splice junction dataset: /path/to/sjdblist.csv or /path/to/sjdblist.tab. 
#                                 Note: the splice junction dataset must be in the format of Column 1: X; Column 2: Accession Version; Column 3: Start Position; Column 4: Stop Position
#   --bpLeft BPLEFT               Number of bases to the left of the start position to include. Default: 150bp
#   --bpRight BPRIGHT             Number of bases to the right of the stop position to include. Default: 150bp
#   --destination DESTINATION     Path to directory to save the sequence to: /path/to/destination
```

## Examples

### Generate sequences from chromosome number and intron start and stop coordinates

```sh
$ primerdesigner -c --chromosome 1 --startPos 163310 --stopPos 163645 --destination /path/to/destination

### OUTPUT
# Chromosome 1 sequence loaded
# 300bp sequence length constructed
# chr1_163310-163645.fasta created in /path/to/destination
```

### Generate sequences from an X-labeled splice junction dataset

```sh
$ primerdesigner -s --intronX 1 --sjPath /path/to/sjdblist.csv --destination /path/to/destination

### OUTPUT
# Novel intron 1
# NC_051336.1: 163310:163645
# Chromosome 1 sequence loaded
# 300bp sequence length constructed
# chr1_163310-163645.fasta created in /path/to/destination
```

The splice junction dataset needs to be a .csv or .tab file organized as follows:
 
![SJ table example](sj.png)

## License

PrimerDesigner is released under an [GNU General Public License v3.0](https://github.com/dpatrinos/PrimerDesigner/blob/main/LICENSE) license.

## Acknowledgements

 - [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/10116/)
 - Jacob S. Roberts, Ron A. Perets, Kathryn S. Sarfert, John J. Bowman, Patrick A. Ozark, Gregg B. Whitworth, Sarah N. Blythe, and Natalia Toporikova, High-fat high-sugar diet induces polycystic ovary syndrome in a rodent model, *Biology of Reproduction*, Volume 96, Issue 3, March 2017, Pages 551–562, https://doi.org/10.1095/biolreprod.116.142786
 - Washington and Lee University Summer Research Scholars Program, Lexington, VA

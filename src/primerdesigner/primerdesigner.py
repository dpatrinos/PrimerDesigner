#!python
# coding: utf-8

import pandas as pd
import fastaparser as fp
from argparse import ArgumentParser
import pkg_resources
import pathlib
import gzip
import os
import sys

def fromCoordinates(molecule_chromosome, start_pos, stop_pos, bp_left, bp_right, destination_dir):
    DATA_PATH = pkg_resources.resource_filename("primerdesigner", "data")

    if "NC_" in molecule_chromosome:
        with open(os.path.abspath(os.path.join(DATA_PATH, "chr2acc.txt")), "r") as f:
            chr2acc = pd.read_csv(f, sep="\t", header=None, comment = "#")
            chromosome = chr2acc.loc[chr2acc[1] == molecule_chromosome, 0].iloc[0]
    
    else:
        chromosome = molecule_chromosome
    
    with gzip.open(os.path.abspath(os.path.join(DATA_PATH, "chr{}.fna.gz".format(chromosome))), mode="rt") as f:
        next(f)
        chromosome_sequence = f.read().replace("\n", "")

    print("Chromosome", chromosome, "sequence loaded")

    five_sequence = chromosome_sequence[(start_pos-bp_left-1):start_pos]
    three_sequence = chromosome_sequence[(stop_pos+1):(stop_pos+bp_right)]
    complete_sequence = five_sequence + three_sequence
    print(str(len(complete_sequence)) + "bp sequence length constructed")

    destination_dir = pathlib.Path(destination_dir).expanduser().resolve()

    with open(os.path.join(destination_dir, "chr{}_{}-{}.fasta".format(chromosome, start_pos, stop_pos)), "w") as fasta_file:
        writer = fp.Writer(fasta_file)
        header = ('Sequence spanning exon-exon junction of intron {}:{} on chromosome {}').format(start_pos, stop_pos, chromosome)
        writer.writefasta((header, complete_sequence))
    
    print("chr{}_{}-{}.fasta".format(chromosome, start_pos, stop_pos) + " created in " + str(destination_dir))

def fromSJDataset(intron_X, bp_left, bp_right, sj_path, destination_dir):
    if sj_path.endswith(".csv"):
        with open(sj_path, "r") as f:
            sj_dataset = pd.read_csv(f)

    elif sj_path.endswith(".tab"):
        with open(sj_path, "r") as f:
            sj_dataset = pd.read_csv(f, sep="\t")

    row = sj_dataset.loc[sj_dataset.iloc[:,0] == intron_X]
    molecule = row.iat[0, 1]
    start_pos = int(row.iat[0, 2])
    stop_pos = int(row.iat[0, 3])
    print("\nNovel intron " + str(intron_X) + "\n" + molecule + ": " + str(start_pos) + ":" + str(stop_pos))

    fromCoordinates(molecule, start_pos, stop_pos, bp_left, bp_right, destination_dir)

def main():
    parser = ArgumentParser(
        prog = "primerdesigner",
        description = "Create sequence for design of primers to span an exon-exon junction"
    )

    run_mode = parser.add_mutually_exclusive_group(required=True)
    run_mode.add_argument('-c', '--coordinates', action='store_true', help="Create a sequence from a chromosome, start position, and stop position")
    run_mode.add_argument('-s', '--sjDataset', action='store_true', help="Create a sequence from a X-labeled splice junction dataset. See --sjDatasetPath for more information")

    molecule_chromosome = parser.add_mutually_exclusive_group(required='--coordinates' in sys.argv)
    molecule_chromosome.add_argument('--accessionVersion', type=str, help='Molecule name as accession.version (e.g. NC_000001.11)')
    molecule_chromosome.add_argument('--chromosome', type=str, help='Chromosome number (e.g. 1). Note: Either --accessionVersion or --chromosome must be specified, but not both')
    parser.add_argument('--startPos', required='--coordinates' in sys.argv, type=int, help='Chromosome-relative coordinate of the start of the intron')
    parser.add_argument('--stopPos', required='--coordinates' in sys.argv, type=int, help='Chromosome-relative coordinate of the start of the intron')

    parser.add_argument('--intronX', required='--sjDataset' in sys.argv, type=int, help='Intron X of the splice junction to use')
    parser.add_argument('--sjPath', required='--sjDataset' in sys.argv, type=str, help='Path to the splice junction dataset: /path/to/sjdblist.csv or /path/to/sjdblist.tab. Note: the splice junction dataset must be in the format of Column 1: X; Column 2: Accession Version; Column 3: Start Position; Column 4: Stop Position')

    parser.add_argument('--bpLeft', default=150, type=int, help='Number of bases to the left of the start position to include. Default: 150bp')
    parser.add_argument('--bpRight', default=150, type=int, help='Number of bases to the right of the stop position to include. Default: 150bp')

    parser.add_argument('--destination', required=True, type=str, help='Path to directory to save the sequence to: /path/to/destination')

    args = parser.parse_args()

    if not pathlib.Path(args.destination).expanduser().resolve().exists():
        parser.exit(1, message="Destination directory does not exist")

    if args.coordinates == True:
        if args.accessionVersion != None:
            fromCoordinates(args.accessionVersion, args.startPos, args.stopPos, args.bpLeft, args.bpRight, args.destination)
        elif args.chromosome != None:
            fromCoordinates(args.chromosome, args.startPos, args.stopPos, args.bpLeft, args.bpRight, args.destination)
    
    elif args.sjDataset == True:
        fromSJDataset(args.intronX, args.bpLeft, args.bpRight, args.sjPath, args.destination)
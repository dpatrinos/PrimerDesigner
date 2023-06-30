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

def fromCoordinates(molecule_chromosome, strand, start_pos, stop_pos, bp_left, bp_right, destination):
    DATA_PATH = pkg_resources.resource_filename("primerdesigner", "data")

    if "NC_" in molecule_chromosome:
        with open(os.path.abspath(os.path.join(DATA_PATH, "chr2acc.txt")), "r") as f:
            chr2acc = pd.read_csv(f, sep="\t", header=None, comment = "#")
            chromosome = chr2acc.loc[chr2acc[1] == molecule_chromosome, 0].iloc[0]
    
    else:
        chromosome = molecule_chromosome
    
    with gzip.open(os.path.abspath(os.path.join(DATA_PATH, "chr{}.fna.gz".format(chromosome))), mode="rt") as f:
        next(f)
        chromosome_sequence = "X" + f.read().replace("\n", "") # X is a dummy character to make the sequence 1-based

    print("Chromosome", chromosome, "sequence loaded")
    
    five_sequence = chromosome_sequence[(start_pos-bp_left):start_pos]
    three_sequence = chromosome_sequence[(stop_pos+1):(stop_pos+bp_right+1)]
    complete_sequence = five_sequence + three_sequence
    print(str(len(complete_sequence)) + "bp sequence length constructed")
        
    if strand == "-":
        complement_sequence = fp.FastaSequence(complete_sequence).complement(reverse=True).sequence_as_string()
        complete_sequence = complement_sequence

    destination = pathlib.Path(destination).expanduser().resolve()

    with open(os.path.join(destination, "chr{}_{}-{}.fasta".format(chromosome, start_pos, stop_pos)), "w") as fasta_file:
        writer = fp.Writer(fasta_file)
        header = ('{} strand sequence spanning exon-exon junction of intron {}:{} on chromosome {} [{}bp left; {}bp right]').format(strand, start_pos, stop_pos, chromosome, bp_left, bp_right)
        writer.writefasta((header, complete_sequence))
    
    print("chr{}_{}-{}.fasta".format(chromosome, start_pos, stop_pos) + " created in " + str(destination))

def fromSJDataset(intron_X, strand, bp_left, bp_right, sj_path, destination):
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
    print("\nIntron " + str(intron_X) + "\n" + molecule + ": " + str(start_pos) + ":" + str(stop_pos))

    fromCoordinates(molecule, strand, start_pos, stop_pos, bp_left, bp_right, destination)

def main():
    parser = ArgumentParser(
        prog = "primerdesigner",
        description = "Create sequence for design of primers to span an exon-exon junction"
    )

    run_mode = parser.add_mutually_exclusive_group(required=True)
    run_mode.add_argument('-c', '--coordinates', action='store_true', help="Create a sequence from a chromosome, start position, and stop position")
    run_mode.add_argument('-s', '--sj', action='store_true', help="Create a sequence from a X-labeled splice junction dataset. See --sjPath for more information")

    strand = parser.add_mutually_exclusive_group(required=True)
    strand.add_argument('-p', '--plus', action='store_true', help='Intron is on the plus strand')
    strand.add_argument('-m', '--minus', action='store_true', help='Intron is on the minus strand')

    parser.add_argument('--chr', required='--coordinates' in sys.argv, type=str, help='Chromosome number (e.g. 1)')
    parser.add_argument('--start', required='--coordinates' in sys.argv, type=int, help='Chromosome-relative coordinate of the start of the intron')
    parser.add_argument('--stop', required='--coordinates' in sys.argv, type=int, help='Chromosome-relative coordinate of the start of the intron')

    parser.add_argument('--intron', required='--sj' in sys.argv, type=int, help='Intron X of the splice junction to use')
    parser.add_argument('--sjPath', required='--sj' in sys.argv, type=str, help='Path to the splice junction dataset: /path/to/sjdblist.csv or /path/to/sjdblist.tab. Note: the splice junction dataset must be in the format of Column 1: X; Column 2: Accession Version; Column 3: Start Position; Column 4: Stop Position')

    parser.add_argument('--left', default=150, type=int, help='Number of bases to the left of the start position to include. Default: 150bp')
    parser.add_argument('--right', default=150, type=int, help='Number of bases to the right of the stop position to include. Default: 150bp')

    parser.add_argument('--destination', default=os.getcwd(), type=str, help='Path to directory to save the sequence to /path/to/destination. Default: current working directory')

    args = parser.parse_args()

    if not pathlib.Path(args.destination).expanduser().resolve().exists():
        parser.exit(1, message="Destination directory does not exist")

    if args.plus == True:
        strand_char = "+"

    else:
        strand_char = "-"

    if args.coordinates == True:
        fromCoordinates(args.chr, strand_char, args.start, args.stop, args.left, args.right, args.destination)

    elif args.sj == True:
        fromSJDataset(args.intron, strand_char, args.left, args.right, args.sjPath, args.destination)
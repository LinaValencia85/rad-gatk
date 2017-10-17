#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
This script takes a table produced by GATK that contains the SNPs
called in all individuals and counts the number of loci that statisfy
a minimum coverage depth for a locus in an individual and a minimum
number of samples per locus. The output reports chromosome, number of
samples, number of SNPs in the locus, length, and starting and ending
coordinates for each locus
'''


__author__      = "Edgardo M. Ortiz"
__credits__     = "Lina M. Valencia"
__version__     = "1.0"
__email__       = "e.ortiz.v@gmail.com"
__date__        = "2017-10-17"


import sys
import argparse


# This function checks number of samples with the SNP and the depth
# of each SNP in each sample
def get_valid_samples(line, mindepth, minsample, columns):
    nsamp = 0
    for i in xrange(4,columns,2):
        if line.split()[i] != "./.":
            if line.split()[i+1] != "NA":
                if int(line.split()[i+1]) >= mindepth:
                    nsamp += 1
    if nsamp >= minsample:
        return nsamp
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description="Get loci statistics from GATK (across samples = (i)pyrad's step 7)")
    parser.add_argument("-i", "--input", action="store", dest="filename", required=True,
        help="Name of input file (the VCF matrix grom GATK across samples)")
    parser.add_argument("-d", "--min-locus-depth", action="store", dest="mindepth", type=int, default=6,
        help="Minimum number of reads in a RAD locus, default=6")
    parser.add_argument("-s", "--min-samples", action="store", dest="minsample", type=int, default=4,
        help="Minimum number of samples in a locus, default=4")
    parser.add_argument("-l", "--mean-locus-length", action="store", dest="maxlocuslen", type=int, default=270,
        help="Maximum RAD locus length in basepairs, default=270")
    args = parser.parse_args()

    filename = args.filename
    mindepth = args.mindepth
    minsample = args.minsample
    meanlocuslen = args.meanlocuslen

    with open(filename) as vcftable:
        locipersample = []  # List of counts of loci per sample
        loci = ["Locus,Chromosome,numSamples,numSNPs,Length,Start,End"] # Output list, with header as first line
        chrom = "1"         # Current chromosome
        locstart = 0        # Starting coordinate of current locus
        locus_number = 1    # Locus ID
        locend = 0          # Ending coordinate of current locus
        numsnps = 1         # Number of SNPs in current locus
        numsnps_total = 0   # Running sum of total SNPs
        numsamples = 0      # Number of samples in current locus
        linecount = 0       # Counter for lines in table
        columns = 0         # Numer of columns in table
        for line in vcftable:

            # Skip table's header line #
            if not line.startswith("CHROM"):

                # First SNP position is consider temporarily starting and ending of the locus 
                if linecount == 1:
                    locstart = int(line.split()[1])
                    locend = int(line.split()[1])

                # Check if locus meets mindepth and minsample 
                if get_valid_samples(line, mindepth, minsample, columns):
                    numsnps_total += 1

                    # Considering a minimum distance between loci of 80bp, we will assume a new locus
                    # has started after menalocuslen+80 
                    if int(line.split()[1])-locstart > (meanlocuslen+80) or int(line.split()[1])-locstart < 0:

                        # If locus has minimum required number of samples, add info to output 
                        if numsamples >= minsample:
                            loci.append(str(locus_number)+","+chrom+","+str(numsamples)+","+str(numsnps)+","+str(locend-locstart)+","+str(locstart)+","+str(locend))
                            locus_number += 1

                            # This loop keeps a running sum of loci for each sample #
                            for s in xrange(4,columns,2):
                                if line.strip("\n").split()[s+1] != "NA":
                                    if int(line.strip("\n").split()[s+1]) >= mindepth:
                                        locipersample[(s-4)/2][1] += 1
                        numsnps = 1
                        numsamples = get_valid_samples(line, mindepth, minsample, columns)
                        locstart = int(line.split()[1])
                        locend = int(line.split()[1])
                        chrom = line.split()[0]

                    # Keep parsing lines if SNPs are very close to each other (locus has not finished) 
                    else:
                        locend = int(line.split()[1])
                        nsamp = get_valid_samples(line, mindepth, minsample, columns)
                        numsamples = max(numsamples, nsamp)
                        numsnps += 1
                        chrom = line.split()[0]

            # Use table's header line to get number of columns, number of samples and sample names 
            else:
                columns = len(line.strip("\n").split())
                for i in xrange(4,columns,2):
                    locipersample.append([line.strip("\n").split()[i].lstrip("./").strip("_unmerged.GT").strip("_merged.GT"),0])
            linecount += 1


    # Prepare and write samples per locus output 
    outfile = open(filename.split('.')[0]+"_gatkS7_samples_snps_per_locus.csv", "w")
    outfile.write("\n".join(loci)+"\nTotal SNPs:"+str(numsnps_total)+"\n")
    outfile.close()

    locipersampleout = []
    for i in range(0,len(locipersample)):
        locipersampleout.append(locipersample[i][0]+"\t"+str(locipersample[i][1]))

    # Prepare and write loci per sample output 
    outfile = open(filename.split('.')[0]+"_gatkS7_loci_per_sample.csv", "w")
    outfile.write("\n".join(locipersampleout)+"\n")
    outfile.close()


if __name__ == "__main__":
    main()

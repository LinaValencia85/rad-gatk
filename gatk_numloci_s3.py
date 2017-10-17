#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
This script takes a table produced by GATK for a single individual
and based on the distance between sites identifies the start and
end of each locus. Finally it reports the locus number, the chromosome
of origin, the depth, length, and starting and ending coordinates
'''


__author__      = "Edgardo M. Ortiz"
__credits__     = "Lina M. Valencia"
__version__     = "1.0"
__email__       = "e.ortiz.v@gmail.com"
__date__        = "2017-10-17"


import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Get RAD loci statistics from GATK (within sample = (i)pyrad's step 3)")
    parser.add_argument("-i", "--input", action="store", dest="filename", required=True,
        help="Name of input file (the VCF matrix grom GATK within a sample)")
    parser.add_argument("-d", "--min-locus-depth", action="store", dest="mindepth", type=int, default=6,
        help="Minimum number of reads in a RAD locus, default=6")
    parser.add_argument("-l", "--mean-locus-length", action="store", dest="meanlocuslen", type=int, default=270,
        help="Mean RAD locus length in basepairs, default=270")
    args = parser.parse_args()

    filename = args.filename
    mindepth = args.mindepth
    meanlocuslen = args.meanlocuslen

    with open(filename) as variantvcf:
        loci = ["Locus,Chromosome,Depth,Length,Start,End"]  # Output list, header as first line
        locus_number = 1    # Counter for locus ID, will be added +1 on each step
        locstart = 0        # Starting coordinate of current locus
        locend = 0          # Ending coordinate of current locus
        depth = 0           # Maximum depth of current locus
        chrom = '1'         # Current chromosome
        linecount = 0       # Counter for total of lines in table SNPs
        for line in variantvcf:

            # Skip table's header line 
            if not line.startswith("CHROM"):

                # First SNP position is consider temporarily starting and ending of the locus 
                if linecount == 1:
                    locstart = int(line.split()[1])
                    locend = int(line.split()[1])

                # Skip if a genotype could not be called #
                if line.split()[3] != "NA":

                    # Check site has minimum required depth #
                    if int(line.split()[3]) >= mindepth:

                        # Considering a minimum distance between loci of 80bp, we will assume a new locus
                        # has started after menalocuslen+80 
                        if int(line.split()[1])-locstart > (meanlocuslen+80) or int(line.split()[1])-locstart < 0:

                            # If the locus is shorter than 270bp it means it comes from merged pairs,
                            # therefore the depth of these loci should be ~2x the minimum depth because the 
                            # mapping was done with unmerged reads and we should not count the reads of this 
                            # type of locus twice. If locus is longer than 270bp it comes from unmerged pairs.
                            # Under any of these conditions the current locus information should be appended
                            # to the output list and a new locus should start 
                            if depth >= mindepth*1.9 or locend-locstart > meanlocuslen:
                                loci.append(str(locus_number)+","+chrom+","+str(depth)+","+str(locend-locstart)+","+str(locstart)+","+str(locend))
                                locus_number += 1
                            locstart = int(line.split()[1])
                            locend = int(line.split()[1])
                            depth = int(line.split()[3])
                            chrom = line.split()[0]

                        # Keep parsing lines if SNPs are very close to each other (locus has not finished) 
                        else:
                            locend = int(line.split()[1])
                            depth = max(int(line.split()[3]), depth)
                            chrom = line.split()[0]
                linecount += 1

    # Prepare and write output file 
    outfile = open(filename.split('.')[0]+"_gatkS3.csv", "w")
    outfile.write("\n".join(loci)+"\n")
    outfile.close()


if __name__ == "__main__":
    main()

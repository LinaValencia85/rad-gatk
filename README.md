# rad-gatk
Tools to obtain locus-based statistics from RADseq data analyzed with GATK

## _Brief description_
[GATK](https://software.broadinstitute.org/gatk/) was designed to map whole genome shotgun reads (randomly fragmented DNA) to a reference genome in order to discover and call variants. However, reads from a RAD experiment can also be used in GATK with some modifications in the preliminary steps. Most notably, we must skip the "Eliminate duplicates" step since we would loose most of the coverage per locus.

GATK outputs VCF files where only data about individual SNPs are reported without reference to each specific RAD locus. The following  scripts attempt to recover information about each particular RAD locus based on the genomic coordinates of the SNPs, by determining if adjacent SNPs belong to a single RAD locus or not.

## _Usage_
Each script has few options, for example the minimum read depth to consider a locus as valid, or the mean locus length of your RAD loci (e.g. if you sequenced PE 2x150 you should probably have a mean locus length of ~300bp.

In order to use the scripts be sure that in GATK you run the following command specifying t
To access help on each parameter just type `python gatk-rad-loci-stats-s3.py -h` :

```
usage: gatk-rad-loci-stats-s3.py [-h] -i FILENAME [-d MINDEPTH] [-l MEANLOCUSLEN]

Get RAD loci statistics from GATK (within sample = (i)pyrad's step 3)

optional arguments:
  -h, --help            show this help message and exit
  -i FILENAME, --input FILENAME
                        Name of input file (the VCF matrix grom GATK within a
                        sample)
  -d MINDEPTH, --min-locus-depth MINDEPTH
                        Minimum number of reads in a RAD locus, default=6
  -l MEANLOCUSLEN, --mean-locus-length MEANLOCUSLEN
                        Mean RAD locus length in basepairs, default=270
```
or `python gatk-rad-loci-stats-s7.py -h`:
```
usage: gatk-rad-loci-stats-s7.py [-h] -i FILENAME [-d MINDEPTH] [-s MINSAMPLE]
                          [-l MEANLOCUSLEN]

Get loci statistics from GATK (across samples = (i)pyrad's step 7)

optional arguments:
  -h, --help            show this help message and exit
  -i FILENAME, --input FILENAME
                        Name of input file (the VCF matrix grom GATK across
                        samples)
  -d MINDEPTH, --min-locus-depth MINDEPTH
                        Minimum number of reads in a RAD locus, default=6
  -s MINSAMPLE, --min-samples MINSAMPLE
                        Minimum number of samples in a locus, default=4
  -l MEANLOCUSLEN, --mean-locus-length MEANLOCUSLEN
                        Mean RAD locus length in basepairs, default=270
```

## _Examples_

_Example 1:_ If you want to obtain RAD locus information from `sample_1` for loci covered at least 10x and assuming a mean locus length of 300bp:
```bash
python gatk-rad-loci-stats-s3.py -i sample_1.vcf.table -d 10 -l 300
```
_Example 2:_ If you want statistics per RAD locus across samples, for loci represented by at least 30 samples, and assuming a mean locus length of 250bp:
```bash
python gatk-rad-loci-stats-s7.py -i across_samples.vcf.table -s 30 -l 250
```

## _Credits_
- Code: [Edgardo M. Ortiz](mailto:e.ortiz.v@gmail.com)
- Data and testing: [Lina M. Valencia](mailto:linavalencia85@gmail.com)

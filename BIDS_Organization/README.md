# BIDS_Organization

## Behavioral data manipulation software created for UT Cognitive Neuroscience Lab.

This software is used to convert raw behavioral data to BIDS formatted data.

To run in terminal:

``` sh BIDS_conversion.sh ```

How it works:
* shell script accesses UT psych server
* shell script locates tasks to be converted to BIDS format
* shell script calls R script and passes raw files specified by first parameter
* R script manipulates data to BIDS specification
* R script saves data in .tsv format to location specified by second parameter

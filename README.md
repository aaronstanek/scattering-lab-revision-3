# Scattering Lab Revision 3

This repository has two goals.
To take document existing draft code.
And to create new functionality which does not yet exist.

## Integrate to CSV

`integrate_to_csv.integrate_to_csv(folderpath,outputfile)`

folderpath and outputfile are strings that refer to an existing directory and a nonexistent file respectively

This function will take the .ord.json files in the directory, compute the time integral of each event, and deposit the results in the output file

## Calibrate

`calibrate.calibrate(infile,outfile,coef)`

infile and outfile are strings that refer to an existing source csv and a nonexistent destination csv

coef is a dictionary mapping ints to floats

the keys indicate a channel to be scaled, and the values are how much to scale a particular channel by

## Making Cuts

cut.py contains a class called cut_instruction, the constructor looks like `cut.cut_instruction(channel,direction,value)`

channel is an int, referring to a channel, direction is a string, telling the program which direction to cut, and value is a float indicating where the cut should be placed

if `direction == "a"` then the program will remove events above value, if `direction == "b"` then the program will remove events below value

`cut.cut(infile,outfile,cutinfo)``

infile and outfile are strings, referring to an existing csv source file and a nonexistent output file

cutinfo is a list of cut_instruction, indicating what cuts to be made

## Binning Data

To plot or analyze data, it is helpful to put it into bins

`bins.single_channel_bins(infile,outfile,channel,bin_count)`

infile and outfile are strings, referring to an existing csv source file and a nonexistent output file

channel and bin_count are ints referring indicating which channel to bin and how many bins to bin it into

`bins.double_channel_bins(infile,outfile,channel1,bin_count1,channel2,bin_count2)`

infile and outfile are strings, referring to an existing csv source file and a nonexistent output file

channel and bin_count1 are ints that refer to a channel and indicate how many bins to bin that channel into

channe2 and bin_count2 are ints that refer to a different channel and indicate how many bins to bin that channel into

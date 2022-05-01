# DC Power Flow Calculation

DC power-flow non-iterative calculation for a N-bus M-branch power system, based on James D. McCalley book chapter.

This code is solely based on the methodology layed-down by the book chapter, authored by Iowa State University's Dr. James D. McCalley:

http://home.engineering.iastate.edu/~jdm/ee553/DCPowerFlowEquations.pdf

Moreover, the code is a fork/improved functionality of the repository at the following link: https://github.com/soummyaroy1/dc-power-flow/blob/master/run.py

The modifications done to the oiginal code, done by Kennedy Caisley, are the following:

- rather than using flat/text files, SQLite database is utilized for reading the input data, as well as writing the output results, to the same .db file, which is updated after each execution of this code

- incidence matrix is used in order to obtain the consolidated power flow across the system, rather than calculating the power flow for each line individually, base on the obtained buses' angle

- pandas are used in combination with numpy, in order to obtain streamlined reading and writing using SQLite


**Note: If running from ipyhton, please cd into the folder with downloaded files containing network.db and dc_pf_clean.py**

MINTmap (available at http://cm.jefferson.edu/MINTcodes)
------------------------------

1. General Information
----------------------
This code was created by Phillipe Loher and Isidore Rigoutsos.
MINTmap can be used to generate tRF profiles from Short-RNA datasets.
More information can be found at http://cm.jefferson.edu/MINTcodes/

If used, please cite:
Loher, P. et al. MINTmap: fast and exhaustive profiling of nuclear and mitochondrial tRNA fragments from short RNA-seq data. Sci. Rep. 7, 41184; doi: 10.1038/srep41184 (2017).

Note: Color-space reads are not supported in this tool.  For information on methods and color-space, please see paper at http://www.nature.com/articles/srep41184 .
Contact us at: https://cm.jefferson.edu/contact-us/


2. License
---------------
MINTmap is available under the open source GNU GPL v3.0 license (https://www.gnu.org/licenses/gpl-3.0.en.html).  
Optional MINTplates is included in the /MINTplates subdirectory and is governed by a seperate license.  See MINTplates/README.txt for more information.


3. Other software requirements
---------------
Java v1.8 (or greater) and Perl v5 (or greater) are required


4. Usage Information
--------------------
INPUT:
usage: ./MINTmap.pl -f trimmedfastqfile [-p outputprefix] [-l lookuptable] [-s tRNAsequences] [-o tRFtypes] [-d customRPM] [-a assembly] [-h]

-f trimmedfastqfile
This is a required argument. The file “trimmedfastqfile” contains the sequenced reads to be analyzed. It's important that quality and adaptor trimming is performed on this file before calling MINTmap.  If “trimmedfastqfile” ends in “.gz” it will be treated as a gzipped FASTQ file.

-p outputprefix
If not specified, “outputprefix” will be set to 'output' and all output files will be generated in the current working directory. The “outputprefix” is a string that will be prepended in the output files that MINTmap will generate. The string is meant to serve as a mnemonic for the user.

-l lookuptable
Unless specified by the user, this argument will be set automatically to 'LookupTable.tRFs.MINTmap_v1.txt'.  The “lookuptable” is the name of the file containing all possible tRFs of lengths 16-50 nt for the tRNA space currently in use. Every tRF sequence listed in this file is associated with a “Y”(es) or “N”(o) value that is the answer to the question “is the tRF sequence present in tRNA space exclusively?” The first two lines of the lookup table should include file-level md5 checksum values for the files that are specified with the –s and –o flags to ensure that concordant files are used.

-s tRNAsequences
Unless specified by the user, this argument will be set to 'tRNAspace.Spliced.Sequences.MINTmap_v1.fa'.  The “tRNAsequences” is the name of the file that contains the sequences that comprise the true tRNA space and can serve as potential source(s) of tRFs. Only spliced tRNA sequences with no post-transcriptional modifications should be included in this file. The string used to label each sequence in this file should be unique and, ideally, should contain the tRNA name and tRNA-locus coordinates that will be used in the output of MINTmap.

-o tRFtypes
This is an optional argument. Unless specified, this argument will be set automatically to 'OtherAnnotations.MINTmap_v1.txt'.  If the user specifies a file that does not exist, the structural type column in the output files will be set to 'na' (Not Applicable).  The “tRFtypes” is the filename for the file that contains the lookup table which associated for tRFs with their structural type. This file contains two columns separated by a ‘tab.’ The first column lists the sequences of a tRF. The second column list the structural type for that tRF sequence. If a tRF can have multiple structural types (because it appears at different locations in different isodecoders), the second column will list all structural types, separated by commas.

-d customRPM
This is an optional argument. The value “customRPM” is meant to be used as alternative denominator when computing the RPM abundance of a tRF. When this parameter is defined by the user, an additional column in the output files will be populated with RPM values that have been calculated using this value in the denominator – i.e. these values will be equal to raw reads/<customRPM>*1,000,000. A common value to use here is the original number of sequenced reads prior to quality- and adaptor-trimming.

-a assembly
Unless specified, this argument is automatically set to 'GRCh37'. The value of “assembly” refers to the genome assembly version used. The standard notation (e.g. “GRCh37”) is expected. This value is listed in the HTML output files in the table headers and is also part of the hyperlink to the MINTbase record of a tRF.

-j MINTplatesPath
Unless specified, this argument is automatically set to 'MINTplates/'.  The value of “MINTplatesPath“ refers to the path of the included MINTplates program which generates assembly-independent identifers for tRF sequences.

-z Don't add any post-modifications when searching the tRNA annotations file (rarely needed)

-h
This is an optional argument that shows the user a list of the various parameters.

OUTPUT:
- Plain text and HTML file pairs for exclusive tRFs profiles (*.exclusive-tRFs.expression.*) .  RPM and annotation information included.  HTML file also links to verbose MINTbase records.
- Plain text and HTML file pairs for non-exclusive tRFs profiles (*.ambiguous-tRFs.expression.*).  RPM and annotation information included.  HTML file also links to verbose MINTbase records.
- High level mapping stats are also generated seperately for exclusive and non-exclusive tRFs (*.countsmeta.txt)


5.  Example Run
--------------------
./MINTmap.pl -f ExampleRun/exampleInput.fastq.gz


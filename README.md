# MINTmap

In response to many requests, we are making available a stable, pre-release
version of MINTmap **version 2.0-alpha**. (MINTmap v2.0 is currently in active
development).

For the latest version of the code, including previous releases, visit
[https://cm.jefferson.edu/MINTmap](https://cm.jefferson.edu/MINTmap/).

MINTmap identifies and quantifies tRNA-derived fragments (tRFs) directly from a
*trimmed* short RNA-Seq dataset (fastq file). (Note: in a trimmed fastq file,
the listed sequenced reads have already had their sequencing adaptors removed.)

**NOTES:**

- MINTmap does *not* yet operate on fastq files where the reads still contain
adaptor fragments.

- Files containing color-space reads cannot be processed by this tool. For
information on how to extend the tool to color-space, see
[*MINTmap: fast and exhaustive profiling of nuclear and mitochondrial tRNA fragments from short RNA-seq data*](https://pubmed.ncbi.nlm.nih.gov/28220888/).

## General information
MINTmap is developed and maintained by the
[Computational Medicine Center](https://cm.jefferson.edu),
Thomas Jefferson University.

To cite MINTmap use:
  *Loher, P. et al. MINTmap: fast and exhaustive profiling of
  nuclear and mitochondrial tRNA fragments from short RNA-seq data.
  Sci. Rep. 7, 41184; doi: 10.1038/srep41184 (2017).*

You can contact us at
[cmcadmins@jefferson.edu](mailto://cmcadmins@jefferson.edu)


## License and Terms of Use

- If you use this tool, please cite:
[Loher et al, "MINTmap: fast and exhaustive profiling of nuclear and mitochondrial tRNA fragments from short RNA-seq data", *Sci Rep*, 2017](https://pubmed.ncbi.nlm.nih.gov/28220888/)

- MINTmap is available under the open source GNU GPL v3.0 license
([https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html)).

- MINTmap uses the "license plate" scheme to generate unique and unambiguous
labels for tRFs. This labeling scheme was originally described in
[*MINTbase: a framework for the interactive exploration of mitochondrial and nuclear tRNA fragments*](https://pubmed.ncbi.nlm.nih.gov/27153631/),
and subsequently extended to
[rRNA-derived fragments (rRFs)](https://pubmed.ncbi.nlm.nih.gov/32279660/)
and, more recently, to
[microRNA (miRNA) and miRNA isoforms (isomiRs)](https://pubmed.ncbi.nlm.nih.gov/33471076/).


## Installation using Anaconda

#### 1. Download the [Anaconda Installer](https://www.anaconda.com/products/individual#Downloads)

Note: If you are using macOS or Windows, download the **graphical** Anaconda
Installer.  
Also, the minimum recommended Anaconda version is 4.6.

#### 2. Run the Anaconda Installer

Note: In Linux follow the next steps to install Anaconda using the non-graphical
Anaconda Installer:

1. Open a terminal and run the downloaded installer script like this:
```
    bash ~/Downloads/Anaconda3-2020.11-Linux-x86_64.sh
```
Note that your downloaded Anaconda script might have a slightly different
filename.

2. When the installer prompts:
*Do you wish the installer to initialize Anaconda3 by running conda init?*,
press yes.

#### 3. Download and uncompress MINTmap

Note: If you are viewing this README file after downloading the latest MINTmap
release from https://cm.jefferson.edu/MINTmap, please proceed to the next step.
Otherwise, please download the latest version from
https://cm.jefferson.edu/MINTmap and uncompress the downloaded file.

#### 4. Open a terminal application

Note: In macOS and linux open the Terminal application.
In Windows, open the application *Anaconda Powershell Prompt (Anaconda3)*,
which you can find in the *Start Menu*.  

#### 5. Inside the terminal, start a bash shell by running:

    bash

#### 6. Initialize your Anaconda python environment by running:

    conda create --name snowflakes python

This creates an Anaconda environment named snowflakes and installs python in it.
You can give your environment a name other than snowflakes that reflects
the project you are working on.
 
#### 7. Activate the Anaconda python environment by running:

    conda activate snowflakes

#### 8. Change directory to where you uncompressed MINTmap, e.g. run:

    cd Downloads/MINTmap-v2.0-alpha/

#### 9. Install MINTmap inside the anaconda environment by running:

    pip install dist/MINTmap-2.0a0-py3-none-any.whl


## Example Usage

To generate tRF profiles using the example that resides in the directory
`ExampleRun` (included in the MINTmap download) do the following:

#### 1. Open a terminal application

Note: In macOS and linux open the Terminal application.
In Windows, open the application *Anaconda Powershell Prompt (Anaconda3)*,
which you can find in the *Start Menu*.

#### 2. Inside the terminal, start a bash shell by running:

    bash

#### 3. Activate the anaconda environment by running:

    conda activate snowflakes

#### 4. Change directory to the directory of this README file. e.g. run:

    cd Downloads/MINTmap/

#### 5. Change directory to the directory of the `ExampleRun` by running:

    cd ExampleRun

#### 6. Generate tRF profiles using the example (included in MINTmap download) trimmed fastq file by running:

    MINTmap exampleInput.trimmed.fastq.gz

Note: The above command creates the output files in the current directory.

Note: A *trimmed* FASTQ file includes sequencer reads from a core sequencing
facility in which any ligated adaptors have already been removed.
Reads must already have adaptors removed prior to calling MINTmap.
The included MINTmap example FASTQ file has already has been trimmed.

#### 7. List the output files in the current directory by running:

    ls

The output of the above command should be:

    exampleInput.trimmed.fastq.gz
    output-MINTmap_v2.0-alpha-ambiguous-tRFs.countsmeta.txt
    output-MINTmap_v2.0-alpha-ambiguous-tRFs.expression.html
    output-MINTmap_v2.0-alpha-ambiguous-tRFs.expression.txt
    output-MINTmap_v2.0-alpha-exclusive-tRFs.countsmeta.txt
    output-MINTmap_v2.0-alpha-exclusive-tRFs.expression.html
    output-MINTmap_v2.0-alpha-exclusive-tRFs.expression.txt

## Output Files

* Plain text and HTML file pairs for exclusive tRFs profiles
(\*.exclusive-tRFs.expression.\*).  
RPM and annotation information included.  
HTML file also links to verbose MINTbase records.
* Plain text and HTML file pairs for non-exclusive tRFs profiles
(\*.ambiguous-tRFs.expression.\*).  
RPM and annotation information included.  
HTML file also links to verbose MINTbase records.
* High level mapping stats are also generated separately for exclusive and
non-exclusive tRFs (\*.countsmeta.txt)

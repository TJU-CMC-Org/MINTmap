# MINTmap

To download the MINTmap tool, please visit
[cm.jefferson.edu/MINTmap](https://cm.jefferson.edu/MINTmap).

MINTmap generates tRF (tRNA fragment) profiles from a trimmed short RNA-Seq
dataset. A *trimmed* short RNA-Seq dataset, includes sequencer reads from a core
sequencing facility in which any ligated adaptors have already been removed.
Reads must already have adaptors removed prior to calling MINTmap.

Note: Color-space reads are not supported in this tool.
For information on methods and color-space, please see
[this paper](http://www.nature.com/articles/srep41184).

MINTmap is developed and maintained by the
[Computational Medicine Center](https://cm.jefferson.edu),
Thomas Jefferson University.

To cite MINTmap use:
  *Loher, P. et al. MINTmap: fast and exhaustive profiling of
  nuclear and mitochondrial tRNA fragments from short RNA-seq data.
  Sci. Rep. 7, 41184; doi: 10.1038/srep41184 (2017).*

You can contact us at
[cmcadmins@jefferson.edu](mailto://cmcadmins@jefferson.edu)


## License

MINTmap is available under the open source GNU GPL v3.0 license
(https://www.gnu.org/licenses/gpl-3.0.en.html).  
Included MINTplates library uses a different license, for more information see
the README file within the downloadable bundle.


## Publications

* Loher, P, Telonis, AG, Rigoutsos, I. MINTmap: fast and exhaustive profiling of
nuclear and mitochondrial tRNA fragments from short RNA-seq data.
Sci Rep. 2017;7 :41184.
doi: [10.1038/srep41184](http://dx.doi.org/10.1038/srep41184).
PubMed [PMID:28220888](http://www.ncbi.nlm.nih.gov/pubmed/28220888).
PubMed Central [PMC5318995](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5318995).

* Pliatsika, V, Loher, P, Telonis, AG, Rigoutsos, I. MINTbase: a framework for
the interactive exploration of mitochondrial and nuclear tRNA fragments.
Bioinformatics. 2016;32 (16):2481-9. doi: 
[10.1093/bioinformatics/btw194](http://dx.doi.org/10.1093/bioinformatics/btw194).
PubMed [PMID:27153631](http://www.ncbi.nlm.nih.gov/pubmed/27153631).
PubMed Central [PMC4978933](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4978933).


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

    cd Downloads/MINTmap/

#### 9. Install MINTmap inside the anaconda environment by running:

    pip install dist/MINTmap-2.0.0a0-py3-none-any.whl


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
* High level mapping stats are also generated seperately for exclusive and
non-exclusive tRFs (\*.countsmeta.txt)

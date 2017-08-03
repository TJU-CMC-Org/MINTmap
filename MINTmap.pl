#!/usr/bin/perl
use strict;
use warnings;
use Digest::MD5 qw (md5_hex);
use Sys::Hostname;

my $scriptversion = "MINTmap_v1";

# config settings
my $DEFAULT_LOOKUPTABLE="LookupTable.tRFs.MINTmap_v1.txt";
my $DEFAULT_TRNASPLICEDSEQUENCES="tRNAspace.Spliced.Sequences.MINTmap_v1.fa"; # used for annotationing where the tRF may come from
my $DEFAULT_OTHERANNOTATIONS="OtherAnnotations.MINTmap_v1.txt"; # used for annotating the tRF-type
my $DEFAULT_OUTPREFIX="output"; # output prefix to use if not it's not specified as a command line argument
my $DEFAULT_FRAGMENTTYPE="tRF";
my $ASSEMBLY_MINTBASE="GRCh37"; # assembly version that MINTbase uses
my $PATH_MINTPLATES="MINTplates/";

# globals
my %opt;
my $stat_totalstartingreads = 0;
my $md5sum_trnasequences = "na"; # MD5sum of trnasequences fasta.  The MD5SUM in the lookup table must match this to make sure they are paired correctly
my $md5sum_otherannotations = "na"; # MD5sum of trf other annotations.  The MD5SUM in the lookup table must match this to make sure they are paired correctly
my $using_otherannotations = 1;

# defines
my $index_argv_fastq = 0;
my $index_argv_outputprefix = 1;
my $index_argv_lookuptable = 2;
my $argv_maxparams = $index_argv_lookuptable + 1;

sub usage ()
{
   print STDERR << "EOF";
Use this program to generate tRF profiles

version: $scriptversion
INPUT:
usage: $0 -f trimmedfastqfile [-p outputprefix] [-l lookuptable] [-s tRNAsequences] [-o tRFtypes] [-d customRPM] [-a assembly] [-j MINTplatesPath] [-h]

-f trimmedfastqfile
This is a required argument. The file “trimmedfastqfile” contains the sequenced reads to be analyzed. If “trimmedfastqfile” ends in “.gz” it will be treated as a gzipped FASTQ file.

-p outputprefix
If not specified, “outputprefix” will be set to '$DEFAULT_OUTPREFIX' and all output files will be generated in the current working directory. The “outputprefix” is a string that will be prepended in the output files that MINTmap will generate. The string is meant to serve as a mnemonic for the user.

-l lookuptable 
Unless specified by the user, this argument will be set automatically to '$DEFAULT_LOOKUPTABLE'.  The “lookuptable” is the name of the file containing all possible tRFs of lengths 16-50 nt for the tRNA space currently in use. Every tRF sequence listed in this file is associated with a “Y”(es) or “N”(o) value that is the answer to the question “is the tRF sequence present in tRNA space exclusively?” The first two lines of the lookup table should include file-level md5 checksum values for the files that are specified with the –s and –o flags to ensure that concordant files are used. 

-s tRNAsequences
Unless specified by the user, this argument will be set to '$DEFAULT_TRNASPLICEDSEQUENCES'.  The “tRNAsequences” is the name of the file that contains the sequences that comprise the true tRNA space and can serve as potential source(s) of tRFs. Only spliced tRNA sequences with no post-transcriptional modifications should be included in this file. The string used to label each sequence in this file should be unique and, ideally, should contain the tRNA name and tRNA-locus coordinates that will be used in the output of MINTmap. 

-o tRFtypes
This is an optional argument. Unless specified, this argument will be set automatically to '$DEFAULT_OTHERANNOTATIONS'.  If the user specifies a file that does not exist, the structural type column in the output files will be set to 'na' (Not Applicable).  The “tRFtypes” is the filename for the file that contains the lookup table which associated for tRFs with their structural type. This file contains two columns separated by a ‘tab.’ The first column lists the sequences of a tRF. The second column list the structural type for that tRF sequence. If a tRF can have multiple structural types (because it appears at different locations in different isodecoders), the second column will list all structural types, separated by commas. 

-d customRPM
This is an optional argument. The value “customRPM” is meant to be used as alternative denominator when computing the RPM abundance of a tRF. When this parameter is defined by the user, an additional column in the output files will be populated with RPM values that have been calculated using this value in the denominator – i.e. these values will be equal to raw reads/<customRPM>*1,000,000. A common value to use here is the original number of sequenced reads prior to quality- and adaptor-trimming. 

-a assembly
Unless specified, this argument is automatically set to '$ASSEMBLY_MINTBASE'. The value of “assembly” refers to the genome assembly version used. The standard notation (e.g. “$ASSEMBLY_MINTBASE”) is expected. This value is listed in the HTML output files in the table headers and is also part of the hyperlink to the MINTbase record of a tRF.

-j MINTplatesPath
Unless specified, this argument is automatically set to '$PATH_MINTPLATES'.  The value of “MINTplatesPath“ refers to the path of the included MINTplates program which generates assembly-independent identifers for tRF sequences.

-z No post-modification
When this flag is used, do not pass any post-modifications when searching the tRNA annotations file (rarely needed)

-t fragment type
This is an optional argument. Unless specified, this argument will be set automatically to '$DEFAULT_FRAGMENTTYPE'.

-h 
This is an optional argument that shows the user a list of the various parameters.

OUTPUT:
- Plain text and HTML file pairs for exclusive tRFs profiles (*.exclusive-tRFs.expression.*) .  RPM and annotation information included.  HTML file also links to verbose MINTbase records.
- Plain text and HTML file pairs for non-exclusive tRFs profiles (*.ambiguous-tRFs.expression.*).  RPM and annotation information included.  HTML file also links to verbose MINTbase records.
- High level mapping stats are also generated seperately for exclusive and non-exclusive tRFs (*.countsmeta.txt)

EOF
   exit;
}

# display program help and check parameters for errors
sub checkArguments
{
   use Getopt::Std;
   my $opt_string = 'f:p:l:s:o:d:a:j:t:hz';
   getopts ("$opt_string", \%opt) or usage ();

   # hookup help parameter and enforce required variables
   if (defined $opt{h} || !(defined $opt{f}))
   {
      usage ();
   }

   if (defined $opt{z})
   {
      printf ("Flag -z detected, not expanding tRNA-annotations file with post-modifications\n");
   }

   # set optional fields to default values if not specified
   if (!(defined $opt{p}))
   {
      $opt{p} = $DEFAULT_OUTPREFIX;
   }
   if (!(defined $opt{l}))
   {
      $opt{l} = $DEFAULT_LOOKUPTABLE;
   }
   if (!(defined $opt{s}))
   {
      $opt{s} = $DEFAULT_TRNASPLICEDSEQUENCES;
   }
   if (!(defined $opt{o}))
   {
      $opt{o} = $DEFAULT_OTHERANNOTATIONS;
   }
   if (!(defined $opt{a}))
   {
      $opt{a} = $ASSEMBLY_MINTBASE;
   }
   if (!(defined $opt{j}))
   {
      $opt{j} = $PATH_MINTPLATES;
   }
   if (!(defined $opt{t}))
   {
      $opt{t} = $DEFAULT_FRAGMENTTYPE;
   }

   # error check if files exist
   my $openString = "error";

   # check if input file exists
   if (! (-e $opt{f}))
   {
      printf (STDERR "Error, exiting: FASTQ file %s not found\n", $opt{f});
      exit (1);
   }
   # check if lookup table exists
   if (! (-e $opt{l}))
   {
      printf (STDERR "Error, exiting: Lookup Table %s not found\n", $opt{l});
      exit (1);
   }
   # check if tRNA fasta file exists
   if (! (-e $opt{s}))
   {
      printf (STDERR "Error, exiting: tRNA fasta file %s not found\n", $opt{s});
      exit (1);
   }
   # check if tRNA-type annotation file exists
   if (! (-e $opt{o}))
   {
      $using_otherannotations = 0;
      printf ("tRF-annotation file %s not found, the tRF type column will be set to 'na'\n", $opt{o});
   }
   # check if input file is gzipped (see if it ends in .gz), if it ends in a gz we need to open it with gunzip
   if ($opt{f} =~ m/\.gz$/)
   {
      $openString = sprintf ("gunzip -c %s |", $opt{f});
   }
   else
   {
      $openString = sprintf ("<%s", $opt{f});
   }

   return $openString;
}

# load pre-computed lookup table into memory
sub loadLookupTable
{
   my $hash_exclusive = $_[0];
   my $hash_notexclusive = $_[1];

   open my $ifh, "<$opt{l}" or die $!;

   # get md5sum of tRNA sequences from first line in lookup table.  If it doesn't match, report an error and exit
   my $md5check = <$ifh>; 
   chomp $md5check;
   $md5check =~ s/^.*MD5SUM://;
   if ($md5check ne $md5sum_trnasequences)
   {
      printf (STDERR "Error, exiting: md5sum defined in lookup table %s (%s) does not match that of the tRNA sequences %s (%s)\n", $opt{l}, $md5check, $opt{s}, $md5sum_trnasequences);
      exit (1);
   }

   $md5check = <$ifh>; 
   chomp $md5check;
   if (substr ($md5check, 0, 17) ne "#OTHERANNOTATIONS")
   {
      printf (STDERR "Error, the second line of the LOOKUP table must start with '#OTHERANNOTATIONS' even if the otherannotations file does not exist.  Exiting.\n");
      exit (1);
   }
   if ($using_otherannotations == 1) # only do the MD5CHECK if the file exists because it's optional
   {
      $md5check =~ s/^.*MD5SUM://;
      if ($md5check ne $md5sum_otherannotations)
      {
         printf (STDERR "Error, exiting: md5sum defined in lookup table %s (%s) does not match that of the tRF types %s (%s)\n", $opt{l}, $md5check, $opt{o}, $md5sum_otherannotations);
         exit (1);
      }
   }

   while (my $line = <$ifh>)
   {
      chomp $line; 
      my @splitline = split (/\t/, $line);
      my $fragseq = $splitline[0];

      # Note: a Y in col2 means the tRF sequence is exclusive to tRNA space and a N means it's not exclusive
      if ($splitline[1] eq "Y") 
      {
         $hash_exclusive->{$splitline[0]} = 0;
      }
      elsif ($splitline[1] eq "N")
      {
         $hash_notexclusive->{$splitline[0]} = 0;
      }
      else
      {
         printf (STDERR "Error, exiting: Lookup value of %s in %s not recognized\n", $splitline[1], $opt{l});
         exit (1);
      }
   }
   close ($ifh);
}

# load tRNA fasta into memory
sub loadtRNAfasta
{
   my $hash_tRNAseqs = $_[0];

   open my $ifh, "<$opt{s}" or die $!;
   $md5sum_trnasequences  = Digest::MD5->new->addfile($ifh)->hexdigest; # get md5sum of the tRNA sequence files and then open it
   seek $ifh, 0, 0;  # rewind the file after getting md5sum
   while (my $line = <$ifh>)
   {
      # read header from fasta file
      chomp $line; 
      if (!($line =~ m/^>/))
      {
         printf (STDERR "Error, exiting: Expected FASTA header but received %s\n", $line);
         exit (1);
      }
      my $trnaname = $line;
      $trnaname =~ s/^>//; # remove the > from the header name to get the tRNA name
      if (!($trnaname =~ m/^[-.|+_A-Za-z0-9]+$/))
      {
         printf (STDERR "Error, exiting: Only characters [-.|+_A-Za-z0-9] allowed in FASTA label but received %s.  Note, no whitespace is allowed\n", $trnaname);
         exit (1);
      }

      # read sequence from fasta file
      my $seq = <$ifh>;
      chomp $seq;
      if (!($seq =~ m/^[ATCGN]+$/))
      {
         printf (STDERR "Error, exiting: Only characters [ATCGN] allowed in FASTA sequence but received %s\n", $seq);
         exit (1);
      }
      
      # add to hash
      $hash_tRNAseqs->{$trnaname} = $seq;
   }
   close ($ifh);
}

# load other tRF annotations
sub loadOtherAnnotations
{
   my $hash_otherannotations = $_[0];

   open my $ifh, "<$opt{o}" or die $!;
   $md5sum_otherannotations = Digest::MD5->new->addfile($ifh)->hexdigest; # get md5sum of the tRNA sequence files and then open it
   seek $ifh, 0, 0;  # rewind the file after getting md5sum
   while (my $line = <$ifh>)
   {
      chomp $line;
      my @linesplit = split (/\t/, $line);
      # add to hash
      $hash_otherannotations->{$linesplit[0]} = $linesplit[1];
   }
   close ($ifh);
}

sub getAnnotations 
{
   my $trfseq                 = $_[0];
   my $hash_tRNAs             = $_[1];
   my $array_annotationoutput = $_[2]; # store output here

   my $trfseq_len = length ($trfseq);

   # look for the tRFseq across all tRNA spliced sequences
   foreach my $trnaname (keys %{$hash_tRNAs})
   {
      my $trnaseq = $hash_tRNAs->{$trnaname};
      if (!defined $opt{z})
      {
         $trnaseq = $hash_tRNAs->{$trnaname} . "CCA"; # get tRNA spliced sequence and add CCA to it

         # check for -1 5' tRF since it's an exception
         my $trf5ptrunc = $trfseq;
         $trf5ptrunc =~ s/^.//; # remove the first NT from the tRF to check for 5' -1 post-modification possibilities
         if ($trf5ptrunc eq substr ($trnaseq, 0, length ($trf5ptrunc)))
         {
            push (@{$array_annotationoutput}, sprintf ("%s@%d%s.%d.%d", $trnaname, -1, substr ($trfseq, 0, 1), length ($trf5ptrunc), $trfseq_len));
         }
      }

      # now lets check the rest of them
      for (my $i = 0; $i < length ($trnaseq) - length ($trfseq) + 1; $i++)
      {
         if ($trfseq eq substr ($trnaseq, $i, $trfseq_len))
         {
            push (@{$array_annotationoutput}, sprintf ("%s@%d.%d.%d", $trnaname, $i + 1, $i + $trfseq_len, $trfseq_len));
         }
      }
   }

   if (scalar (@{$array_annotationoutput}) < 1)
   {
      printf (STDERR "Error, exiting: no annotations in sequence file %s found for tRF %s\n", $opt{s}, $trfseq);
      exit (1);
   }
}

# encode tRF sequences and store in output hash called MINTplates
# e.g. java -cp ./MINTplates/ MINTcodes_tRF_license_plates -e MINTplates/example_sequences_to_encode.txt
sub generatesPlates 
{
   my $allexpressed_tRFs = $_[0];
   my $outputplates_hash = $_[1];

   my $host = hostname;
   my $hostprefix="$$\_$host"; # set prefix to unique host and pid incase process is ran multiple times on same machine
   open my $ofh, ">tmp.mintmap.seqstoencode.$hostprefix.txt" or die $!;
   foreach my $mykey (keys %{$allexpressed_tRFs}) 
   {
      chomp $mykey;
      printf ($ofh "%s\n", $mykey);
   }
   close ($ofh);

   # run java program
   printf ("Running Java-based MINTplates\n");
   `java -cp $opt{j} MINTcodes_tRF_license_plates -e tmp.mintmap.seqstoencode.$hostprefix.txt > tmp.mintmap.seqstoencode.encoded.$hostprefix.txt`;

   open my $ifh, "<tmp.mintmap.seqstoencode.encoded.$hostprefix.txt" or die $!;
   foreach my $line (<$ifh>)
   {
      if ($line =~ m/\t/) # only look at MINTplate output lines with tabs in them as the others are information
      {
         chomp $line;
         my @splitline = split (/\t/, $line);

         if ($opt{t} ne "tRF") # if fragment is not a tRF, rename the MINTplate prefix
         {
            $splitline[1] =~ s/^tRF/$opt{t}/;
         }
         $outputplates_hash->{$splitline[0]} = $splitline[1];
      }
   }
   close ($ifh);

   # cleanup
   unlink ("tmp.mintmap.seqstoencode.$hostprefix.txt");
   unlink ("tmp.mintmap.seqstoencode.encoded.$hostprefix.txt");
}

sub createOutput
{
   my $read_hash = $_[0];
   my $annotation_hash = $_[1];
   my $otherannotations_hash = $_[2]; # currently used for tRF-type
   my $mintplates_hash = $_[3];
   my $total_frags_in_file = $_[4];
   my $tRFtypes = $_[5];
   my $filename = "";

   # output the tRFs in decreasing order of expression (double counting is not a problem because we are dealing with the raw reads)
   $filename = "$opt{p}-$scriptversion-$tRFtypes.expression.txt";
   printf ("Creating output file: %s\n", $filename);
   open my $ofh, ">$filename" or die $!;
   $filename = "$opt{p}-$scriptversion-$tRFtypes.expression.html";
   printf ("Creating output file: %s\n", $filename);
   open my $ofh_html, ">$filename" or die $!;
   printf ($ofh "MINTbase Unique ID\ttRF sequence\ttRF type(s)\tUnnormalized read counts\tRPM read counts (using all counts from this file[%d] in denominator)\tRPM read counts (using read count of input file from -f parameter[%d] in denominator)\tRPM read counts (using read count from optional -d parameter[%s] in denominator)\tSequence locations in tRNA space (comma deliminated)\n", $total_frags_in_file, $stat_totalstartingreads, defined ($opt{d}) ? $opt{d} : "na" );
   printf ($ofh_html "<html><head><title>%s expression</title></head>", $tRFtypes);
   printf ($ofh_html '<style> tr:nth-of-type(odd) { background-color:#ccc; } body { font-size: 18px; } table { font-size: 16px; } </style>');
   
   printf ($ofh_html '<body><p style="font-size:22px; display:inline">Table of %s for %s</p>', $tRFtypes, $opt{a});
   printf ($ofh_html '<br />Created by the <a target="_blank" href="http://cm.jefferson.edu">Computational Medicine Center</a> at <a target="_blank" href="http://www.jefferson.edu/">Thomas Jefferson University</a> using the MINTmap tool located <a target="_blank" href="http://cm.jefferson.edu/MINTcodes/">here</a>.<br />Please cite: Loher, P. <i>et al.</i> MINTmap: fast and exhaustive profiling of nuclear and mitochondrial tRNA fragments from short RNA-seq data. <i>Sci. Rep.</i> 7, 41184; doi: 10.1038/srep41184 (2017).');
   printf ($ofh_html '<br /><br /><table style="width=100%%"><tr><td><b>MINTbase Unique ID</b><br />(sequence derived)</td><td><b>tRF sequence</b></td><td><b>tRF type(s)</b></td><td><center><b>Unnormalized<br />read counts</b></center></td><td><center><b>RPM read counts (using all counts from this file[%d] in denominator)</b></center></td><td><center><b>RPM read counts (using read count of input file from -f parameter[%d] in denominator)</b></center></td><td><center><b>RPM read counts (using read count from optional -d parameter[%s] in denominator)</b></center></td><td><center><b>MINTbase Summary Record</b></center></td><td><center><b>Sequence locations in tRNA space<br />(comma deliminated)</b></td></center></tr>', $total_frags_in_file, $stat_totalstartingreads, defined ($opt{d}) ? $opt{d} : "na");

   foreach my $mykey (sort { $read_hash->{$b} <=> $read_hash->{$a} or $a cmp $b } keys %{$read_hash}) 
   {
      if ($read_hash->{$mykey} != 0) # don't print things with 0 expression
      {
         my $unnorm_numreads = $read_hash->{$mykey};
         my $rpm_1 = (($unnorm_numreads/$total_frags_in_file)*1000000);
         my $rpm_2 = (($unnorm_numreads/$stat_totalstartingreads)*1000000);
         my $rpm_3 = "na";
         my $annotations = join (', ', @{$annotation_hash->{$mykey}});
         if (defined $opt{d})
         {
            $rpm_3 = sprintf ("%.2f", (($unnorm_numreads/$opt{d})*1000000));
         } 
      
         my $otherannotations = 'na';
         if ($using_otherannotations == 1)
         {
            $otherannotations = $otherannotations_hash->{$mykey};
         }

         printf ($ofh "%s\t%s\t%s\t%d\t%.2f\t%.2f\t%s\t%s\n", $mintplates_hash->{$mykey}, $mykey, $otherannotations, $unnorm_numreads, $rpm_1, $rpm_2, $rpm_3, $annotations);
         my $mintbase_html = "na";
         if ($opt{t} eq "tRF")
         {
            $mintbase_html = sprintf ('<a target="_blank" href="https://cm.jefferson.edu/MINTbase/InputController?g=%s&v=s&fs=%s">Summary</a>', $opt{a}, $mykey);
         }
         printf ($ofh_html '<tr><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>%.2f</td><td>%.2f</td><td>%s</td><td>%s</td><td>%s</td></tr>', $mintplates_hash->{$mykey}, $mykey, $otherannotations, $unnorm_numreads, $rpm_1, $rpm_2, $rpm_3, $mintbase_html, $annotations);
      }
   }
   printf ($ofh_html "</table></body></html>");
   close ($ofh);
   close ($ofh_html);

   $filename = "$opt{p}-$scriptversion-$tRFtypes.countsmeta.txt";
   printf ("Creating output file: %s\n", $filename);
   open $ofh, ">$filename" or die $!;
   printf ($ofh "Total reads in -f input file\tTotal unnormalized reads in %s\tPercent\n", $tRFtypes, $tRFtypes);
   printf ($ofh "%ld\t%ld\t%.2f%%\n", $stat_totalstartingreads, $total_frags_in_file, ($total_frags_in_file / $stat_totalstartingreads) * 100);
   close ($ofh);
}


# lets begin main program
printf ("$0 ($scriptversion) starting\n");

# load arguments passed into script and perform argument error checking
my $openFastqString = checkArguments ();

# load tRNA spliced sequences into memory
printf ("Loading spliced tRNA sequences\n");
my %fastfrag_tRNAannotations = (); # Hash for tRFs that store all possible annotations for the tRF in trNA-space:  hash(tRFseq)->(array of strings)
my %trnaseq = (); # Hash for tRNA spliced sequences (no post-modifications should be included here as we'll handle them in the matching): hash(tRNAname)->sequence
loadtRNAfasta (\%trnaseq);

# loading tRF type annotations
my %trfannotations = ();
if ($using_otherannotations == 1)
{
   printf ("Loading tRF annotations\n");
   loadOtherAnnotations (\%trfannotations);
}

# load pre-computed lookup table into memory
printf ("Loading Lookup Table\n");
my %fastfrag_exclusive    = ();    # Hash for tRFs that are exclusive to tRNA-space:  hash(tRFseq)->count
my %fastfrag_notexclusive = ();    # Hash for tRFs that are not exclusive to tRNA-space:  hash(tRFseq)->count
loadLookupTable (\%fastfrag_exclusive, \%fastfrag_notexclusive);


# read in fastq file
printf ("Reading in fastq file\n");
my $stat_totalfragmentreads_exclusive = 0;
my $stat_totalfragmentreads_notexclusive = 0;
open my $ifh, "$openFastqString" or die $!;
while (defined (my $line_header = <$ifh>) && defined (my $line_seq = <$ifh>) && defined (my $line_misc = <$ifh>) && defined (my $line_phred = <$ifh>))
{
   chomp $line_seq;

   $stat_totalstartingreads++;
   if ($line_seq =~ m/[^ATCGN]/)
   {
      printf (STDERR "Error, exiting: Unrecognized character in fastq sequence %s, only [ATCGN]'s allowed\n", $line_seq);
      exit (1);
   }
   else
   {
      if (defined $fastfrag_exclusive{$line_seq} && defined $fastfrag_notexclusive{$line_seq})
      {
         printf (STDERR "Error, exiting: Fragment %s should not exist in both buckets\n", $line_seq);
         exit (1);
      }
      elsif (defined $fastfrag_exclusive{$line_seq}) # if it's defined in this hash, it means it's an exclusive tRF
      {
         $stat_totalfragmentreads_exclusive++;
         $fastfrag_exclusive{$line_seq}++;     # increment the count for this particular sequence

         # the first time we see the tRF, lets get the tRNA annotation(s) for it
         if ($fastfrag_exclusive{$line_seq} == 1)
         {
            if (!defined ($fastfrag_tRNAannotations{$line_seq}))
            {
               $fastfrag_tRNAannotations{$line_seq} = ();
               getAnnotations ($line_seq, \%trnaseq, \@{$fastfrag_tRNAannotations{$line_seq}});
            }
            else
            {
               printf (STDERR "Error, shouldn't ever get here, error 101\n");
               exit (1);
            }
         }
      }
      elsif (defined $fastfrag_notexclusive{$line_seq}) # if it's defined in this hash, it mean it's a non-exclusive tRF
      {
         $stat_totalfragmentreads_notexclusive++;
         $fastfrag_notexclusive{$line_seq}++;     # increment the count for this particular sequence

         # the first time we see the tRF, lets get the tRNA annotation(s) for it
         if ($fastfrag_notexclusive{$line_seq} == 1)
         {
            if (!defined ($fastfrag_tRNAannotations{$line_seq}))
            {
               $fastfrag_tRNAannotations{$line_seq} = ();
               getAnnotations ($line_seq, \%trnaseq, \@{$fastfrag_tRNAannotations{$line_seq}});
            }
            else
            {
               printf (STDERR "Error, shouldn't ever get here, error 102\n");
               exit (1);
            }
         }
      }
   }
}
close ($ifh);

# generate License Plate information
my %MINTplates = ();
generatesPlates (\%fastfrag_tRNAannotations, \%MINTplates);

# create output files for both the exclusive and non-exclusive tRFs
printf ("Generating output:\n");
createOutput (\%fastfrag_exclusive, \%fastfrag_tRNAannotations, \%trfannotations, \%MINTplates, $stat_totalfragmentreads_exclusive, "exclusive-$opt{t}s");
createOutput (\%fastfrag_notexclusive, \%fastfrag_tRNAannotations, \%trfannotations, \%MINTplates, $stat_totalfragmentreads_notexclusive, "ambiguous-$opt{t}s");

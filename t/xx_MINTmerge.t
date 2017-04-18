#! /usr/bin/perl
use strict;
use warnings;
use stefans_libs::root;
use Test::More tests => 2;
use stefans_libs::flexible_data_structures::data_table;

use FindBin;
my $plugin_path = "$FindBin::Bin";

my ( $value, @values, $exp, $outfile, @files, );

my $exec = $plugin_path . "/../bin/MINTmerge.pl";
ok( -f $exec, 'the script has been found' );
my $outpath = "$plugin_path/data/output/MINTmerge";
if ( -d $outpath ) {
	system("rm -Rf $outpath");
}
@files = map { "$plugin_path/data/merge$_.txt" } 1,2;
foreach ( @files ) {
	ok ( -f $_, "infile $_" );
}
$outfile = "$outpath/outfile.xls";

my $cmd =
    "perl -I $plugin_path/../lib  $exec "
. " -outfile " . $outfile
. " -files " . join(' ', @files )
. " -debug";
my $start = time;
system( $cmd );
my $duration = time - $start;
print "Execution time: $duration s\n";

ok ( -f $outfile, "the outfile has been created" );
ok ( -f $outfile.".log", "the logfile has been created" );



#print "\$exp = ".root->print_perl_var_def($value ).";\n";

#! /usr/bin/perl -w

=head1 LICENCE

  Copyright (C) 2017-04-04 Stefan Lang

  This program is free software; you can redistribute it 
  and/or modify it under the terms of the GNU General Public License 
  as published by the Free Software Foundation; 
  either version 3 of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful, 
  but WITHOUT ANY WARRANTY; without even the implied warranty of 
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License 
  along with this program; if not, see <http://www.gnu.org/licenses/>.

=head1 CREATED BY
   
   binCreate.pl from git@github.com:stela2502/Stefans_Lib_Esentials.git commit 8976a18c339e2885f28ff97a1210d805eeef87d7
   

=head1  SYNOPSIS

    SEQ_2_LookupTable.pl
       -min_length       :<please add some info!>
       -outfile       :<please add some info!>


       -help           :print this help
       -debug          :verbose output
   
=head1 DESCRIPTION

  Get sequences from a list of reprteteive tRNAs to add to the Lookup table - the matching against the genome will not be performed by this tool.

  To get further help use 'SEQ_2_LookupTable.pl -help' at the comman line.

=cut

use Getopt::Long;
use Pod::Usage;

use strict;
use warnings;

use FindBin;
my $plugin_path = "$FindBin::Bin";

my $VERSION = 'v1.0';


my ( $help, $infile, $debug, $database, $min_length, $outfile);

Getopt::Long::GetOptions(
	 "-infile=s"   => \$infile,
	 "-min_length=s"    => \$min_length,
	 "-outfile=s"    => \$outfile,

	 "-help"             => \$help,
	 "-debug"            => \$debug
);

my $warn = '';
my $error = '';

unless ( defined $min_length) {
	$error .= "the cmd line switch -min_length is undefined!\n";
}
unless ( defined $outfile) {
	$error .= "the cmd line switch -outfile is undefined!\n";
}


if ( $help ){
	print helpString( ) ;
	exit;
}

if ( $error =~ m/\w/ ){
	helpString($error ) ;
	exit;
}

sub helpString {
	my $errorMessage = shift;
	$errorMessage = ' ' unless ( defined $errorMessage); 
	print "$errorMessage.\n";
	pod2usage(q(-verbose) => 1);
}



my ( $task_description);

$task_description .= 'perl '.$plugin_path .'/SEQ_2_LookupTable.pl';
$task_description .= " -infile '$infile'" if (defined $infile);
$task_description .= " -min_length '$min_length'" if (defined $min_length);
$task_description .= " -outfile '$outfile'" if (defined $outfile);



use stefans_libs::Version;
my $V = stefans_libs::Version->new();
my $fm = root->filemap( $outfile );
mkdir( $fm->{'path'}) unless ( -d $fm->{'path'} );

open ( LOG , ">$outfile.log") or die $!;
print LOG $task_description."\n";
close ( LOG );


## Do whatever you want!

my ($data,@data);
my $subset;
$infile ||= '';
if ( -f $infile ){
	open ( IN, "<$infile") or die "I could not open the infile '$infile'\n$!\n";
	while ( <IN> ) {
		next if ( $_ =~ m/^>/ );
        chomp();
        $data->{$_} = 1;
        print "I read seq $_\n" if ( $debug );
	}
	close ( IN );
}else {
	while ( <> ) {
        chomp();
        $data->{$_} = 1;
		print "I read seq $_\n" if ( $debug );
	}
}
@data = sort keys %$data;

open ( my $LOOKUP ,">$outfile"."_LOOKUP.txt" ) or die "$!\n";
open ( my $OtherAnnotations, ">$outfile"."_OtherAnnotations.txt" ) or die "$!\n";

my $i = 0;
foreach ( &cut_to( $min_length, \@data ) ) {
	foreach my $str ( @$_ ) {
		$i ++;
		print $LOOKUP "$str\tY\n";
		print $OtherAnnotations "$str\tfl-tRF-".length($_)."\n";
	}
}

print "I have written $i fragments to $outfile"."_LOOKUP.txt and $outfile"."_OtherAnnotations.txt\n";

close ( $LOOKUP );
close ( $OtherAnnotations );

sub cut_to {
	my ( $length, $data ) = @_;
	print "cut_to started with length $length and ".scalar(@$data)." strings\n" if ( $debug );
	my @data;
	foreach ( @$data ) {
		$data[@data] = substr( $_,0,$length ) if ( length($_) >= $length);
	}
	@data = &unique( \@data );
	print "And returns ".scalar(@data)." $length bp long fragments\n" if ( $debug );
	if ( @data > 0 ) {
		return \@data, &cut_to($length + 1, $data );
	}
	return \@data;
}

sub unique {
	my (  $array ) = @_;
	my $d = { map { $_ => 1 } @$array };
	return sort keys %$d;
}

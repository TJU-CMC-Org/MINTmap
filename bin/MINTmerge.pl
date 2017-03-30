#! /usr/bin/perl -w

=head1 LICENCE

  Copyright (C) 2017-03-29 Stefan Lang

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

   binCreate.pl from git@github.com:stela2502/Stefans_Lib_Esentials.git commit 379745c9cb3ad2ab4f4e5a01908b35e7dc9536df


=head1  SYNOPSIS

    MINTmerge.pl
       -files     :<please add some info!> you can specify more entries to that
       -outfile       :<please add some info!>


       -help           :print this help
       -debug          :verbose output

=head1 DESCRIPTION

  Merge several MINTmap outfiles.

  To get further help use 'MINTmerge.pl -help' at the comman line.

=cut

use Getopt::Long;
use Pod::Usage;

use strict;
use warnings;

use stefans_libs::flexible_data_structures::data_table;

use FindBin;
my $plugin_path = "$FindBin::Bin";

my $VERSION = 'v1.0';


my ( $help, $debug, $database, @files, $outfile);

Getopt::Long::GetOptions(
       "-files=s{,}"    => \@files,
	 "-outfile=s"    => \$outfile,

	 "-help"             => \$help,
	 "-debug"            => \$debug
);

my $warn = '';
my $error = '';

unless ( defined $files[0]) {
	$error .= "the cmd line switch -files is undefined!\n";
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

$task_description .= 'perl '.$plugin_path .'/MINTmerge.pl';
$task_description .= ' -files "'.join( '" "', @files ).'"' if ( defined $files[0]);
$task_description .= " -outfile '$outfile'" if (defined $outfile);



use stefans_libs::Version;
my $V = stefans_libs::Version->new();
my $fm = root->filemap( $outfile );
mkdir( $fm->{'path'}) unless ( -d $fm->{'path'} );

open ( LOG , ">$outfile.log") or die $!;
print LOG $task_description."\n";
close ( LOG );

## Do whatever you want!

my $result = &read_table( shift @files );
$result -> define_subset('reorder', [ @{$result->{'header'}}[0..2,($result->Columns()-1), 3..($result->Columns()-2)] ]);
$result = $result ->GetAsObject( 'reorder' );
$result -> define_subset( 'key', [ @{$result->{'header'}}[0..2] ] );
$result ->createIndex( 'key' );

my ($helper,@targets, $index );

for( my $i = 0; $i < @files; $i ++)
{
   $helper = read_table( $files[$i] );
   @targets = $result -> Add_2_Header( [@{$helper->{'header'}}[3..($helper->Columns()-2)] ]);
   foreach my $this_key ( sort keys %{$helper->{'index'}->{'key'} } ) {
     $index = $result->{'index'}->{'key'};
     if ( $result->{'index'}->{'key'}->{$this_key} ){
        @{@{$result->{'data'}}[ @{$result->{'index'}->{'key'}->{$this_key}} ] }[@targets] =
          @{@{$helper->{'data'}}[ @{$helper->{'index'}->{'key'}->{$this_key}} ]}[3..($helper->Columns()-2)];
     }else {
       #die "add a new entry: \$exp = ".root->print_perl_var_def(  $helper->get_line_asHash( @{$helper->{index}->{'key'}->{$this_key}} )  ).";\n";
       $result->AddDataset ( $helper->get_line_asHash( @{$helper->{'index'}->{'key'}->{$this_key}} )  );
     }
   }
}

$result->write_file($outfile);

sub read_table {
  my $fname = shift;
  my $fm = root->filemap($fname);
  my $r = data_table->new({'no_doubble_cross'=> 1, 'filename' => $fname});
  $r -> define_subset( 'key', [ @{$r->{'header'}}[0..2] ] );
  $r ->createIndex( 'key' );
  map { $r->Rename_Column( $_, "$_ $fm->{'filename_core'}" ) } @{$r->{'header'}}[3..($r->Columns()-2)];

  return $r;
}

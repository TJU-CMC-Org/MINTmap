#!/usr/bin/env perl
# IMPORTANT: if you delete this file your app will not work as
# expected.  You have been warned.

use inc::Module::Install;
use Module::Install::Share;

name 'MINTmap';
version_from 'lib/MINTmap.pm';
author 'Stefan Lang <Stefan.Lang@med.lu.se>';

requires	'Module::Install::Share' => 0;
requires	'File::ShareDir' => 0;

opendir( DIR, 'bin/' ) or die "I could not open the bin folder\n$!\n";
map { install_script "bin/$_" } grep !/^\./,  grep '.pl', readdir(DIR);
close ( DIR );

install_share ('data' );

auto_install();

WriteAll();

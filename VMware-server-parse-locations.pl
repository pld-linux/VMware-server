#!/usr/bin/perl -w
# $Id$
#
# process vmware locations database
# filter the database and keep only single answers not the complete log
#
# purpose: cleanup locations db for making it into default rpm config

use strict;

my (%files, %dirs, %answer, %config);
while (<>) {
	chomp;
	next if /^$/ or /^#/;
	my ($cmd, $args) = split(/ /, $_, 2);
	my ($key, $value) = split(/ /, $args, 2);
	$files{$key} = $value,next if $cmd eq 'file';
	$config{$key} = 1,next if $cmd eq 'config';
	$dirs{$args} = 1,next if $cmd eq 'directory';
	$answer{$key} = $value,next if $cmd eq 'answer';
	delete $answer{$key},next if $cmd eq 'remove_answer';
	delete $files{$key},next if $cmd eq 'remove_file';
	warn "unknown config stub: [$cmd]\n";
}

foreach my $key (sort keys %answer) {
	my $value = $answer{$key};
	printf("answer %s %s\n", $key, $value);
}

while (my($key, $value) = each %dirs) {
	printf("directory %s\n", $key);
}

while (my($key, $value) = each %files) {
	if ($value) {
		printf("file %s %s\n", $key, $value);
	} else {
		printf("file %s\n", $key);
	}
}
while (my($key, $value) = each %files) {
	if ($value) {
		printf("file %s %s\n", $key, $value);
	} else {
		printf("file %s\n", $key);
	}
	if (exists $config{$key}) {
		printf("config %s\n", $key);
		delete $config{$key};
	}
}

while (my($key, $value) = each %config) {
	printf("config %s\n", $key);
}

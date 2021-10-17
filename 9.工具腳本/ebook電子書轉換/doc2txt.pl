#!/usr/bin/perl
# 可以非常快速地轉換老版本的doc文件為TXT
# cpan -T -i Text::Extract::Word
use strict;
use Text::Extract::Word;

my $file_src=$ARGV[0];
my $file_target=$ARGV[0];

if ($file_target =~ /docx/) {
	print("  Usage: $0 <doc file>\n");
	die("[ERROR]: docx file not supported. \n");
}

$file_target =~ s/\.doc$//;
$file_target = $file_target . ".txt";

if ( not -e $file_src ){
	print("  Usage: $0 <doc file>\n");
	die("[ERROR]: doc file doesn't exist: $file_src\n");
}

my $file = Text::Extract::Word->new($file_src);
my $text = $file->get_text();
open(FH, '>', $file_target) or die $!;
print FH $text;
close(FH);
print "Done. $file_target\n";

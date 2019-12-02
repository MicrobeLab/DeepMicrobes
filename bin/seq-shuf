#!/usr/bin/env perl

use warnings;
use strict;

use Data::Dumper;
use File::Temp 'tempfile';

use Getopt::Long;
use Pod::Usage;
use IO::File;

=head1 SYNOPSIS

  # FASTA
  cat A.fa [B.fa ..] | seq-shuf > AB-shuf.fa
  # FASTQ
  cat A.fq [B.fq ..] | seq-shuf > AB-shuf.fq
  # FASTQ paired end
  interleave A_[12].fq .. | seq-shuf --pe | interleaved-split 1> A-shuf_1.fq 2> A-shuf_2.fq

=head1 OPTIONS

=over

=item -p/--pe/--paired-end [OFF]

Input are paired end reads in interleaved format.

=item -t/--numper-of-tmp-files [100]

Number of tmp files, the input is split in. The split files are loaded into
memory entirely. For very large files >100G, it may be necessary to increase -t.

=back

=cut

=head1 MAIN

=cut

my $VERSION = 0.2.1;

my %def = (
           tmpn => 100,
       );

my %opt = ();
GetOptions(                     # use %opt (Cfg) as defaults
           \%opt, qw(
                        pe|p|paired-end!
                        tmpn|number-of-tmp-file|t=i
                        version|V!
                        debug|D!
                        help|h!
                   )
          ) or die 'Failed to "GetOptions"';

# help
$opt{help} && pod2usage(1);

# version
if ($opt{version}) {
    print "$VERSION\n"; 
    exit 0;
}

%opt = (%def, %opt);


my $tmpn=$opt{tmpn};
my @tmps;
for (my $i=0;$i<$tmpn;$i++) {
    push @tmps, [tempfile("seq-shuf-XXXXXXXX", UNLINK => 1)];
}

# check format
my $is_fastq;
my $c = qx(head -c1); # read with bash, perl STDIN read would buffer stuff
$is_fastq = 1 if $c eq '@';
$is_fastq = 0 if $c eq '>';
die 'Neither FASTA nor FASTQ' unless defined $is_fastq;

my $rec;
my $sed;

if ($is_fastq) {
    $rec=$opt{pe} ? "1~8" : "1~4";
    $sed= '(echo -n "'.$c.'"; cat <&0) | sed "'.$rec.'{s/^/\x0/}"';
}elsif ($opt{pe}) {
    die "Paired end FASTA not supported";
}else{
    $sed = '(echo -n "'.$c.'"; cat <&0) | sed "s/^>/\x0>/"';
}

$/="\0";
print STDERR $sed;
open (SED, "$sed |") or die $!;
# write records to random files
while (<SED>){
    print {$tmps[rand($tmpn)][0]} $_;
};
close SED;

# shuffle and print random files
$/=\1000000;
foreach (@tmps) {
    my $tmp = $_->[1];
    open(SHUF, "shuf -z $tmp | tr -d '\\0' |") or die $!;
    print while <SHUF>;
    close SHUF;
}

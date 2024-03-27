#!/usr/bin/perl
use DBI;
use Encode;
use File::Basename;
use utf8;
binmode(STDERR, "encoding(utf8)");
$MAXLINES = 10000;
my $total = 0;
$dbname = shift(@ARGV);

my @excluded = qw(speaker num note head castList bibl foreign stage);
my @taglist;

$dbh = DBI->connect("DBI:SQLite:dbname=$dbname", '','', {AutoCommit , 0});
for (@ARGV) {
	my $filename = $_;
	my ($shortname, $directory) = fileparse($filename);
	my $newfilename = "$directory/$shortname.ided";
	print STDERR "Reading $shortname...";

	my $header;
	my $body;
	my $newtext;
	my $tokencount = 0;
	my $inheader = 1;
	my $lasttokenid;
	my $excluding = 0;
	
	open (CURRENTFILE, "<:utf8", $filename);
	open (NEWFILE, ">:utf8", $newfilename);
	while (<CURRENTFILE>) {
		my $line = $_;
		my $newline = "";
		if ($inheader) {
			$excluding = 0;
			@taglist = ();
			if ($_ =~ /<\/tei[Hh]eader>/) { # Changed to match NewLatintexts too. - Matt S
			    $inheader = 0;
			}
			print NEWFILE $line;
		}
		elsif (!$inheader) {
			my $lastoffset = 0;
			#while ($line =~ m/(<[^>]*>)|([\p{L}\p{M}\x{2019}]+)|([\.\x{002E};\x{037E},\x{00B7}\x{0387}\x{002C}])|(&[#a-zA-Z0-9]{1,20};)/g ) {
			while ($line =~ m/(<[^>]*>)|([\p{L}\p{M}]+)|([\.\x{002E};\x{037E},\x{00B7}\x{0387}\x{002C}])|(&[#a-zA-Z0-9]{1,20};)/g ) {
				my ($tag, $word, $punct, $entity) = ($1, $2, $3, $4);
				my ($start, $end) = ($-[0], $+[0]);
				my $length = $end - $start;
				my $type;
				my $content;
				my $tokenid;
			
				my ($tagname, $closetag, $tagend);
				if ($tag  =~ m/<([\/]*)([^ ]+)(.*?)>/g) {
					($tagname, $closetag, $tagend) = ($2, $1, $3);
				}

				#printf STDERR "(%s %s [%s])", $tag, $tagname, @taglist;

				# Check against an excluded list of tags so that Greek inside those tags is not given ids
				if ( grep { /^$tagname$/ } @excluded ) {
					# if the tag is not a closing tag and not self-closing, then push it onto $taglist
					# else pop it off list
					if ( !$closetag && $tagend !~ /\//) {
						push @taglist, $tagname;
					} else {
						pop @taglist, $tagname;
					}
					# if $taglist is not empty then we are in excluding mode
					if (scalar @taglist > 0) {
						$excluding = 1;
					} else {
						$excluding = 0;
					}
					next;
				}
				
				if ($word) {
					$type = "word";
					$content = $word;
#					if ($content eq "lt" or $content eq "gt" or $content eq "lsqb" or $content eq "rsqb") {
#						next;
#					}
				}
				elsif ($punct) {
					$type = "punct";
					$content = $punct;
				}
				elsif ($tag) {
					next;
				}
				elsif ($entity) {
				    next;
				}

				# if we're in excluding mode then skip
				if ($excluding) {
					next;
				}

				$tokencount++;
				$total++;
				my $insertquery = $dbh->prepare("insert into tokens (content, file, seq, type) values (\"$content\", \"$shortname\", $tokencount,\"$type\");");
				$insertquery->execute();
				#token id is autoincremented, so we need to fetch it.
				my $tokenid = $dbh->last_insert_id(null,null, "tokens", null);

				if ($type eq "word") {
					$length = length($content);
					$newline .= substr($line, $lastoffset, $start - $lastoffset) . "<w id=\"$tokenid\">$content<\/w>";
					$lastoffset = $end;
				}	

				if ($tokencount % $MAXLINES == 0) {
					$dbh->commit();
					print STDERR "$tokencount - ";
				}
			}
			$newline .= substr($line, $lastoffset);
			print NEWFILE $newline;
		}
	}
	$dbh->commit();
	print STDERR "$tokencount tokens.  $total so far.  ";
	print STDERR length($header) . "b header, " . length($body) . "b body\n";
	print STDERR "writing $newfilename\n";
	
	close NEWFILE;
}


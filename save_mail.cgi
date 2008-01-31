#!/usr/local/bin/perl
# Save email-related options for a virtual server

require './virtual-server-lib.pl';
&ReadParse();
&error_setup($text{'mail_err'});
$d = &get_domain($in{'dom'});
&can_edit_domain($d) && &can_edit_mail() || &error($text{'edit_ecannot'});
$oldd = { %$d };
&require_mail();

# Validate inputs
if ($supports_bcc) {
	$in{'bcc_def'} || $in{'bcc'} =~ /^\S+\@\S+$/ ||
		&error($text{'mail_ebcc'});
	}

&ui_print_unbuffered_header(&domain_in($d), $text{'mail_title'}, "");

# Update BCC setting
if ($supports_bcc) {
	$bcc = &get_domain_sender_bcc($d);
	if (!$in{'bcc_def'}) {
		# Update BCC setting
		&$first_print(&text('mail_bccing', $in{'bcc'}));
		&save_domain_sender_bcc($d, $in{'bcc'});
		&$second_print($text{'setup_done'});
		}
	elsif ($bcc && $in{'bcc_def'}) {
		# Turn off BCC
		&$first_print($text{'mail_nobcc'});
		&save_domain_sender_bcc($d, undef);
		&$second_print($text{'setup_done'});
		}
	else {
		&$second_print($text{'mail_bccoff'});
		}
	}

# Update alias mode
if (defined($in{'aliascopy'}) && $d->{'mail'}) {
	$aliasdom = &get_domain($d->{'alias'});
	if ($d->{'aliascopy'} && !$in{'aliascopy'}) {
		# Switch to catchall
		&$first_print($text{'save_aliascopy0'});
		&delete_alias_virtuals($d);
		&create_virtuser({ 'from' => '@'.$d->{'dom'},
				   'to' => [ '%1@'.$aliasdom->{'dom'} ] });
		&$second_print($text{'setup_done'});
		}
	elsif (!$d->{'aliascopy'} && $in{'aliascopy'}) {
		# Switch to copy mode
		&$first_print($text{'save_aliascopy1'});
		&copy_alias_virtuals($d, $aliasdom);
		&$second_print($text{'setup_done'});
		}
	$d->{'aliascopy'} = $in{'aliascopy'};
	}

&save_domain($d);
&run_post_actions();

# All done
&webmin_log("mail", "domain", $d->{'dom'});
&ui_print_footer(&domain_footer_link($d),
		 "", $text{'index_return'});


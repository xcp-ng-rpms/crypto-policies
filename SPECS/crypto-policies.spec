%global git_date 20190807
%global git_commit_hash 9b1477b

Name:           crypto-policies
Version:        %{git_date}
Release:        1.git%{git_commit_hash}%{?dist}
Summary:        Systemwide crypto policies

License:        LGPLv2+
URL:            https://gitlab.com/redhat-crypto/fedora-crypto-policies

# This is a tarball of the git repository without the .git/
# directory.
# For RHEL-8 we use the upstream branch next-default.
Source0:        crypto-policies-git%{git_commit_hash}.tar.gz

BuildArch: noarch
BuildRequires: asciidoc
BuildRequires: libxslt
BuildRequires: openssl
BuildRequires: gnutls-utils >= 3.6.0
BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: bind
BuildRequires: perl-interpreter
BuildRequires: perl-generators
BuildRequires: perl(File::pushd), perl(File::Temp), perl(File::Copy)
BuildRequires: perl(File::Which)
BuildRequires: python3-devel

# used by update-crypto-policies
Requires: coreutils
Requires: grep
Requires: sed
Requires(post): coreutils
Requires(post): grep
Requires(post): sed
Conflicts: nss < 3.44.0
Conflicts: libreswan < 3.28
Conflicts: openssh < 8.0p1
# used by fips-mode-setup
Recommends: grubby

%description
This package provides a tool update-crypto-policies, which sets
the policy applicable for the various cryptographic back-ends, such as
SSL/TLS libraries. The policy set by the tool will be the default policy
used by these back-ends unless the application user configures them otherwise.

The package also provides a tool fips-mode-setup, which can be used
to enable or disable the system FIPS mode.

%prep
%setup -q -n %{name}

%build
make %{?_smp_mflags}

%install
mkdir -p -m 755 %{buildroot}%{_datarootdir}/crypto-policies/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/back-ends/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/local.d/
mkdir -p -m 755 %{buildroot}%{_bindir}

make DESTDIR=%{buildroot} DIR=%{_datarootdir}/crypto-policies MANDIR=%{_mandir} %{?_smp_mflags} install
install -p -m 644 default-config %{buildroot}%{_sysconfdir}/crypto-policies/config

%check
make check %{?_smp_mflags}

%post
%{_bindir}/update-crypto-policies --no-check >/dev/null


%files

%dir %{_sysconfdir}/crypto-policies/
%dir %{_sysconfdir}/crypto-policies/back-ends/
%dir %{_sysconfdir}/crypto-policies/local.d/
%dir %{_datarootdir}/crypto-policies/

%config(noreplace) %{_sysconfdir}/crypto-policies/config

%ghost %{_sysconfdir}/crypto-policies/back-ends/gnutls.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openssl.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/opensslcnf.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openssh.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/opensshserver.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/nss.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/bind.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/java.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/krb5.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openjdk.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/libreswan.config

%{_bindir}/update-crypto-policies
%{_bindir}/fips-mode-setup
%{_bindir}/fips-finish-install
%{_mandir}/man7/crypto-policies.7*
%{_mandir}/man8/update-crypto-policies.8*
%{_mandir}/man8/fips-mode-setup.8*
%{_mandir}/man8/fips-finish-install.8*
%{_datarootdir}/crypto-policies/LEGACY
%{_datarootdir}/crypto-policies/DEFAULT
%{_datarootdir}/crypto-policies/FUTURE
%{_datarootdir}/crypto-policies/FIPS
%{_datarootdir}/crypto-policies/EMPTY
%{_datarootdir}/crypto-policies/default-config
%{_datarootdir}/crypto-policies/reload-cmds.sh

%{!?_licensedir:%global license %%doc}
%license COPYING.LESSER

%changelog
* Wed Aug  7 2019 Tomáš Mráz <tmraz@redhat.com> - 20190807-1.git9b1477b
- gnutls: enable TLS-1.3 in the FIPS policy

* Mon Aug  5 2019 Tomáš Mráz <tmraz@redhat.com> - 20190613-2.git21ffdc8
- fix ownership of policy directories
- nss: enable X25519 in appropriate policies and conflict with old nss
- openssh: conflict with old incompatible openssh version

* Thu Jun 13 2019 Tomáš Mráz <tmraz@redhat.com> - 20190613-1.git21ffdc8
- openssh: add missing curve25519-sha256 to the key exchange list
- openssh: fix RSA certificate support
- fips-mode-setup: drop the kernel boot option if there is no separate
  /boot drive
- fips-finish-install: regenerate all initramdisks
- add libssh configuration backend

* Mon Feb 18 2019 Tomáš Mráz <tmraz@redhat.com> - 20181217-6.git9a35207
- libreswan: Allow coalescing the IKE/IPSEC proposals

* Fri Feb  8 2019 Tomáš Mráz <tmraz@redhat.com> - 20181217-5.git9a35207
- cleanups of the crypto-policies.7 manual page

* Fri Feb  1 2019 Tomáš Mráz <tmraz@redhat.com> - 20181217-4.git9a35207
- Java: Fix FIPS and FUTURE policy to allow RSA certificates in TLS

* Tue Jan 22 2019 Tomáš Mráz <tmraz@redhat.com> - 20181217-3.git9a35207
- cleanup duplicate and incorrect information from update-crypto-policies.8
  manual page

* Mon Jan 21 2019 Tomáš Mráz <tmraz@redhat.com> - 20181217-2.git9a35207
- add crypto-policies.7 manual page

* Mon Dec 17 2018 Tomáš Mráz <tmraz@redhat.com> - 20181217-1.git9a35207
- update-crypto-policies: Fix endless loop
- update-crypto-policies: Add warning about the need of system restart
- fips-mode-setup: Use grub2-editenv to modify the kernelopts for BLS

* Thu Nov 22 2018 Tomáš Mráz <tmraz@redhat.com> - 20181122-1.git70769d9
- update-crypto-policies: fix error on multiple matches in local.d
- Print warning when update-crypto-policies --set is used in the FIPS mode
- Java: Add 3DES and RC4 to legacy algorithms in LEGACY policy
- OpenSSL: Properly disable non AEAD and AES128 ciphersuites in FUTURE
- libreswan: Add chacha20_poly1305 to all policies and drop ikev1 from LEGACY

* Fri Oct 26 2018 Tomáš Mráz <tmraz@redhat.com> - 20181026-1.gitcc78cb7
- Fix regression in discovery of additional configuration
- NSS: add DSA keyword to LEGACY policy
- GnuTLS: Add 3DES and RC4 to LEGACY policy

* Tue Sep 25 2018 Tomáš Mráz <tmraz@redhat.com> - 20180925-2.git3ce363a
- Improve the package description

* Tue Sep 25 2018 Tomáš Mráz <tmraz@redhat.com> - 20180925-1.git3ce363a
- Use Recommends instead of Requires for grubby
- Revert setting of HostKeyAlgorithms for ssh client for now

* Fri Sep 21 2018 Tomáš Mráz <tmraz@redhat.com> - 20180921-1.git62bafde
- OpenSSH: Generate policy for sign algorithms
- Enable >= 255 bits EC curves in FUTURE policy
- OpenSSH: Add group1 key exchanges in LEGACY policy
- NSS: Add SHA224 to hash lists
- Print warning when update-crypto-policies --set FIPS is used
- fips-mode-setup: Kernel boot options are now modified with grubby

* Mon Aug 13 2018 Tomáš Mráz <tmraz@redhat.com> - 20180801-2.git2b95ede
- Fix build to use the system python

* Wed Aug  1 2018 Tomáš Mráz <tmraz@redhat.com> - 20180801-1.git2b95ede
- Add OpenSSL configuration file include support
- Disable TLS-1.0, 1.1 and DH with less than 2048 bits in DEFAULT policy

* Tue Jul 24 2018 Tomáš Mráz <tmraz@redhat.com> - 20180723-1.gitdb825c0
- Initial FIPS mode setup support
- NSS: Add tests for the generated policy
- Enable TLS-1.3 if available in the respective TLS library
- Enable SHA1 in certificates in LEGACY policy
- Disable CAMELLIA
- libreswan: Multiple bug fixes in policies

* Wed Apr 25 2018 Tomáš Mráz <tmraz@redhat.com> - 20180425-1.git6ad4018
- Restart/reload only enabled services
- Do not enable PSK ciphersuites by default in gnutls and openssl
- krb5: fix when more than 2048 bits keys are required
- Fix discovery of additional configurations #1564595
- Fix incorrect ciphersuite setup for libreswan

* Tue Mar  6 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20180306-1.gitaea6928
- Updated policy to reduce DH parameter size on DEFAULT level, taking into
  account feedback in #1549242,1#534532.
- Renamed openssh-server.config to opensshserver.config to reduce conflicts
  when local.d/ appending is used.

* Tue Feb 27 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20180227-1.git0ce1729
- Updated to include policies for libreswan

* Mon Feb 12 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20180112-1.git386e3fe
- Updated to apply the settings as in StrongCryptoSettings project. The restriction
  to TLS1.2, is not yet applied as we have no method to impose that in openssl.
  https://fedoraproject.org/wiki/Changes/StrongCryptoSettings

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 20171115-3.git921600e
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171115-2.git921600e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 15 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20171115-1.git921600e
- Updated openssh policies for new openssh without rc4
- Removed policies for compat-gnutls28

* Wed Aug 23 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170823-1.git8d18c27
- Updated gnutls policies for 3.6.0

* Wed Aug 16 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170816-1.git2618a6c
- Updated to latest upstream
- Restarts openssh server on policy update

* Wed Aug  2 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170802-1.git9300620
- Updated to latest upstream
- Reloads openssh server on policy update

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170606-4.git7c32281
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Igor Gnatenko <ignatenko@redhat.com> - 20170606-3.git7c32281
- Restore Requires(post)

* Mon Jul 24 2017 Troy Dawson <tdawson@redhat.com> 20170606-2.git7c32281
- perl dependency renamed to perl-interpreter <ppisar@redhat.com>
- remove useless Requires(post) <ignatenko@redhat.com>
- Fix path of libdir in generate-policies.pl (#1474442) <tdawson@redhat.com>

* Tue Jun  6 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170606-1.git7c32281
- Updated to latest upstream
- Allows gnutls applications in LEGACY mode, to use certificates of 768-bits

* Wed May 31 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170531-1.gitce0df7b
- Updated to latest upstream
- Added new kerberos key types

* Sat Apr 01 2017 Björn Esser <besser82@fedoraproject.org> - 20170330-3.git55b66da
- Add Requires for update-crypto-policies in %%post

* Fri Mar 31 2017 Petr Šabata <contyk@redhat.com> - 20170330-2.git55b66da
- update-crypto-policies uses gred and sed, require them

* Thu Mar 30 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170330-1-git55b66da
- GnuTLS policies include RC4 in legacy mode (#1437213)

* Fri Feb 17 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160214-2-gitf3018dd
- Added openssh file

* Tue Feb 14 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160214-1-gitf3018dd
- Updated policies for BIND to address #1421875

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161111-2.gita2363ce
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 11 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20161111-1-gita2363ce
- Include OpenJDK documentation.

* Tue Sep 27 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160926-2-git08b5501
- Improved messages on error.

* Mon Sep 26 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160926-1-git08b5501
- Added support for openssh client policy

* Wed Sep 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160921-1-git75b9b04
- Updated with latest upstream.

* Thu Jul 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-2-gitdb5ca59
- Added support for administrator overrides in generated policies in local.d

* Thu Jul 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-1-git340cb69
- Fixed NSS policy generation to include allowed hash algorithms

* Wed Jul 20 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-1-gitcaa4a8d
- Updated to new version with auto-generated policies

* Mon May 16 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160516-1-git8f69c35
- Generate policies for NSS
- OpenJDK policies were updated for opendjk 8

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151104-2.gitf1cba5f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151104-1-gitcf1cba5f
- Generate policies for compat-gnutls28 (#1277790)

* Fri Oct 23 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151005-2-gitc8452f8
- Generated files are put in a %%ghost directive

* Mon Oct  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151005-1-gitc8452f8
- Updated policies from upstream
- Added support for the generation of libkrb5 policy
- Added support for the generation of openjdk policy

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150518-2.gitffe885e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150518-1-gitffe885e
- Updated policies to remove SSL 3.0 and RC4 (#1220679)

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-3-git2eeb03b
- Added make check

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-2-git44afaa1
- Removed support for SECLEVEL (#1199274)

* Thu Mar  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-1-git098a8a6
- Include AEAD ciphersuites in gnutls (#1198979)

* Sun Jan 25 2015 Peter Robinson <pbrobinson@fedoraproject.org> 20150115-3-git9ef7493
- Bump release so lastest git snapshot is newer NVR

* Thu Jan 15 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150115-2-git9ef7493
- Updated to newest upstream version.
- Includes bind policies (#1179925)

* Tue Dec 16 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-2-gitd4aa178
- Corrected typo in gnutls' future policy (#1173886)

* Mon Nov 24 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-1-gitd4aa178
- re-enable SSL 3.0 (until its removal is coordinated with a Fedora change request)

* Thu Nov 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141120-1-git9a26a5b
- disable SSL 3.0 (doesn't work in openssl)

* Fri Sep 05 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140905-1-git4649b7d
- enforce the acceptable TLS versions in openssl

* Wed Aug 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140827-1-git4e06f1d
- fix issue with RC4 being disabled in DEFAULT settings for openssl

* Thu Aug 14 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140814-1-git80e1e98
- fix issue in post script run on upgrade (#1130074)

* Tue Aug 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140812-1-gitb914bfd
- updated crypto-policies from repository

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 20140708-2-git3a7ae3f
- fix license handling

* Tue Jul 08 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140708-1-git3a7ae3f
- updated crypto-policies from repository

* Fri Jun 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140620-1-gitdac1524
- updated crypto-policies from repository
- changed versioning

* Thu Jun 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-7-20140612gita2fa0c6
- updated crypto-policies from repository

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7.20140522gita50bad2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-6-20140522gita50bad2
- Require(post) coreutils (#1100335).

* Tue May 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-5-20140522gita50bad2
- Require coreutils.

* Thu May 22 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-4-20140522gita50bad2
- Install the default configuration file.

* Wed May 21 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-3-20140520git81364e4
- Run update-crypto-policies after installation.

* Tue May 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-2-20140520git81364e4
- Updated spec based on comments by Petr Lautrbach.

* Mon May 19 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-1-20140519gitf15621a
- Initial package build


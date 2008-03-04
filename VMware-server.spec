#
# This doesn't work at all yet. I don't know if the management interface is needed
# (bundling apache seems like a sooooooooo great idea). Maybe it is possible to
# setup the server part by hand. The perl module in perl/control.tar needs to
# be packaged (vmware-cmd requires that). Something needs to be done with
# the authd (inetd integration is needed I guess).
#
# The modules from any-any upgrade are too old (I used the ones comming with VMw-S).
#
# It builds on amd64, I have changed the networking package not to require the main package
# so it can be installed outside 32bit chroot.
#
# But hey, it's at least free ;-)
#
# I probably won't have time to work on this, switching to vmware-player.
# TODO:
# problem with libsexy/libsexymm:
# ln -s /usr/lib/libsexy.so.2 /usr/lib/libsexy.so.1
# ln -s /usr/lib/libsexymm.so.2 /usr/lib/libsexymm.so.1
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace utilities
%bcond_with	internal_libs	# internal libs stuff
%bcond_with	verbose		# verbose build (V=1)
#
%include	/usr/lib/rpm/macros.perl
#
%define		ver	2.0
%define		subver	63231
%define		rel	0.1
%define		urel	115
%define		ccver	%(rpm -q --qf %{V} gcc)
#
Summary:	VMware Server
Summary(pl.UTF-8):	VMware Server - wirtualna platforma dla stacji roboczej
Name:		VMware-server
Version:	%{ver}.%{subver}
Release:	%{rel}
License:	custom, non-distributable
Group:		Applications/Emulators
# http://www.vmware.com/beta/server/download.html
Source0:	http://download3.vmware.com/software/vmserver/%{name}-e.x.p-%{subver}.i386.tar.gz
# NoSource0-md5:	853247ff0e313f34bd0c3052de8e2c28
Source1:	http://download3.vmware.com/software/vmserver/%{name}-e.x.p-%{subver}.x86_64.tar.gz
# NoSource1-md5:	0d36ae02640d913251fd11918f798da3
Source2:	http://download3.vmware.com/software/vmserver/VMware-vix-e.x.p-%{subver}.i386.tar.gz
# NoSource2-md5:	c7d162fb8c805143ea5b40e7f62ef4da
Source3:	http://download3.vmware.com/software/vmserver/VMware-vix-e.x.p-%{subver}.x86_64.tar.gz
# NoSource3-md5:	10124d4747e7a579a270376458b7a77b
Source4:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update%{urel}.tar.gz
# NoSource4-md5:	ab33ff7a799fee77f0f4ba5667cd4b9a
Source5:	%{name}.init
Source6:	%{name}-vmnet.conf
Source7:	%{name}.png
Source8:	%{name}.desktop
Source9:	%{name}-nat.conf
Source10:	%{name}-dhcpd.conf
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-run_script.patch
Patch2:		%{name}-init_pl.patch
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
NoSource:	4
URL:		http://www.vmware.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.438
BuildRequires:	sed >= 4.0
Requires:	libgnomecanvasmm
Requires:	libsexy
Requires:	libsexymm
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles %{_libdir}/vmware*/lib/.*\.so.*

%description
VMware Server Virtual Platform is a thin software layer that allows
multiple guest operating systems to run concurrently on a single
standard PC, without repartitioning or rebooting, and without
significant loss of performance.

%description -l pl.UTF-8
VMware Server Virtual Platform to cienka warstwa oprogramowania
pozwalająca na jednoczesne działanie wielu gościnnych systemów
operacyjnych na jednym zwykłym PC, bez repartycjonowania ani
rebootowania, bez znacznej utraty wydajności.

%package debug
Summary:	VMware debug utility
Summary(pl.UTF-8):	Narzędzie VMware do odpluskwiania
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description debug
VMware debug utility.

%description debug -l pl.UTF-8
Narzędzie VMware do odpluskwiania.

%package console
Summary:	VMware console utility
Summary(pl.UTF-8):	Konsola VMware
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description console
A tool for controlling VM.

%description console -l pl.UTF-8
Narzędzie VMware do kontroli VM.

%package help
Summary:	VMware Server help files
Summary(pl.UTF-8):	Pliki pomocy dla VMware Server
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}
Requires:	mozilla

%description help
VMware Server help files.

%description help -l pl.UTF-8
Pliki pomocy dla VMware Server.

%package console-help
Summary:	VMware Server console help files
Summary(pl.UTF-8):	Pliki pomocy dla konsoli VMware Server
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}
Requires:	mozilla

%description console-help
VMware Server console help files.

%description console-help -l pl.UTF-8
Pliki pomocy dla konsoli VMware Server.

%package networking
Summary:	VMware networking utilities
Summary(pl.UTF-8):	Narzędzia VMware do obsługi sieci
Group:		Applications/Emulators
Requires(post,preun):	/sbin/chkconfig
#Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description networking
VMware networking utilities.

%description networking -l pl.UTF-8
Narzędzia VMware do obsługi sieci.

%package samba
Summary:	VMware SMB utilities
Summary(pl.UTF-8):	Narzędzia VMware do SMB
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description samba
VMware SMB utilities.

%description samba -l pl.UTF-8
Narzędzia VMware do SMB.

%package -n kernel-misc-vmci
Summary:	Kernel module for VMware Server
Summary(pl.UTF-8):	Moduł jądra dla VMware Server
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmci) = %{version}-%{rel}

%description -n kernel-misc-vmci
Kernel modules for VMware Server - vmci.

%description -n kernel-misc-vmci -l pl.UTF-8
Moduły jądra dla VMware Server - vmci.

%package -n kernel-misc-vmmon
Summary:	Kernel module for VMware Server
Summary(pl.UTF-8):	Moduł jądra dla VMware Server
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmmon) = %{version}-%{rel}

%description -n kernel-misc-vmmon
Kernel modules for VMware Server - vmmon.

%description -n kernel-misc-vmmon -l pl.UTF-8
Moduły jądra dla VMware Server - vmmon.

%package -n kernel-misc-vmnet
Summary:	Kernel module for VMware Server
Summary(pl.UTF-8):	Moduł jądra dla VMware Server
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmnet) = %{version}-%{rel}

%description -n kernel-misc-vmnet
Kernel modules for VMware Server - vmnet.

%description -n kernel-misc-vmnet -l pl.UTF-8
Moduły jądra dla VMware Server - vmnet.

%prep
%ifarch %{ix86}
%setup -q -T -n vmware-server-distrib -b0 %{?with_userspace:-a2}
%endif
%ifarch %{x8664}
%setup -q -T -n vmware-server-distrib -b1 %{?with_userspace:-a3}
%endif

cd lib/modules
%{__tar} xf source/vmci.tar
%{__tar} xf source/vmmon.tar
%{__tar} xf source/vmnet.tar
mv vmmon-only/linux/driver.c{,.dist}
mv vmnet-only/hub.c{,.dist}
mv vmnet-only/driver.c{,.dist}
rm -rf binary # unusable
cd -

%if 0
tar zxf vmware-mui-distrib/console-distrib/%{name}-console-%{ver}-%{subver}.tar.gz
cp vmware-any-any-update%{urel}/{vmmon,vmnet}.tar lib/modules/source/
cd lib/modules/source
tar xf vmmon.tar
tar xf vmnet.tar
#%patch0 -p0
cp -a vmmon-only{,.clean}
cp -a vmnet-only{,.clean}
cd -
%patch1 -p1
%patch2 -p0
tar xf lib/perl/control.tar
%endif

%build

%if 0
cd vmware-any-any-update%{urel}
chmod u+w ../lib/bin/vmware-vmx ../lib/bin-debug/vmware-vmx ../bin/vmnet-bridge
%endif

%if 0
rm -f update
%{__cc} %{rpmldflags} %{rpmcflags} -o update update.c
./update vmx		../lib/bin/vmware-vmx
./update vmxdebug	../lib/bin-debug/vmware-vmx
./update bridge		../bin/vmnet-bridge
cd -
%endif

%if %{with userspace}
%if 0
	cd control-only
	perl Makefile.PL
	sed -i "s:^INSTALLSITEARCH.*$:INSTALLSITEARCH = %{perl_vendorarch}:" Makefile
	sed -i "s:^INSTALLSITELIB.*$:INSTALLSITELIB = %{perl_vendorlib}:" Makefile
	sed -i "s:^INSTALLSITEMAN1DIR.*$:INSTALLSITEMAN1DIR = %{_mandir}/man1:" Makefile
	sed -i "s:^INSTALLSITEMAN3DIR.*$:INSTALLSITEMAN3DIR = %{_mandir}/man3:" Makefile

	%{__make}
	cd ..
%endif
%endif

%if %{with kernel}
cd lib/modules

%build_kernel_modules -C vmci-only -m vmci SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{ccver}

%build_kernel_modules -C vmmon-only -m vmmon SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{ccver} <<'EOF'
if grep -q "^CONFIG_PREEMPT_RT=y$" o/.config; then
	sed -e '/pollQueueLock/s/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(pollQueueLock)/' \
		-e '/timerLock/s/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(timerLock)/' \
	linux/driver.c.dist > linux/driver.c
else
	cat linux/driver.c.dist > linux/driver.c
fi
EOF

%build_kernel_modules -C vmnet-only -m vmnet SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{ccver} <<'EOF'
if grep -q "^CONFIG_PREEMPT_RT=y$" o/.config; then
	sed -e 's/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(vnetHubLock)/' \
		 hub.c.dist > hub.c
	sed -e 's/RW_LOCK_UNLOCKED/RW_LOCK_UNLOCKED(vnetPeerLock)/' \
		driver.c.dist > driver.c
else
	cat hub.c.dist > hub.c
	cat driver.c.dist > driver.c
fi
EOF
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware{,-server-console} \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/{nat,dhcpd} \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware{,-server-console}/bin \
	$RPM_BUILD_ROOT%{_libdir}/vmware/serverd \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/var/{log,run}/vmware

	cd control-only
	%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT
	cd ..

	# copy other required perl modules
	cp -r lib/perl5/site_perl/5.005/VMware $RPM_BUILD_ROOT%{perl_vendorarch}
	cp -r lib/perl5/site_perl/5.005/i386-linux/VMware/VmdbPerl $RPM_BUILD_ROOT%{perl_vendorarch}/VMware
	cp -r lib/perl5/site_perl/5.005/i386-linux/VMware/{HConfig,VmdbPerl}.pm $RPM_BUILD_ROOT%{perl_vendorarch}/VMware
	cp -r lib/perl5/site_perl/5.005/i386-linux/auto/VMware/{HConfig,VmdbPerl} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/VMware

	# remove unecessary files
	rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/VMware/{HConfig,VmdbPerl,VmPerl}/.{exists,packlist}
%endif

%if %{with kernel}
%install_kernel_modules -m lib/modules/vmci-only/vmci -d misc
%install_kernel_modules -m lib/modules/vmmon-only/vmmon -d misc
%install_kernel_modules -m lib/modules/vmnet-only/vmnet -d misc
%endif

%if %{with userspace}
install %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/vmnet
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet.conf
install %{SOURCE7} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE8} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/nat/nat.conf
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases~

install bin/*-* $RPM_BUILD_ROOT%{_bindir}
install sbin/*-* $RPM_BUILD_ROOT%{_sbindir}
install lib/bin/vmware-vmx $RPM_BUILD_ROOT%{_libdir}/vmware/bin

sed -e ' s@%sitearch%@%{perl_sitearch}@g; s@%sitelib%@%{perl_sitelib}@g; s@%vendorarch%@%{perl_vendorarch}@g; s@%vendorlib%@%{perl_vendorlib}@g; s@%archlib%@%{perl_archlib}@g; s@%privlib%@%{perl_privlib}@g;' < lib/serverd/init.pl.default > $RPM_BUILD_ROOT%{_libdir}/vmware/serverd/init.pl

#cp -r	lib/{bin-debug,config,help*,isoimages,licenses,messages,smb,xkeymap} \
cp -r	lib/{bin-debug,config,help*,isoimages,licenses,messages,share,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

cp -r	vmware-server-console-distrib/lib/{bin-debug,config,help*,messages,share,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware-server-console

install vmware-server-console-distrib/lib/bin/vmware-remotemks $RPM_BUILD_ROOT%{_libdir}/vmware-server-console/bin

cp -r	vmware-server-console-distrib/man/* man/* $RPM_BUILD_ROOT%{_mandir}
gunzip	$RPM_BUILD_ROOT%{_mandir}/man?/*.gz

cat > $RPM_BUILD_ROOT%{_sysconfdir}/vmware-server-console/locations <<EOF
VM_BINDIR=%{_bindir}
VM_LIBDIR=%{_libdir}/vmware-server-console
EOF

%if %{with internal_libs}
install bin/vmware $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmware $RPM_BUILD_ROOT%{_libdir}/vmware/bin
cp -r	lib/lib $RPM_BUILD_ROOT%{_libdir}/vmware

install vmware-server-console-distrib/bin/vmware-server-console $RPM_BUILD_ROOT%{_bindir}
install vmware-server-console-distrib/lib/bin/vmware $RPM_BUILD_ROOT%{_libdir}/vmware-server-console/bin
cp -r	vmware-server-console-distrib/lib/lib $RPM_BUILD_ROOT%{_libdir}/vmware-server-console
%else
install lib/bin/vmware $RPM_BUILD_ROOT%{_bindir}
install vmware-server-console-distrib/lib/bin/vmware-server-console $RPM_BUILD_ROOT%{_bindir}
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post networking
/sbin/chkconfig --add vmnet
%service vmnet restart "VMware networking service"

%preun networking
if [ "$1" = "0" ]; then
	%service vmnet stop
	/sbin/chkconfig --del vmnet
fi

%post	-n kernel-misc-vmci
%depmod %{_kernel_ver}

%postun -n kernel-misc-vmci
%depmod %{_kernel_ver}

%post	-n kernel-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel-misc-vmnet
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc doc/* lib/configurator/vmnet-{dhcpd,nat}.conf
%dir %{_sysconfdir}/vmware
%attr(755,root,root) %{_bindir}/vm-support
%attr(755,root,root) %{_bindir}/vmware-authtrusted
%attr(755,root,root) %{_bindir}/vmware-cmd
%attr(755,root,root) %{_bindir}/vmware
%attr(755,root,root) %{_bindir}/vmware-loop
%attr(755,root,root) %{_bindir}/vmware-mount.pl
%attr(755,root,root) %{_bindir}/vmware-vdiskmanager
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin/vmware-vmx
%{_libdir}/vmware/config
%{_libdir}/vmware/isoimages
%if %{with internal_libs}
%attr(755,root,root) %{_libdir}/vmware/bin/vmware
%{_libdir}/vmware/lib
%attr(755,root,root) %{_libdir}/vmware/lib/wrapper-gtk24.sh
%endif
%dir %{_libdir}/vmware/serverd
%attr(750,root,root) %{_libdir}/vmware/serverd/init.pl
%{_libdir}/vmware/licenses
%dir %{_libdir}/vmware/messages
%{_libdir}/vmware/messages/en
%lang(ja) %{_libdir}/vmware/messages/ja
%{_libdir}/vmware/share
%{_libdir}/vmware/xkeymap
%{_mandir}/man1/vmware.1*
%{_mandir}/man3/*
%{perl_vendorarch}/VMware
%{perl_vendorarch}/auto/VMware
%attr(1777,root,root) %dir /var/run/vmware
%attr(751,root,root) %dir /var/log/vmware
%{_pixmapsdir}/*.png
%{_desktopdir}/%{name}.desktop

%files console
%defattr(644,root,root,755)
%dir %{_sysconfdir}/vmware-server-console
%{_sysconfdir}/vmware-server-console/locations
%attr(755,root,root) %{_bindir}/vmware-server-console
%dir %{_libdir}/vmware-server-console
%dir %{_libdir}/vmware-server-console/bin
%attr(755,root,root) %{_libdir}/vmware-server-console/bin/vmware-remotemks
%{_libdir}/vmware-server-console/config
%if %{with internal_libs}
%attr(755,root,root) %{_libdir}/vmware-server-console/bin/vmware
%{_libdir}/vmware-server-console/lib
%attr(755,root,root) %{_libdir}/vmware-server-console/lib/wrapper-gtk24.sh
%endif
%dir %{_libdir}/vmware-server-console/messages
#%{_libdir}/vmware-server-console/messages/en
%lang(ja) %{_libdir}/vmware-server-console/messages/ja
%{_libdir}/vmware-server-console/share
%{_libdir}/vmware-server-console/xkeymap
%{_mandir}/man1/vmware-server-console.1*

%files console-help
%defattr(644,root,root,755)
%{_libdir}/vmware-server-console/help*

%files debug
%defattr(644,root,root,755)
%dir %{_libdir}/vmware/bin-debug
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin-debug/vmware-vmx
%dir %{_libdir}/vmware-server-console/bin-debug
%attr(755,root,root) %{_libdir}/vmware/bin-debug/vmware-remotemks
%attr(755,root,root) %{_libdir}/vmware-server-console/bin-debug/vmware-remotemks

%files help
%defattr(644,root,root,755)
%{_libdir}/vmware/help*

%files networking
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet.conf
%attr(754,root,root) /etc/rc.d/init.d/vmnet
%attr(755,root,root) %{_bindir}/vmnet-bridge
%attr(755,root,root) %{_bindir}/vmnet-dhcpd
%attr(755,root,root) %{_bindir}/vmnet-natd
%attr(755,root,root) %{_bindir}/vmnet-netifup
%attr(755,root,root) %{_bindir}/vmnet-sniffer
%attr(755,root,root) %{_bindir}/vmware-ping
%dir %{_sysconfdir}/vmware/vmnet8
%dir %{_sysconfdir}/vmware/vmnet8/dhcpd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf
%dir %{_sysconfdir}/vmware/vmnet8/nat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/nat/nat.conf
%verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases*

%if 0
%files samba
%defattr(644,root,root,755)
%doc lib/configurator/vmnet-smb.conf
%attr(755,root,root) %{_bindir}/vmware-nmbd
%attr(755,root,root) %{_bindir}/vmware-smbd
%attr(755,root,root) %{_bindir}/vmware-smbpasswd
%attr(755,root,root) %{_bindir}/vmware-smbpasswd.bin
%{_libdir}/vmware/smb
%endif
%endif

%if %{with kernel}
%files -n kernel-misc-vmci
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmci.ko*

%files -n kernel-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*
%endif

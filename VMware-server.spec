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
%bcond_without	internal_libs	# internal libs stuff
%bcond_without	doc # package huge docs
%bcond_with	verbose		# verbose build (V=1)
#
%include	/usr/lib/rpm/macros.perl
#
%define		ver	2.0
%define		subver	63231
%define		rel	0.5
%define		urel	115
%{expand:%%define	ccver	%(%{__cc} -dumpversion)}
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
Source11:	%{name}-libs
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-run_script.patch
Patch2:		%{name}-init_pl.patch
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
NoSource:	4
URL:		http://www.vmware.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.16}
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.438
BuildRequires:	sed >= 4.0
#Requires:	libgnomecanvasmm
#Requires:	libsexy
#Requires:	libsexymm
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles %{_libdir}/vmware*/lib/.*\.so.*
# TMP hack to compare with upstream rpm
%define		_libdir		%{_prefix}/lib
%define		_docdir		%{_defaultdocdir}/vmware

%define		sonamedeps	%(cat %{SOURCE11} | xargs)

%define		_noautoprov		%sonamedeps
%define		_noautoreq		%sonamedeps

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

%package -n kernel%{_alt_kernel}-misc-vmci
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

%description -n kernel%{_alt_kernel}-misc-vmci
Kernel modules for VMware Server - vmci.

%description -n kernel%{_alt_kernel}-misc-vmci -l pl.UTF-8
Moduły jądra dla VMware Server - vmci.

%package -n kernel%{_alt_kernel}-misc-vmmon
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

%description -n kernel%{_alt_kernel}-misc-vmmon
Kernel modules for VMware Server - vmmon.

%description -n kernel%{_alt_kernel}-misc-vmmon -l pl.UTF-8
Moduły jądra dla VMware Server - vmmon.

%package -n kernel%{_alt_kernel}-misc-vmnet
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

%description -n kernel%{_alt_kernel}-misc-vmnet
Kernel modules for VMware Server - vmnet.

%description -n kernel%{_alt_kernel}-misc-vmnet -l pl.UTF-8
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
#rm -rf binary # unusable
cd -

%{__gzip} -d man/man1/vmware.1.gz

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
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware/state \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware{,-server-console}/bin \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/var/{log,run}/vmware

%if 0
	cd control-only
	%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT
	cd ..
%endif

%if 0
	# copy other required perl modules
	cp -a lib/perl5/site_perl/5.005/VMware $RPM_BUILD_ROOT%{perl_vendorarch}
	cp -a lib/perl5/site_perl/5.005/i386-linux/VMware/VmdbPerl $RPM_BUILD_ROOT%{perl_vendorarch}/VMware
	cp -a lib/perl5/site_perl/5.005/i386-linux/VMware/{HConfig,VmdbPerl}.pm $RPM_BUILD_ROOT%{perl_vendorarch}/VMware
	cp -a lib/perl5/site_perl/5.005/i386-linux/auto/VMware/{HConfig,VmdbPerl} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/VMware

	# remove unecessary files
	rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/VMware/{HConfig,VmdbPerl,VmPerl}/.{exists,packlist}
%endif
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
cp -a lib/webAccess $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/hostd $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a vmware-vix $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/vmacore $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/net-services.sh $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/modules $RPM_BUILD_ROOT%{_libdir}/vmware
rm -rf $RPM_BUILD_ROOT%{_libdir}/vmware/modules/*-only
cp -a lib/configurator $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a etc/hostd $RPM_BUILD_ROOT/etc/vmware/hostd
cp -a etc/installer.sh $RPM_BUILD_ROOT/etc/vmware
cp -a etc/pam.d $RPM_BUILD_ROOT/etc/vmware
cp -a etc/service $RPM_BUILD_ROOT/etc/vmware

install -d $RPM_BUILD_ROOT%{_docdir}
cp -a doc/* $RPM_BUILD_ROOT%{_docdir}
cp -a vmware-vix-distrib/doc/VMwareVix $RPM_BUILD_ROOT%{_docdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -a man/man1/vmware.1 $RPM_BUILD_ROOT%{_mandir}/man1

install installer/services.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/vmware
ln -s vmware $RPM_BUILD_ROOT/etc/rc.d/init.d/vmware-autostart
ln -s vmware $RPM_BUILD_ROOT/etc/rc.d/init.d/vmware-core
ln -s vmware $RPM_BUILD_ROOT/etc/rc.d/init.d/vmware-mgmt
cat > $RPM_BUILD_ROOT%{_sysconfdir}/vmware/locations <<'EOF'
file /etc/vmware/locations
directory /etc/vmware/state
answer BINDIR /usr/bin
answer SBINDIR /usr/sbin
answer LIBDIR /usr/lib/vmware
answer DOCDIR /usr/share/doc/vmware
answer MANDIR /usr/share/man
answer INITDIR /etc/rc.d
answer INITSCRIPTSDIR /etc/rc.d/init.d
file /etc/vmware/not_configured 1205422799
file /etc/rc.d/init.d/vmware 1205422799
answer INSTALL_CYCLE yes
file /etc/rc.d/init.d/vmware-mgmt
file /etc/rc.d/init.d/vmware-core
file /etc/rc.d/init.d/vmware-autostart
EOF

rm $RPM_BUILD_ROOT/usr/bin/vmware-uninstall.pl
rm $RPM_BUILD_ROOT/usr/bin/vmware-vimdump
rm $RPM_BUILD_ROOT/usr/share/applications/VMware-server.desktop
rm $RPM_BUILD_ROOT/usr/share/pixmaps/VMware-server.png

%if 0
sed -e '
s@%sitearch%@%{perl_sitearch}@g;
s@%sitelib%@%{perl_sitelib}@g;
s@%vendorarch%@%{perl_vendorarch}@g;
s@%vendorlib%@%{perl_vendorlib}@g;
s@%archlib%@%{perl_archlib}@g;
s@%privlib%@%{perl_privlib}@g;' < lib/serverd/init.pl.default > $RPM_BUILD_ROOT%{_libdir}/vmware/serverd/init.pl
%endif

cp -a	lib/{config,help,isoimages,licenses,messages,share,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

%if 0
cp -a	vmware-server-console-distrib/lib/{bin-debug,config,help*,messages,share,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware-server-console

install vmware-server-console-distrib/lib/bin/vmware-remotemks $RPM_BUILD_ROOT%{_libdir}/vmware-server-console/bin

cp -a	vmware-server-console-distrib/man/* man/* $RPM_BUILD_ROOT%{_mandir}
gunzip	$RPM_BUILD_ROOT%{_mandir}/man?/*.gz
%endif

cat > $RPM_BUILD_ROOT%{_sysconfdir}/vmware-server-console/locations <<EOF
VM_BINDIR=%{_bindir}
VM_LIBDIR=%{_libdir}/vmware-server-console
EOF

%if %{with internal_libs}
install bin/vmware $RPM_BUILD_ROOT%{_bindir}
install lib/bin/* $RPM_BUILD_ROOT%{_libdir}/vmware/bin
#install lib/bin/vmware $RPM_BUILD_ROOT%{_libdir}/vmware/bin
cp -a	lib/lib $RPM_BUILD_ROOT%{_libdir}/vmware

%if 0
install vmware-server-console-distrib/bin/vmware-server-console $RPM_BUILD_ROOT%{_bindir}
install vmware-server-console-distrib/lib/bin/vmware $RPM_BUILD_ROOT%{_libdir}/vmware-server-console/bin
cp -a	vmware-server-console-distrib/lib/lib $RPM_BUILD_ROOT%{_libdir}/vmware-server-console
%endif

%else
%if 0
install lib/bin/vmware $RPM_BUILD_ROOT%{_bindir}
install vmware-server-console-distrib/lib/bin/vmware-server-console $RPM_BUILD_ROOT%{_bindir}
%endif
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

%post	-n kernel%{_alt_kernel}-misc-vmci
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmci
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(444,root,root,755)
#%doc lib/configurator/vmnet-{dhcpd,nat}.conf
%dir %{_sysconfdir}/vmware
%dir %{_sysconfdir}/vmware/state
%dir %{_sysconfdir}/vmware/hostd
%dir %{_sysconfdir}/vmware/hostd/env
%attr(644,root,root) %{_sysconfdir}/vmware/hostd/env/*.xml
%attr(444,root,root) %{_sysconfdir}/vmware/hostd/key.pub
%attr(644,root,root) %{_sysconfdir}/vmware/hostd/*.vha
%attr(644,root,root) %{_sysconfdir}/vmware/hostd/*.xml
%dir %{_sysconfdir}/vmware/pam.d
%attr(644,root,root) %{_sysconfdir}/vmware/pam.d/vmware-authd
%dir %{_sysconfdir}/vmware/service
%attr(644,root,root) %{_sysconfdir}/vmware/service/services.xml
%attr(555,root,root) %{_sysconfdir}/vmware/installer.sh
%{_sysconfdir}/vmware/locations

%attr(754,root,root) /etc/rc.d/init.d/vmware
%attr(754,root,root) /etc/rc.d/init.d/vmware-autostart
%attr(754,root,root) /etc/rc.d/init.d/vmware-core
%attr(754,root,root) /etc/rc.d/init.d/vmware-mgmt

%attr(555,root,root) %{_bindir}/vm-support
#%attr(755,root,root) %{_bindir}/vmware-authtrusted
#%attr(755,root,root) %{_bindir}/vmware-cmd
#%attr(755,root,root) %{_bindir}/vmware-loop
#%attr(755,root,root) %{_bindir}/vmware-mount.pl
%attr(555,root,root) %{_bindir}/vmware-config.pl
%attr(555,root,root) %{_bindir}/vmware-mount
#%attr(555,root,root) %{_bindir}/vmware-uninstall.pl
#%attr(555,root,root) %{_bindir}/vmware-vimdump
%attr(555,root,root) %{_bindir}/vmware-vimsh
%attr(555,root,root) %{_bindir}/vmware-vsh
%attr(555,root,root) %{_bindir}/vmware-watchdog
%attr(555,root,root) %{_bindir}/vmware-vdiskmanager
%attr(4555,root,root) %{_sbindir}/vmware-authd
%attr(555,root,root) %{_sbindir}/vmware-authdlauncher
%attr(555,root,root) %{_sbindir}/vmware-hostd
%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
# warning: SUID !!!
%attr(555,root,root) %{_libdir}/vmware/bin/vmware-vmx
%{_libdir}/vmware/config
%{_libdir}/vmware/isoimages
%if %{with internal_libs}
%attr(555,root,root) %{_bindir}/vmware
# - XXX -networking
%attr(4555,root,root) %{_bindir}/vmware-ping
#%attr(755,root,root) %{_libdir}/vmware/bin/vmware
%attr(555,root,root) %{_libdir}/vmware/bin/openssl
%attr(555,root,root) %{_libdir}/vmware/bin/vmplayer
%attr(555,root,root) %{_libdir}/vmware/bin/vmrun
%attr(755,root,root) %{_libdir}/vmware/bin/vmware-hostd
%attr(755,root,root) %{_libdir}/vmware/bin/vmware-hostd-dynamic
%attr(555,root,root) %{_libdir}/vmware/bin/vmware-remotemks
%attr(555,root,root) %{_libdir}/vmware/bin/vmware-remotemks-debug
%attr(555,root,root) %{_libdir}/vmware/bin/vmware-vimdump
%attr(555,root,root) %{_libdir}/vmware/bin/vmware-vmx-debug
%attr(777,root,root) %{_libdir}/vmware/bin/vmware-vmx-stats
%attr(755,root,root) %{_libdir}/vmware/bin/vmware-vsh

%dir %{_libdir}/vmware/lib
%{_libdir}/vmware/lib/libXau.so.6
%{_libdir}/vmware/lib/libXcursor.so.1
%{_libdir}/vmware/lib/libXdmcp.so.6
%{_libdir}/vmware/lib/libXfixes.so.3
%{_libdir}/vmware/lib/libXft.so.2
%{_libdir}/vmware/lib/libXinerama.so.1
%{_libdir}/vmware/lib/libXrandr.so.2
%{_libdir}/vmware/lib/libXrender.so.1
%{_libdir}/vmware/lib/libart_lgpl_2.so.2
%{_libdir}/vmware/lib/libatk-1.0.so.0
%{_libdir}/vmware/lib/libatkmm-1.6.so.1
%{_libdir}/vmware/lib/libcairo.so.2
%{_libdir}/vmware/lib/libcairomm-1.0.so.1
%{_libdir}/vmware/lib/libcrypto.so.0.9.7
%{_libdir}/vmware/lib/libcurl.so.3
%{_libdir}/vmware/lib/libcurl.so.4
%{_libdir}/vmware/lib/libfontconfig.so.1
%{_libdir}/vmware/lib/libfreetype.so.6
%{_libdir}/vmware/lib/libgdk-x11-2.0.so.0
%{_libdir}/vmware/lib/libgdk_pixbuf-2.0.so.0
%{_libdir}/vmware/lib/libgdkmm-2.4.so.1
%{_libdir}/vmware/lib/libglib-2.0.so.0
%{_libdir}/vmware/lib/libglibmm-2.4.so.1
%{_libdir}/vmware/lib/libglibmm_generate_extra_defs-2.4.so.1
%{_libdir}/vmware/lib/libgmodule-2.0.so.0
%{_libdir}/vmware/lib/libgobject-2.0.so.0
%{_libdir}/vmware/lib/libgthread-2.0.so.0
%{_libdir}/vmware/lib/libgtk-x11-2.0.so.0
%{_libdir}/vmware/lib/libgtkmm-2.4.so.1
%{_libdir}/vmware/lib/libpango-1.0.so.0
%{_libdir}/vmware/lib/libpangocairo-1.0.so.0
%{_libdir}/vmware/lib/libpangoft2-1.0.so.0
%{_libdir}/vmware/lib/libpangomm-1.4.so.1
%{_libdir}/vmware/lib/libpangox-1.0.so.0
%{_libdir}/vmware/lib/libpangoxft-1.0.so.0
%{_libdir}/vmware/lib/librsvg-2.so.2
%{_libdir}/vmware/lib/libsexy.so.2
%{_libdir}/vmware/lib/libsexymm.so.2
%{_libdir}/vmware/lib/libsigc-2.0.so.0
%{_libdir}/vmware/lib/libssl.so.0.9.7
%{_libdir}/vmware/lib/libview.so.2
%{_libdir}/vmware/lib/libxmlrpc.so.3
%{_libdir}/vmware/lib/libxmlrpc_client.so.3
%{_libdir}/vmware/lib/libxmlrpc_util.so.3
%{_libdir}/vmware/lib/libxmlrpc_xmlparse.so.3
%{_libdir}/vmware/lib/libxmlrpc_xmltok.so.3


%dir %{_libdir}/vmware/lib/libexpat.so.0
%attr(755,root,root) %{_libdir}/vmware/lib/libexpat.so.0/libexpat.so.0
%dir %{_libdir}/vmware/lib/libgcc_s.so.1
%attr(755,root,root) %{_libdir}/vmware/lib/libgcc_s.so.1/libgcc_s.so.1
%dir %{_libdir}/vmware/lib/libgvmomi.so.0
%attr(555,root,root) %{_libdir}/vmware/lib/libgvmomi.so.0/libgvmomi.so.0
%dir %{_libdir}/vmware/lib/libpng12.so.0
%attr(755,root,root) %{_libdir}/vmware/lib/libpng12.so.0/libpng12.so.0
%dir %{_libdir}/vmware/lib/libstdc++.so.6
%attr(755,root,root) %{_libdir}/vmware/lib/libstdc++.so.6/libstdc++.so.6
%dir %{_libdir}/vmware/lib/libvmwarebase.so.0
%attr(555,root,root) %{_libdir}/vmware/lib/libvmwarebase.so.0/libvmwarebase.so.0
%dir %{_libdir}/vmware/lib/libvmwareui.so.0
%attr(555,root,root) %{_libdir}/vmware/lib/libvmwareui.so.0/libvmwareui.so.0
%dir %{_libdir}/vmware/lib/libxml2.so.2
%attr(755,root,root) %{_libdir}/vmware/lib/libxml2.so.2/libxml2.so.2


%attr(555,root,root) %{_libdir}/vmware/lib/wrapper-gtk24.sh
%endif
#%dir %{_libdir}/vmware/serverd
#%attr(750,root,root) %{_libdir}/vmware/serverd/init.pl
%{_libdir}/vmware/licenses
%dir %{_libdir}/vmware/messages
#%{_libdir}/vmware/messages/en
%lang(ja) %{_libdir}/vmware/messages/ja
%{_libdir}/vmware/share
%{_libdir}/vmware/xkeymap
%dir %{_libdir}/vmware/hostd
%attr(755,root,root) %{_libdir}/vmware/hostd/*.so
%{_libdir}/vmware/hostd/locale
%dir %{_libdir}/vmware/hostd/docroot
%dir %{_libdir}/vmware/hostd/docroot/client
%dir %{_libdir}/vmware/hostd/docroot/sdk
%dir %{_libdir}/vmware/hostd/docroot/downloads
%{_libdir}/vmware/hostd/docroot/*.png
%{_libdir}/vmware/hostd/docroot/*.js
%{_libdir}/vmware/hostd/docroot/*.jpeg
%{_libdir}/vmware/hostd/docroot/*.html
%{_libdir}/vmware/hostd/docroot/*.css
%{_libdir}/vmware/hostd/docroot/en
%attr(644,root,root) %{_libdir}/vmware/hostd/docroot/client/VMware-viclient.exe
%attr(644,root,root) %{_libdir}/vmware/hostd/docroot/client/clients-template.xml
%attr(644,root,root) %{_libdir}/vmware/hostd/docroot/sdk/vim.wsdl
%attr(644,root,root) %{_libdir}/vmware/hostd/docroot/sdk/vimService.wsdl

%attr(755,root,root) %{_libdir}/vmware/hostd/py
%attr(755,root,root) %{_libdir}/vmware/hostd/wsdl
%{_mandir}/man1/vmware.1*
#%{_mandir}/man3/*
#%{perl_vendorarch}/VMware
#%{perl_vendorarch}/auto/VMware
%attr(1777,root,root) %dir /var/run/vmware
%attr(751,root,root) %dir /var/log/vmware
#%{_pixmapsdir}/*.png
#%{_desktopdir}/%{name}.desktop

%dir %{_libdir}/vmware/vmacore
%attr(755,root,root) %{_libdir}/vmware/vmacore/libvmacore.so.*.*
%attr(755,root,root) %{_libdir}/vmware/vmacore/libvmomi.so.*.*

# belongs to -help
%{_libdir}/vmware/help

%defattr(444,root,root,755)
%dir %doc %{_docdir}
%doc %{_docdir}/[ERo]*
%defattr(644,root,root,755)
%doc %dir %{_docdir}/VMwareVix
%doc %{_docdir}/VMwareVix/lang
%doc %{_docdir}/VMwareVix/errors
%doc %{_docdir}/VMwareVix/types
%attr(444,root,root) %doc %{_docdir}/VMwareVix/*.html
%dir %{_docdir}/VMwareVix/samples
%attr(666,root,root) %doc %{_docdir}/VMwareVix/samples/*.c

%defattr(-,root,root,755)
%dir %{_libdir}/vmware/webAccess
%defattr(444,root,root,755)
%dir %{_libdir}/vmware/webAccess/java
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/bin/*
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/bin
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*/headless/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*/motif21/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*/native_threads/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*/xawt/*.so
# yeah. go figure
%attr(777,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*/server/libjsig.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*/server/libjvm.so
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/*.jar
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/ext
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/font*
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/im
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/images
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/zi
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/audio
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/cmm
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/security
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/management
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/oblique-fonts
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/psfont*
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/[A-Z]*
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/.systemPrefs
%attr(644,root,root) %{_libdir}/vmware/webAccess/vmware*
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/awt_robot
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/gtkhelper
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/jvm.cfg
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/classlist
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/content-types.properties
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/flavormap.properties
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/jvm.hprof.txt
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/logging.properties
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/net.properties
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/sound.properties
%{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/server/Xusage.txt
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/headless
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/motif21
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/native_threads
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/server
%dir %{_libdir}/vmware/webAccess/java/jre1.5.0_07/lib/amd64/xawt

%defattr(444,root,root,755)
%dir %{_libdir}/vmware/webAccess/tomcat
%dir %{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/common
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/conf
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/logs
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/server
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/temp
%defattr(555,root,root,755)
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/bin
%defattr(644,root,root,755)
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/webapps
%defattr(444,root,root,755)
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/LICENSE
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/NOTICE
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/RELEASE-NOTES
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-5.5.17/RUNNING.txt

%defattr(444,root,root,755)
%{_libdir}/vmware/vmware-vix

%defattr(555,root,root,755)
%{_libdir}/vmware/net-services.sh

%defattr(444,root,root,755)
%{_libdir}/vmware/modules
%{_libdir}/vmware/configurator

# -networking stuff
%attr(555,root,root) %{_bindir}/vmnet-bridge
%attr(555,root,root) %{_bindir}/vmnet-dhcpd
%attr(555,root,root) %{_bindir}/vmnet-natd
%attr(555,root,root) %{_bindir}/vmnet-netifup
%attr(555,root,root) %{_bindir}/vmnet-sniffer

%files console
%defattr(644,root,root,755)
%dir %{_sysconfdir}/vmware-server-console
%{_sysconfdir}/vmware-server-console/locations
#%attr(755,root,root) %{_bindir}/vmware-server-console
%dir %{_libdir}/vmware-server-console
%dir %{_libdir}/vmware-server-console/bin
#%attr(755,root,root) %{_libdir}/vmware-server-console/bin/vmware-remotemks
#%{_libdir}/vmware-server-console/config
%if %{with internal_libs}
#%attr(755,root,root) %{_libdir}/vmware-server-console/bin/vmware
#%{_libdir}/vmware-server-console/lib
#%attr(755,root,root) %{_libdir}/vmware-server-console/lib/wrapper-gtk24.sh
%endif
#%dir %{_libdir}/vmware-server-console/messages
#%{_libdir}/vmware-server-console/messages/en
#%lang(ja) %{_libdir}/vmware-server-console/messages/ja
#%{_libdir}/vmware-server-console/share
#%{_libdir}/vmware-server-console/xkeymap
#%{_mandir}/man1/vmware-server-console.1*

%files console-help
%defattr(644,root,root,755)
#%{_libdir}/vmware-server-console/help*

%files debug
%defattr(644,root,root,755)
#%dir %{_libdir}/vmware/bin-debug
# warning: SUID !!!
#%attr(4755,root,root) %{_libdir}/vmware/bin-debug/vmware-vmx
#%dir %{_libdir}/vmware-server-console/bin-debug
#%attr(755,root,root) %{_libdir}/vmware/bin-debug/vmware-remotemks
#%attr(755,root,root) %{_libdir}/vmware-server-console/bin-debug/vmware-remotemks

%if 0
%files help
%defattr(644,root,root,755)
%{_libdir}/vmware/help
%endif

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
%files -n kernel%{_alt_kernel}-misc-vmci
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmci.ko*

%files -n kernel%{_alt_kernel}-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel%{_alt_kernel}-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*
%endif

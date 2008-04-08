# TODO
# - make vmware-config.pl work
# - sane permissions
# - switch to proper %{_libdir} when done for 64bit arch
# - use system java, tomcat, etc packages
# - package webAccess elsewhere, seems noarch mostly (but if using system pkgs for java/tomcat leave it still huge)
# - put things back to subpackages (if makes sense)
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
%define		subver	84186
%define		rel	0.5
%{expand:%%global	ccver	%(%{__cc} -dumpversion)}
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
# NoSource0-md5:	30f20c55a76ba46543df0e80bd21affc
Source1:	http://download3.vmware.com/software/vmserver/%{name}-e.x.p-%{subver}.x86_64.tar.gz
# NoSource1-md5:	31dcec2889bcac228f76f0914e89469b
Source2:	http://download3.vmware.com/software/vmserver/VMware-vix-e.x.p-%{subver}.i386.tar.gz
# NoSource2-md5:	d81db3079785a7454902aed222e611ad
Source3:	http://download3.vmware.com/software/vmserver/VMware-vix-e.x.p-%{subver}.x86_64.tar.gz
# NoSource3-md5:	bc7bdf81d14887861b4f5413e78fd539
Source4:	%{name}.png
Source5:	%{name}.desktop
Source6:	%{name}-authd.rc-inetd
Source7:	%{name}-nat.conf
Source8:	%{name}-dhcpd.conf
Source9:	%{name}-dhcpd-hostonly.conf
Source10:	%{name}-parse-locations.pl
Source11:	%{name}-libs
Source12:	%{name}-locations
Patch0:		%{name}-config-rc-inetd.patch
Patch1:		%{name}-config-kernel.patch
Patch2:		%{name}-config-pam.patch
Patch3:		%{name}-initscript.patch
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
URL:		http://www.vmware.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.16}
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.449
BuildRequires:	sed >= 4.0
Requires:	%{name}-isoimages = %{version}
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

%description -n kernel%{_alt_kernel}-misc-vmnet
Kernel modules for VMware Server - vmnet.

%description -n kernel%{_alt_kernel}-misc-vmnet -l pl.UTF-8
Moduły jądra dla VMware Server - vmnet.

%package -n kernel%{_alt_kernel}-misc-vsock
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
Requires:	kernel%{_alt_kernel}-misc-vmci = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vsock
Kernel modules for VMware Server - vsock.

%description -n kernel%{_alt_kernel}-misc-vsock -l pl.UTF-8
Moduły jądra dla VMware Server - vsock.

%prep
%ifarch %{ix86}
%setup -q -T -n vmware-server-distrib -b0 %{?with_userspace:-a2}
%endif
%ifarch %{x8664}
%setup -q -T -n vmware-server-distrib -b1 %{?with_userspace:-a3}
%endif

rm -rf lib/isoimages # packaged by %{name}-isoimages.spec

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cd lib/modules
%{__tar} xf source/vmci.tar
%{__tar} xf source/vmmon.tar
%{__tar} xf source/vmnet.tar
%{__tar} xf source/vsock.tar
mv vmmon-only/linux/driver.c{,.dist}
mv vmnet-only/hub.c{,.dist}
mv vmnet-only/driver.c{,.dist}
rm -rf binary # unusable
cd -

%{__gzip} -d man/man1/vmware.1.gz

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
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

cp -a vmci-only/Module.symvers vsock-only
%build_kernel_modules -C vsock-only -m vsock SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{ccver} -c
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m lib/modules/vmci-only/vmci -d misc
%install_kernel_modules -m lib/modules/vmmon-only/vmmon -d misc
%install_kernel_modules -m lib/modules/vmnet-only/vmnet -d misc
%install_kernel_modules -m lib/modules/vsock-only/vsock -d misc
%endif

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet{1,8}/{nat,dhcpd} \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware/state \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware/bin \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d} \
	$RPM_BUILD_ROOT/var/{log,run}/vmware \
	$RPM_BUILD_ROOT/var/lib/vmware/{hostd,"Virtual Machines"}

install %{SOURCE4} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/nat/nat.conf
install %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf
install %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet1/dhcpd/dhcpd.conf
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/parse-locations.pl
cp -a %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/locations

touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet{1,8}/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet{1,8}/dhcpd/dhcpd.leases~

install bin/*-* $RPM_BUILD_ROOT%{_bindir}
install sbin/*-* $RPM_BUILD_ROOT%{_sbindir}
install lib/bin/vmware-vmx $RPM_BUILD_ROOT%{_libdir}/vmware/bin
cp -a lib/webAccess $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/hostd $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a vmware-vix $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/vmacore $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/net-services.sh $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a lib/configurator $RPM_BUILD_ROOT%{_libdir}/vmware
cp -a %{SOURCE6} $RPM_BUILD_ROOT%{_libdir}/vmware/configurator/authd-rc-inetd.conf
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd
sed -e 's,%port%,902,;s,%authd%,%{_sbindir}/vmware-authd,' %{SOURCE6} > $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/vmware-authd
cp -a etc/hostd $RPM_BUILD_ROOT/etc/vmware/hostd
cp -a etc/installer.sh $RPM_BUILD_ROOT/etc/vmware
cp -a etc/pam.d/vmware-authd $RPM_BUILD_ROOT/etc/pam.d
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

rm $RPM_BUILD_ROOT/usr/bin/vmware-uninstall.pl
rm $RPM_BUILD_ROOT/usr/bin/vmware-vimdump
rm $RPM_BUILD_ROOT/usr/share/applications/VMware-server.desktop
rm $RPM_BUILD_ROOT/usr/share/pixmaps/VMware-server.png

cp -a	lib/{config,help,licenses,messages,share,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

%if %{with internal_libs}
install bin/vmware $RPM_BUILD_ROOT%{_bindir}
install lib/bin/* $RPM_BUILD_ROOT%{_libdir}/vmware/bin
cp -a	lib/lib $RPM_BUILD_ROOT%{_libdir}/vmware
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

%post	-n kernel%{_alt_kernel}-misc-vsock
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vsock
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/vmware-authd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/vmware-authd
%dir %{_sysconfdir}/vmware
%dir %{_sysconfdir}/vmware/state
%dir %{_sysconfdir}/vmware/hostd
%dir %{_sysconfdir}/vmware/hostd/env
%{_sysconfdir}/vmware/hostd/env/*.xml
%{_sysconfdir}/vmware/hostd/key.pub
%{_sysconfdir}/vmware/hostd/*.vha
%{_sysconfdir}/vmware/hostd/*.xml
%dir %{_sysconfdir}/vmware/service
%{_sysconfdir}/vmware/service/services.xml
%{_sysconfdir}/vmware/installer.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/locations
%attr(755,root,root) %{_sysconfdir}/vmware/parse-locations.pl

# vmnet1: HostOnly
%dir %{_sysconfdir}/vmware/vmnet1
%dir %{_sysconfdir}/vmware/vmnet1/dhcpd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet1/dhcpd/dhcpd.conf
%ghost %{_sysconfdir}/vmware/vmnet1/dhcpd/dhcpd.leases*

# vmnet8: NAT
%dir %{_sysconfdir}/vmware/vmnet8
%dir %{_sysconfdir}/vmware/vmnet8/dhcpd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf
%dir %{_sysconfdir}/vmware/vmnet8/nat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/nat/nat.conf
%ghost %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases*

%attr(754,root,root) /etc/rc.d/init.d/vmware
%attr(754,root,root) /etc/rc.d/init.d/vmware-autostart
%attr(754,root,root) /etc/rc.d/init.d/vmware-core
%attr(754,root,root) /etc/rc.d/init.d/vmware-mgmt

%attr(555,root,root) %{_bindir}/vm-support
%attr(555,root,root) %{_bindir}/vmware-config.pl
%attr(555,root,root) %{_bindir}/vmware-mount
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
%if %{with internal_libs}
%attr(555,root,root) %{_bindir}/vmware
# - XXX -networking
%attr(4555,root,root) %{_bindir}/vmware-ping
%attr(555,root,root) %{_libdir}/vmware/bin/openssl
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
%{_libdir}/vmware/lib/libcrypto.so.0.9.7
%{_libdir}/vmware/lib/libcurl.so.4
%{_libdir}/vmware/lib/libglib-2.0.so.0
%{_libdir}/vmware/lib/libgobject-2.0.so.0
%{_libdir}/vmware/lib/libgthread-2.0.so.0
%{_libdir}/vmware/lib/libssl.so.0.9.7
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
%dir %{_libdir}/vmware/lib/libxml2.so.2
%attr(755,root,root) %{_libdir}/vmware/lib/libxml2.so.2/libxml2.so.2
%dir %{_libdir}/vmware/lib/libpixops.so.2.0.2
%attr(755,root,root) %{_libdir}/vmware/lib/libpixops.so.2.0.2/libpixops.so.2.0.2

%attr(555,root,root) %{_libdir}/vmware/lib/wrapper-gtk24.sh
%endif
%{_libdir}/vmware/licenses
%dir %{_libdir}/vmware/messages
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
%attr(444,root,root) %doc %{_docdir}/VMwareVix/*.css
%dir %{_docdir}/VMwareVix/samples
%attr(666,root,root) %doc %{_docdir}/VMwareVix/samples/*.c

%defattr(-,root,root,755)
%dir %{_libdir}/vmware/webAccess
%defattr(444,root,root,755)
# TODO: use system java-sun
%dir %{_libdir}/vmware/webAccess/java
%dir %{_libdir}/vmware/webAccess/java/jre*
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/bin/*
%dir %{_libdir}/vmware/webAccess/java/jre*/bin
%dir %{_libdir}/vmware/webAccess/java/jre*/lib
%ifarch %{ix86}
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/i386
%endif
%ifarch %{x8664}
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/amd64
%endif
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/*/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/*/headless/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/*/motif21/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/*/native_threads/*.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/*/xawt/*.so
# yeah. go figure
%attr(777,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/*/server/libjsig.so
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/*/server/libjvm.so
%{_libdir}/vmware/webAccess/java/jre*/lib/*.jar
%{_libdir}/vmware/webAccess/java/jre*/lib/ext
%{_libdir}/vmware/webAccess/java/jre*/lib/font*
%{_libdir}/vmware/webAccess/java/jre*/lib/im
%{_libdir}/vmware/webAccess/java/jre*/lib/images
%{_libdir}/vmware/webAccess/java/jre*/lib/zi
%{_libdir}/vmware/webAccess/java/jre*/lib/audio
%{_libdir}/vmware/webAccess/java/jre*/lib/cmm
%{_libdir}/vmware/webAccess/java/jre*/lib/security
%{_libdir}/vmware/webAccess/java/jre*/lib/management
%{_libdir}/vmware/webAccess/java/jre*/lib/oblique-fonts
%{_libdir}/vmware/webAccess/java/jre*/lib/psfont*
%{_libdir}/vmware/webAccess/java/jre*/[A-Z]*
%attr(644,root,root) %{_libdir}/vmware/webAccess/vmware*
%ifarch %{ix86}
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/i386/awt_robot
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/i386/gtkhelper
%{_libdir}/vmware/webAccess/java/jre*/lib/i386/jvm.cfg
%{_libdir}/vmware/webAccess/java/jre*/lib/i386/server/Xusage.txt
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/i386/headless
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/i386/motif21
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/i386/native_threads
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/i386/server
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/i386/xawt
%endif
%ifarch %{x8664}
%{_libdir}/vmware/webAccess/java/jre*/.systemPrefs
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/amd64/awt_robot
%attr(555,root,root) %{_libdir}/vmware/webAccess/java/jre*/lib/amd64/gtkhelper
%{_libdir}/vmware/webAccess/java/jre*/lib/amd64/jvm.cfg
%{_libdir}/vmware/webAccess/java/jre*/lib/amd64/server/Xusage.txt
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/amd64/headless
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/amd64/motif21
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/amd64/native_threads
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/amd64/server
%dir %{_libdir}/vmware/webAccess/java/jre*/lib/amd64/xawt
%endif
%{_libdir}/vmware/webAccess/java/jre*/lib/classlist
%{_libdir}/vmware/webAccess/java/jre*/lib/content-types.properties
%{_libdir}/vmware/webAccess/java/jre*/lib/flavormap.properties
%{_libdir}/vmware/webAccess/java/jre*/lib/jvm.hprof.txt
%{_libdir}/vmware/webAccess/java/jre*/lib/logging.properties
%{_libdir}/vmware/webAccess/java/jre*/lib/net.properties
%{_libdir}/vmware/webAccess/java/jre*/lib/sound.properties

%defattr(444,root,root,755)
%dir %{_libdir}/vmware/webAccess/tomcat
%dir %{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/conf
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/temp
%defattr(555,root,root,755)
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/bin
%defattr(644,root,root,755)
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/webapps
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/lib
%defattr(444,root,root,755)
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/LICENSE
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/NOTICE
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/RELEASE-NOTES
%{_libdir}/vmware/webAccess/tomcat/apache-tomcat-*/RUNNING.txt

%defattr(444,root,root,755)
%{_libdir}/vmware/vmware-vix

%defattr(555,root,root,755)
%{_libdir}/vmware/net-services.sh

%defattr(444,root,root,755)
%{_libdir}/vmware/configurator

# -networking stuff
%attr(555,root,root) %{_bindir}/vmnet-bridge
%attr(555,root,root) %{_bindir}/vmnet-dhcpd
%attr(555,root,root) %{_bindir}/vmnet-natd
%attr(555,root,root) %{_bindir}/vmnet-netifup
%attr(555,root,root) %{_bindir}/vmnet-sniffer

%if 0
%files console
%defattr(644,root,root,755)
%dir %{_sysconfdir}/vmware-server-console
%{_sysconfdir}/vmware-server-console/locations
%dir %{_libdir}/vmware-server-console
%dir %{_libdir}/vmware-server-console/bin

%files console-help
%defattr(644,root,root,755)

%files debug
%defattr(644,root,root,755)

%files help
%defattr(644,root,root,755)
%{_libdir}/vmware/help

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

%files -n kernel%{_alt_kernel}-misc-vsock
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vsock.ko*
%endif

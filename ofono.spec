Summary:	oFono - Open Source Telephony
Summary(pl.UTF-8):	oFono - telefonia o otwartych źródłach
Name:		ofono
Version:	1.24
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	https://www.kernel.org/pub/linux/network/ofono/%{name}-%{version}.tar.xz
# Source0-md5:	be24e80f6551f46fea0c5b5879964d6c
Patch0:		%{name}-missing.patch
URL:		https://01.org/ofono
BuildRequires:	bluez-libs-devel >= 4.99
BuildRequires:	dbus-devel >= 1.4
BuildRequires:	ell-devel >= 0.2
BuildRequires:	gcc >= 5:3.4
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	mobile-broadband-provider-info-devel
BuildRequires:	pkgconfig
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:143
BuildRequires:	xz
Requires:	dbus >= 1.4
Requires:	glib2 >= 1:2.32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
oFono is an infrastructure for building mobile telephony (GSM/UMTS)
applications. oFono is licensed under GPL v2, and it includes a
high-level D-Bus API for use by telephony applications of any license.
oFono also includes a low-level plug-in API for integrating with open
source as well as third party telephony stacks, cellular modems and
storage back-ends.

%description -l pl.UTF-8
oFono to infrastruktura do tworzenia aplikacji związanych z telefonią
komórkową (GSM/UMTS). oFono jest wydawane na licencji GPL v2 i zawiera
wysokopoziomowe API D-Bus do wykorzystywania przez aplikacje na
dowolnej licencji. oFono zawiera także niskopoziomowe API wtyczek do
integracji z oprogramowaniem o otwartych źródłach, a także stosami
telefonicznych innych producentów, modemami komórkowymi oraz
backendami do przechowywania danych.

%package devel
Summary:	Header files for oFono plugins
Summary(pl.UTF-8):	Pliki nagłówkowe dla wtyczek oFono
Group:		Development/Libraries
Requires:	dbus-devel >= 1.4
Requires:	glib2-devel >= 1:2.32
# doesn't require base

%description devel
Header files for oFono plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla wtyczek oFono.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	--enable-dundee \
	--enable-ell \
	--enable-mbimmodem \
	--enable-pie \
	--enable-threads \
	--enable-tools
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ofono/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/dundee
%attr(755,root,root) %{_sbindir}/ofonod
%dir %{_libdir}/ofono
%dir %{_libdir}/ofono/plugins
%dir %{_sysconfdir}/ofono
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ofono/phonesim.conf
/etc/dbus-1/system.d/dundee.conf
/etc/dbus-1/system.d/ofono.conf
/lib/systemd/system/dundee.service
/lib/systemd/system/ofono.service
%{_mandir}/man8/ofonod.8*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt
%{_includedir}/ofono
%{_pkgconfigdir}/ofono.pc

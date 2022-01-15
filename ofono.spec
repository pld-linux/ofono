Summary:	oFono - Open Source Telephony
Summary(pl.UTF-8):	oFono - telefonia o otwartych źródłach
Name:		ofono
Version:	1.34
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	https://www.kernel.org/pub/linux/network/ofono/%{name}-%{version}.tar.xz
# Source0-md5:	0d0fe9ed5b263f3cc9e11f6cb997d3ef
URL:		https://01.org/ofono
BuildRequires:	dbus-devel >= 1.6
BuildRequires:	ell-devel >= 0.12
BuildRequires:	gcc >= 5:3.4
BuildRequires:	glib2-devel >= 1:2.68
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	mobile-broadband-provider-info-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:143
BuildRequires:	xz
Requires:	dbus >= 1.6
Requires:	ell >= 0.12
Requires:	glib2 >= 1:2.68
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
Requires:	dbus-devel >= 1.6
Requires:	glib2-devel >= 1:2.68
# doesn't require base

%description devel
Header files for oFono plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla wtyczek oFono.

%prep
%setup -q

# no debug symbols in ofono itself
# and it requires __ell_debug__ section start/stop symbols, which are not exported from shared ell (as of ell 0.17)
%{__sed} -i -e '/l_debug_enable/d' src/main.c

%build
%configure \
	--disable-silent-rules \
	--enable-dundee \
	--enable-external-ell \
	--enable-mbimmodem \
	--enable-pie \
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

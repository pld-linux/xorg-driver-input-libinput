Summary:	A libinput-based X.org input driver
Summary(pl.UTF-8):	Sterownik wejściowy X.org oparty na libinput
Name:		xorg-driver-input-libinput
Version:	0.10.0
Release:	2
License:	MIT
Group:		X11/Applications
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-input-libinput-%{version}.tar.bz2
# Source0-md5:	e0d6fc2aceba154e57501d36e361d3f7
Source1:	90-libinput.conf
# Source1-md5: xyz
Patch0:		0001-Only-init-abs-axes-if-we-don-t-have-acceleration.patch
# fedora Bug 1208992 - Mouse cursor doesn't move when moving the physical mouse slowly
Patch1:		0001-Use-the-new-unaccelerated-valuator-ValuatorMask-feat.patch
Patch2:		0001-Fix-missing-scroll-methods-default-scroll-button-pro.patch
URL:		http://xorg.freedesktop.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	libinput-devel >= 0.11.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(macros) >= 1.389
BuildRequires:	xorg-proto-inputproto-devel >= 2.2
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	xorg-util-util-macros >= 1.8
BuildRequires:	xorg-xserver-server-devel >= 1.10
%{?requires_xorg_xserver_xinput}
Requires:	libinput >= 0.11.0
Requires:	xorg-xserver-server >= 1.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an X driver based on libinput. It is a thin wrapper around
libinput, so while it does provide all features that libinput supports
it does little beyond.

%description -l pl.UTF-8
Sterownik wejściowy X oparty na libinput. Jest to bardzo cienkie
obudowanie biblioteki libinput, więc udostępnia wszystkie funkcje
obsługiwane przez libinput, ale niewiele poza tym.

%package devel
Summary:	Header file for libinput driver
Summary(pl.UTF-8):	Plik nagłówkowy sterownika libinput
Group:		Development/Libraries

%description devel
Header file for libinput driver.

%description devel -l pl.UTF-8
Plik nagłówkowy sterownika libinput.

%prep
%setup -q -n xf86-input-libinput-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/90-libinput.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/*/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README.md
/etc/X11/xorg.conf.d/90-libinput.conf
%attr(755,root,root) %{_libdir}/xorg/modules/input/libinput_drv.so
%{_mandir}/man4/libinput.4*

%files devel
%defattr(644,root,root,755)
%{_includedir}/xorg/libinput-properties.h
%{_pkgconfigdir}/xorg-libinput.pc

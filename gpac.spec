#
# TODO: soname for libm4systems(?)
# - use system mozilla includes
#
# Conditional build:
%bcond_with	amr
%bcond_without	faad
%bcond_without	ffmpeg
%bcond_without	freetype
%bcond_without	jpeg
%bcond_without	js
%bcond_without	mad
%bcond_without	png
%bcond_without	xvid
%bcond_with	wx
#
Summary:	GPAC - an implementation of the MPEG-4 Systems standard (ISO/IEC 14496-1)
Summary(pl):	GPAC - implementacja standardu MPEG-4 Systems (ISO/IEC 14496-1)
Name:		gpac
Version:	0.4.0
Release:	1
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/gpac/%{name}-%{version}.tar.gz
# Source0-md5:	a8b4b3206cabda946850240f1e7aea93
Source1:	http://www.3gpp.org/ftp/Specs/archive/26_series/26.073/26073-530.zip
# Source1-md5:	705f6993fbf890e92eb7a331e7c716d1
Patch0:		%{name}-install.patch
Patch1:		%{name}-wxWidgets.patch
URL:		http://gpac.sourceforge.net/
BuildRequires: 	SDL-devel
%{?with_wx:BuildRequires:	wxGTK2-devel >= 2.5.4}
%{?with_faad:BuildRequires:	faad2-devel}
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
%{?with_freetype:BuildRequires:	freetype-devel}
%{?with_js:BuildRequires:	js-devel}
%{?with_jpeg:BuildRequires:	libjpeg-devel}
%{?with_mad:BuildRequires:	libmad-devel}
%{?with_png:BuildRequires:	libpng-devel}
BuildRequires:	libxml2-devel
%{?with_xvid:BuildRequires:	xvid-devel}
Requires:	SDL
%{?with_faad:Requires:	faad2}
%{?with_ffmpeg:Requires:	ffmpeg}
%{?with_freetype:Requires:	freetype}
%{?with_js:Requires:	js}
%{?with_jpeg:Requires:	libjpeg}
%{?with_png:Requires:	libpng}
%{?with_mad:Requires:	libmad}
%{?with_xvid:Requires:	xvid}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreq   libm4systems.so
%define         _plugindir      %{_libdir}/browser-plugins

%description
GPAC is an implementation of the MPEG-4 Systems standard (ISO/IEC
14496-1) developed from scratch in ANSI C.

The main development goal is to provide a clean (a.k.a. readable by as
many people as possible), small and flexible alternative to the MPEG-4
Systems reference software (known as IM1 and distributed in ISO/IEC
14496-5). The MPEG-4 Reference software is indeed a very large piece
of software, designed to verify the standard rather than provide a
small, production-stable software. GPAC is written in ANSI C for
portability reasons (embedded platforms and DSPs) with a simple goal:
keep the memory footprint as low as possible. The project will at term
provide player(s), systems encoders and publishing tools for content
distribution.

%description -l pl
GPAC to implementacja standardu MPEG-4 Systems (ISO/IEC 14496-1)
stworzona od zera w ANSI C.

G³ównym celem tworzenia jej jest dostarczenie czystej (tzn. czytelnej
dla jak najwiêkszej liczby ludzi), ma³ej i elastycznej alternatywy dla
wzorcowego oprogramowania MPEG-4 Systems (znanego jako IM1 i
rozprowadzanego w ISO/IEC 14496-5). Wzorcowe oprogramowanie MPEG-4
jest bardzo du¿± porcj± kodu, zaprojektowan± raczej do zweryfikowania
standardu ni¿ dostarczenia ma³ej, stabilnej wersji produkcyjnej. GPAC
jest pisany w ANSI C ze wzglêdu na przeno¶no¶æ (platformy wbudowane i
DSP) z prostym celem: wymagaæ tak ma³o pamiêci, jak to tylko mo¿liwe.
Projekt docelowo dostarczy odtwarzacz(e), kodery systemowe i narzêdzia
do publikacji w celu dystrybucji materia³ów.

%package -n browser-plugin-%{name}
Summary:	GPAC browser plugin
Summary(pl):	Wtyczka GPAC do przegl±derek WWW
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins(%{_target_cpu})

%define browsers mozilla, mozilla-firefox

%description -n browser-plugin-%{name}
GPAC plugin for Netscape-compatible WWW browsers.

Supported browsers: %{browsers}.

%description -n browser-plugin-%{name} -l pl
Wtyczka GPAC dla przegl±darek WWW zgodnych z Netscape.

Obs³ugiwane przegl±darki: %{browsers}.

%prep
%setup -q -n gpac
%patch0 -p1 
%{?with_wx:%patch1 -p1}
%if %{with amr}
mkdir -p Plugins/amr_dec/AMR_NB
cd Plugins/amr_dec/AMR_NB
unzip -j %{SOURCE1}
unzip -j 26073-530_ANSI_C_source_code.zip
%endif
chmod a+x configure

# files for w32 and Linux were swapped
rm -rf applications/osmozilla/nsIOsmozilla.xpt_linux
mv applications/osmozilla/nsIOsmozilla.xpt_w32 applications/osmozilla/nsIOsmozilla.xpt_linux

%build
%configure \
	--enable-oss-audio \
	%{?with_amr: --enable-amr-nb} \
	%{!?with_faad: --disable-faad} \
	%{!?with_ffmpeg: --disable-ffmpeg} \
	%{!?with_freetype: --disable-ft} \
	%{!?with_jpeg: --disable-jpeg} \
	%{!?with_js: --disable-js} \
	%{!?with_mad: --disable-mad} \
	%{!?with_png: --disable-png} \
	--extra-cflags="-fPIC" \
	--extra-ldflags="-fPIC" \
	%{!?with_xvid: --disable-xvid}

%{__make} \
	DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	plugdir=$RPM_BUILD_ROOT%{_libdir}/gpac \
	real_plugdir=%{_libdir}/gpac \
	prefix=$RPM_BUILD_ROOT/usr \
	MOZILLA_DIR=$RPM_BUILD_ROOT%{_plugindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%triggerin -n browser-plugin-%{name} -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins nposmozilla.so nposmozilla.xpt

%triggerun -n browser-plugin-%{name} -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins nposmozilla.so nposmozilla.xpt

%triggerin -n browser-plugin-%{name} -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins nposmozilla.so nposmozilla.xpt
if [ -d /usr/%{_lib}/mozilla ]; then
	umask 022
	rm -f /usr/%{_lib}/mozilla/components/{compreg,xpti}.dat
	if [ -x /usr/bin/regxpcom ]; then
		MOZILLA_FIVE_HOME=/usr/%{_lib}/mozilla /usr/bin/regxpcom
	fi
fi

%triggerun -n browser-plugin-%{name} -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins nposmozilla.so nposmozilla.xpt
if [ -d /usr/%{_lib}/mozilla ]; then
	umask 022
	rm -f /usr/%{_lib}/mozilla/components/{compreg,xpti}.dat
	if [ -x /usr/bin/regxpcom ]; then
		MOZILLA_FIVE_HOME=/usr/%{_lib}/mozilla /usr/bin/regxpcom
	fi
fi

%triggerpostun -n browser-plugin-%{name} -- mozilla-plugin-%{name}
%nsplugin_install -f -d %{_libdir}/mozilla/plugins nposmozilla.so nposmozilla.xpt

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS Changelog README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%dir %{_libdir}/gpac
%attr(755,root,root) %{_libdir}/gpac/*.so
%{_mandir}/man1/*

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/nposmozilla.so
%{_plugindir}/nposmozilla.xpt

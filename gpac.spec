# TODO
# - soname for libm4systems(?)
# - use system mozilla includes
# - ./configure[692]: wx-config: not found
# - ./configure[693]: wx-config: not found
# - CC, CFLAGS
# - Xiph Theora: no
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
Summary(pl.UTF-8):	GPAC - implementacja standardu MPEG-4 Systems (ISO/IEC 14496-1)
Name:		gpac
Version:	0.4.0
Release:	4
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/gpac/%{name}-%{version}.tar.gz
# Source0-md5:	a8b4b3206cabda946850240f1e7aea93
Source1:	http://www.3gpp.org/ftp/Specs/archive/26_series/26.073/26073-530.zip
# Source1-md5:	705f6993fbf890e92eb7a331e7c716d1
Patch0:		%{name}-install.patch
Patch1:		%{name}-wxWidgets.patch
Patch2:		%{name}-amd64.patch
Patch3:		%{name}-libdir.patch
URL:		http://gpac.sourceforge.net/
BuildRequires:	SDL-devel
%{?with_faad:BuildRequires:	faad2-devel}
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
%{?with_freetype:BuildRequires:	freetype-devel}
%{?with_js:BuildRequires:	js-devel}
%{?with_jpeg:BuildRequires:	libjpeg-devel}
%{?with_mad:BuildRequires:	libmad-devel}
%{?with_png:BuildRequires:	libpng-devel}
BuildRequires:	libxml2-devel
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	unzip
%{?with_wx:BuildRequires:	wxGTK2-devel >= 2.5.4}
%{?with_xvid:BuildRequires:	xvid-devel}
Requires:	SDL
%{?with_faad:Requires:	faad2}
%{?with_ffmpeg:Requires:	ffmpeg}
%{?with_freetype:Requires:	freetype}
%{?with_js:Requires:	js}
%{?with_jpeg:Requires:	libjpeg}
%{?with_mad:Requires:	libmad}
%{?with_png:Requires:	libpng}
%{?with_xvid:Requires:	xvid}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreq   libm4systems.so

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

%description -l pl.UTF-8
GPAC to implementacja standardu MPEG-4 Systems (ISO/IEC 14496-1)
stworzona od zera w ANSI C.

Głównym celem tworzenia jej jest dostarczenie czystej (tzn. czytelnej
dla jak największej liczby ludzi), małej i elastycznej alternatywy dla
wzorcowego oprogramowania MPEG-4 Systems (znanego jako IM1 i
rozprowadzanego w ISO/IEC 14496-5). Wzorcowe oprogramowanie MPEG-4
jest bardzo dużą porcją kodu, zaprojektowaną raczej do zweryfikowania
standardu niż dostarczenia małej, stabilnej wersji produkcyjnej. GPAC
jest pisany w ANSI C ze względu na przenośność (platformy wbudowane i
DSP) z prostym celem: wymagać tak mało pamięci, jak to tylko możliwe.
Projekt docelowo dostarczy odtwarzacz(e), kodery systemowe i narzędzia
do publikacji w celu dystrybucji materiałów.

%package -n browser-plugin-%{name}
Summary:	GPAC browser plugin
Summary(pl.UTF-8):	Wtyczka GPAC do przegląderek WWW
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})

%description -n browser-plugin-%{name}
GPAC plugin for Netscape-compatible WWW browsers.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka GPAC dla przeglądarek WWW zgodnych z Netscape.

%prep
%setup -q -n %{name}
%patch0 -p1
%{?with_wx:%patch1 -p1}
%patch2 -p1
%patch3 -p1
%if %{with amr}
mkdir -p Plugins/amr_dec/AMR_NB
cd Plugins/amr_dec/AMR_NB
unzip -j %{SOURCE1}
unzip -j 26073-530_ANSI_C_source_code.zip
cd ../../..
%endif
chmod a+x configure

# files for w32 and Linux were swapped
rm -rf applications/osmozilla/nsIOsmozilla.xpt_linux
mv applications/osmozilla/nsIOsmozilla.xpt_w32 applications/osmozilla/nsIOsmozilla.xpt_linux

%build
%configure \
	--extra-cflags="-fPIC" \
	--extra-ldflags="-fPIC" \
	--enable-oss-audio \
	%{?with_amr:--enable-amr-nb} \
	%{!?with_faad:--disable-faad} \
	%{!?with_ffmpeg:--disable-ffmpeg} \
	%{!?with_freetype:--disable-ft} \
	%{!?with_jpeg:--disable-jpeg} \
	%{!?with_js:--disable-js} \
	%{!?with_mad:--disable-mad} \
	%{!?with_png:--disable-png} \
	%{!?with_xvid:--disable-xvid}

%{__make} -j1 \
	XLIBDIR="/usr/X11R6/%{_lib}" \
	DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	plugdir=$RPM_BUILD_ROOT%{_libdir}/gpac \
	real_plugdir=%{_libdir}/gpac \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	MOZILLA_DIR=$RPM_BUILD_ROOT%{_browserpluginsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

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
%attr(755,root,root) %{_browserpluginsdir}/nposmozilla.so
%{_browserpluginsdir}/nposmozilla.xpt

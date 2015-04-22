# TODO:
# - Platinum UPnP: http://www.plutinosoft.com/platinum
# - AVCap: http://libavcap.sourceforge.net/
# - OpenSVCDecoder: http://opensvcdecoder.sourceforge.net/
# - libfreenect: http://openkinect.org/wiki/Main_Page
#
# Conditional build:
%bcond_with	amr		# AMR-NB and AMR-WB (floating-point) support
%bcond_without	directfb	# DirectFB support
%bcond_without	faad		# AAC decoding support
%bcond_without	ffmpeg		# ffmpeg support
%bcond_without	freetype	# freetype support
%bcond_without	jpeg		# JPEG support
%bcond_with	js		# JavaScript support
%bcond_without	mad		# MP3 support
%bcond_without	png		# PNG support
%bcond_without	xvid		# xvid support
%bcond_without	wx		# wxWidgets support
%bcond_without	plugin		# don't build xulrunner/firefox/iceweasel plugin
#
%define	snap	20141007
#
%ifarch x32
%undefine	with_plugin
%endif
Summary:	GPAC - an implementation of the MPEG-4 Systems standard (ISO/IEC 14496-1)
Summary(pl.UTF-8):	GPAC - implementacja standardu MPEG-4 Systems (ISO/IEC 14496-1)
Name:		gpac
Version:	0.5.0
Release:	15.%{snap}.1
License:	LGPL v2+
Group:		Applications/Multimedia
# Source0:	http://downloads.sourceforge.net/gpac/%{name}-%{version}.tar.gz
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	9e37b324e490d3118622d77bf238cb16
Patch0:		%{name}-install.patch
Patch1:		%{name}-xulrunner.patch
Patch2:		%{name}-amr.patch
Patch3:		%{name}-install-is-not-clean.patch
Patch4:		%{name}-flags.patch
Patch5:		wxWidgets3.patch
Patch6:		%{name}-js.patch
Patch7:		%{name}-apps.patch
URL:		http://gpac.sourceforge.net/
%{?with_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 0.9
%{?with_amr:BuildRequires:	amrnb-devel}
%{?with_amr:BuildRequires:	amrwb-devel}
%{?with_faad:BuildRequires:	faad2-devel}
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.6}
%{?with_freetype:BuildRequires:	freetype-devel}
%{?with_wx:BuildRequires:	gtk+2-devel >= 2:2.20.1}
BuildRequires:	jack-audio-connection-kit-devel
%{?with_js:BuildRequires:	js-devel < 2:1.8.5}
%{?with_jpeg:BuildRequires:	libjpeg-devel}
%{?with_mad:BuildRequires:	libmad-devel}
BuildRequires:	libogg-devel
%{?with_png:BuildRequires:	libpng-devel}
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	openjpeg-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
%{?with_wx:BuildRequires:	wxGTK2-unicode-devel >= 2.6.0}
BuildRequires:	xmlrpc-c-server-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
%{?with_plugin:BuildRequires:	xulrunner-devel >= 2:9.0.0}
%{?with_xvid:BuildRequires:	xvid-devel}
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package devel
Summary:	Header files for GPAC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GPAC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GPAC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GPAC.

%package static
Summary:	Static GPAC library
Summary(pl.UTF-8):	Statyczna biblioteka GPAC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GPAC library.

%description static -l pl.UTF-8
Statyczna biblioteka GPAC.

%package gui
Summary:	wxWidgets-based GUI for GPAC
Summary(pl.UTF-8):	Oparty na wxWidgets graficzny interfejs do GPAC
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description gui
Osmo4 - wxWidgets-based GUI for GPAC.

%description gui -l pl.UTF-8
Osmo4 - oparty na wxWidgets graficzny interfejs do GPAC.

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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

sed -i -e 's/wx-config/wx-gtk2-unicode-config/' configure
chmod a+x configure

%build
# not autoconf configure
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_lib} \
	--mandir=%{_mandir} \
	--X11-path=/usr \
	--cc="%{__cc}" \
	--cpp="%{__cxx}" \
	--disable-opt \
	%{!?with_wx:--disable-wx} \
	%{?with_amr:--enable-amr} \
	--enable-pic \
	--extra-cflags="%{rpmcflags} -DFF_API_CLOSE_INPUT_FILE" \
	--extra-ldflags="%{rpmldflags}" \
	%{?with_plugin:--mozdir=%{_browserpluginsdir}} \
	%{?with_plugin:--xulsdk-path="/usr/include/xulrunner -I/usr/include/nspr"} \
	%{!?with_faad:--use-faad=no} \
	%{!?with_ffmpeg:--use-ffmpeg=no} \
	%{!?with_freetype:--use-ft=no} \
	%{!?with_jpeg:--use-jpeg=no} \
	%{!?with_js:--use-js=no} \
	%{!?with_mad:--use-mad=no} \
	%{!?with_png:--use-png=no} \
	%{!?with_xvid:--use-xvid=no} \
	--enable-joystick

%{!?with_directfb: sed -i 's/CONFIG_DIRECTFB.*/CONFIG_DIRECTFB=no/' config.mak}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} -j1 install install-lib \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C applications install \
	DESTDIR=$RPM_BUILD_ROOT \
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
%attr(755,root,root) %{_bindir}/MP4Box
%attr(755,root,root) %{_bindir}/MP4Client
%attr(755,root,root) %{_libdir}/libgpac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpac.so.3
%dir %{_libdir}/gpac
%attr(755,root,root) %{_libdir}/gpac/gm_*.so
%{_datadir}/gpac
%{_mandir}/man1/gpac.1*
%{_mandir}/man1/mp4box.1*
%{_mandir}/man1/mp4client.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpac.so
%{_includedir}/gpac
%{_pkgconfigdir}/gpac.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgpac_static.a

%if %{with wx}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/DashCast
%attr(755,root,root) %{_bindir}/Osmo4
%endif

%if %{with plugin}
%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/nposmozilla.so
%{_browserpluginsdir}/nposmozilla.xpt
%endif

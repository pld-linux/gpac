# TODO:
# - Platinum UPnP: http://www.plutinosoft.com/platinum (for platinum module)
# - OpenSVCDecoder: http://opensvcdecoder.sourceforge.net/ (for opensvc_dec module)
# - libopenhevc: https://github.com/OpenHEVC/openHEVC (for openhevc_dec module, replaces ffmpeg_in module)
#
# Conditional build:
%bcond_with	amr		# AMR-NB and AMR-WB (floating-point) support
%bcond_with	directfb	# DirectFB support
%bcond_without	faad		# AAC decoding support
%bcond_without	ffmpeg		# ffmpeg support
%bcond_without	freenect	# freenect (MS Kinect driver) module
%bcond_without	freetype	# freetype support
%bcond_without	jpeg		# JPEG support
%bcond_with	js		# JavaScript support in Osmo4 and modules
%bcond_without	mad		# MP3 support
%bcond_without	png		# PNG support
%bcond_without	xvid		# xvid support
#
Summary:	GPAC - an implementation of the MPEG-4 Systems standard (ISO/IEC 14496-1)
Summary(pl.UTF-8):	GPAC - implementacja standardu MPEG-4 Systems (ISO/IEC 14496-1)
Name:		gpac
Version:	2.4.0
Release:	1
License:	LGPL v2+
Group:		Applications/Multimedia
#Source0Download: https://github.com/gpac/gpac/releases
Source0:	https://github.com/gpac/gpac/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	de748e69984cd8b3b695347a3c9ae4d6
Patch0:		%{name}-ffmpeg.patch
URL:		https://gpac.io/
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
BuildRequires:	jack-audio-connection-kit-devel
%{?with_js:BuildRequires:	js-devel < 2:1.8.5}
%{?with_freenect:BuildRequires:	libfreenect-devel}
%{?with_jpeg:BuildRequires:	libjpeg-devel}
%{?with_mad:BuildRequires:	libmad-devel}
BuildRequires:	libogg-devel
%{?with_png:BuildRequires:	libpng-devel}
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	openjpeg2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	xmlrpc-c-server-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
%{?with_xvid:BuildRequires:	xvid-devel}
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Obsoletes:	gpac-gui < 1.0.1-1
Obsoletes:	browser-plugin-gpac < 2
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

%prep
%setup -q
%patch -P0 -p1

chmod a+x configure

%build
# not autoconf configure
./configure \
	--verbose \
	--prefix=%{_prefix} \
	--libdir=%{_lib} \
	--mandir=%{_mandir} \
	--X11-path=/usr \
	--cc="%{__cc}" \
	--cxx="%{__cxx}" \
	--disable-opt \
	%{?with_amr:--enable-amr} \
	--enable-pic \
	--extra-cflags="%{rpmcflags}" \
	--extra-ldflags="%{rpmldflags}" \
	%{!?with_faad:--use-faad=no} \
	%{!?with_ffmpeg:--use-ffmpeg=no} \
	%{!?with_freenect:--use-freenect=no} \
	%{!?with_freetype:--use-freetype=no} \
	%{!?with_jpeg:--use-jpeg=no} \
	%{!?with_mad:--use-mad=no} \
	%{!?with_png:--use-png=no} \
	%{!?with_xvid:--use-xvid=no}

%{!?with_directfb: sed -i 's/CONFIG_DIRECTFB.*/CONFIG_DIRECTFB=no/' config.mak}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} -j1 install install-lib \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C applications install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog README.md
%attr(755,root,root) %{_bindir}/MP4Box
%attr(755,root,root) %{_bindir}/gpac
%attr(755,root,root) %{_libdir}/libgpac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpac.so.12
%dir %{_libdir}/gpac
%attr(755,root,root) %{_libdir}/gpac/gm_*.so
%{_datadir}/gpac
%{_mandir}/man1/gpac.1*
%{_mandir}/man1/gpac-filters.1*
%{_mandir}/man1/mp4box.1*
%{_desktopdir}/gpac.desktop
%{_iconsdir}/hicolor/*x*/apps/gpac.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpac.so
%{_includedir}/gpac
%{_pkgconfigdir}/gpac.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgpac_static.a

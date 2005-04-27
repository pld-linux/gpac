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
Version:	0.2.4
Release:	1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/gpac/%{name}-%{version}.tar.gz
# Source0-md5:	cbbea28e99c23d1839d38c54c2cc090a
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

%prep
%setup -q -n gpac
%patch0 -p1 
%{?with_wx:%patch1 -p1}
%if %{with amr}
mkdir -p Plugins/amr_dec/AMR_NB
cd Plugins/amr_dec/AMR_NB
# XXX: (conditional?) SourceN?
unzip -j %{_sourcedir}/26073-530.zip
unzip -j 26073-530_ANSI_C_source_code.zip
%endif
chmod a+x configure

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
	%ifarch amd64
	--extra-cflags="-fPIC" \
	--extra-ldflags="-fPIC" \
	%endif
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
        prefix=$RPM_BUILD_ROOT/usr

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS Changelog README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man1/*


%bcond_with	amr
%bcond_without	js
%bcond_without	freetype
%bcond_without	faad
%bcond_without	jpeg
%bcond_without	png
%bcond_without	mad
%bcond_without	xvid
%bcond_without	ffmpeg

Summary:	GPAC - an implementation of the MPEG-4 Systems standard (ISO/IEC 14496-1)
Summary(pl):	GPAC - implementacja standardu MPEG-4 Systems (ISO/IEC 14496-1)
Name:		gpac
Version:	0.2.1
Release:	1
License:	GPL
Group:		Applications
Source0:	http://mesh.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	3a3e193e805ab177f44514ca3289b461
# Source0-size:	2227080
Source1:	http://www.3gpp.org/ftp/Specs/archive/26_series/26.073/26073-530.zip
# Source1-md5:	705f6993fbf890e92eb7a331e7c716d1
# Source1-size:	916695
URL:		http://gpac.sourceforge.net/
BuildRequires: 	SDL-devel
#BuildRequires:	wxWidgets-devel
%{!?_without_js:BuildRequires: js-devel}
%{!?_without_freetype:BuildRequires: freetype-devel}
%{!?_without_faad:BuildRequires: faad2-devel}
%{!?_without_jpeg:BuildRequires: libjpeg-devel}
%{!?_without_png:BuildRequires: libpng-devel}
%{!?_without_mad:BuildRequires: libmad-devel}
%{!?_without_xvid:BuildRequires: xvid-devel}
%{!?_without_ffmpeg:BuildRequires: ffmpeg-devel}
Requires:	SDL
#Requires:	wxWidgets
%{!?_without_js:Requires: js}
%{!?_without_freetype:Requires: freetype}
%{!?_without_faad:Requires: faad2}
%{!?_without_jpeg:Requires: libjpeg-6b}
%{!?_without_png:Requires: libpng}
%{!?_without_mad:Requires: libmad}
%{!?_without_xvid:Requires: xvid}
%{!?_without_ffmpeg:Requires: ffmpeg}
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

The current GPAC release (0.2.1) is far from being complete but
already covers a very large part of the standard, and can probably be
seen as the most advanced and robust 2D MPEG-4 Player available
worldwide (its 3D side is not to be neglected though).

%prep
%setup -q -n gpac
%if %{?_with_amr:1}%{!?_with_amr:0}
mkdir -p Plugins/amr_dec/AMR_NB
cd Plugins/amr_dec/AMR_NB
unzip -j ../../SOURCES/26073-530.zip
unzip -j 26073-530_ANSI_C_source_code.zip
cd ../../..
%endif


%build
%configure --enable-oss-audio \
	%{?_with_amr: --enable-amr-nb} \
	%{?_without_js: --disable-js} \
	%{?_without_freetype: --disable-ft} \
	%{?_without_faad: --disable-faad} \
	%{?_without_jpeg: --disable-jpeg} \
	%{?_without_png: --disable-png} \
	%{?_without_mad: --disable-mad} \
	%{?_without_xvid: --disable-xvid} \
	%{?_without_ffmpeg: --disable-ffmpeg}

%{__make} \
	DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS Changelog COPYING README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man1/*

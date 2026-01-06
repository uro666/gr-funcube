%define major 3
%define devname %mklibname gr-funcube -d

%define gitdate 20260105
%define gitcommit 932ada084b88e1ad3132bc5fee96b4401d1c6c3c

%global git_short_commit %(echo %{gitcommit} | cut -c -8)
%global git_suffix %{gitdate}git%{git_short_commit}

Name:		gr-funcube
Version:	3.10.0~rc3^%{git_suffix}
Release:	1
Summary:	GNURadio support for FUNcube Dongle Pro and FUNcube Dongle Pro+
URL:		https://github.com/dl1ksv/gr-funcube
License:	GPL-3.0-or-later
Group:		System/Libraries
Source0:	%{name}-%{gitdate}-%{gitcommit}.tar.zst

BuildSystem:	cmake
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	cmake(boost_numpy)
BuildRequires:	cmake(hidapi)
BuildRequires:	doxygen
BuildRequires:	gnuradio-pmt-devel
BuildRequires:	gnuradio-utils
BuildRequires:	graphviz
BuildRequires:	fdupes
BuildRequires:	mpir-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(gmpxx)
BuildRequires:	pkgconfig(gnuradio-audio)
BuildRequires:	pkgconfig(gnuradio-blocks)
BuildRequires:	pkgconfig(gnuradio-runtime)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libunwind-llvm)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(pybind11)
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(volk) >= 3.2
BuildRequires:	python-gnuradio-pmt
BuildRequires:	python-gnuradio-runtime
BuildRequires:	python%{pyver}dist(numpy)
BuildRequires:	python%{pyver}dist(pygccxml)

%description
gr-funcube is an linux oot-module for gnuradio to implement a FUNcube
Dongle and a FUNcube Dongle PRO+ source. It autodetects the correct
soundcard from /proc/asound/cards. This idea was taken from the osmosdr
drivers. To control the device, the hidraw code of the HID API is used.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Libraries/Other
Requires:	%{name} = %{EVRD}
Suggests:	%{name}-doc = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package -n python-%{name}
Summary:	Python bindings for FCD and FCDpro Plus
Group:		Development/Libraries/Python
Requires:	%{name} = %{EVRD}

%description -n python-gr-funcube
gr-funcube is an linux oot-module for gnuradio to implement a FUNcube
Dongle and a FUNcube Dongle PRO+ source. It autodetects the correct
soundcard from /proc/asound/cards. This idea was taken from the osmosdr
drivers. To control the device, the hidraw code of the HID API is used.

%package doc
Summary:	Documentation for gr-funcube
Group:		Documentation/Other
Requires:	%{name} = %{EVRD}
BuildArch:	noarch

%description doc
Documentation for gr-funcube module for GNU Radio.

%prep
%autosetup -n %{name}-%{gitdate}-%{gitcommit} -p1

%build
export LDFLAGS="%{ldflags} -lpython%{pyver}"
%global _cmake_module_linker_flags_extra -lpython%{pyver}
%cmake \
	-DGR_TEST_LIBRARY_DIRS=../lib \
    -DGR_PKG_DOC_DIR=%{_docdir}/%{name} \
    -DENABLE_DOXYGEN=ON \
    -G Ninja
%ninja_build

%install
%ninja_install -C build
%fdupes %{buildroot}%{_prefix}
install -Dm 0644 50-funcube.rules %{buildroot}%{_udevrulesdir}/50-funcube.rules

%check
pushd build
%ninja_test
popd

%post   -n %{name} -p /sbin/ldconfig
%postun -n %{name} -p /sbin/ldconfig

%files
%exclude %{_docdir}/%{name}/html
%exclude %{_docdir}/%{name}/xml
%license COPYING
%doc README.md
%{_datadir}/gnuradio/grc/blocks/*.yml
%{_libdir}/libgnuradio-funcube.so.%{major}*
%{_udevrulesdir}/50-funcube.rules

%files -n %{devname}
%{_includedir}/funcube
%{_libdir}/libgnuradio-funcube.so
%{_libdir}/cmake/funcube

%files -n python-%{name}
%{python_sitearch}/funcube

%files doc
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/html
%{_docdir}/%{name}/xml


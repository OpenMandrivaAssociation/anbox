%global optflags %{optflags} -Wno-error=missing-field-initializers

Name:		anbox
Version:	20190525
Release:	1
Summary:	Run Android apps in a container
Group:		Applications/Internet
URL:		http://anbox.io/
Source0:	https://github.com/anbox/anbox/archive/master/%{name}-%{version}.tar.gz
Patch0:		anbox-clang.patch
Patch1:		anbox-20181218-linkage.patch
Patch2:		anbox-libcpu_features-soname.patch
Patch3:		anbox-20190525-compile.patch
License:	GPLv3
BuildRequires:	pkgconfig(lxc) >= 3.0
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	cmake(SDL2)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(protobuf-lite)
BuildRequires:	pkgconfig(properties-cpp)
BuildRequires:	binutils-devel
BuildRequires:	libdwarf-devel
BuildRequires:	lxc
BuildRequires:	cmake ninja
BuildRequires:	gtest-source >= 1.8.1
Requires:	lxc >= 3.0

%description
Run Android apps in a container

%prep
%autosetup -p1 -n anbox-master

%cmake \
	-DANBOX_VERSION="OpenMandriva %{version}" \
	-DGMOCK_INCLUDE_DIRS=/usr/src/googletest/googlemock/include \
	-DGMOCK_SOURCE_DIR=/usr/src/googletest/googlemock \
	-DGTEST_INCLUDE_DIRS=/usr/src/googletest/googletest/include \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# -devel files for static libraries that aren't even installed
# aren't really worth packaging...
rm -rf	\
	%{buildroot}%{_includedir} \
	%{buildroot}%{_prefix}/lib/backward \
	%{buildroot}%{_libdir}/cmake \
	%{buildroot}%{_libdir}/libcpu_features.so

%files
%{_bindir}/anbox
%{_bindir}/list_cpu_features
%{_datadir}/anbox
%{_libdir}/libcpu_features.so.0*

%global optflags %{optflags} -Wno-error=missing-field-initializers

Name:		anbox
Version:	20200905
Release:	1
Summary:	Run Android apps in a container
Group:		Applications/Internet
URL:		http://anbox.io/
Source0:	https://github.com/anbox/anbox/archive/master/%{name}-%{version}.tar.gz
# Anbox actually calls for b9593c8b395318bb2bc42683a94f962564cc4664
# But that one is broken on ARM, so let's use something more current...
Source1:	https://github.com/google/cpu_features/archive/339bfd32be1285877ff517cba8b82ce72e946afd.tar.gz
Source2:	https://github.com/Kistler-Group/sdbus-cpp/archive/3b735bf1aad65277f56e65c828a22455cbaf5245.tar.gz
Source3:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/anbox/99-anbox.rules
Source4:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/anbox/anbox-container-manager.service
Source5:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/anbox/anbox-session-manager.service
Source6:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/anbox/dev-binderfs.mount
Source7:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/anbox/anbox.desktop
Patch0:		anbox-clang.patch
Patch1:		anbox-20181218-linkage.patch
Patch2:		anbox-libcpu_features-soname.patch
# This should give the Android container enough time to start even on an ARM box
Patch3:		https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/anbox/give-more-time-to-start.patch
Patch4:		https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/anbox/python3.patch
License:	GPLv3
BuildRequires:	pkgconfig(lxc) >= 3.0
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	cmake(SDL2)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(protobuf-lite)
BuildRequires:	pkgconfig(properties-cpp)
BuildRequires:	pkgconfig(gtest)
BuildRequires:	binutils-devel
BuildRequires:	libdwarf-devel
BuildRequires:	lxc
BuildRequires:	cmake ninja
BuildRequires:	gtest-source >= 1.8.1
Requires:	lxc >= 3.0

%description
Run Android apps in a container.

%prep
%setup -n anbox-master -a 1 -a 2
rmdir external/cpu_features external/sdbus-cpp
mv cpu_features-* external/cpu_features
mv sdbus-cpp-* external/sdbus-cpp
%autopatch -p1

export CC=gcc
export CXX=g++
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

install -c -Dm644 -t %{buildroot}/lib/udev/rules.d %{S:3}
install -c -Dm644 -t %{buildroot}/lib/systemd/system %{S:4}
install -c -Dm644 -t %{buildroot}/lib/systemd/user %{S:5}
install -c -Dm644 -t %{buildroot}/lib/systemd/system %{S:6}
install -c -Dm644 -t %{buildroot}%{_datadir}/applications/ %{S:7}
install -Dm644 snap/gui/icon.png %{buildroot}%{_datadir}/pixmaps/anbox.png
install -Dm755 scripts/anbox-bridge.sh %{buildroot}%{_datadir}/anbox/
install -Dm755 scripts/anbox-shell.sh %{buildroot}%{_datadir}/anbox/

%files
%{_bindir}/anbox
%{_bindir}/list_cpu_features
%{_datadir}/anbox
%{_libdir}/libcpu_features.so.0*
/lib/udev/rules.d/*
/lib/systemd/system/*.mount
/lib/systemd/system/*.service
/lib/systemd/user/*.service
%{_datadir}/applications/anbox.desktop
%{_datadir}/pixmaps/anbox.png

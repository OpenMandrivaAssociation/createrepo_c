%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Creates a common metadata repository
Name:		createrepo_c
Version:	0.15.8
Release:	1
License:	GPLv2+
Group:		System/Configuration/Packaging
URL:		https://github.com/rpm-software-management/createrepo_c
Source0:	https://github.com/rpm-software-management/createrepo_c/archive/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(rpm)
BuildConflicts:	pkgconfig(rpm) >= 5
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(zck)
BuildRequires:	pkgconfig(drpm)
BuildRequires:	pkgconfig(modulemd-2.0) >= 2.3.0
BuildRequires:	python-nose
BuildRequires:	python-sphinx
BuildRequires:	ninja

%description
C implementation of Createrepo. This utility will generate a common
metadata repository from a directory of rpm packages

%package -n %{libname}
Summary:	Library for repodata manipulation
Group:		System/Libraries

%description -n %{libname}
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.

%package -n %{develname}
Summary:	Library for repodata manipulation
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{develname}
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

%package -n python-%{name}
Summary:	Python 3 bindings for the createrepo_c library
Group:		Development/Python
Provides:	python3-%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n python-%{name}
Python 3 bindings for the createrepo_c library.

%prep
%autosetup -p1

%build
%cmake -DPYTHON_DESIRED:str=3 -G Ninja -DWITH_LIBMODULEMD=ON -DWITH_ZCHUNK=ON
%ninja_build

%install
%ninja_install -C build

%check
# Compile C tests
#make tests

# Run Python 3 tests
#make ARGS="-V" test

%files
%{_datadir}/bash-completion/completions/*
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c
%{_bindir}/sqliterepo_c
%{_mandir}/man8/createrepo_c.8.*
%{_mandir}/man8/mergerepo_c.8.*
%{_mandir}/man8/modifyrepo_c.8.*
%{_mandir}/man8/sqliterepo_c.8.*

%files -n %{libname}
%{_libdir}/libcreaterepo_c.so.%{major}*

%files -n %{develname}
%doc COPYING
%dir %{_includedir}/createrepo_c
%{_libdir}/libcreaterepo_c.so
%{_libdir}/pkgconfig/createrepo_c.pc
%{_includedir}/createrepo_c/*

%files -n python-%{name}
%{python3_sitearch}/createrepo_c/
%{python3_sitearch}/createrepo_c-*.egg-info

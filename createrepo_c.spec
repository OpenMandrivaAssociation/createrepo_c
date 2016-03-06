%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Creates a common metadata repository
Name:		createrepo_c
Version:	0.10.0
Release:	1
License:	GPLv2
Group:		System/Configuration/Packaging
URL:		https://github.com/rpm-software-management/createrepo_c
Source0:	https://github.com/rpm-software-management/createrepo_c/archive/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	magic-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-nose
BuildRequires:	python-sphinx
Requires:	%{libname} =  %{EVRD}

%description
C implementation of Createrepo. This utility will generate a common
metadata repository from a directory of rpm packages


%package %{libname}
Summary:    Library for repodata manipulation
Group:      System/Libraries

%description %{libname}
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.


%package %{develname}
Summary:    Library for repodata manipulation
Group:      Development/C
Requires:   %{libname} =  %{EVRD}

%description %{develname}
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

%prep
%setup -q

%build
%cmake -DPYTHON_DESIRED:str=3
%make -C build

%install
%makeinstall_std -C build

%files
%{_sysconfdir}/bash_completion.d/createrepo_c.bash
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c
%{_bindir}/sqliterepo_c
%{_mandir}/man8/createrepo_c.8.*
%{_mandir}/man8/mergerepo_c.8.*
%{_mandir}/man8/modifyrepo_c.8.*
%{_mandir}/man8/sqliterepo_c.8.*

%files %{libname}
%{_libdir}/libcreaterepo_c.so.{major}*

%files %{develname}
%doc COPYING
%doc doc/html
%dir %{_includedir}/createrepo_c
%{_libdir}/libcreaterepo_c.so
%{_libdir}/pkgconfig/createrepo_c.pc
%{_includedir}/createrepo_c/*

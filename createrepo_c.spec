%define major 1
%define libname %mklibname %{name}
%define oldlibname %mklibname %{name} 0
%define develname %mklibname %{name} -d

Summary:	Creates a common metadata repository
Name:		createrepo_c
Version:	1.0.4
Release:	2
License:	GPLv2+
Group:		System/Configuration/Packaging
URL:		https://github.com/rpm-software-management/createrepo_c
Source0:	https://github.com/rpm-software-management/createrepo_c/archive/%{name}-%{version}.tar.gz
# We hit this assert at times (maybe when there are really old
# rpm5 packages left in the tree being replaced at last?)
# Give some useful info and try to do the right thing
# instead of aborting with assert.
Patch0:		createrepo_c-0.21.1-debug-instead-of-assert.patch
Patch1:		createrepo_c-optimize-cr_copy_file.patch
# This makes createrepo_c too verbose, but is useful to debug
# e.g. hangs while examining a specific package
#Patch2:		createrepo_c-debug.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(sqlite3) >= 3.6.18
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(zck)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(modulemd-2.0) >= 2.3.0
BuildRequires:	python-sphinx
BuildRequires:	ninja

%description
C implementation of Createrepo. This utility will generate a common
metadata repository from a directory of rpm packages

%package -n %{libname}
Summary:	Library for repodata manipulation
Group:		System/Libraries
%rename %oldlibname

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
%cmake \
	-DWITH_LIBMODULEMD:BOOL=ON \
	-DENABLE_DRPM:BOOL=OFF \
	-DWITH_ZCHUNK:BOOL=ON \
	-DWITH_ZSTD:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

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
%doc %{_mandir}/man8/createrepo_c.8.*
%doc %{_mandir}/man8/mergerepo_c.8.*
%doc %{_mandir}/man8/modifyrepo_c.8.*
%doc %{_mandir}/man8/sqliterepo_c.8.*

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

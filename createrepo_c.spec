%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Creates a common metadata repository
Name:		createrepo_c
Version:	0.10.0
Release:	5
License:	GPLv2+
Group:		System/Configuration/Packaging
URL:		https://github.com/rpm-software-management/createrepo_c
Source0:	https://github.com/rpm-software-management/createrepo_c/archive/%{name}-%{version}.tar.gz
# Make it possible to disable drpm/deltarpm support
Patch0:		createrepo_c-fix-cmake.patch
# Patch from upstream to fix Prov/Req filtering rules, see mga#19509
Patch1:		createrepo_c-PR70.patch
# Add support for RPM 5 to createrepo_c
Patch2:		createrepo_c-0.10.0-Add-RPM-5-support.patch
# Fixup memory allocation issues with createrepo_c + RPM 5 (build on patch 2)
Patch3:		createrepo_c-0.10.0-fix-rpm5.patch
# Serialize rpmReadPackageFiles() with mutex for createrepo_c + RPM 5 (build on patch 3)
Patch4:		createrepo_c-0.10.0-serialize-rpmReadPackageFiles-rpm5.patch
# Attempt to handle DistEpoch in a semi-sane manner
Patch5:		createrepo_c-handle-DistEpoch.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	magic-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(bash-completion)
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
BuildRequires:	ninja
Requires:	%{libname} =  %{EVRD}

%description
C implementation of Createrepo. This utility will generate a common
metadata repository from a directory of rpm packages


%package -n %{libname}
Summary:    Library for repodata manipulation
Group:      System/Libraries

%description -n %{libname}
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.


%package -n %{develname}
Summary:    Library for repodata manipulation
Group:      Development/C
Requires:   %{libname} = %{EVRD}

%description -n %{develname}
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

%package -n python-%{name}
Summary:    Python 3 bindings for the createrepo_c library
Group:      Development/Python
Provides:   python3-%{name} = %{EVRD}
Requires:   %{libname} = %{EVRD}

%description -n python-%{name}
Python 3 bindings for the createrepo_c library.


%prep
%setup -q
%apply_patches

%build
%cmake -DPYTHON_DESIRED:str=3 -DRPM5:BOOL=ON -G Ninja
%ninja

%install
%ninja_install -C build

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

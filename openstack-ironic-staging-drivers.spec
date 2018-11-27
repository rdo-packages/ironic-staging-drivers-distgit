# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname ironic-staging-drivers
%global module ironic_staging_drivers
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name: openstack-%{sname}
Version: XXX
Release: XXX
Summary: Staging drivers for OpenStack Ironic
License: ASL 2.0
URL: http://launchpad.net/%{sname}/

Source0: http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz

BuildArch: noarch

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-pbr
BuildRequires: python%{pyver}-setuptools
BuildRequires: git
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: openwsman-python%{pyver}
%else
BuildRequires: openwsman-python
%endif

Requires: openstack-ironic-conductor
Requires: python%{pyver}-ironic-lib >= 2.5.0
Requires: python%{pyver}-oslo-concurrency >= 3.26.0
Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-oslo-service >= 1.24.0
Requires: python%{pyver}-six >= 1.10.0
Requires: python%{pyver}-jsonschema >= 2.6.0
Requires: python%{pyver}-pbr >= 2.0.0

%description
The Ironic Staging Drivers is used to hold out-of-tree Ironic drivers
which doesn't have means to provide a 3rd Party CI at this point in
time which is required by Ironic.

%if 0%{?with_doc}
%package doc
Summary: Ironic Staging Drivers documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-oslo-sphinx

%description doc
This package contains the Ironic Staging Drivers documentation.
%endif

%package -n python%{pyver}-ironic-staging-drivers-tests
Summary: Ironic Staging Drivers unit tests
%{?python_provide:%python_provide python%{pyver}-ironic-staging-drivers-tests}
Requires: %{name} = %{version}-%{release}

BuildRequires: python%{pyver}-ironic-tests
BuildRequires: python%{pyver}-mock
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-os-testr
BuildRequires: python%{pyver}-testrepository
BuildRequires: python%{pyver}-testscenarios
BuildRequires: python%{pyver}-testresources
BuildRequires: python%{pyver}-testtools

Requires: python%{pyver}-ironic-tests
Requires: python%{pyver}-mock
Requires: python%{pyver}-oslotest
Requires: python%{pyver}-os-testr
Requires: python%{pyver}-testrepository
Requires: python%{pyver}-testscenarios
Requires: python%{pyver}-testresources
Requires: python%{pyver}-testtools

%description -n python%{pyver}-ironic-staging-drivers-tests
This package contains the Ironic Staging Drivers unit test files.

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f *requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%check
%{pyver_bin} setup.py test

%install
%{pyver_install}

%files -n openstack-%{sname}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%files -n python%{pyver}-ironic-staging-drivers-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%changelog
* Tue Dec 06 2016 Lucas Alvares Gomes <lucasagomes@gmail.com> 0.4.0-1
– Initial Packaging

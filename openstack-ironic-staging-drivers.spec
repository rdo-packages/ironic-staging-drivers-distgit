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

BuildRequires: python3-devel
BuildRequires: python3-pbr
BuildRequires: python3-setuptools
BuildRequires: git
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: openwsman-python3
%else
BuildRequires: openwsman-python
%endif

Requires: openstack-ironic-conductor
Requires: python3-ironic-lib >= 2.5.0
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-oslo-service >= 1.24.0
Requires: python3-jsonschema >= 2.6.0
Requires: python3-pbr >= 2.0.0

%description
The Ironic Staging Drivers is used to hold out-of-tree Ironic drivers
which doesn't have means to provide a 3rd Party CI at this point in
time which is required by Ironic.

%if 0%{?with_doc}
%package doc
Summary: Ironic Staging Drivers documentation

BuildRequires: python3-sphinx
BuildRequires: python3-oslo-sphinx

%description doc
This package contains the Ironic Staging Drivers documentation.
%endif

%package -n python3-ironic-staging-drivers-tests
Summary: Ironic Staging Drivers unit tests
%{?python_provide:%python_provide python3-ironic-staging-drivers-tests}
Requires: %{name} = %{version}-%{release}

BuildRequires: python3-ironic-tests
BuildRequires: python3-mock
BuildRequires: python3-oslotest
BuildRequires: python3-os-testr
BuildRequires: python3-testrepository
BuildRequires: python3-testscenarios
BuildRequires: python3-testresources
BuildRequires: python3-testtools

Requires: python3-ironic-tests
Requires: python3-mock
Requires: python3-oslotest
Requires: python3-os-testr
Requires: python3-testrepository
Requires: python3-testscenarios
Requires: python3-testresources
Requires: python3-testtools

%description -n python3-ironic-staging-drivers-tests
This package contains the Ironic Staging Drivers unit test files.

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f *requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
%{__python3} setup.py build_sphinx
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%check
%{__python3} setup.py test

%install
%{py3_install}

%files -n openstack-%{sname}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%files -n python3-ironic-staging-drivers-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests

%changelog

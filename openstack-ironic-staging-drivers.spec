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

BuildRequires: python2-devel
BuildRequires: python2-pbr
BuildRequires: python2-setuptools
BuildRequires: git

Requires: openstack-ironic-conductor
Requires: python-ironic-lib >= 2.5.0
Requires: python2-oslo-concurrency >= 3.25.0
Requires: python2-oslo-config >= 5.1.0
Requires: python2-oslo-i18n >= 3.15.3
Requires: python2-oslo-log >= 3.36.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-oslo-service >= 1.24.0
Requires: python2-six >= 1.10.0
Requires: python2-jsonschema >= 2.6.0
Requires: python2-pbr >= 2.0.0

%description
The Ironic Staging Drivers is used to hold out-of-tree Ironic drivers
which doesn't have means to provide a 3rd Party CI at this point in
time which is required by Ironic.

%if 0%{?with_doc}
%package doc
Summary: Ironic Staging Drivers documentation

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx

%description doc
This package contains the Ironic Staging Drivers documentation.
%endif

%package -n python-ironic-staging-drivers-tests
Summary: Ironic Staging Drivers unit tests
Requires: %{name} = %{version}-%{release}

BuildRequires: python-ironic-tests
BuildRequires: python2-mock
BuildRequires: python2-oslotest
BuildRequires: python2-os-testr
BuildRequires: python2-testrepository
BuildRequires: python2-testscenarios
BuildRequires: python2-testresources
BuildRequires: python2-testtools

Requires: python-ironic-tests
Requires: python2-mock
Requires: python2-oslotest
Requires: python2-os-testr
Requires: python2-testrepository
Requires: python2-testscenarios
Requires: python2-testresources
Requires: python2-testtools

%description -n python-ironic-staging-drivers-tests
This package contains the Ironic Staging Drivers unit test files.

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f *requirements.txt

%build
%py2_build

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%check
%{__python2} setup.py test

%install
%py2_install

%files -n openstack-%{sname}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%files -n python-ironic-staging-drivers-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%changelog
* Tue Dec 06 2016 Lucas Alvares Gomes <lucasagomes@gmail.com> 0.4.0-1
– Initial Packaging

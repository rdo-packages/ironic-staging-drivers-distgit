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
BuildRequires: python-pbr
BuildRequires: python-setuptools
BuildRequires: git

Requires: openstack-ironic-conductor
Requires: python-ironic-lib
Requires: python-oslo-concurrency
Requires: python-oslo-config
Requires: python-oslo-i18n
Requires: python-oslo-log
Requires: python-oslo-utils
Requires: python-oslo-service
Requires: python-six
Requires: python-jsonschema

%description
The Ironic Staging Drivers is used to hold out-of-tree Ironic drivers
which doesn't have means to provide a 3rd Party CI at this point in
time which is required by Ironic.

%if 0%{?with_doc}
%package doc
Summary: Ironic Staging Drivers documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
This package contains the Ironic Staging Drivers documentation.
%endif

%package -n python-ironic-staging-drivers-tests
Summary: Ironic Staging Drivers unit tests
Requires: %{name} = %{version}-%{release}

BuildRequires: python-ironic-tests
BuildRequires: python-mock
BuildRequires: python-oslotest
BuildRequires: python-os-testr
BuildRequires: python-testrepository
BuildRequires: python-testscenarios
BuildRequires: python-testresources
BuildRequires: python-testtools

Requires: python-ironic-tests
Requires: python-mock
Requires: python-oslotest
Requires: python-os-testr
Requires: python-testrepository
Requires: python-testscenarios
Requires: python-testresources
Requires: python-testtools

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

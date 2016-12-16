%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname ironic-staging-drivers
%global module ironic_staging_drivers

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

%package doc
Summary: Ironic Staging Drivers documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
This package contains the Ironic Staging Drivers documentation.

%package tests
Summary: Ironic Staging Drivers tests

Requires: python-mock
Requires: python-oslotest
Requires: python-os-testr
Requires: python-testresources

%description tests
This package contains the Ironic Staging Drivers test files.

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f *requirements.txt

%build
%py2_build
# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

%files -n openstack-%{sname}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files doc
%license LICENSE
%doc doc/build/html README.rst

%files tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%changelog
* Tue Dec 06 2016 Lucas Alvares Gomes <lucasagomes@gmail.com> 0.4.0-1
– Initial Packaging

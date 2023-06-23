%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

%global sname ironic-staging-drivers
%global module ironic_staging_drivers
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name: openstack-%{sname}
Version: XXX
Release: XXX
Summary: Staging drivers for OpenStack Ironic
License: Apache-2.0
URL: http://launchpad.net/%{sname}/

Source0: http://tarballs.opendev.org/x/%{sname}/%{sname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.opendev.org/x/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch: noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core
Requires: openstack-ironic-conductor

%description
The Ironic Staging Drivers is used to hold out-of-tree Ironic drivers
which doesn't have means to provide a 3rd Party CI at this point in
time which is required by Ironic.

%if 0%{?with_doc}
%package doc
Summary: Ironic Staging Drivers documentation

%description doc
This package contains the Ironic Staging Drivers documentation.
%endif

%package -n python3-ironic-staging-drivers-tests
Summary: Ironic Staging Drivers unit tests
BuildRequires: python3-ironic-tests

Requires: %{name} = %{version}-%{release}
# Keeping explicit requires for test supbpackage
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git


sed -i /.*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
sed -i /^${pkg}.*/d doc/requirements.txt
sed -i /^${pkg}.*/d test-requirements.txt
done
# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%{__python3} setup.py build_sphinx
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%check
%tox -e %{default_toxenv}

%install
%pyproject_install

%files -n openstack-%{sname}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.dist-info
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

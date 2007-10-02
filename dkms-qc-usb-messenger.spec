%define module_name qc-usb-messenger
%define version 1.3

Name:		dkms-%{module_name}
Version:	%version
Release:	%mkrel 2
Summary:	DKMS-ready driver for the Quickcam USB Messenger
License:	GPL
Source:		http://home.mag.cx/messenger/source/%{module_name}-%{version}.tar.bz2
Group:		Development/Kernel
Requires(pre):	dkms
Requires(post): dkms
Buildroot:	%{_tmppath}/%{name}-%{version}-root
Buildarch:	noarch
Obsoletes:	%{module_name}-dkms
Provides:	%{module_name}-dkms

%description
This package contains a DKMS-ready driver for the Logitech Quickcam USB
Messenger.


%prep
%setup -q -c -n %{module_name}-%{version}
chmod -R go=u-w .

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/
cp -rf * %{buildroot}/usr/src/%{module_name}-%{version}
cat > %{buildroot}/usr/src/%{module_name}-%{version}/dkms.conf <<EOF

PACKAGE_VERSION="%{version}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module_name}"
#MAKE[0]="make quickcam.ko"
CLEAN="make clean"
BUILT_MODULE_NAME[0]="quickcam"
DEST_MODULE_LOCATION[0]="/kernel/3rdparty/qc-usb-messenger/"
DEST_MODULE_NAME[0]="qc-usb-messenger"
AUTOINSTALL=yes
EOF

%post
  dkms add -m %{module_name} -v %{version} --rpm_safe_upgrade
  dkms build -m %{module_name} -v %{version} --rpm_safe_upgrade
  dkms install -m %{module_name} -v %{version} --rpm_safe_upgrade

%preun
  dkms remove -m %{modname} -v %{version}-%{release} --rpm_safe_upgrade --all
	
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/src/%{module_name}-%{version}


%define		_modname	flvinfo
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - Provides file info of FLV files
Name:		php-pecl-%{_modname}
Version:	0.0.6
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	%{_modname}-%{version}.tar.bz2
# Source0-md5:	1ac00465d8890f328063db548169f821
Patch0:		flvinfo-lib64.patch
BuildRequires:	ffmpeg-devel >= 0.4.9-3.20061204.1.3
BuildRequires:	php-devel >= 4:5.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(%{_modname})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides information about FLV video dimensions. It
uses libavformat from ffmpeg to do so.

In PECL status of this extension is: %{_status}.

%package -n flvinfo
Summary:	flvinfo
Group:		Applications

%description -n flvinfo
flvinfo program.

%prep
%setup -q -n %{_modname}-%{version}
%if "%{_lib}" != "lib"
%patch0 -p1
%endif

%build
phpize
%configure
%{__make}
%{__make} flvinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_sysconfdir}/conf.d}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF
install flvinfo $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc {CREDITS,EXPERIMENTAL}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so

%files -n flvinfo
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/flvinfo

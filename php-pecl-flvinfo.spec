%define		_modname	flvinfo
%define		_status		beta
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - Provides file info of FLV files
Name:		php4-pecl-%{_modname}
Version:	0.0.4
Release:	2
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	%{_modname}-%{version}.tar.bz2
# Source0-md5:	8472916c3465f92eec9437e74495eb9e
BuildRequires:	ffmpeg-devel
BuildRequires:	php-devel >= 4:5.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides information about FLV video dimensions. It
uses libavformat from ffmpeg to do so.

In PECL status of this extension is: %{_status}.

%prep
%setup -q -n %{_modname}-%{version}

%build
phpize
%configure
%{__make}
%{__make} flvinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/conf.d}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF
install flvinfo $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc {CREDITS,EXPERIMENTAL}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
%attr(755,root,root) %{_bindir}/flvinfo

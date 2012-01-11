%define		modname	flvinfo
%define		status	stable
Summary:	%{modname} - Provides file info of FLV files
Name:		php-pecl-%{modname}
Version:	0.5
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
BuildRequires:	ffmpeg-devel >= 0.4.9-3.20061204.1.3
BuildRequires:	php-devel >= 4:5.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(%{modname})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cvsroot	:ext:cvs.delfi.ee:/usr/local/cvs
%define		_cvsmodule	php/ext/flvinfo

%description
This extension provides information about FLV video dimensions. It
uses libavformat from ffmpeg to do so.

In PECL status of this extension is: %{status}.

%package -n flvinfo
Summary:	flvinfo
Group:		Applications

%description -n flvinfo
flvinfo program.

%prep
%setup -qcT
cd ..
cvs -d %{_cvsroot} co %{?_cvstag:-r %{_cvstag}} -d %{name}-%{version} -P %{_cvsmodule}
cd -

%build
phpize
%configure
%{__make}
%{__make} flvinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_sysconfdir}/conf.d}

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF
install -p flvinfo $RPM_BUILD_ROOT%{_bindir}

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%files -n flvinfo
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/flvinfo

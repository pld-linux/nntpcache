Summary:	News caching proxy
Summary(pl):	Proxy buforuj�cy dost�p do news�w
Name:		nntpcache
Version:	2.4.0b5
Release:	1
License:	Free for non-commercial use
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	ftp://ftp.nntpcache.org/pub/nntpcache/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-config.patch
URL:		http://www.nntpcache.org/
BuildRequires:	pam-devel
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Install this program if you have slow link to news server and/or many
users using news and want to save bandwidth. This program will forward
NNTP request to specified server and will return replies to client,
also caching them. So if request can be satisfied (fully or partially)
using cached data, it will be, and only data not found in cache will
be requested from server. This can save a lot of time, especially, if
your users use news clients which dont do any caching by themselves
(such as slrn, which downloads headers every time user enters group).

%description -l pl
Zainstaluj ten program, je�li masz wolne po��czenie z serwerem news
albo/i wielu u�ytkownik�w korzystaj�cych z news�w, a chcesz odci��y�
��cze. Ten program przekazuje rz�dzania NNTP do podanego serwera a
nast�pnie zwraca odpowiedzi do klienta, jednocze�nie zachowuj�c je
lokalnie. Tak wi�c je�li rz�danie mo�e zosta� wype�nione, ca�kowicie
lub cz�ciowo, korzystaj�c z danych posiadanych lokalnie, zostan� one
u�yte, a z serwera b�d� sprowadzone wy��cznie informacje niedost�pne
lokalnie. Mo�e to zaoszcz�dzi� wiele czasu, szczeg�lnie je�li twoi
u�ytkownicy u�ywaj� klient�w news, kt�re same nie buforuj� danych (jak
np. slrn, kt�ry �ci�ga nag��wki przy ka�dym wej�ciu na grup�).

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
# Ugly, but works :) It is regenerated by ./configure.
cp mk/rules.mk{.in,}
autoheader;autoconf;automake; 

%configure 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/nntp \
	   $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d \
	   $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} install DESTDIR="$RPM_BUILD_ROOT"

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/nntpcache.config{-dist,}
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/nntpcache.servers{-dist,}
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/nntpcache.access{-dist,}
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/innreport.conf{-dist,}
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pubring.pgp{-dist,}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/http $RPM_BUILD_ROOT%{_datadir}/%{name}

gzip -9nf AUTHORS COPYING ChangeLog FAQ HACKING LICENSING README{,.INN}

%post
/sbin/chkconfig --add %{name}
if [ -r /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start NNTP Cache daemons."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(770,root,news) %dir %{_sysconfdir}/%{name}
%attr(640,root,news) %config %{_sysconfdir}/%{name}/nntpcache.config
%attr(640,root,news) %config %{_sysconfdir}/%{name}/nntpcache.servers
%attr(640,root,news) %config %{_sysconfdir}/%{name}/nntpcache.access
%attr(640,root,news) %config %{_sysconfdir}/%{name}/pubring.pgp
%attr(640,root,news) %config %{_sysconfdir}/%{name}/spam.filter
%attr(750,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libexecdir}/*
%attr(755,root,root) %{_sbindir}/newshound
%attr(755,root,root) %{_sbindir}/nntpcached
%{_datadir}/%{name}
%attr(770,root,news) %dir /var/cache/nntp
%{_mandir}/man8/*

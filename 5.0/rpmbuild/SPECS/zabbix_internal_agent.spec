%define         zabbix_user zabbix
%define         name       zabbix-agentd
%define         version    3.0.4
%define         directory_root %{_sourcedir}


Name:           %{name}
Version:        %{version}
Release:        1%{?dist}
Summary:        Zabbix Koolearn Customer Release
Vendor:         Koolearn
Packager:       LiMing<liming@koolearn.com>
BuildRoot:      %_topdir/BUILDROOT
Prefix:         /tol/app/zabbix-%{version}

Group:          Applications/System
License:        GPLv2
URL:            www.koolearn.com
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc,make
#Requires:       readline-devel,pcre-devel,openssl-devel,lua,LuaJIT

%description

Zabbix Koolearn Customer Release


%prep
%setup -q

%build


./configure \
    --prefix=%{prefix} \
    --enable-agent

make -j4


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#cp -r %{directory_root}/zabbix_agentd_etc/* $RPM_BUILD_ROOT%{prefix}/etc/
mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp -r %{directory_root}/zabbix_internal_agentd_etc/* $RPM_BUILD_ROOT%{prefix}/etc/
cp -r %{directory_root}/zabbix_agentd_init/zabbix_agentd $RPM_BUILD_ROOT/etc/init.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make clean


%files
%defattr(-,root,root,-)
%doc
   /tol/app/zabbix-3.0.4/bin
   /tol/app/zabbix-3.0.4/sbin
   /tol/app/zabbix-3.0.4/etc
   /tol/app/zabbix-3.0.4/lib
   /tol/app/zabbix-3.0.4/share
   /etc/init.d/zabbix_agentd

%pre
   if [ $1 == 1 ];then
     /usr/sbin/useradd -r %{zabbix_user} 2> /dev/null
   fi
   mkdir -p /tol/logs/zabbix

%post
   ln -s %{prefix} /tol/app/zabbix
   chown zabbix:zabbix /tol/logs/zabbix
   /sbin/chkconfig --add zabbix_agentd
   /sbin/chkconfig zabbix_agentd on
   /etc/init.d/zabbix_agentd start

%preun
    MSG=`ps aux | grep zabbix_agentd | grep -v "grep"`
    if [ -z "$MSG" ];then
        killall zabbix_agentd 1>/dev/null 2>/dev/null
    fi

%postun
    rm -rf %{prefix}
    rm -rf /tol/app/zabbix
    rm -rf /etc/init.d/zabbix_agentd

%changelog

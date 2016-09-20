2016年9月20号增加 Centos 5.* 系统的rpmbuild

5.*系统的rpmbuild和6.*的rpmbuild区别有以下

BuildRoot:      %_topdir/BUILDROOT


对于卸载之前的任务需要更改,目前还未更改，下个版本进行更改

%preun
if [ $1 == 0 ];then
    /etc/init.d/php-fpm stop > /dev/null 2>&1
    /sbin/chkconfig --del php-fpm
    if [ -e '/etc/profile.d/custom_profile_new.sh' ];then
        sed -i 's@%{_prefix}/bin:@@' /etc/profile.d/custom_profile_new.sh
    else
        sed -i 's@%{_prefix}/bin:@@' /etc/profile
    fi
fi


卸载之后的执行没有对chkconfig 添加的服务进行删除，下个版本处理

%postun
    rm -rf %{prefix}
    rm -rf /tol/app/zabbix
    rm -rf /etc/init.d/zabbix_agentd

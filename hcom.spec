# add --with java_compile option, i.e. disable java_compile by default
%bcond_with java_compile

%global build_type %{?_build_type:%{_build_type}}
# 如果没有提供，则设置默认值
%if "%{build_type}" == ""
    %global build_type release
%endif

%global with_hcom_perf %{?_with_hcom_perf:%{_with_hcom_perf}}
# 如果没有提供，则设置默认值
%if "%{with_hcom_perf}" == ""
    %global with_hcom_perf 0
%endif

%global with_htracer_cli %{?_with_htracer_cli:%{_with_htracer_cli}}
# 如果没有提供，则设置默认值
%if "%{with_htracer_cli}" == ""
    %global with_htracer_cli 0
%endif

%if %{undefined rpm_version}
    %define rpm_version 25.3.0
%endif

%if %{undefined rpm_release}
    %define rpm_release B017
%endif

%if %{undefined rpm_build_date}
    %define rpm_build_date %(date +"%%Y-%%m-%%d-%%H:%%M:%%S")
%endif

%if %{undefined package_name}
    %define package_name ubs-comm
%endif

%global package_suffix ubs-comm
%global debug_package %{nil}

Name:           %{package_suffix}
Version       : %{rpm_version}
Release       : %{rpm_release}
Summary:        HCOM
License       : Proprietary
Provides      : Huawei Technologies Co., Ltd
Source0       : %{package_name}.tar.gz
BuildRoot     : %{_buildirootdir}/%{name}_%{version}-build
buildArch     : aarch64 x86_64
ExclusiveArch : aarch64

BuildRequires: make gcc cmake libboundscheck rdma-core-devel umdk-urma-devel
Requires: libboundscheck umdk-urma-lib rdma-core

%description
HCOM是一个适用于C/S架构应用程序的高性能通信库

%package devel
Summary: Development header files and dynamic library for HCOM

%description devel
This package contains development header files and dynamic library for HCOM

%package debuginfo
Summary: Debuginfo for HCOM

%description debuginfo
This package contains debug info of hcom.so
%prep
%setup -q -b 0 -c -n %{name}

%build
cd %{_builddir}/%{name} && export HCOM_BUILD_RPM=off && export HCOM_BUILD_UB=on && export HCOM_BUILD_HTRACER=on && bash -x build.sh

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib64/
mkdir -p  %{buildroot}/usr/local/jars/hcom
mkdir -p %{buildroot}/usr/include/hcom/capi
mkdir -p %{buildroot}/usr/local/bin

cp %{_builddir}/%{package_name}/dist/hcom/lib/libhcom.so  %{buildroot}/usr/lib64/
cp %{_builddir}/%{package_name}/dist/hcom/lib/libhcom_static.a  %{buildroot}/usr/lib64/
cp %{_builddir}/%{package_name}/dist/hcom/lib/libhcom.so.debug  %{buildroot}/usr/lib64/
cp -r %{_builddir}/%{package_name}/dist/hcom/include/hcom/*  %{buildroot}/usr/include/hcom/

%if %{with java_compile}
    cp %{_builddir}/%{package_name}/hcom/jars/*  %{buildroot}/usr/local/jars/hcom/
%endif

%if %{with_hcom_perf}
    cp -r %{_builddir}/%{package_name}/hcom/hcom_perf  %{buildroot}/usr/local/bin/
%endif

%if %{with_htracer_cli}
    cp -r %{_builddir}/%{package_name}/hcom/bin/htracer_cli  %{buildroot}/usr/local/bin/
%endif

%files
%defattr(-,root,root)
%{_prefix}/lib64/libhcom.so
%{_prefix}/lib64/libhcom_static.a
%if %{with java_compile}
    %{_prefix}/local/jars/hcom/*.jar
%endif

%files devel
%defattr(-,root,root)
%{_prefix}/include/hcom/capi/*.h
%{_prefix}/include/hcom/*.h
%if %{with_hcom_perf} || %{with_htracer_cli}
    %{_prefix}/local/bin/*
%endif
%{_prefix}/lib64/libhcom.so
%{_prefix}/lib64/libhcom_static.a
%if %{with java_compile}
    %{_prefix}/local/jars/hcom/*.jar
%endif

%files debuginfo
%defattr(-,root,root)
%{_prefix}/lib64/libhcom.so.debug

%define __os_install_post %{nil}

%changelog
* Mon Nov 17 2025 Yan Zhihan <yanzhihan@huawei.com> - 25.3.0-B017
- Package init
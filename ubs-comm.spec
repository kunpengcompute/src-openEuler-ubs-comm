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

%global with_multicast %{?_with_multicast:%{_with_multicast}}
# 如果没有提供，则设置默认值
%if "%{with_multicast}" == ""
    %global with_multicast 1
%endif

%global with_htracer_cli %{?_with_htracer_cli:%{_with_htracer_cli}}
# 如果没有提供，则设置默认值
%if "%{with_htracer_cli}" == ""
    %global with_htracer_cli 1
%endif

%if %{undefined rpm_version}
    %define rpm_version 1.0.1
%endif

%if %{undefined rpm_release}
    %define rpm_release 4
%endif

%if %{undefined rpm_build_date}
    %define rpm_build_date %(date +"%%Y-%%m-%%d-%%H:%%M:%%S")
%endif

%if %{undefined package_name}
    %define package_name ubs-comm
%endif

%global package_suffix ubs-comm

Name:           %{package_suffix}
Version       : %{rpm_version}
Release       : %{rpm_release}
Summary:        HCOM
License       : GPL-2.0-only
Provides      : Huawei Technologies Co., Ltd
Source0       : %{package_name}-%{version}.tar.gz
BuildRoot     : %{_buildirootdir}/%{name}_%{version}-build
buildArch     : aarch64 x86_64
ExclusiveArch : aarch64 x86_64

BuildRequires: make gcc cmake libboundscheck rdma-core-devel
%ifarch aarch64
BuildRequires: umdk-urma-devel
%endif

Requires: libboundscheck
Requires: %{name}-lib = %{version}

%description
HCOM是一个适用于C/S架构应用程序的高性能通信库

%package devel
Summary: Development header files and dynamic library for HCOM
Requires:       ubs-comm-lib = %{version}

%description devel
This package contains development header files and dynamic library for HCOM

%package lib
Summary: Dynamic library for HCOM

%description lib
This package contains dynamic library for HCOM

%prep
%setup -q -b 0 -c -n %{name}-%{version}

%build
cd %{_builddir}/%{name}-%{version} && export HCOM_BUILD_RPM=off && export HCOM_BUILD_UB=on && export HCOM_BUILD_HTRACER=on && export HCOM_BUILD_MULTICAST=on && bash -x build.sh

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib64/
mkdir -p  %{buildroot}/usr/local/jars/hcom
mkdir -p %{buildroot}/usr/include/hcom/capi
mkdir -p %{buildroot}/usr/local/bin

cp %{_builddir}/%{package_name}-%{version}/dist/hcom/lib/libhcom.so.0.0.1  %{buildroot}/usr/lib64/
ln -s libhcom.so.0.0.1 %{buildroot}%{_libdir}/libhcom.so.0
ln -s libhcom.so.0     %{buildroot}%{_libdir}/libhcom.so
cp %{_builddir}/%{package_name}-%{version}/dist/hcom/lib/libhcom_static.a  %{buildroot}/usr/lib64/
cp -r %{_builddir}/%{package_name}-%{version}/dist/hcom/include/hcom/*  %{buildroot}/usr/include/hcom/

%if %{with java_compile}
    cp %{_builddir}/%{package_name}-%{version}/hcom/jars/*  %{buildroot}/usr/local/jars/hcom/
%endif

%if %{with_hcom_perf}
    cp -r %{_builddir}/%{package_name}-%{version}/tools/perf_test/build/hcom_perf  %{buildroot}/usr/local/bin/
%endif

%if %{with_htracer_cli}
    cp -r %{_builddir}/%{package_name}-%{version}/dist/hcom_3rdparty/hcom_tracer/htracer_cli  %{buildroot}/usr/local/bin/
%endif

# 主包仅依赖 lib 子包
%files
%defattr(-,root,root)
%doc

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
%if %{with_multicast}
    %{_prefix}/include/hcom/multicast/*.h
%endif

%files lib
%defattr(-,root,root)
%{_prefix}/lib64/libhcom.so.0
%{_prefix}/lib64/libhcom.so.0.0.1

%changelog
* Thu May 21 2026 Pan Hengzhi <panhengzhi@h-partners.com> - 1.0.1-4
- update spec.

* Tue May 19 2026 Pan Hengzhi <panhengzhi@h-partners.com> - 1.0.1-3
- update for urma, bugfix.

* Mon May 11 2026 Pan Hengzhi <panhengzhi@h-partners.com> - 1.0.1-2
- add multicast + hlc.

* Wed Apr 22 2026 Pan Hengzhi <panhengzhi@h-partners.com> - 1.0.1-1
- Package init
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg tdepowersave
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.7.3
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Power management applet for Trinity
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	libdbus-tqt-1-devel >= %{tde_epoch}:0.63
BuildRequires:	libdbus-1-tqt-devel >= %{tde_epoch}:0.9

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires: libtool
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# UDEV support
%define with_tdehwlib 1
BuildRequires:  pkgconfig(udev)

# XSCREENSAVER support
#  Disabled on RHEL4
#  RHEL 8: available in EPEL
#  RHEL 9: available in EPEL
%define with_xscreensaver 1
BuildRequires:  pkgconfig(xscrnsaver)

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# GAMIN support
#  Not on openSUSE.
%if 0%{!?suse_version}
%define with_gamin 1
BuildRequires:	pkgconfig(gamin)
%endif

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(xtst)


Obsoletes:		trinity-kpowersave < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-kpowersave = %{?epoch:%{epoch}:}%{version}-%{release}


%description
TDEPowersave is a TDE systray applet which allows to control the power 
management settings and policies of your computer.

Current feature list:
 * support for ACPI, APM and PMU
 * trigger suspend to disk/ram and standby
 * switch cpu frequency policy (between: performance, dynamic and powersave)
 * applet icon with information about AC state, battery fill and battery
   (warning) states
 * applet tooltip with information about battery fill and remaining battery 
   time/percentage
 * autosuspend (to suspend the machine if the user has been inactive for a 
   defined time)
 * a global configurable blacklist with programs which prevent autosuspend
   (e.g. videoplayer and cd burning tools)
 * trigger lock screen and select the lock method
 * KNotify support
 * online help
 * localisations for many languages
 
TDEPowersave supports schemes with following configurable specific 
settings for:
 * screensaver
 * DPMS
 * autosuspend
 * scheme specific blacklist for autosuspend
 * notification settings


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
	
if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DCONFIG_INSTALL_DIR="%{tde_confdir}" \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}


%post
# Disables automatic poweroff, make sure we match both "kpowersave" and "tdepowersave"
if [ $1 = 1 ] && [ -r /etc/acpi/actions/power.sh ]; then
  %__cp -f "/etc/acpi/actions/power.sh" "/etc/acpi/actions/power.sh.tdepowersavebackup"
  %__sed -i "/etc/acpi/actions/power.sh" -e "s|kpowersave|powersave|"
fi

%postun
if [ $1 = 0 ] && [ -r "/etc/acpi/actions/power.sh.tdepowersavebackup" ]; then
  %__mv -f "/etc/acpi/actions/power.sh.tdepowersavebackup" "/etc/acpi/actions/power.sh"
fi


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING TODO
%{tde_bindir}/tdepowersave
%{tde_libdir}/libtdeinit_tdepowersave.la
%{tde_libdir}/libtdeinit_tdepowersave.so
%{tde_tdelibdir}/tdepowersave.la
%{tde_tdelibdir}/tdepowersave.so
%{tde_tdeappdir}/tdepowersave.desktop
%{tde_datadir}/apps/tdepowersave/
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_datadir}/autostart/tdepowersave-autostart.desktop
%config(noreplace) %{tde_confdir}/tdepowersaverc
%{tde_mandir}/man1/tdepowersave.*

%lang(cs) %{tde_tdedocdir}/HTML/cs/tdepowersave/
%lang(de) %{tde_tdedocdir}/HTML/de/tdepowersave/
%lang(en) %{tde_tdedocdir}/HTML/en/tdepowersave/
%lang(fi) %{tde_tdedocdir}/HTML/fi/tdepowersave/
%lang(hu) %{tde_tdedocdir}/HTML/hu/tdepowersave/
%lang(nb) %dir %{tde_tdedocdir}/HTML/nb
%lang(nb) %{tde_tdedocdir}/HTML/nb/tdepowersave/


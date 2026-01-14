%bcond clang 1
%bcond tdehwlib 1
%bcond xscreensaver 1
%bcond gamin 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg tdepowersave
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.7.3
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Power management applet for Trinity
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:  cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DCONFIG_INSTALL_DIR=%{_sysconfdir}/trinity
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DBUILD_ALL=ON

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	libdbus-tqt-1-devel >= %{tde_epoch}:0.63
BuildRequires:	libdbus-1-tqt-devel >= %{tde_epoch}:0.9

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires:  libtool

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes


# UDEV support
%{?with_tdehwlib:BuildRequires:  pkgconfig(udev)}

# XSCREENSAVER support
#  Disabled on RHEL4
#  RHEL 8: available in EPEL
#  RHEL 9: available in EPEL
%{?with_xscreensaver:BuildRequires:  pkgconfig(xscrnsaver)}

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# GAMIN support
%{?with_gamin:BuildRequires:	pkgconfig(gamin)}

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


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"
	

%install -a
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
%{tde_prefix}/bin/tdepowersave
%{tde_prefix}/%{_lib}/libtdeinit_tdepowersave.la
%{tde_prefix}/%{_lib}/libtdeinit_tdepowersave.so
%{tde_prefix}/%{_lib}/trinity/tdepowersave.la
%{tde_prefix}/%{_lib}/trinity/tdepowersave.so
%{tde_prefix}/share/applications/tde/tdepowersave.desktop
%{tde_prefix}/share/apps/tdepowersave/
%{tde_prefix}/share/icons/hicolor/*/*/*.png
%{tde_prefix}/share/autostart/tdepowersave-autostart.desktop
%config(noreplace) %{_sysconfdir}/trinity/tdepowersaverc
%{tde_prefix}/share/man/man1/tdepowersave.*

%lang(cs) %{tde_prefix}/share/doc/tde/HTML/cs/tdepowersave/
%lang(de) %{tde_prefix}/share/doc/tde/HTML/de/tdepowersave/
%lang(en) %{tde_prefix}/share/doc/tde/HTML/en/tdepowersave/
%lang(fi) %{tde_prefix}/share/doc/tde/HTML/fi/tdepowersave/
%lang(hu) %{tde_prefix}/share/doc/tde/HTML/hu/tdepowersave/
%lang(nb) %dir %{tde_prefix}/share/doc/tde/HTML/nb
%lang(nb) %{tde_prefix}/share/doc/tde/HTML/nb/tdepowersave/


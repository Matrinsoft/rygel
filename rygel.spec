## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global apiver 2.8

Name:          rygel
Version:       46~rc.0
Release:       %autorelease
Summary:       A collection of UPnP/DLNA services

License:       LGPL-2.1-or-later AND CC-BY-SA-3.0
URL:           https://wiki.gnome.org/Projects/Rygel
Source0:       https://download.gnome.org/sources/%{name}/%{gnome_major_version}/%{name}-%{gnome_tarball_version}.tar.xz

%gnome_check_version

BuildRequires: desktop-file-utils
BuildRequires: docbook-style-xsl
BuildRequires: gettext
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc
BuildRequires: libunistring-devel
BuildRequires: meson
BuildRequires: systemd-rpm-macros
BuildRequires: vala
BuildRequires: valadoc
BuildRequires: pkgconfig(gee-0.8)
BuildRequires: pkgconfig(gst-editing-services-1.0)
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-pbutils-1.0)
BuildRequires: pkgconfig(gtk4)
BuildRequires: pkgconfig(gupnp-1.6)
BuildRequires: pkgconfig(gupnp-av-1.0)
BuildRequires: pkgconfig(gupnp-dlna-2.0)
BuildRequires: pkgconfig(libmediaart-2.0)
BuildRequires: pkgconfig(libsoup-3.0)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(tinysparql-3.0)
BuildRequires: python3dist(docutils)
BuildRequires: python3dist(pyyaml)
BuildRequires: /usr/bin/xsltproc

%description
Rygel is a home media solution that allows you to easily share audio, video and
pictures, and control of media player on your home network. In technical terms
it is both a UPnP AV MediaServer and MediaRenderer implemented through a plug-in
mechanism. Interoperability with other devices in the market is achieved by
conformance to very strict requirements of DLNA and on the fly conversion of
media to format that client devices are capable of handling.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package localsearch
Summary: Localsearch plugin for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-tracker <= %{version}

%description localsearch
A plugin for rygel to use localsearch to locate media on the local machine.

%prep
%autosetup -p1 -n %{name}-%{gnome_tarball_version}

%build
%meson \
  -Dapi-docs=true \
  -Dintrospection=enabled \
  -Dexamples=false
%meson_build

%install
%meson_install

%find_lang %{name}

%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%check
# Verify the desktop files
desktop-file-validate %{buildroot}/%{_datadir}/applications/rygel.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/rygel-preferences.desktop

%files -f %{name}.lang
%license COPYING COPYING.logo
%doc AUTHORS NEWS README.md
%config(noreplace) %{_sysconfdir}/rygel.conf
%{_bindir}/rygel
%{_bindir}/rygel-preferences
%{_libdir}/librygel-core-%{apiver}.so.0*
%{_libdir}/librygel-db-%{apiver}.so.0*
%{_libdir}/librygel-renderer-%{apiver}.so.0*
%{_libdir}/librygel-renderer-gst-%{apiver}.so.0*
%{_libdir}/librygel-server-%{apiver}.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/RygelCore-%{apiver}.typelib
%{_libdir}/girepository-1.0/RygelRenderer-%{apiver}.typelib
%{_libdir}/girepository-1.0/RygelRendererGst-%{apiver}.typelib
%{_libdir}/girepository-1.0/RygelServer-%{apiver}.typelib
%dir %{_libdir}/rygel-%{apiver}
%dir %{_libdir}/rygel-%{apiver}/engines
%dir %{_libdir}/rygel-%{apiver}/plugins
%{_libdir}/rygel-%{apiver}/engines/librygel-media-engine-gst.so
%{_libdir}/rygel-%{apiver}/engines/librygel-media-engine-simple.so
%{_libdir}/rygel-%{apiver}/engines/media-engine-gst.plugin
%{_libdir}/rygel-%{apiver}/engines/media-engine-simple.plugin
%{_libdir}/rygel-%{apiver}/plugins/librygel-external.so
%{_libdir}/rygel-%{apiver}/plugins/external.plugin
%{_libdir}/rygel-%{apiver}/plugins/librygel-gst-launch.so
%{_libdir}/rygel-%{apiver}/plugins/gst-launch.plugin
%{_libdir}/rygel-%{apiver}/plugins/librygel-media-export.so
%{_libdir}/rygel-%{apiver}/plugins/media-export.plugin
%{_libdir}/rygel-%{apiver}/plugins/librygel-mpris.so
%{_libdir}/rygel-%{apiver}/plugins/mpris.plugin
%{_libdir}/rygel-%{apiver}/plugins/librygel-playbin.so
%{_libdir}/rygel-%{apiver}/plugins/playbin.plugin
%{_libexecdir}/rygel/
%{_datadir}/rygel/
%{_datadir}/applications/rygel*
%{_datadir}/dbus-1/services/org.gnome.Rygel1.service
%{_datadir}/icons/hicolor/*/apps/rygel*
%{_mandir}/man1/rygel.1*
%{_mandir}/man5/rygel.conf.5*
%{_userunitdir}/rygel.service

%files localsearch
%{_libdir}/rygel-%{apiver}/plugins/librygel-localsearch.so
%{_libdir}/rygel-%{apiver}/plugins/localsearch.plugin

%files devel
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%doc %{_datadir}/gtk-doc/html/librygel*
%{_libdir}/librygel-*.so
%{_includedir}/rygel-%{apiver}
%{_libdir}/pkgconfig/rygel*.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/RygelCore-%{apiver}.gir
%{_datadir}/gir-1.0/RygelRenderer-%{apiver}.gir
%{_datadir}/gir-1.0/RygelRendererGst-%{apiver}.gir
%{_datadir}/gir-1.0/RygelServer-%{apiver}.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/rygel*.deps
%{_datadir}/vala/vapi/rygel*.vapi

%changelog
## START: Generated by rpmautospec
* Mon Aug 31 2026 Milan Crha <mcrha@redhat.com> - 46~rc.0-1
- Update to 46.rc.0

* Thu Aug 06 2026 Jan Grulich <jgrulich@redhat.com> - 46~beta-1
- Update to 46.beta

* Fri Jul 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Mon Jun 29 2026 Milan Crha <mcrha@redhat.com> - 46~alpha-1
- Update to 46.alpha

* Tue May 26 2026 nmontero <nmontero@redhat.com> - 45.2-1
- Update to 45.2

* Wed Mar 25 2026 Jan Grulich <jgrulich@redhat.com> - 45.1-5
- Add configuration for release-monitoring

* Mon Mar 02 2026 Jan Grulich <jgrulich@redhat.com> - 45.1-4
- Packit: drop upstream_project_url and rely on release-monitoring only

* Wed Feb 25 2026 Jan Grulich <jgrulich@redhat.com> - 45.1-3
- Packit: drop fast_forward_merge_into as current stable branches diverge

* Tue Feb 24 2026 Jan Grulich <jgrulich@redhat.com> - 45.1-2
- Onboard to Packit for stable Fedora branches

* Mon Jan 19 2026 Jan Horak <jhorak@redhat.com> - 45.1-1
- Update to 45.1

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 45.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Dec 19 2025 David King <amigadave@amigadave.com> - 45.0-2
- Own plugin directories (#2283502)

* Mon Sep 15 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 45.0-1
- Update to 45.0

* Thu Sep 04 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 45~rc-1
- Update to 45.rc

* Tue Aug 05 2025 Marek Kasik <mkasik@redhat.com> - 45~beta-1
- Update to 45.beta

* Tue Aug 05 2025 Marek Kasik <mkasik@redhat.com> - 45~alpha-3
- Fix autochangelog / autorelease

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 45~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 45~alpha-1
- Update to 45.alpha

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 0.44.2-1
- Update to 0.44.2

* Thu Feb 06 2025 nmontero <nmontero@redhat.com> - 0.44.1-4
- Rebuild for the renaming of tracker to tinysparql

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.44.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Oct 13 2024 David King <amigadave@amigadave.com> - 0.44.1-2
- Use systemd scriptlets for user unit

* Sun Oct 13 2024 David King <amigadave@amigadave.com> - 0.44.1-1
- Update to 0.44.1

* Wed Sep 18 2024 nmontero <nmontero@redhat.com> - 0.44.0-1
- Update to 0.44.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Nieves Montero <nmontero@redhat.com> - 0.43.0-1
- Update to 0.43.0

* Tue May 07 2024 David King <amigadave@amigadave.com> - 0.42.6-1
- Update to 0.42.6

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Kalev Lember <klember@redhat.com> - 0.42.5-1
- Update to 0.42.5

* Wed Aug 02 2023 Kalev Lember <klember@redhat.com> - 0.42.4-1
- Update to 0.42.4

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 24 2023 David King <amigadave@amigadave.com> - 0.42.3-1
- Update to 0.42.3

* Mon Apr 03 2023 David King <amigadave@amigadave.com> - 0.42.2-1
- Update to 0.42.2

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 0.42.1-1
- Update to 0.42.1

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 10 2022 David King <amigadave@amigadave.com> - 0.42.0-2
- Fix devel subpackage installation (#2152302)

* Mon Nov 21 2022 David King <amigadave@amigadave.com> - 0.42.0-1
- Update to 0.42.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 David King <amigadave@amigadave.com> - 0.40.4-1
- Update to 0.40.4

* Tue Jan 25 2022 David King <amigadave@amigadave.com> - 0.40.3-2
- Use pkgconfig for BuildRequires

* Mon Jan 24 2022 David King <amigadave@amigadave.com> - 0.40.3-1
- Update to 0.40.3

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Sep 18 2021 Kalev Lember <klember@redhat.com> - 0.40.2-1
- Update to 0.40.2

* Fri Aug 20 2021 Kalev Lember <klember@redhat.com> - 0.40.1-5
- Rebuilt for gupnp-av and gupnp-dlna soname bumps

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 20 2021 Kalev Lember <klember@redhat.com> - 0.40.1-3
- Fix directory ownership for gtk-doc, gir and vala directories

* Sat Feb 20 2021 Kalev Lember <klember@redhat.com> - 0.40.1-2
- Build tracker 3.0 plugin, disable tracker 2.0

* Sat Feb 20 2021 Kalev Lember <klember@redhat.com> - 0.40.1-1
- Update to 0.40.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 14 2020 Kalev Lember <klember@redhat.com> - 0.40.0-1
- Update to 0.40.0

* Tue Aug 18 2020 Kalev Lember <klember@redhat.com> - 0.39.2-2
- Tighten soname globs

* Tue Aug 18 2020 Kalev Lember <klember@redhat.com> - 0.39.2-1
- Update to 0.39.2
- Switch to the meson build system

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 12 2020 Kalev Lember <klember@redhat.com> - 0.38.3-1
- Update to 0.38.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 0.36.2-2
- Rebuilt against fixed atk (#1626575)

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 0.36.2-1
- Update to 0.36.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 06 2018 Kalev Lember <klember@redhat.com> - 0.36.1-2
- Drop ldconfig scriptlets

* Tue Feb 06 2018 Kalev Lember <klember@redhat.com> - 0.36.1-1
- Update to 0.36.1

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.36.0-3
- Switch to %%ldconfig_scriptlets

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.36.0-2
- Remove obsolete scriptlets

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 0.36.0-1
- Update to 0.36.0

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 0.35.0-1
- Update to 0.35.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-3
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 0.34.0-1
- Update to 0.34.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 0.33.92-1
- Update to 0.33.92

* Mon Mar 06 2017 Kalev Lember <klember@redhat.com> - 0.33.90-1
- Update to 0.33.90

* Tue Feb 14 2017 Richard Hughes <richard@hughsie.com> - 0.33.1-1
- Update to 0.33.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 0.32.1-1
- Update to 0.32.1

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com> - 0.32.0-1
- Update to 0.32.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 0.31.6-2
- Move desktop file verification to the check section

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 0.31.6-1
- Update to 0.31.6

* Fri Sep 02 2016 Kalev Lember <klember@redhat.com> - 0.31.5-2
- Don't set group tags

* Fri Sep 02 2016 Kalev Lember <klember@redhat.com> - 0.31.5-1
- Update to 0.31.5

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 0.31.4-2
- Ship man pages

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 0.31.4-1
- Update to 0.31.4

* Thu Jul 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> - 0.31.3-3
- drop no longer shipped files

* Wed Jul 20 2016 Richard Hughes <richard@hughsie.com> - 0.31.3-2
- Add BR for libxslt to bring in xsltproc for man pages

* Wed Jul 20 2016 Richard Hughes <richard@hughsie.com> - 0.31.3-1
- Update to 0.31.3

* Wed Jun 22 2016 Richard Hughes <richard@hughsie.com> - 0.31.2-1
- Update to 0.31.2

* Mon May 23 2016 Peter Robinson <pbrobinson@gmail.com> - 0.31.1-1
- Update to 0.31.1

* Tue Apr 26 2016 Peter Robinson <pbrobinson@gmail.com> - 0.31.0-1
- 0.31.0

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 0.30.1-1
- Update to 0.30.1

* Thu Mar 24 2016 Kalev Lember <klember@redhat.com> - 0.30.0-2
- Fix the build

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 0.30.0-1
- Update to 0.30.0

* Tue Mar 15 2016 Kalev Lember <klember@redhat.com> - 0.29.5-1
- Update to 0.29.5

* Tue Mar 01 2016 Richard Hughes <richard@hughsie.com> - 0.29.4-1
- Update to 0.29.4

* Tue Feb 16 2016 Richard Hughes <richard@hughsie.com> - 0.29.3-1
- Update to 0.29.3

* Thu Feb 11 2016 Peter Robinson <pbrobinson@gmail.com> - 0.29.2-1
- 0.29.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 0.29.1-2
- Update upstream URLs

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 0.29.1-1
- Update to 0.29.1

* Mon Dec 14 2015 Debarshi Ray <debarshir@gnome.org> - 0.28.2-1
- Update to 0.28.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 0.28.1-1
- Update to 0.28.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 0.28.0-1
- Update to 0.28.0

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 0.27.6-1
- Update to 0.27.6

* Mon Aug 31 2015 Kalev Lember <klember@redhat.com> - 0.27.5-1
- Update to 0.27.5

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 0.27.4-3
- Drop an unrecognized configure option

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 0.27.4-2
- Use make_install macro

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 0.27.4-1
- Update to 0.27.4

* Tue Jul 28 2015 Kalev Lember <klember@redhat.com> - 0.27.3-1
- Update to 0.27.3

* Tue Jun 30 2015 Kalev Lember <klember@redhat.com> - 0.27.2-1
- Update to 0.27.2

* Fri Jun 19 2015 Dennis Gilmore <dennis@ausil.us> - 0.27.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Kalev Lember <kalevlember@gmail.com> - 0.27.1-1
- Update to 0.27.1

* Sun May 10 2015 Kalev Lember <kalevlember@gmail.com> - 0.26.1-1
- Update to 0.26.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 0.26.0-1
- Update to 0.26.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 0.25.3-4
- Drop pkgconfig dep from the -devel subpackage

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 0.25.3-3
- Tighten deps with the _isa macro

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 0.25.3-2
- Use license macro for the COPYING file

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 0.25.3-1
- Update to 0.25.3

* Thu Feb 19 2015 Richard Hughes <richard@hughsie.com> - 0.25.2.1-1
- Update to 0.25.2.1

* Tue Feb 17 2015 Richard Hughes <richard@hughsie.com> - 0.25.2-1
- Update to 0.25.2

* Mon Jan 26 2015 Adam Williamson <awilliam@redhat.com> - 0.25.1-3
- add files for a new plugin

* Mon Jan 26 2015 Adam Williamson <awilliam@redhat.com> - 0.25.1-2
- Adjust file list for API bump to 2.6, use a %%global for it

* Tue Jan 20 2015 Richard Hughes <richard@hughsie.com> - 0.25.1-1
- Update to 0.25.1

* Fri Dec 19 2014 Richard Hughes <richard@hughsie.com> - 0.25.0-1
- Update to 0.25.0

* Mon Nov 10 2014 Peter Robinson <pbrobinson@gmail.com> - 0.24.2-1
- 0.24.2

* Tue Oct 14 2014 Peter Robinson <pbrobinson@gmail.com> - 0.24.1-2
- update ver

* Tue Oct 14 2014 Peter Robinson <pbrobinson@gmail.com> - 0.24.1-1
- 0.24.1

* Tue Sep 23 2014 Peter Robinson <pbrobinson@gmail.com> - 0.24.0-2
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec

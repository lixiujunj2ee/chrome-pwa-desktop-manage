Name:           chrome-pwa-desktop-manage
Version:        1.0.6
Release:        1%{?dist}
Summary:        Manage Chrome PWA desktop shortcuts

License:        MIT
URL:            https://github.com/lixiujunj2ee/chrome-pwa-desktop-manage
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch
Requires:       python3

%description
A tool to manage Chrome Progressive Web Apps desktop shortcuts on Linux.

%prep
%autosetup -n %{name}-%{version}

%build
# nothing to build

%install
rm -rf %{buildroot}

# binaries
install -Dm755 pwa %{buildroot}%{_bindir}/pwa
install -Dm755 start_app.sh %{buildroot}%{_bindir}/chrome-pwa-desktop-manage

# app files
install -d %{buildroot}%{_datadir}/%{name}
cp -a *.py pwa %{buildroot}%{_datadir}/%{name}/

# desktop
install -Dm644 com.github.lixiujunj2ee.ChromePWADesktopManage.desktop \
  %{buildroot}%{_datadir}/applications/com.github.lixiujunj2ee.ChromePWADesktopManage.desktop

# icon
install -Dm644 icons/chrome-pwa-desktop-manage.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/com.github.lixiujunj2ee.ChromePWADesktopManage.png

# metainfo
install -Dm644 com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml \
  %{buildroot}%{_metainfodir}/com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml

%files
%{_bindir}/pwa
%{_bindir}/chrome-pwa-desktop-manage
%{_datadir}/%{name}
%{_datadir}/applications/com.github.lixiujunj2ee.ChromePWADesktopManage.desktop
%{_datadir}/icons/hicolor/128x128/apps/com.github.lixiujunj2ee.ChromePWADesktopManage.png
%{_metainfodir}/com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml

%changelog
* Mon Dec 29 2025 lixiujunj2ee - 1.0.6-1
- Initial COPR release


Name:           chrome-pwa-desktop-manage
Version:        1.0.0
Release:        1%{?dist}
Summary:        Manage Chrome Progressive Web Apps desktop shortcuts

License:        MIT
URL:            https://github.com/lixiujunj2ee/chrome-pwa-desktop-manage

BuildArch:      noarch
Requires:       python3
Requires:       google-chrome-stable
Requires:       python3-flet
Requires:       python3-packaging
Requires:       python3-os
Requires:       python3-tendo
Requires:       python3-subprocess
Requires:       python3-threading

%description
A user-friendly tool to manage Chrome PWA desktop shortcuts on Linux.
Ensures single instance opening and easy management of installed PWAs.

%prep
%autosetup -n chrome-pwa-desktop-manage-%{version}

%install
# 安装 Python 入口
install -d %{buildroot}%{_datadir}/%{name}
cp -a main.py pwa/ *.py %{buildroot}%{_datadir}/%{name}/

# 安装 Go binary
install -Dm755 pwa %{buildroot}%{_bindir}/pwa

# 安装 GUI 文件
install -Dm644 com.github.lixiujunj2ee.ChromePWADesktopManage.desktop %{buildroot}%{_datadir}/applications/com.github.lixiujunj2ee.ChromePWADesktopManage.desktop

# 安装 desktop 文件
install -Dm644 com.github.lixiujunj2ee.ChromePWADesktopManage.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/com.github.lixiujunj2ee.ChromePWADesktopManage.png

# 安装 metainfo
install -Dm644 com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml %{buildroot}%{_metainfodir}/com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml

%post
update-desktop-database &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files
%{_bindir}/chrome-pwa-desktop-manage
%{_bindir}/pwa

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/

%{_datadir}/applications/com.github.lixiujunj2ee.ChromePWADesktopManage.desktop
%{_datadir}/icons/hicolor/128x128/apps/com.github.lixiujunj2ee.ChromePWADesktopManage.png
%{_metainfodir}/com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml

%changelog
* Mon Dec 29 2025 lixiujunj2ee <lixiujunj2ee@email.com> - 1.0.0-1
- Initial RPM package
- Install pwa script to /usr/bin/pwa for global access

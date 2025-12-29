Name:           chrome-pwa-desktop-manage
Version:        1.0.6
Release:        1%{?dist}
Source0:        %{name}-%{version}.tar.gz
Summary:        Manage Chrome Progressive Web Apps desktop shortcuts

License:        MIT
URL:            https://github.com/lixiujunj2ee/chrome-pwa-desktop-manage

BuildArch:      noarch

Requires:       python3

%description
A user-friendly tool to manage Chrome PWA desktop shortcuts on Linux.
Provides GUI management and ensures single-instance opening of PWAs.

%prep
%autosetup -S git

%install
rm -rf %{buildroot}

# 安装全局可执行命令
install -Dm755 pwa %{buildroot}%{_bindir}/pwa
install -Dm755 start_app.sh %{buildroot}%{_bindir}/chrome-pwa-desktop-manage

# 安装 Python 源码和资源到 /usr/share
install -Dm644 main.py %{buildroot}%{_datadir}/%{name}/main.py
cp -a pwa/ *.py %{buildroot}%{_datadir}/%{name}/  # 如果有其他 .py 文件

# 安装 .desktop 文件
install -Dm644 com.github.lixiujunj2ee.ChromePWADesktopManage.desktop \
    %{buildroot}%{_datadir}/applications/com.github.lixiujunj2ee.ChromePWADesktopManage.desktop

# 安装图标
install -Dm644 icons/chrome-pwa-desktop-manage.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/com.github.lixiujunj2ee.ChromePWADesktopManage.png

# 安装 AppStream metainfo
install -Dm644 com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml \
    %{buildroot}%{_metainfodir}/com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml

%post
update-desktop-database &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files
%{_bindir}/pwa
%{_bindir}/chrome-pwa-desktop-manage
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/com.github.lixiujunj2ee.ChromePWADesktopManage.desktop
%{_datadir}/icons/hicolor/128x128/apps/com.github.lixiujunj2ee.ChromePWADesktopManage.png
%{_metainfodir}/com.github.lixiujunj2ee.ChromePWADesktopManage.metainfo.xml

%changelog
* Mon Dec 29 2025 lixiujunj2ee - 1.0.6-1
- Initial successful RPM release for Copr
- Fixed %install directory creation and permissions

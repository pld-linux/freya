#
# Conditional build:
%bcond_with	avahi		# build with Avahi (Built-in Serverlist)
%bcond_without	glyr	# build with libglyr (Now Playing Browser)
%bcond_with	libnotify	# build with libnotify (For notifcations)

# TODO
# - fails to understand libnotify is there
#   -- checking for modules 'OPTIONAL;libnotify'
#   --   package 'OPTIONAL' not found
#   Disabling libnotify support, since deps were not found.
# - does not support out of tree build:
#   freya-1.0.2/src/Init/cmdoptions.cc:10:26: fatal error: ../../config.h: No such file or directory
# - avahi build fails:
#   freya-1.0.2/src/Browser/Avahi/ServerList.hh:88:5: error: 'Avahi' does not name a type
#   freya-1.0.2/src/Browser/Avahi/ServerList.cc: In constructor 'Browser::ServerList::ServerList(Glib::RefPtr<Gtk::Builder>&, GManager::BrowserList&)':
#   freya-1.0.2/src/Browser/Avahi/ServerList.cc:51:5: error: 'avahi_handle' was not declared in this scope
# - mpdclinet link fails:
#   freya-1.0.2/src/MPD/Client.cc: In member function 'virtual void MPD::Client::fill_playlists(MPD::AbstractItemlist&)':
#   freya-1.0.2/src/MPD/Client.cc:278:40: error: 'mpd_send_list_playlists' was not declared in this scope
Summary:	A simple and slim mpd client
Name:		freya
Version:	1.0.2
Release:	0.1
License:	GPL v3+
Group:		Applications/Multimedia
URL:		https://github.com/studentkittens/Freya
# VCS: git:https://github.com/studentkittens/Freya.git
Source0:	https://github.com/studentkittens/Freya/tarball/master/%{name}.tgz
# Source0-md5:	6e6686e2ef4845c17e32183d33405cc4
%{?with_avahi:BuildRequires:	avahi-devel}
%{?with_avahi:BuildRequires:	avahi-glib-devel}
BuildRequires:	cmake
BuildRequires:	glibmm-devel
%{?with_glyr:BuildRequires:	glyr-devel}
BuildRequires:	gtkmm3-devel
BuildRequires:	libmpdclient-devel
%{?with_libnotify:BuildRequires:	libnotify-devel}
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fun and slim Client for the MPD Server.

%prep
%setup -qc
mv *-Freya-*/* .

%build
%cmake \
	-DUSE_GLYR=%{!?with_glyr:NO}%{?with_glyr:YES} \
	-DUSE_LIBNOTIFY=%{!?with_libnotify:NO}%{?with_libnotify:YES} \
	-DUSE_AVAHI=%{!?with_avahi:NO}%{?with_avahi:YES} \
	.
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.textile

Summary: FastRI is a *much* faster alternative to the Ruby ri command-line tool
Name: ruby-fastri
Version: 0.3.1
Release: %mkrel 3
Source0: http://rubyforge.org/frs/download.php/31654/fastri-%{version}.tar.gz
Source1: fastri.init.sh
Source2: fastri.sysconfig
# adds a daemon mode enabled by --daemon option
Patch0: fastri-0.3.1-mdv-daemonize.patch
# let ri load rubygems, seems it needs it at least for Gems::Version ...
Patch1: fastri-0.3.1-mdv-ri_paths_needs_rubygems.patch
License: Ruby or GPL+
Group: Development/Ruby
Url: http://rubyforge.org/projects/fastri/
BuildRequires: ruby
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define fastri_user nobody
%define fastri_grp nogroup

%description
FastRI is an alternative to the ri command-line tool. It is *much* faster, and
also allows you to offer RI lookup services over DRb. FastRI is a bit smarter
than ri, and can find classes anywhere in the hierarchy without specifying the
"full path". It also knows about gems, and can tell you e.g. which extensions
to a core class were added by a specific gem.


%prep
%setup -q -n fastri-%{version}
%patch0 -p1
%patch1 -p1


%build
ruby setup.rb config --prefix=%{buildroot}%{_prefix} \
			--libruby=%{buildroot}/usr/lib/ruby \
			--librubyver=%{buildroot}%{ruby_libdir} \
			--librubyverarch=%{buildroot}%{ruby_vendorarchdir} \
			--siteruby=%{buildroot}/usr/lib/ruby/site_ruby \
			--siterubyver=%{buildroot}%{ruby_sitelibdir} \
			--siterubyverarch=%{buildroot}%{ruby_sitearchdir}
ruby setup.rb setup


%check
ruby setup.rb test


%install
rm -rf %{buildroot}
ruby setup.rb install
# save a few bytes
rm -f %{buildroot}%{_bindir}/qri && ln -s fri %{buildroot}%{_bindir}/qri
mkdir -p %{buildroot}%{_initrddir}
cp -p %SOURCE1 %{buildroot}%{_initrddir}/fastri
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cp -p %SOURCE2 %{buildroot}%{_sysconfdir}/sysconfig/fastri
mkdir -p %{buildroot}/var/cache/fastri
mkdir -p %{buildroot}/var/log
touch %{buildroot}/var/log/fastri.log


%clean
rm -rf %{buildroot}


%post
%_post_service fastri


%preun
%_preun_service fastri


%files
%defattr(-,root,root)
%doc CHANGES README.en THANKS LICENSE
%dir %attr(-,%fastri_user,%fastri_grp) /var/cache/fastri
%ghost %attr(-,%fastri_user,%fastri_grp) /var/log/fastri.log
%{_initrddir}/fastri
%{_sysconfdir}/sysconfig/fastri
%{_bindir}/fastri-server
%{_bindir}/fri
%{_bindir}/qri
%{_bindir}/ri-emacs
%{ruby_sitelibdir}/fastri/full_text_index.rb
%{ruby_sitelibdir}/fastri/full_text_indexer.rb
%{ruby_sitelibdir}/fastri/name_descriptor.rb
%{ruby_sitelibdir}/fastri/ri_index.rb
%{ruby_sitelibdir}/fastri/ri_service.rb
%{ruby_sitelibdir}/fastri/util.rb
%{ruby_sitelibdir}/fastri/version.rb



# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: cmake
Epoch: 100
Version: 3.30.1
Release: 1%{?dist}
Summary: Cross-platform make system
License: BSD-3-Clause
URL: https://github.com/Kitware/CMake/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: bzip2-devel
BuildRequires: ccache
BuildRequires: coreutils
BuildRequires: curl-devel
BuildRequires: expat-devel
BuildRequires: fdupes
BuildRequires: findutils
BuildRequires: gcc-c++
BuildRequires: gcc-gfortran
BuildRequires: jsoncpp-devel
BuildRequires: libarchive-devel
BuildRequires: libuv-devel
BuildRequires: libzstd-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: rhash-devel
BuildRequires: sed
BuildRequires: xz-devel
BuildRequires: zlib-devel
Requires: make

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is possible
to support complex environments requiring system configuration,
preprocessor generation, code generation, and template instantiation.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags} %{?_fmoddir:-I%{_fmoddir}}"
export FCFLAGS="%{optflags} %{?_fmoddir:-I%{_fmoddir}}"
export LDFLAGS="-Wl,-z,relro -Wl,--as-needed"
set -ex && \
    mkdir -p Build && \
    pushd Build && \
    ../bootstrap \
        --prefix=/usr \
        --bindir=/bin \
        --mandir=/share/man \
        --system-libs \
        --no-system-cppdap \
        --verbose \
        -- \
        -DBUILD_CursesDialog:BOOL=ON \
        -DBUILD_QtDialog:BOOL=ON \
        -DBUILD_TESTING:BOOL=OFF \
        -DCMAKE_CXX_COMPILER_LAUNCHER:STRING="ccache" \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-O2 -g -DNDEBUG" \
        -DCMAKE_C_FLAGS:STRING="-O2 -g -DNDEBUG" \
        -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-O2 -g -DNDEBUG" \
        -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
        -DCMAKE_SKIP_BOOTSTRAP_TEST:BOOL=ON \
        -DCMAKE_SKIP_RPATH:BOOL=ON \
        -DCMAKE_USE_RELATIVE_PATHS:BOOL=ON \
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON && \
    popd
%make_build -C Build

%install
%make_install -C Build
install -Dpm755 -d %{buildroot}%{_libdir}/cmake
install -Dpm755 -d %{buildroot}%{_prefix}/lib/rpm
install -Dpm755 -d %{buildroot}%{_prefix}/lib/rpm/fileattrs
install -Dpm755 -d %{buildroot}%{_rpmconfigdir}/macros.d
install -Dpm755 -t %{buildroot}%{_prefix}/lib/rpm cmake.prov
install -Dpm644 -t %{buildroot}%{_prefix}/lib/rpm/fileattrs cmake.attr
install -Dpm644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.cmake
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_prefix}/doc
fdupes -qnrps %{buildroot}%{_datadir}/cmake
fdupes -qnrps %{buildroot}%{_datadir}/cmake-*

%package -n cmake-gui
Summary: CMake graphical user interface
Requires: cmake = %{epoch}:%{version}-%{release}
Requires: hicolor-icon-theme
Requires: shared-mime-info

%description -n cmake-gui
This is a Graphical User Interface for CMake, a cross-platform build
system.

%package -n cmake-data
Summary: Dummy pacakge
Requires: cmake = %{epoch}:%{version}-%{release}
Conflicts: cmake-data < %{epoch}:%{version}-%{release}

%description -n cmake-data
Dummy pacakge.

%package -n cmake-filesystem
Summary: Dummy pacakge
Requires: cmake = %{epoch}:%{version}-%{release}
Conflicts: cmake-filesystem < %{epoch}:%{version}-%{release}

%description -n cmake-filesystem
Dummy pacakge.

%package -n cmake-implementation
Summary: Dummy pacakge
Requires: cmake = %{epoch}:%{version}-%{release}
Conflicts: cmake-implementation < %{epoch}:%{version}-%{release}

%description -n cmake-implementation
Dummy pacakge.

%package -n cmake-rpm-macros
Summary: Dummy pacakge
Requires: cmake = %{epoch}:%{version}-%{release}
Conflicts: cmake-rpm-macros < %{epoch}:%{version}-%{release}

%description -n cmake-rpm-macros
Dummy pacakge.

%package -n cmake3
Summary: Dummy pacakge
Requires: cmake = %{epoch}:%{version}-%{release}
Conflicts: cmake3 < %{epoch}:%{version}-%{release}

%description -n cmake3
Dummy pacakge.

%files
%license Copyright.txt
%dir %{_datadir}/aclocal
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%dir %{_datadir}/cmake*
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%dir %{_datadir}/vim
%dir %{_datadir}/vim/vimfiles
%dir %{_datadir}/vim/vimfiles/indent
%dir %{_datadir}/vim/vimfiles/syntax
%dir %{_libdir}/cmake
%exclude %{_bindir}/cmake-gui
%{_bindir}/*
%{_datadir}/aclocal/cmake.m4
%{_datadir}/bash-completion/completions/*
%{_datadir}/cmake*/*
%{_datadir}/emacs/site-lisp/cmake-mode.el
%{_datadir}/vim/vimfiles/indent/cmake.vim
%{_datadir}/vim/vimfiles/syntax/cmake.vim
%{_rpmconfigdir}/cmake.prov
%{_rpmconfigdir}/fileattrs/cmake.attr
%{_rpmconfigdir}/macros.d/macros.cmake

%files -n cmake-gui
%license Copyright.txt
%dir %{_datadir}/applications
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/*
%dir %{_datadir}/icons/hicolor/*/apps
%dir %{_datadir}/mime
%{_bindir}/cmake-gui
%{_datadir}/applications/cmake-gui.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/mime/packages

%files -n cmake-data
%license Copyright.txt

%files -n cmake-filesystem
%license Copyright.txt

%files -n cmake-implementation
%license Copyright.txt

%files -n cmake-rpm-macros
%license Copyright.txt

%files -n cmake3
%license Copyright.txt

%changelog

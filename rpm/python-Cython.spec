Name:           python-Cython
Version:        0.19.1
Release:        0
Url:            http://www.cython.org
Summary:        The Cython compiler for writing C extensions for the Python language
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/C/Cython/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  fdupes
BuildRequires:  python-devel
Provides:       python-cython = %{version}
Obsoletes:      python-cython < %{version}
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
%{!?python_sitearch: %global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%description
The Cython language makes writing C extensions for the Python language as
easy as Python itself.  Cython is a source code translator based on the
well-known Pyrex, but supports more cutting edge functionality and
optimizations.

The Cython language is very close to the Python language (and most Python
code is also valid Cython code), but Cython additionally supports calling C
functions and declaring C types on variables and class attributes. This
allows the compiler to generate very efficient C code from Cython code.

This makes Cython the ideal language for writing glue code for external C
libraries, and for fast C modules that speed up the execution of Python
code.

%prep
%setup -q -n %{name}-%{version}/upstream
sed -i "s|^#!.*||" Cython/Debugger/{libpython,Cygdb}.py cython.py # Fix non-executable scripts
sed -i "s|\r||" Demos/callback/{README.txt,cheesefinder.h} Demos/embed/Makefile.{unix,msc.static} Doc/primes.c # Fix EOL encoding

%build
CFLAGS="%{optflags}" python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
%fdupes -s %{buildroot}%{python_sitearch} %{buildroot}%{_docdir}

# Disabled testsuite as it takes a long time:
#%%check
#python runtests.py

%files
%defattr(-,root,root,-)
%doc COPYING.txt LICENSE.txt README.txt ToDo.txt USAGE.txt Doc Demos
%{_bindir}/cygdb
%{_bindir}/cython
%{python_sitearch}/Cython/
%{python_sitearch}/*.egg-info
%{python_sitearch}/cython.py*
%{python_sitearch}/pyximport/
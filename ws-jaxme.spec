# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name jaxme

Name:           ws-jaxme
Version:        0.5.1
Release:        4.6%{?dist}
Epoch:          0
Summary:        Open source implementation of JAXB

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://ws.apache.org/jaxme/
# svn export http://svn.apache.org/repos/asf/webservices/jaxme/tags/R0_5_1/ ws-jaxme-0.5.1
# tar czf ws-jaxme-0.5.1-src.tar.gz ws-jaxme
Source0:        ws-jaxme-0.5.1-src.tar.gz
Source1:        ws-jaxme-bind-MANIFEST.MF
# generated docs with forrest-0.5.1
Patch0:         ws-jaxme-docs_xml.patch
Patch1:         ws-jaxme-catalog.patch
Patch2:         ws-jaxme-system-dtd.patch
Patch3:         ws-jaxme-jdk16.patch
Patch4:         ws-jaxme-ant-scripts.patch
Patch5:         ws-jaxme-use-commons-codec.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-apache-resolver
BuildRequires:  ant-trax >= 0:1.6
BuildRequires:  antlr
BuildRequires:  jaxp_transform_impl
BuildRequires:  jakarta-commons-codec
BuildRequires:  junit
BuildRequires:  hsqldb
BuildRequires:  log4j
BuildRequires:  xalan-j2
BuildRequires:  xmldb-api
BuildRequires:  xmldb-api-sdk
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
BuildRequires:  xml-commons-resolver
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-dtds
Requires:       antlr
Requires:       jaxp_transform_impl
Requires:       jakarta-commons-codec
Requires:       junit
Requires:       hsqldb
Requires:       log4j
Requires:       xalan-j2
Requires:       xmldb-api
Requires:       xmldb-api-sdk
Requires:       xerces-j2
Requires:       xml-commons-apis
Requires:       jpackage-utils
Requires(postun): jpackage-utils

%description
A Java/XML binding compiler takes as input a schema 
description (in most cases an XML schema, but it may 
be a DTD, a RelaxNG schema, a Java class inspected 
via reflection, or a database schema). The output is 
a set of Java classes:
* A Java bean class matching the schema description. 
  (If the schema was obtained via Java reflection, 
  the original Java bean class.)
* Read a conforming XML document and convert it into 
  the equivalent Java bean.
* Vice versa, marshal the Java bean back into the 
  original XML document.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils
Requires(postun): jpackage-utils

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{name}
Group:          Documentation

%description    manual
%{summary}.

%prep
%setup -q -n %{name}
for j in $(find . -name "*.jar"); do
    mv $j $j.no
done

%patch0 -p0
%patch1 -p0
%patch2 -p1
DOCBOOKX_DTD=`%{_bindir}/xmlcatalog %{_datadir}/sgml/docbook/xmlcatalog "-//OASIS//DTD DocBook XML V4.5//EN" 2>/dev/null`
%{__perl} -pi -e 's|@DOCBOOKX_DTD@|$DOCBOOKX_DTD|' src/documentation/manual/jaxme2.xml
%patch3 -p1
%patch4 -b .sav
%patch5 -b .sav

%build
export OPT_JAR_LIST="xalan-j2 ant/ant-trax xalan-j2-serializer xml-commons-resolver ant/ant-apache-resolver"
export CLASSPATH=$(build-classpath antlr hsqldb commons-codec junit log4j xmldb-api xerces-j2 xml-commons-jaxp-1.3-apis)
ant all Docs.all \
-Dbuild.sysclasspath=first \
-Ddocbook.home=%{_datadir}/sgml/docbook \
-Ddocbookxsl.home=%{_datadir}/sgml/docbook/xsl-stylesheets

mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u dist/jaxmeapi-%{version}.jar META-INF/MANIFEST.MF

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{base_name}
for jar in dist/*.jar; do
   install -m 644 ${jar} $RPM_BUILD_ROOT%{_javadir}/%{base_name}/
done
(cd $RPM_BUILD_ROOT%{_javadir}/%{base_name} && 
    for jar in *-%{version}*; 
        do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; 
    done
)

(cd $RPM_BUILD_ROOT%{_javadir}/%{base_name} && 
    for jar in *.jar; 
        do ln -sf ${jar} ws-${jar}; 
    done
)

#javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/src/documentation/content/apidocs \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf build/docs/src/documentation/content/apidocs

#manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr build/docs/src/documentation/content/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -pm 644 LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/LICENSE
%{_javadir}/%{base_name}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}

%changelog
* Mon Jan 25 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.1-4.6
- Fix Non-standard group usage.
- Fix Mixed use of spaces/tabs.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:0.5.1-4.5
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> - 0:0.5.1-2.3
- BR docbook-style-xsl.
- BR ant-apache-resolver.

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> - 0:0.5.1-2.3
- Partial sync with jpackage to get build fixes.
- Add osgi manifest to jaxmeapi.jar.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.5.1-2.2
- drop repotag
- fix license tag

* Mon Feb 12 2007 Deepak Bhole <dbhole@redhat.com> - 0:0.5.1-2jpp.1
- Update as per Fedora guidelines.

* Wed May 04 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.5.1-1jpp
- First JPP-1.7 release

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.5-1jpp
- Upgrade to 0.5

* Thu Sep 09 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.3.1-1jpp
- Fix version in changelog
- Upgrade to 0.3.1

* Fri Aug 30 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.4jpp
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:2.0-0.b1.2jpp
- Upgrade to Ant 1.6.X

* Fri Mar 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.1jpp
- First JPackage release

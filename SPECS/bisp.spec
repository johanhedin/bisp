Name:           bisp
Version:        4.19.1.11663
Release:        1%{?dist}
Summary:        BankID Security Application for Linux

Group:          Applications/Internet
License:        Other
URL:            https://install.bankid.com/Download/All
Source0:        https://install.bankid.com/Repository/BISP-%{version}.tar.gz
Source1:        get_bisp.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       mozilla-filesystem
BuildRequires:  /usr/bin/hexdump /usr/bin/xxd

# Put "fake" version numbers on the .so files to shut rpmlint up
Provides:      libai.so = %{version}, libbisp.so = %{version}, libtokenapi.so = %{version}  

# Enable possibility to override the default dependency checking
%define _use_internal_dependency_generator 0

# Don't use the build in "provides" since it will "provide" the plugins in /usr/lib/personal
%define __find_provides %{nil}

# We still want to have requirements automatically figured out
%define __find_requires /usr/lib/rpm/find-requires

# Do not strip the binaries
%define __os_install_post %{nil}


%description
BankID Security Application for Linux is a set of programs and a Firefox plugin
used for digital authentication and signing in bank environments.


%prep
%setup -q -n BISP-%{version}


%build
# BankID normally installs in /usr/local and have hard coded paths in the
# binaries that point out files under /usr/local.
#
# When packaging RPMs, you should not put files in /usr/local since that
# location is for locally installed files and not stuff that comes in
# RPM format.
#
# The script below will replace /usr/local with /usr in the files needed
# to be able to package BIPS "correctly".

# Change /usr/local to /usr in scripts and desktop files
sed -i 's/\/usr\/local/\/usr/g' personal.desktop
sed -i 's/\/usr\/local/\/usr/g' personal.sh
sed -i 's/\/usr\/local/\/usr/g' persadm.sh

# Function to replace strings in binary files
function patch_strings_in_file() {
    local FILE="$1"
    local PATTERN="$2"
    local REPLACEMENT="$3"

    # Find all unique strings in FILE that contain the pattern 
    STRINGS=$(strings ${FILE} | grep ${PATTERN} | sort -u -r)

    if [ "${STRINGS}" != "" ] ; then
        echo "File '${FILE}' contain strings with '${PATTERN}' in them:"

        for OLD_STRING in ${STRINGS} ; do
            # Create the new string with a simple bash-replacement
            NEW_STRING=${OLD_STRING//${PATTERN}/${REPLACEMENT}}

            # Create null terminated ASCII HEX representations of the strings
            OLD_STRING_HEX="$(echo -n ${OLD_STRING} | xxd -g 0 -u -ps -c 256)00"
            NEW_STRING_HEX="$(echo -n ${NEW_STRING} | xxd -g 0 -u -ps -c 256)00"

            if [ ${#NEW_STRING_HEX} -le ${#OLD_STRING_HEX} ] ; then
                # Pad the replacement string with null terminations so the
                # length matches the original string
                while [ ${#NEW_STRING_HEX} -lt ${#OLD_STRING_HEX} ] ; do
                    NEW_STRING_HEX="${NEW_STRING_HEX}00"
                done

                # Now, replace every occurrence of OLD_STRING with NEW_STRING 
                echo -n "Replacing ${OLD_STRING} with ${NEW_STRING}... "
                hexdump -ve '1/1 "%.2X"' ${FILE} | \
                sed "s/${OLD_STRING_HEX}/${NEW_STRING_HEX}/g" | \
                xxd -r -p > ${FILE}.tmp
                mv ${FILE}.tmp ${FILE}
                echo "Done!"
            else
                echo "New string '${NEW_STRING}' is longer than old" \
                     "string '${OLD_STRING}'. Skipping."
            fi
        done
    fi
}



# List binary files in wich we will patch paths
FILES=$(ls *.so personal.bin persadm)

OLD_LIB_BASE_PATH="/usr/local/lib/personal"
NEW_LIB_BASE_PATH="/usr/lib/personal"

OLD_BIN_BASE_PATH="/usr/local/bin"
NEW_BIN_BASE_PATH="/usr/bin"

# Replace /usr/local/lib/personal with /usr/lib/personal and
# /usr/local/bin with /usr/bin
for FILE in ${FILES} ; do
    patch_strings_in_file ${FILE} ${OLD_LIB_BASE_PATH} ${NEW_LIB_BASE_PATH}
    patch_strings_in_file ${FILE} ${OLD_BIN_BASE_PATH} ${NEW_BIN_BASE_PATH}
done


%install
rm -rf %{buildroot}

# Create install layout
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_libdir}/personal
install -m 755 -d %{buildroot}%{_libdir}/personal/icons
install -m 755 -d %{buildroot}%{_libdir}/personal/config
install -m 755 -d %{buildroot}%{_libdir}/personal/lang
install -m 755 -d %{buildroot}%{_libdir}/mozilla/plugins
install -m 755 -d %{buildroot}%{_datadir}/applications
install -m 755 -d html

# Install files in the buildroot
# Install libplugins.so as libbisp.so to not conflict file wise with a manual install
install -m 755 libplugins.so %{buildroot}%{_libdir}/mozilla/plugins/libbisp.so
install -m 755 libai.so libtokenapi.so %{buildroot}%{_libdir}
install -m 755 libBranding.so libCardEdb.so libCardGTOClsc.so libCardOberthur.so \
               libCardPrisma.so libCardSetec.so libCardSiemens.so libP11.so persadm \
               personal.bin %{buildroot}%{_libdir}/personal
install -m 755 persadm.sh %{buildroot}%{_bindir}/persadm
install -m 755 personal.sh %{buildroot}%{_bindir}/personal
# Install personal.desktop as bisp-personal.desktop to not conflict whith a manual install
install -m 644 personal.desktop %{buildroot}%{_datadir}/applications/bisp-personal.desktop
install -m 644 nexus_logo_32x32.png %{buildroot}%{_libdir}/personal/icons
install -m 644 BankID_Security_Application_Help* html
install -m 644 Personal.cfg %{buildroot}%{_libdir}/personal/config
chmod 644 BankIDUbuntu_ReadMe*
for D in $(ls ../lang) ; do
    install -m 755 -d %{buildroot}%{_libdir}/personal/lang/${D}
    install -m 644 ../lang/${D}/*.mo %{buildroot}%{_libdir}/personal/lang/${D}
done


%post
/sbin/ldconfig


%postun
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc Release.txt html BankIDUbuntu_ReadMe*
%dir %{_libdir}/personal
%{_libdir}/personal/*
%{_libdir}/*.so
%{_libdir}/mozilla/plugins/*.so
%{_bindir}/*
%{_datadir}/applications/*.desktop


%changelog
* Sun Nov 04 2012 Name - 4.19.1.11663-1
- Initial release


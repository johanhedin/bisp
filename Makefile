
# Get the requested BISP version from the spec-file
VERSION=$(shell grep 'Version:' SPECS/bisp.spec | awk -F':' '{print $$2}' | sed -e 's/[\t ]//g')


# The "catch all" target
all: rpm
	

dirs:
	mkdir -p {BUILD,BUILDROOT,SRPMS,RPMS}


# Download BISP from bankid.com if not alread downloaded
SOURCES/BISP-$(VERSION).tar.gz:
	cd SOURCES; ./get_bisp.sh $(VERSION)


# Build the rpm
rpm: dirs SOURCES/BISP-$(VERSION).tar.gz
	rpmbuild --target=i686 --define "_topdir ${PWD}" -ba SPECS/bisp.spec


# Clean everything
clean:
	rm -f SOURCES/BISP-*
	rm -rf BUILD BUILDROOT SRPMS RPMS

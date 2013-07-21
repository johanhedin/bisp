bisp
====

The scripts here allow you to automatically download a BankID tar archive for
Linux and then build a Fedora/CentOS RPM that can easily be installed with all
dependencies taken care of.

The RPM:s are i686 but work equally well on x86\_64. To be able to use
the Firefox pluing on x86\_64 you need to install nspluginwrapper.

Build
====
Checkout and build the RPM like this:

$ git clone https://github.com/johanhedin/bisp
$ cd bisp
$ make
$ sudo yum install RPMS/i686/bisp-4.19.1.11663-1.fc17.i686.rpm

The actual name of the RPM depends on the current version of bisp and
your distribution.

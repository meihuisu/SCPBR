# Autoconf/automake file

# General compiler/linker flags
AM_CFLAGS = ${CFLAGS}
AM_FCFLAGS = ${FCFLAGS}
AM_LDFLAGS = ${LDFLAGS}

install:
	mkdir -p ${prefix}/data
	cp ./config ${prefix}/data
	cp -R ./sjfz ${prefix}/data
	chmod og+r ${prefix}/data/config
	chmod -R og+r ${prefix}/data/sjfz
	chmod og+x ${prefix}/data/sjfz

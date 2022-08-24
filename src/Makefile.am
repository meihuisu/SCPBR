# Autoconf/automake file

# General compiler/linker flags
AM_CFLAGS = ${CFLAGS}
AM_LDFLAGS = ${LDFLAGS}

TARGETS = libscpbr.a libscpbr.so

all: $(TARGETS)

install:
	mkdir -p ${prefix}
	mkdir -p ${prefix}/lib
	mkdir -p ${prefix}/include
	cp libscpbr.so ${prefix}/lib
	cp libscpbr.a ${prefix}/lib
	cp scpbr.h ${prefix}/include

libscpbr.a: scpbr_static.o 
	$(AR) rcs $@ $^

libscpbr.so: scpbr.o
	$(CC) -shared $(AM_CFLAGS) -o libscpbr.so $^ $(AM_LDFLAGS)

scpbr.o: scpbr.c
	$(CC) -fPIC -DDYNAMIC_LIBRARY -o $@ -c $^ $(AM_CFLAGS)
	
scpbr_static.o: scpbr.c
	$(CC) -o $@ -c $^ $(AM_CFLAGS)
	
clean:
	rm -rf $(TARGETS)
	rm -rf *.o 


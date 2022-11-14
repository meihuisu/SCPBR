# Autoconf/automake file

# General compiler/linker flags
AM_CFLAGS = ${CFLAGS}
AM_LDFLAGS = ${LDFLAGS}

TARGETS = libsjfz.a libsjfz.so

all: $(TARGETS)

install:
	mkdir -p ${prefix}
	mkdir -p ${prefix}/lib
	mkdir -p ${prefix}/include
	cp libsjfz.so ${prefix}/lib
	cp libsjfz.a ${prefix}/lib
	cp sjfz.h ${prefix}/include

libsjfz.a: sjfz_static.o 
	$(AR) rcs $@ $^

libsjfz.so: sjfz.o
	$(CC) -shared $(AM_CFLAGS) -o libsjfz.so $^ $(AM_LDFLAGS)

sjfz.o: sjfz.c
	$(CC) -fPIC -DDYNAMIC_LIBRARY -o $@ -c $^ $(AM_CFLAGS)
	
sjfz_static.o: sjfz.c
	$(CC) -o $@ -c $^ $(AM_CFLAGS)
	
clean:
	rm -rf $(TARGETS)
	rm -rf *.o 


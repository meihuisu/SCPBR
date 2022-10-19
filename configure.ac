#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_INIT([SCPBR],[1.0],[mei@usc.edu])
AC_CONFIG_SRCDIR([src])
AM_INIT_AUTOMAKE([foreign no-exeext])

# Checks for programs.
AC_PROG_CC

# Checks for libraries.

AC_CHECK_HEADERS([stdlib.h string.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST

# Checks for library functions.

# Set final CFLAGS and LDFLAGS
#CFLAGS="$CHECK_CFLAGS"
#LDFLAGS="$CHECK_LDFLAGS"
#LDFLAGS="$LDFLAGS -lm"

AC_CONFIG_FILES([Makefile
		data/Makefile
		src/Makefile
		test/Makefile])
AC_OUTPUT

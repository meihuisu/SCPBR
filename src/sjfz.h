#ifndef SJFZ_H
#define SJFZ_H

/**
 * @file sjfz.h
 * @brief Main header file for SJFZ library.
 * @author - SCEC 
 * @version 1.0
 *
 * Delivers San Jacinto Fault Zone velocity model
 *
 */

// Includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#include "ucvm_model_dtypes.h"

/* config string */
#define SJFZ_CONFIG_MAX 1000

// Structures
/** Defines a point (latitude, longitude, and depth) in WGS84 format */
typedef struct sjfz_point_t {
  /** Longitude member of the point */
  double longitude;
  /** Latitude member of the point */
  double latitude;
  /** Depth member of the point */
  double depth;
} sjfz_point_t;

/** Defines the material properties this model will retrieve. */
typedef struct sjfz_properties_t {
  /** P-wave velocity in meters per second */
  double vp;
  /** S-wave velocity in meters per second */
  double vs;
  /** Density in g/m^3 */
  double rho;
        /** NOT USED from basic_property_t */
        double qp;
        /** NOT USED from basic_property_t */
        double qs;
} sjfz_properties_t;

/** The SJFZ configuration structure. */
typedef struct sjfz_configuration_t {
  /** The zone of UTM projection */
  int utm_zone;
  /** The model directory */
  char model_dir[128];
  /** Number of x points */
  int nx;
  /** Number of y points */
  int ny;
  /** Number of z points */
  int nz;
  /** Depth in meters */
  double depth;
  /** Top left corner easting */
  double top_left_corner_lon;
  /** Top left corner northing */
  double top_left_corner_lat;
  /** Top right corner easting */
  double top_right_corner_lon;
  /** Top right corner northing */
  double top_right_corner_lat;
  /** Bottom left corner easting */
  double bottom_left_corner_lon;
  /** Bottom left corner northing */
  double bottom_left_corner_lat;
  /** Bottom right corner easting */
  double bottom_right_corner_lat;
  /** Bottom right corner northing */
  double bottom_right_corner_lon;
  /** Z interval for the data */
  double depth_interval;
        /** Bilinear or Trilinear Interpolation on or off (1 or 0) */
        int interpolation;

} sjfz_configuration_t;

// define data status
typedef enum { SJFZ_DATA_NA = 0,
               SJFZ_DATA_FILE = 1,
               SJFZ_DATA_MEMORY = 2 } sjfz_data_t;
#define SJFZ_DATA_FAIL 1
#define SJFZ_DATA_USABLE 0
#define SJFZ_DATA_SUCCESS 2
/** The model structure which points to available portions of the model. */
typedef struct sjfz_model_t {
  /** A pointer to the Vp data either in memory or disk. Null if does not exist. */
  void *vp;
  /** Vp status: 0 = not found, 1 = found and not in memory, 2 = found and in memory */
  sjfz_data_t vp_status;
  /** A pointer to the Vs data either in memory or disk. Null if does not exist. */
  void *vs;
  /** Vs status: 0 = not found, 1 = found and not in memory, 2 = found and in memory */
  sjfz_data_t vs_status;
} sjfz_model_t;

// Constants
/** The version of the model. */
extern const char *sjfz_version_string;

// Variables
/** Set to 1 when the model is ready for query. */
extern int sjfz_is_initialized;

/** Location of the binary data files. */
extern char sjfz_data_directory[128];

/** Configuration parameters. */
extern sjfz_configuration_t *sjfz_configuration;
/** Holds pointers to the velocity model data OR indicates it can be read from file. */
extern sjfz_model_t *sjfz_velocity_model;

/** The height of this model's region, in meters. */
extern double sjfz_total_height_m;
/** The width of this model's region, in meters. */
extern double sjfz_total_width_m;

// UCVM API Required Functions

#ifdef DYNAMIC_LIBRARY

/** Initializes the model */
int model_init(const char *dir, const char *label);
/** Cleans up the model (frees memory, etc.) */
int model_finalize();
/** Returns version information */
int model_version(char *ver, int len);
/** Queries the model */
int model_query(sjfz_point_t *points, sjfz_properties_t *data, int numpts);

#endif

// SJFZ Related Functions

/** Initializes the model */
int sjfz_init(const char *dir, const char *label);
/** Cleans up the model (frees memory, etc.) */
int sjfz_finalize();
/** Returns version information */
int sjfz_version(char *ver, int len);
/** Queries the model */
int sjfz_query(sjfz_point_t *points, sjfz_properties_t *data, int numpts);

// Non-UCVM Helper Functions
/** Reads the configuration file. */
int sjfz_read_configuration(char *file, sjfz_configuration_t *config);
void print_error(char *err);
/** Retrieves the value at a specified grid point in the model. */
void sjfz_read_properties(int x, int y, int z, sjfz_properties_t *data);
/** Attempts to malloc the model size in memory and read it in. */
int sjfz_try_reading_model(sjfz_model_t *model);
/** Calculates density from Vs. */
double sjfz_calculate_density(double vp);
/** Calculates Vs from Vp. */
double sjfz_calculate_vs(double vp);

// Interpolation Functions
/** Linearly interpolates two sjfz_properties_t structures */
void sjfz_linear_interpolation(double percent, sjfz_properties_t *x0, sjfz_properties_t *x1, sjfz_properties_t *ret_properties);
/** Bilinearly interpolates the properties. */
void sjfz_bilinear_interpolation(double x_percent, double y_percent, sjfz_properties_t *four_points, sjfz_properties_t *ret_properties);
/** Trilinearly interpolates the properties. */
void sjfz_trilinear_interpolation(double x_percent, double y_percent, double z_percent, sjfz_properties_t *eight_points,
               sjfz_properties_t *ret_properties);

#endif

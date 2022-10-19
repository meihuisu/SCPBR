#ifndef TEST_HELPER_H
#define TEST_HELPER_H

#include "ucvm_model_dtypes.h"
#include "%%cvmhbn%.h"

/* Constants */
#define MAX_TEST_POINTS 10
#define PLACEHOLDER -99999.0

/* modes of operation */
#define MODE_NONE 0
#define MODE_ELEVATION 2
#define MODE_DEPTH 4

/* Test data sets */
typedef enum { VX_TEST_DATASET_NOBKG = 0, 
	       VX_TEST_DATASET_BKG, 
	       VX_TEST_DATASET_NOGTL } vx_test_dataset_t;

typedef struct %%cvmhbn%_surf_t {
        /** Longitude member of the point */
        double longitude;
        /** Latitude member of the point */
        double latitude;
        /** Depth member of the point */
        double surf;
} %%cvmhbn%_surf_t;

extern %%cvmhbn%_surf_t test_surfs[100];
extern int test_surfs_cnt;

int test_assert_file_exist(const char* filename);

double init_preset_ucvm_surface(%%cvmhbn%_surf_t *surfs);
double get_preset_ucvm_surface(double, double);

/* Retrieve basic test points */
int get_depth_test_point(%%cvmhbn%_point_t *pt, %%cvmhbn%_properties_t *expect);
int get_elev_test_point(%%cvmhbn%_point_t *pt, %%cvmhbn%_properties_t *expect,
                        double *pt_elevation, double *pt_surf);

/* Retrieve expected surface elev at the test points */
int get_surf_values(double *surf_values);

/* Retrieve expected mat props at the test points */
int get_mat_props(float *vp, float *vs, double *rho, vx_test_dataset_t ds);

/* run with model api */
int run%%CVMHBN%(const char *bindir, const char *cvmdir, 
	  const char *infile, const char *outfile,
          int mode);

/* Execute vx_cvmhibbn as a child process */
int runVX%%CVMHBN%(const char *bindir, const char *cvmdir, 
	  const char *infile, const char *outfile,
          int mode);

/* Execute vx_lite_cvmhibbn as a child process */
int runVXLite%%CVMHBN%(const char *bindir, const char *cvmdir, 
	      const char *infile, const char *outfile,
	      int mode);

#endif

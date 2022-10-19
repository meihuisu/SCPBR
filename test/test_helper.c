/** 
   test_helper.c
**/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "unittest_defs.h"
#include "test_helper.h"

int debug_mode=0;
scpbr_surf_t test_surfs[100];
int test_surfs_cnt=0;

double init_preset_ucvm_surface(scpbr_surf_t *surfs) {
  char fname[100];
  char line[100];
  char key[50];
  char value[50];
  FILE *fp;

  strcpy(fname,"./inputs/scpbr_ucvm_surf.dat");
  fp = fopen(fname, "r");
  if (fp == NULL) { return(1); }

  // process one line at a time
  int i=0;
  while (fgets(line, sizeof(line), fp) != NULL) {
    if (line[0] != '#' && line[0] != ' ' && line[0] != '\n') {
       if(sscanf(line, "%lf,%lf,%lf", &(surfs[i].longitude), &(surfs[i].latitude), &(surfs[i].surf))!=3) 
         continue;
       i++;
    }
  }
  test_surfs_cnt=i;
  return i;
}

double get_preset_ucvm_surface(double y, double x) {
  for(int i=0; i<test_surfs_cnt; i++) {
   if( test_surfs[i].longitude == y && test_surfs[i].latitude == x) {
     return test_surfs[i].surf;
   }
  }
  return 0;
}

// get model specific test points and expected values
int get_depth_test_point(scpbr_point_t *pt, scpbr_properties_t *expect) {

  char fname[100];
  char line[100];
  char key[50];
  char value[50];
  FILE *fp;

  strcpy(fname,"./inputs/scpbr_depth_test_point.dat");
  fp = fopen(fname, "r");
  if (fp == NULL) { return(1); }

  // process one line at a time
  while (fgets(line, sizeof(line), fp) != NULL) {
    if (line[0] != '#' && line[0] != ' ' && line[0] != '\n') {
       sscanf(line, "%s = %s", key, value);

       // Which variable are we editing?
       if (strcmp(key, "longitude") == 0) {
         pt->longitude = atof(value);
         continue;
       }
       if (strcmp(key, "latitude") == 0) {
         pt->latitude = atof(value);
         continue;
       }
       if (strcmp(key, "depth") == 0) {
         pt->depth = atof(value);
         continue;
       }
       if (strcmp(key, "vs") == 0) {
         expect->vs = atof(value);
         continue;
       }
       if (strcmp(key, "vp") == 0) {
         expect->vp = atof(value);
         continue;
       }
       if (strcmp(key, "rho") == 0) {
         expect->rho = atof(value);
         continue;
       }
    }
  }
  return 0;
}

// get model specific test points and expected values
int get_elev_test_point(scpbr_point_t *pt, scpbr_properties_t *expect, double *pt_elevation, double *pt_surf) {

  char fname[100];
  char line[100];
  char key[50];
  char value[50];
  FILE *fp;

  strcpy(fname,"./inputs/scpbr_elev_test_point.dat");
  fp = fopen(fname, "r");
  if (fp == NULL) { return(1); }

  // process one line at a time
  while (fgets(line, sizeof(line), fp) != NULL) {
    if (line[0] != '#' && line[0] != ' ' && line[0] != '\n') {
       sscanf(line, "%s = %s", key, value);

       // Which variable are we editing?
       if (strcmp(key, "longitude") == 0) {
         pt->longitude = atof(value);
         continue;
       }
       if (strcmp(key, "latitude") == 0) {
         pt->latitude = atof(value);
         continue;
       }
       if (strcmp(key, "pt_elevation") == 0) {
         *pt_elevation = atof(value);
         continue;
       }
       if (strcmp(key, "pt_surf") == 0) {
         *pt_surf = atof(value);
         continue;
       }
       if (strcmp(key, "vs") == 0) {
         expect->vs = atof(value);
         continue;
       }
       if (strcmp(key, "vp") == 0) {
         expect->vp = atof(value);
         continue;
       }
       if (strcmp(key, "rho") == 0) {
         expect->rho = atof(value);
         continue;
       }
    }
  }

  return 0;
}


/*************************************************************************/
int runSCPBR(const char *bindir, const char *cvmdir, 
	  const char *infile, const char *outfile, int mode)
{
  scpbr_point_t pt;
  scpbr_properties_t ret;

  FILE *infp, *outfp;
  char line[1000];

  char *envstr=getenv("UCVM_INSTALL_PATH");
  if(envstr != NULL) {
    if (test_assert_int(model_init(envstr, "scpbr"), 0) != 0) {
      return(1);
    }
  } else if (test_assert_int(model_init("..", "scpbr"), 0) != 0) {
    return(1);
  }

  int zmode = UCVM_COORD_GEO_ELEV;
  switch (mode) {
    case MODE_ELEVATION:
      zmode = UCVM_COORD_GEO_ELEV;
      break;
    case MODE_DEPTH:
      zmode = UCVM_COORD_GEO_DEPTH;
      break;
    case MODE_NONE:
      break; // default
  }

  if (test_assert_int(model_setparam(0, UCVM_PARAM_QUERY_MODE, zmode), 0) != 0) {
      return(1);
  }

  /* open infile, outfile */
  infp = fopen(infile, "r");
  if (infp == NULL) {
    printf("FAIL: cannot open %s\n", infile);
    return(1);
  }
  outfp = fopen(outfile, "w");
  if (outfp == NULL) {
    printf("FAIL: cannot open %s\n", outfile);
    return(1);
  }

/* process one term at a time */
  while(fgets(line, 1000, infp) != NULL) {
    if(line[0] == '#') continue; // a comment 
    if (sscanf(line,"%lf %lf %lf",
         &pt.longitude,&pt.latitude,&pt.depth) == 3) {
      if (test_assert_int(model_query(&pt, &ret, 1), 0) == 0) {
         fprintf(outfp,"%lf %lf %lf\n",ret.vs, ret.vp, ret.rho);
      }
    }
  }
  fclose(infp);
  fclose(outfp);
                
  if (test_assert_int(model_finalize(),0) != 0) {
      return(1);
  }

  return(0);
}

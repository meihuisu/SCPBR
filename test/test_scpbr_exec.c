/**
   test_scpbr_exec.c

   uses scpbr's model api,
       model_init, model_query, model_finalize
**/

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <getopt.h>
#include <assert.h>
#include "scpbr.h"
#include "unittest_defs.h"
#include "test_helper.h"
#include "test_scpbr_exec.h"

int test_setup()
{
  printf("Test: model_init() and model_finalize()\n");

  char *envstr=getenv("UCVM_INSTALL_PATH");
  if(envstr != NULL) {
    if (test_assert_int(model_init(envstr, "scpbr"), 0) != 0) {
      return(1);
    }
  } else if (test_assert_int(model_init("..", "scpbr"), 0) != 0) {
    return(1);
  }

  if (test_assert_int(model_finalize(), 0) != 0) {
    return(1);
  }

  printf("PASS\n");
  return(0);
}

int test_query_by_depth()
{
  printf("Test: model_query() by depth\n");

  scpbr_point_t pt;
  scpbr_properties_t expect;
  scpbr_properties_t ret;

// Initialize the model, try to use Use UCVM_INSTALL_PATH
  char *envstr=getenv("UCVM_INSTALL_PATH");
  if(envstr != NULL) {
    if (test_assert_int(model_init(envstr, "scpbr"), 0) != 0) {
      return(1);
    }
  } else if (test_assert_int(model_init("..", "scpbr"), 0) != 0) {
    return(1);
  }

  int zmode = UCVM_COORD_GEO_DEPTH;
  if( get_depth_test_point(&pt,&expect) != 0) {
      return(1);
  }

  //fprintf(stderr,"depth test points (%lf,%lf,%lf)\n",pt.longitude,pt.latitude,pt.depth);
  //fprintf(stderr,"depth result expected (%lf,%lf,%lf)\n",expect.vp,expect.vs,expect.rho);
 
  if (test_assert_int(model_query(&pt, &ret, 1), 0) != 0) {
      return(1);
  }

  // Close the model.
  assert(model_finalize() == 0);

  if ( test_assert_double(ret.vs, expect.vs) ||
       test_assert_double(ret.vp, expect.vp) ||
       test_assert_double(ret.rho, expect.rho) ) {
     printf("FAIL\n");
     return(1);
     } else {
       printf("PASS\n");
       return(0);
  }

}

int test_query_points_by_depth()
{
  printf("Test: model_query() points by depth\n");

  FILE  *infp, *outfp;
  scpbr_point_t pt;
  scpbr_properties_t ret;

  char infile[1280];
  char outfile[1280];
  char reffile[1280];
  char currentdir[1000];

  /* Save current directory */
  getcwd(currentdir, 1000);

  sprintf(infile, "%s/%s", currentdir, "./inputs/test-depth.in");
  sprintf(outfile, "%s/%s", currentdir, "test-depth.out");
  sprintf(reffile, "%s/%s", currentdir, "./ref/test-depth.ref");

  if (test_assert_file_exist(infile) != 0) {
    return _failure("filed not found");
  }

  infp = fopen(infile, "r");
  if (infp == NULL) {
    return _failure("input file not found");
  }
  outfp = fopen(outfile, "w");
  if (outfp == NULL) {
    return _failure("output file can not be open");
  }

  char *envstr=getenv("UCVM_INSTALL_PATH");
  if(envstr != NULL) {
    if (test_assert_int(model_init(envstr, "scpbr"), 0) != 0) {
      return _failure("model_init failed");
    }
  } else if (test_assert_int(model_init("..", "scpbr"), 0) != 0) {
    return _failure("model_init failed");
  }

  int zmode = UCVM_COORD_GEO_DEPTH;

/* process one term at a time */
  char line[1001];
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

  /* Perform diff btw outfile and ref */
  if (test_assert_file(outfile, reffile) != 0) {
    printf("unmatched result\n");
    printf("%s\n",outfile);
    printf("%s\n",reffile);
    return _failure("diff file");
  }

  // Close the model.
  if(model_finalize() != 0) {
      return _failure("model_finalize failed");
  }
  unlink(outfile);

  return _success();
}


int suite_scpbr_exec(const char *xmldir)
{
  suite_t suite;
  char logfile[256];
  FILE *lf = NULL;

  /* Setup test suite */
  strcpy(suite.suite_name, "suite_scpbr_exec");

  suite.num_tests = 3;
  suite.tests = malloc(suite.num_tests * sizeof(test_t));
  if (suite.tests == NULL) {
    fprintf(stderr, "Failed to alloc test structure\n");
    return(1);
  }
  test_get_time(&suite.exec_time);

  /* Setup test cases */
  strcpy(suite.tests[0].test_name, "test_setup");
  suite.tests[0].test_func = &test_setup;
  suite.tests[0].elapsed_time = 0.0;

  strcpy(suite.tests[1].test_name, "test_query_by_depth");
  suite.tests[1].test_func = &test_query_by_depth;
  suite.tests[1].elapsed_time = 0.0;

  strcpy(suite.tests[2].test_name, "test_query_points_by_depth");
  suite.tests[2].test_func = &test_query_points_by_depth;
  suite.tests[2].elapsed_time = 0.0;

  if (test_run_suite(&suite) != 0) {
    fprintf(stderr, "Failed to execute tests\n");
    return(1);
  }

  if (xmldir != NULL) {
    sprintf(logfile, "%s/%s.xml", xmldir, suite.suite_name);
    lf = init_log(logfile);
    if (lf == NULL) {
      fprintf(stderr, "Failed to initialize logfile\n");
      return(1);
    }
    
    if (write_log(lf, &suite) != 0) {
      fprintf(stderr, "Failed to write test log\n");
      return(1);
    }

    close_log(lf);
  }

  free(suite.tests);

  return 0;
}

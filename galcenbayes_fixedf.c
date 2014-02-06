/*
 * galcenbayes_fixedf.c
 * Perform a Bayesian analysis for given survey parameters, for the given
 *  magnetar fraction, as described in Chennamangalam & Lorimer (2014). In
 *  addition to lognormal luminosity funciton, also performs analysis for power
 *  law.
 *
 * Usage: galcenbayes_fixedf smin nu beta N f
 *  smin - flux density limit, in mJy
 *  nu - observing frequency, in GHz
 *  beta - power law exponent
 *  N - maximum number of pulsars (upper limit of prior on N)
 *  f - magnetar fraction
 *  
 * Example: galcenbayes_fixedf 0.050 4.85 -0.8 100000 0.010 > survey.nvsf
 *  Use plotnvsf.py to plot the contents of survey.nvsf.
 *
 * Created by Duncan Lorimer
 * Modified by Jayanth Chennamangalam
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

float erfcc(float x)
{
	float t,z,ans;

	z=fabs(x);
	t=1.0/(1.0+0.5*z);
	ans=t*exp(-z*z-1.26551223+t*(1.00002368+t*(0.37409196+t*(0.09678418+
		t*(-0.18628806+t*(0.27886807+t*(-1.13520398+t*(1.48851587+
		t*(-0.82215223+t*0.17087277)))))))));
	return x >= 0.0 ? ans : 2.0-ans;
}
#define LMIN    0.1     /* mJy kpc^2 */
#define NMIN    1       /* equal to n */
#define NMAX    100000
int main(int argc, char **argv) 
{
  int N=0,upperlimit=0,lowerlimit=0,median=0,NMax=NMAX,mode=0;
  float theta=0.0,ldet=0.0,smin=0.0,nu=0.0,dgc=0.0,mu=0.0,sigma=0.0,alpha=0.0,amean=0.0,asig=0.0,dalpha=0.0,mean=0.0,max=0.0;
  float prob[NMAX]={0.0},cdf[NMAX]={0.0},exponent=0.0,sum=0.0;
  int upperlimit_pl=0,lowerlimit_pl=0,median_pl=0,mode_pl=0;
  float theta_pl=0.0,beta=0.0,gamma=0.0,mean_pl=0.0,max_pl=0.0;
  float prob_pl[NMAX]={0.0},cdf_pl[NMAX]={0.0};
  double sum_pl=0.0,f=0.0,df=0.0;

  mu=-1.1;
  sigma=0.9;
  amean=-1.41;
  asig=0.96;
  dgc=8.25;
  dalpha=0.1;
  beta=-0.8;
  f=0.01;
  df=0.1;   /* for easy comparison with prior on f */

  if (argc<6)
  {
    puts("Usage: galcenbayes_fixedf smin nu beta N f");
    exit(0);
  }
  smin=atof(argv[1]);
  nu=atof(argv[2]);
  beta=atof(argv[3]);
  NMax=atoi(argv[4]);
  f=atof(argv[5]);

  sum=0.0;
  sum_pl=0.0;
  for (N=NMIN; N<NMax; N++)
  {
    prob[N]=0.0;
    prob_pl[N]=0.0;
    for (alpha=amean-8.0; alpha<=amean+8.0; alpha+=dalpha)
    {
      ldet=smin*pow(1.4/nu,alpha)*dgc*dgc;
      exponent=pow(alpha-amean,2.0)/2.0/asig/asig;
      /* lognormal */
      theta=0.5*erfcc((log10(ldet)-mu)/sqrt(2)/sigma);
      if (theta > 1.0)  /* sanity check */
      {
        fprintf(stderr, "ERROR: theta = %f > 1!\n", theta);
        return -1;
      }
      gamma=0.5*erfcc((log10(smin*dgc*dgc)-mu)/sqrt(2)/sigma);
      prob[N]+=pow(1.0-theta,(float)N*(1.0-f))*exp(-1.0*exponent)*((float)N*f)*gamma*powf(1-gamma,((float)N*f)-1)*dalpha*df;
      /* power law */
      if (ldet > LMIN)
      {
        theta_pl=powf(ldet/LMIN, beta);
      } else /* pulsar will be detected */
      {
        theta_pl=1.0; 
      }
      if (theta_pl > 1.0)   /* sanity check */
      {
        fprintf(stderr, "ERROR: theta_pl = %f > 1!\n", theta_pl);
        return -1;
      }
      prob_pl[N]+=powf(1.0-theta_pl,(float)N*(1.0-f))*exp(-1.0*exponent)*((float)N*f)*gamma*powf(1-gamma,((float)N*f)-1)*dalpha*df;
    }
    sum+=prob[N];
    cdf[N]=sum;
    sum_pl+=prob_pl[N];
    cdf_pl[N]=sum_pl;
  }
  for (N=NMIN; N<NMax; N++) {
    //printf("%d %f %f %f %f\n",N,prob[N],cdf[N]/sum,prob_pl[N],cdf_pl[N]/sum_pl);
    if (cdf[N]/sum<0.01) lowerlimit=N;
    if (cdf[N]/sum<0.5) median=N;
    if (cdf[N]/sum<0.99) upperlimit=N;
    if (cdf_pl[N]/sum_pl<0.01) lowerlimit_pl=N;
    if (cdf_pl[N]/sum_pl<0.5) median_pl=N;
    if (cdf_pl[N]/sum_pl<0.99) upperlimit_pl=N;
  }
  for (N=NMIN; N<NMax; N++) {
    prob[N]=prob[N]/sum;
    mean+=(N*prob[N]);
    if (prob[N] > max) {
        max=prob[N];
        mode=N;
    }
    prob_pl[N]=prob_pl[N]/sum_pl;
    mean_pl+=(N*prob_pl[N]);
    if (prob_pl[N] > max_pl) {
        max_pl=prob_pl[N];
        mode_pl=N;
    }
  }
  printf("%f %g %d %d %d %d\n", f, mean, mode, lowerlimit, median, upperlimit);
  fprintf(stderr,"Lognormal:\n");
  fprintf(stderr,"Mean of N                    = %g\n",mean);
  fprintf(stderr,"Mode of N                    = %d\n",mode);
  fprintf(stderr,"99 percent lower bound for N = %d\n",lowerlimit);
  fprintf(stderr,"Median for N                 = %d\n",median);
  fprintf(stderr,"99 percent upper bound for N = %d\n",upperlimit);
  fprintf(stderr,"Power law:\n");
  fprintf(stderr,"Mean of N                    = %g\n",mean_pl);
  fprintf(stderr,"Mode of N                    = %d\n",mode_pl);
  fprintf(stderr,"99 percent lower bound for N = %d\n",lowerlimit_pl);
  fprintf(stderr,"Median for N                 = %d\n",median_pl);
  fprintf(stderr,"99 percent upper bound for N = %d\n",upperlimit_pl);
}


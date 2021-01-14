import ctypes
import numpy as np

t0 = 0.0
t1 = 10.0
nintervals = 20.0

hllDll = ctypes.WinDLL("B://Downloads//wetransfer-cf71fd//deliver_1//Debug//vehicle.dll")
vehicle = hllDll.Vehicle(True, True, t0, const double t1, const double nintervals,
  const double tol_in, const double tol_out,
  const double tol_dphi, const double tol_phi,
  const int nn, const double krr_explicit, const double crr_explicit,
  const char* xml1_path, const char* xml2_path,
  const int npoints, const double vx,
  const double *x_p_l_n, const double *y_p_l_n, const double *z_p_l_n,
  const double *x_p_l_n1, const double *y_p_l_n1, const double *z_p_l_n1,
  const double *x_p_r_n, const double *y_p_r_n, const double *z_p_r_n,
  const double *x_p_r_n1, const double *y_p_r_n1, const double *z_p_r_n1,
  const double *x_v_l_n, const double *y_v_l_n, const double *z_v_l_n,
  const double *x_v_l_n1, const double *y_v_l_n1, const double *z_v_l_n1,
  const double *x_v_r_n, const double *y_v_r_n, const double *z_v_r_n,
  const double *x_v_r_n1, const double *y_v_r_n1, const double *z_v_r_n1,
  double *cp_positions, double *cp_velocities, double *cp_forces);)
#ifndef VEHICLE_H_INCLUDED
#define VEHICLE_H_INCLUDED

#ifdef MATHLIBRARY_EXPORTS
#define MATHLIBRARY_API __declspec(dllexport)
#else
#define MATHLIBRARY_API __declspec(dllimport)
#endif

extern "C" MATHLIBRARY_API void Vehicle(
  const bool cosim_converge, const bool is_first_time,
  const double t0, const double t1, const double nintervals,
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
  double *cp_positions, double *cp_velocities, double *cp_forces);

// cosim_converge : cosimulation converge
// is_first_time : is the first you are calling vehicle
// t0 : previous cosimulation time
// t1 : current  cosimulation time
// nintervals : number of intervals for vehicle solution, thus time-step = (t1 - t0)/nintervals
// tol_in : velocity tolerance (1e-3 or lower)
// tol_out : residual tolerance (1e-2 or lower), must be tol_in < tol_out
// tol_dphi : tolerance for dphi_dt (1e-3 or lower)
// tol_phi : tolerance for phi (1e-2 or lower)
// nn : for crrs, krrs (10,100,1000,...), if nn = 0 then krrs = crrs = 0
// krr_explicit : explicit value for all krrs, works when nn = -1
// crr_explicit : explicit value for all crrs, works when nn = -1
// xml1_path : path for xml1
// xml2_path : path for xml2
// npoints : number of interpolation points for the position-velocity splines
// vx : the constant forward velocity of all bodies

// x_p_l_n  : x coords of interpolation points, for position spline, left rail, spline at n
// y_p_l_n  : y coords of interpolation points, for position spline, left rail, spline at n
// z_p_l_n  : z coords of interpolation points, for position spline, left rail, spline at n
// x_p_l_n1 : x coords of interpolation points, for position spline, left rail, spline at n + 1
// y_p_l_n1 : y coords of interpolation points, for position spline, left rail, spline at n + 1
// z_p_l_n1 : z coords of interpolation points, for position spline, left rail, spline at n + 1

// x_p_r_n  : x coords of interpolation points, for position spline, right rail, spline at n
// y_p_r_n  : y coords of interpolation points, for position spline, right rail, spline at n
// z_p_r_n  : z coords of interpolation points, for position spline, right rail, spline at n
// x_p_r_n1 : x coords of interpolation points, for position spline, right rail, spline at n + 1
// y_p_r_n1 : y coords of interpolation points, for position spline, right rail, spline at n + 1
// z_p_r_n1 : z coords of interpolation points, for position spline, right rail, spline at n + 1

// x_v_l_n  : x coords of interpolation points, for velocity spline, left rail, spline at n
// y_v_l_n  : y coords of interpolation points, for velocity spline, left rail, spline at n
// z_v_l_n  : z coords of interpolation points, for velocity spline, left rail, spline at n
// x_v_l_n1 : x coords of interpolation points, for velocity spline, left rail, spline at n + 1
// y_v_l_n1 : y coords of interpolation points, for velocity spline, left rail, spline at n + 1
// z_v_l_n1 : z coords of interpolation points, for velocity spline, left rail, spline at n + 1

// x_v_r_n  : x coords of interpolation points, for velocity spline, right rail, spline at n
// y_v_r_n  : y coords of interpolation points, for velocity spline, right rail, spline at n
// z_v_r_n  : z coords of interpolation points, for velocity spline, right rail, spline at n
// x_v_r_n1 : x coords of interpolation points, for velocity spline, right rail, spline at n + 1
// y_v_r_n1 : y coords of interpolation points, for velocity spline, right rail, spline at n + 1
// z_v_r_n1 : z coords of interpolation points, for velocity spline, right rail, spline at n + 1

// cp_positions : xyz coords of the contact points (cp one per wheel, thus two per wheelset)
    // example for two wheelsets: cp_positions = { x_first_wheelset_left_wheel,
    //                                             y_first_wheelset_left_wheel,
    //                                             z_first_wheelset_left_wheel,
    //                                             x_first_wheelset_right_wheel,
    //                                             y_first_wheelset_right_wheel,
    //                                             z_first_wheelset_right_wheel,
    //                                             x_second_wheelset_left_wheel,
    //                                             y_second_wheelset_left_wheel,
    //                                             z_second_wheelset_left_wheel,
    //                                             x_second_wheelset_right_wheel,
    //                                             y_second_wheelset_right_wheel,
    //                                             z_second_wheelset_right_wheel }
// cp_velocities : xyz velocity components of the contact points
    // example for two wheelsets: cp_velocities = "see cp_positions"
// cp_forces : xyz force components at the contact points
    // example for two wheelsets: cp_forces = "see cp_positions"










#endif // VEHICLE_H_INCLUDED


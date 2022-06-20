& input_ml 
debug = .false. 
ml_type =     0
train_only = .false. 
write_design_matrix = .false. 
write_inn = .false. 
pblas_driver = .false. 
!-------------------Function Fit form-----------------------!
snap_order =     1
snap_type_quadratic =     1
order_nlinear =     2
polyc_n_poly =     2
polyc_n_hermite =     2
!-----------------Algo Fit / regularization form--------------!
snap_fit_type =     0
snap_regularization_type =     0
snap_class_constraints = "02"
lambda_krr = -0.100000000000000D+01
min_lambda_krr =  0.100000000000000D-09
max_lambda_krr =  0.100000000000000D+11
svd_rcond = -0.100000000000000D+01
n_values_lambda_krr =     21
!---------------------------Kernel / -------------------------!
write_kernel_matrix = .false. 
kernel_type =      4
np_kernel_ref =    400
np_kernel_full =    800
np_omega =      4
kernel_dump =      1
classes_for_kernel = " 01 02"
length_kse =  0.100000000000000D+01
sigma_kse =  0.100000000000000D+01
length_kernel =  0.100000000000000D+01
sigma_kernel =  0.100000000000000D+01
kernel_power =  0.200000000000000D+01
power_mcd =  0.333330005407333D+00
!----------------------DB and Elements ------------------------!
db_file = "db_model.in"
db_path = "DB/"
build_subdata = .false. 
selection_type =     3
seed =        11
weighted = .false. 
weighted_auto = .false. 
weighted_3ch = .false. 
fix_no_of_elements =     1
iread_energy =     2
chemical_elements = "Fe"
chemical_elements_invisible = ""
weight_per_element = "1.d0"
weight_per_element_3ch = "1.d0"
ref_energy_per_element = "0.d0"
n_pca =     3
classes_for_mcd = " 01 02"
classes_for_kernel = " 01 02"
sign_stress =  0.100000000000000D+01
sign_stress_big_box =  0.100000000000000D+01
!------------------------Descriptors------------------------!
descriptor_type =      1
write_desc = .false. 
write_desc_dump = .false. 
read_desc_dump = .false. 
desc_forces = .true. 
val_desc_max =  0.100000000000000D+01
r_cut =  0.500000000000000D+01
!---G2----
n_g2_eta =      3
n_g2_rs =      1
eta_max_g2 =  0.800000000000000D+00
!---G3----
n_g3_eta =      3
n_g3_zeta =      2
n_g3_lambda =      2
!---BehPar----
strict_behler = .false. 
!---AFS----
afs_type =      1
n_rbf =      4
n_rbf_afs =      4
n_rbf_so3 =      4
n_cheb =      5
!---MTP----
mtp_poly_min =      2
mtp_poly_max =      5
!---SO3/BS03----
l_max =      4
radial_pow_so4 =      1
lbso3_diag = .true. 
!---SO4/BS04----
j_max =    1.5000000000
inv_r0_input =  0.993633802276324D+00
lbso4_diag = .false. 
!---SOAP----
alpha_soap =    2.0000000000
n_soap =      2
r_cut_width_soap =  0.500000000000000D+00
lsoap_diag = .false. 
lsoap_norm = .true. 
lsoap_lnorm = .true. 
nspecies_soap =      1
lsoap = .false. 
lsoap_fcut_wes = .false. 
!---BODY----
body_D_max(1) =      1
body_D_max(2) =      2
body_D_max(3) =      3
body_D_max(4) =      4
body_D_max(5) =      5
l_body_order(1) = .true. 
l_body_order(2) = .true. 
l_body_order(3) = .true. 
l_body_order(4) = .true. 
l_body_order(5) = .false. 
bond_dist_transform =      3
bond_beta =  0.200000000000000D+01
bond_dist_ann =  0.100000000000000D+01
!----MiLaDy----
rmat_dim =     20
power_line =  0.200000000000000D+01
power_coeff_renorm =  0.333000000000000D+00
!----ACD----
acd = .false. 
acd_fcut = .false. 
acd_weighted = .false. 
kappa_acd =      1
acd_threshold =  0.100000000000000D+01
alpha_acd =  0.100000000000000D+01
temp_ini =  0.100000000000000D+01
ksi_ini =  0.100000000000000D+01
tau =  0.950000000000000D+00
mc_step =      1000
!----mag----
r_cut_magnetic =  0.530000019073486D+01
magnetic_sld_j_dim =     10
magnetic_sld_s2_dim =     10
magnetic_sld_s4_dim =     10
!----------------------Genetical algo-----------------------!
optimize_weights = .false. 
optimize_weights_L1 = .false. 
optimize_weights_L2 = .false. 
optimize_weights_Le = .false. 
optimize_ga_population =     40
class_no_optimize_weights = ""
max_iter_optimize_weights =     40
factor_energy_error =  0.100000000000000D+01
factor_force_error =  0.100000000000000D+01
factor_stress_error =  0.100000000000000D+01
!--------------------------LBFGS----------------------------!
lbfgs_m_hess =     40
lbfgs_max_steps =  20000
lbfgs_print(1) =    100
lbfgs_print(2) =      0
lbfgs_eps =  0.100000000000000D-01
lbfgs_gtol =  0.400000000000000D+00
lbfgs_xtol =  0.100000000000000D-15
!-----------------------OLD UNUSED----------------------------!
iread_ml =      0
isave_ml =      0
toy_model = .false. 
kcross = .false. 
search_hyp = .false. 
sparsification = .false. 
sparsification_by_acd = .false. 
sparsification_by_entropy = .false. 
sparsification_by_cur = .false. 
marginal_likelihood = .false. 
krr_error = .false. 
target_type =         1
force_comp =         1
n_kcross =         0
dim_data =       100
nd_fingerprint =         3
n_frac =    0.0000000000
max_data =      0
rescale = .false. 
s_max_r =  0.100000000000000D+02
s_max_i =  0.000000000000000D+00
s_min_r =  0.000000000000000D+00
s_min_i =  0.100000000000000D+01
kelem =      0
ns_data =    100
i_begin =      0
pref = "00"
& end 

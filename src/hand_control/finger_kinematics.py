import numpy as np
import sympy as sym

# ------------------- Calculations of Tendon Lengths at single joint ------------------- #
# TODO: Add your own functions here to calculate the tendon lengths for each joint


def gen_tendon_length(theta, R, R_1, alpha_1, X_1, R_2, alpha_2, X_2):
    '''Generate tendon length through a single joint'''
    # R = radius of the rolling cylinders
    # R_1, alpha_1, X_1 = cylinder coordinates of the point T1 in system 1
    # R_2, alpha_2, X_2 = cylinder coordinates of the point T2 in system 2

    r_1_T1 = sym.Matrix([X_1, -R_1*sym.sin(alpha_1), R_1*sym.cos(alpha_1)])
    r_0_2 = sym.Matrix([0, 0, 2*R])
    r_2_T2 = sym.Matrix([X_2, -R_2*sym.sin(alpha_2), R_2*sym.cos(alpha_2)])

    C_10 = gen_elt_rot_matrix_about_x(theta/2)
    C_12 = gen_elt_rot_matrix_about_x(theta)

    # this is with reference to frame 1 (left subscript)
    r_T1_T2 = -r_1_T1 + (C_10 @ r_0_2) + (C_12 @ r_2_T2)

    return r_T1_T2.norm()


def gen_elt_rot_matrix_about_x(theta):
    '''Generate an elementary rotation matrix for given angle and axis'''
    return sym.Matrix([[1, 0, 0],
                       [0, sym.cos(theta), -sym.sin(theta)],
                       [0, sym.sin(theta), sym.cos(theta)]])

# ------------------- Calculations of Tendon Lengths for MCPJ Abduction/Adduction ------------------- #


def tendonlength_left_frontal_MCPJ(theta):
    '''Isymut: joint angle of MCP joint in rad
       Output: total normal lengths of left frontal tendon through MCPJ'''

    return gen_tendon_length(theta, 9, 9, 26.4149013 * 2*sym.pi/360, 0, 9, 133.713947 * 2*sym.pi/360, 0)


def tendonlength_right_frontal_MCPJ(theta):
    '''Isymut: joint angle of MCP joint in rad
       Output: total normal lengths of right frontal tendon through MCPJ'''
    return gen_tendon_length(theta, 9, 9, -26.4149013 * 2*sym.pi/360, 0, 9, -133.713947 * 2*sym.pi/360, 0)

# ------------------- Calculations of Tendon Lengths for MCPJ Flexion/Extension ------------------- #


def tendonlength_flexor_MCPJ(theta):
    '''Isymut: joint angle of MCP joint in rad
       Output: total normal lengths of flexor tendon through MCPJ'''

    return gen_tendon_length(theta, 9, 9, 63.2286461 * 2*sym.pi/360, -1, 9, 100.9062206 * 2*sym.pi/360, -1)


def tendonlength_extensor_MCPJ(theta):
    '''Isymut: joint angle of MCP joint in rad
       Output: total normal lengths of extensor tendon through MCPJ'''
    return gen_tendon_length(theta, 3, 3, -23.6679915 * 2*sym.pi/360, -1, 3, -150 * 2*sym.pi/360, -1)

# ------------------- Calculations of Tendon Lengths for PIPJ Flexion/Extension ------------------- #


def tendonlength_flexor_PIPJ(theta):
    '''Isymut: joint angle of PIP joint in rad
       Output: total normal lengths of flexor tendon through PIPJ'''

    # r, alpha,x
    return gen_tendon_length(theta, 6, 6, 111.0330855 * 2*sym.pi/360, -1, 6, 93.6938127 * 2*sym.pi/360, -1)


def tendonlength_extensor_PIPJ(theta):
    '''Isymut: joint angle of PIP joint in rad
       Output: total normal lengths of extensor tendon through PIPJ'''
    return gen_tendon_length(theta, 3, 3, -30 * 2*sym.pi/360, -1, 3, -150 * 2*sym.pi/360, -1)

# --------- Calculations of Tendon Lengths for DIPJ Flexion/Extension (ONLY FOR THUMB) ------------ #


def tendonlength_flexor_DIPJ(theta):
    '''Isymut: joint angle of DIP joint in rad
       Output: total normal lengths of flexor tendon through DIPJ'''

    # r, alpha,x
    return gen_tendon_length(theta, 4.5, 4.5, 92.4388735 * 2*sym.pi/360, -1, 4.5, 105.3006332 * 2*sym.pi/360, -1)


def tendonlength_extensor_DIPJ(theta):
    '''Isymut: joint angle of DIP joint in rad
       Output: total normal lengths of extensor tendon through DIPJ'''
    return gen_tendon_length(theta, 3, 3, -29.9999156 * 2*sym.pi/360, 1, 3, -150 * 2*sym.pi/360, 1)

# ------------------- Calculations of Tendon Lengths for all joints ------------------- #
# TODO: Add your own functions here to calculate the tendon lengths for all joints and for each finger (if needed)


def pose2tendon_finger(theta_MCPJ_frontal, theta_MCPJ_saggital, theta_PIPJ):
    '''Isymut: controllable joint angles
       Output: array of tendon lengths for given joint angles'''
    output = [tendonlength_left_frontal_MCPJ(theta_MCPJ_frontal) + tendonlength_flexor_MCPJ(theta_MCPJ_saggital),
              tendonlength_right_frontal_MCPJ(
        theta_MCPJ_frontal) + tendonlength_flexor_MCPJ(theta_MCPJ_saggital),
        tendonlength_left_frontal_MCPJ(
        theta_MCPJ_frontal) + tendonlength_extensor_MCPJ(theta_MCPJ_saggital),
        tendonlength_right_frontal_MCPJ(
        theta_MCPJ_frontal) + tendonlength_extensor_MCPJ(theta_MCPJ_saggital),
        tendonlength_flexor_PIPJ(theta_PIPJ),
        tendonlength_extensor_PIPJ(theta_PIPJ)]
    return sym.Matrix(output)


def pose2tendon_thumb(theta_pin_prox, theta_pin_dist, theta_PIPJ, theta_DIPJ):
    '''Isymut: controllable joint angles
       Output: array of tendon lengths for given joint angles'''
    pin_prox_rad = 7.5
    pin_dist_rad = 6.5
    output = [-pin_prox_rad * theta_pin_prox,
              pin_prox_rad * theta_pin_prox,
              pin_dist_rad * theta_pin_dist,
              -pin_dist_rad * theta_pin_dist,
              tendonlength_flexor_PIPJ(theta_PIPJ),
              tendonlength_extensor_PIPJ(theta_PIPJ),
              tendonlength_flexor_DIPJ(theta_DIPJ),
              tendonlength_extensor_DIPJ(theta_DIPJ)]
    return sym.Matrix(output)


def pose2tendon_wrist(theta_wrist):
    '''Isymut: controllable joint angles
       Output: array of tendon lengths for given joint angles'''
    output = [8 * theta_wrist]
    return sym.Matrix(output)

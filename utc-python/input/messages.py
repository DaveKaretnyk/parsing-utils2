# Copyright (c) 2012-2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.

# messages shown in modal dialog that need to be clicked away when Stem acquisition is not allowed
error_acquisition_for_c1_a1_not_allowed = r"C1/A1 is not available. "
error_acquisition_for_a2_b2_not_allowed = r"A2/B2 is not available. "

suggestion_acquisition_not_allowed = r"Make sure HT is on, FEG is operational, column valves are open, " \
                                     "and nP Probe STEM mode with three condenser lenses on is active."

# messages shown in modal dialog that need to be clicked away when another STEM acquisition is busy
error_stem_acquisition_active = r"Can not start a new STEM acquisition !"

suggestion_stem_acquisition_active = r"Another STEM acquisition is still active. Please stop first."

# messages shown in modal dialog that need to be clicked away when system is not in STEM mode
error_not_in_stem = r"Microscope is not in STEM mode !"

suggestion_not_in_stem = r"Please switch to STEM mode and make sure you have a good aligned beam."

# algorithm messages
not_converged_error = r"No solution found. Try to improve starting conditions or check calibrations."

not_converged_error_too_many_singular_values = r"No solution found. Try to improve starting conditions or check calibrations."

solution_out_of_range = r"One or more of the found solutions for C1 and A1 is bigger than {0} nm; " \
                        r"Please manually improve focus/stigmation or decrease magnification." \
                        r"solutions: C1={1} |A1|={2}. deviation factor={3} dC1={4}"

focus_solution_out_of_range = r"The found solution for C1 is bigger than {0} nm; " \
                        r"Please manually improve focus or decrease magnification." \
                        r"solution: C1={1}. deviation factor={2} dC1={3}"

stigmator_solution_out_of_range = r"The found solution for A1 is bigger than {0} nm; " \
                        r"Please manually improve stigmation or decrease magnification." \
                        r"solution: |A1|={1}. deviation factor={2} dC1={3}"

stigmator_out_of_range = "Setting stigmator to requested values failed; \nMake sure coarse stigmator is set properly."

invalid_stigmator_values = "Error, trying to set condenser stigmator to invalid values"

stigmator_failed = "Error while setting stigmator; \nMake sure server is running and coarse stigmator is set properly."

stigmator_3fold_out_of_range = "Setting condenser 3fold stigmator to requested values failed; \nMake sure coarse stigmator is set " \
                            "properly."

invalid_stigmator_3fold_values = "Error, trying to set condenser 3fold stigmator to invalid values"

stigmator_3fold_failed = "Error while setting condenser 3fold stigmator; \nMake sure server is running and coarse " \
                         "stigmator is set properly."

stigmator_coma_out_of_range = "Setting coma stigmator to requested values failed; \nMake sure coarse " \
                           "stigmator is set properly."

invalid_stigmator_coma_values = "Error, trying to set coma stigmator to invalid values"

stigmator_coma_failed = "Error while setting coma stigmator; \nMake sure server is running and coarse " \
                         "stigmator is set properly."

error_during_afs = "Error during OptiSTEM: {0}; \nRestoring to starting point conditions for stigmator and defocus settings."

error_during_intermediate_afs = "Error during intermediate OptiSTEM."

second_order_aberrations_too_large = "2nd order aberrations too large, or clipping; Improve alignments"

max_iterations_reached = "Maximum # iterations reached"

error_stem_afs_not_licensed = r"OptiSTEM is not enabled in the microscope security key. "

suggestion_stem_afs_not_licensed = r"Please contact service or your local sales representative on how you can order OptiSTEM."

error_stem_second_order_aberration_correction_not_licensed = r"OptiSTEM+ is not enabled in the microscope security key. "

suggestion_stem_second_order_aberration_correction_not_licensed = r"Please contact service or your local sales representative on how you can order OptiSTEM+."

converged_c1_or_a1_out_of_range = r"The found solution for C1 and/or A1 is out of range"
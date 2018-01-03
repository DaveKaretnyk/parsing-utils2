# Copyright (c) 2012-2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import logging


from fei.infra.tem_server_access.models.product_family import ProductFamily
from fei.infra.tem_server_access.models.lens_type import LensType

from fei.infra.licensing.constants import (LICENSE_CODE_STEM_AFS_FEATURE,
                                           LICENSE_CODE_STEM_2ND_ORDER_CORR_FEATURE,
                                           LICENSE_CODE_MONO_AUTOTUNE_FEATURE,
                                           LICENSE_CODE_SERVICE_MODE_FEATURE)

logger = logging.getLogger(__name__)


class ConfigurationControl(object):
    def __init__(self, omp_worker, instrument, source, configuration, column):
        super(ConfigurationControl, self).__init__()
        self.omp_worker = omp_worker
        self._configuration = configuration
        self._instrument = instrument
        self._source = source
        ol_lens_properties = self.omp_worker.execute_on_worker(
            lambda: column.get_optics().get_lenses().get_objective_lens().get_lens_properties(),
            description="lambda: column.get_optics().get_lenses().get_objective_lens().get_lens_properties()")
        self.cc = self.omp_worker.execute_on_worker(
            lambda: ol_lens_properties.get_chromatic_aberration_coefficient(),
            description="lambda: ol_lens_properties.get_chromatic_aberration_coefficient()")
        self.cs = self.omp_worker.execute_on_worker(
            lambda: ol_lens_properties.get_spherical_aberration_coefficient(),
            description="lambda: ol_lens_properties.get_spherical_aberration_coefficient()")

        try:
            from fei._extensions.Licensing_TEM_API_PythonWrapper import LicensedFeature
            from fei.infra.licensing.FeatureListPython import FeatureListTEM
            self.is_licensing_module_present = True
            self.licensed_feature = LicensedFeature
            self.feature_list_tem = FeatureListTEM

            self.licensed_features_codes = {
                LICENSE_CODE_STEM_AFS_FEATURE:
                    self.feature_list_tem.Feature_STEM_AFS,
                LICENSE_CODE_STEM_2ND_ORDER_CORR_FEATURE:
                    self.feature_list_tem.Feature_STEM_2nd_order_corr,
                LICENSE_CODE_MONO_AUTOTUNE_FEATURE:
                    self.feature_list_tem.Feature_Mono_Autotune,
                LICENSE_CODE_SERVICE_MODE_FEATURE:
                    self.feature_list_tem.Feature_Applications_Service_mode}

            logger.info("Licensing module present")
        except ImportError:
            logger.warning("Licensing module not present. Using IOM for checking the dongle.")
            self.is_licensing_module_present = False
            self.dongle = self.omp_worker.execute_on_worker(
                lambda: self.instrument.get_dongle(),
                "lambda: self.instrument.get_dongle()")

    def __del__(self):
        logger.info("OMP ConfigurationControl destructor")
        self._release_objects()
        self.omp_worker = None

    def disconnect(self):
        logger.info("OMP ConfigurationControl disconnect")
        self.omp_worker.execute_on_worker(
            lambda: self._release_objects(),
            description="lambda: self._release_objects()")

    def _release_objects(self):
        self._source = None
        self._instrument = None
        self._configuration = None

    def is_titan(self):
        product_family = self.omp_worker.execute_on_worker(
            lambda: self._configuration.get_product_family(),
            "self._configuration.get_product_family()")
        return ProductFamily.Titan == product_family

    def is_talos(self):
        product_family = self.omp_worker.execute_on_worker(
            lambda: self._configuration.get_product_family(),
            "self._configuration.get_product_family()")
        return ProductFamily.Talos == product_family

    def is_tecnai(self):
        product_family = self.omp_worker.execute_on_worker(
            lambda: self._configuration.get_product_family(),
            "self._configuration.get_product_family()")
        return ProductFamily.Tecnai == product_family

    def is_high_contrast(self):
        raise Exception("OMP is_high_contrast is not supported")
        # return LensType.HighContrast == self.get_lens_type()

    def is_120(self):
        raise Exception("OMP is_120 is not supported")
        # fixed_values = self.get_ht_fixed_values()
        # max_value = np.max(fixed_values)
        # return (max_value < 125.0e3) and (max_value > 115.0e3)

    def is_200(self):
        raise Exception("OMP is_120 is not supported")
        # fixed_values = self.get_ht_fixed_values()
        # max_value = np.max(fixed_values)
        # return (max_value < 210.0e3) and (max_value > 190.0e3)

    def is_300(self):
        raise Exception("OMP is_300 is not supported")
        # fixed_values = self.get_ht_fixed_values()
        # max_value = np.max(fixed_values)
        # return (max_value < 310.0e3) and (max_value > 290.0e3)

    def get_cs(self):
        return self.cs

    def get_cc(self):
        return self.cc

    def get_lens_type(self):
        return LensType.from_omp(self.omp_worker.execute_on_worker(
            lambda: self._configuration.get_lens_type(),
            "lambda: self._configuration.get_lens_type()"))

    def get_product_family(self):
        product_family = self.omp_worker.execute_on_worker(
            lambda: self._configuration.get_product_family(),
            "lambda: self._configuration.get_product_family()")
        logger.info("Product family returned from omp: {}".format(product_family))
        return ProductFamily.from_omp(product_family)

    def get_product_name(self):
        return self.omp_worker.execute_on_worker(
            lambda: self._configuration.get_product_name(),
            "lambda: self._configuration.get_product_name()")

    def has_image_corrector(self):
        return self.omp_worker.execute_on_worker(
            lambda: self._configuration.is_image_corrector_available(),
            "lambda: self._configuration.is_image_corrector_available()")

    def has_probe_corrector(self):
        return self.omp_worker.execute_on_worker(
            lambda: self._configuration.is_probe_corrector_available(),
            "lambda: self._configuration.is_probe_corrector_available()")

    def is_function_allowed(self, function_id):
        if self.is_licensing_module_present:
            try:
                licensed_feature = self.licensed_feature(
                    self._get_licensed_feature_code(function_id))
                login_succeeded = licensed_feature.login()

                if login_succeeded:
                    if licensed_feature.is_feature_valid():
                        licensed_feature.logout()
                        return True
                    else:
                        return False
                else:
                    logger.error('Login to licensing component rejected')
                    return False
            except Exception as e:
                logger.error(e.message)
                return False
        else:
            return self.omp_worker.execute_on_worker(
                lambda: self._dongle.is_function_allowed(function_id),
                "lambda: self._dongle.is_function_allowed(function_id)")

    def is_service_dongle_attached(self):
        if self.is_licensing_module_present:
            return self.is_function_allowed(LICENSE_CODE_SERVICE_MODE_FEATURE)
        raise Exception("Old dongle not available on Omp")

    def is_factory_dongle_attached(self):
        if self.is_licensing_module_present:
            return self.is_function_allowed(LICENSE_CODE_SERVICE_MODE_FEATURE)
        raise Exception("Old dongle not available on Omp")

    def get_ht_fixed_values(self):
        return self.omp_worker.execute_on_worker(
            lambda: [ht for ht in self._source.get_high_voltage_fixed_values()],
            "lambda: [ht for ht in self._source.get_high_voltage_fixed_values()]")

    def has_energy_filter(self):
        return self.omp_worker.execute_on_worker(
            lambda: self._configuration.is_imaging_filter_available(),
            "lambda: self._configuration.is_imaging_filter_available()")

    def is_monochromator(self):
        return self.omp_worker.execute_on_worker(
            lambda: self._configuration.is_monochromator_available(),
            "lambda: self._configuration.is_monochromator_available()")

    def has_flu_cam(self):
        return self.omp_worker.execute_on_worker(
            lambda: self._configuration.is_flu_cam_available(),
            "lambda: self._configuration.is_flu_cam_available()")

from databases.repository.profiles import DoctorProfileRepository
from models import commons

import logging

class DoctorService:

    @staticmethod
    def search_doctor(search_by, search_key, covid_support):
        if search_by not in ['name', 'speciality']:
            error_message = f'unsupported search filter: {search_by}'
            print(error_message)
            raise BaseException(error_message)

        if search_by == 'name':
            logging.info(f'searching doctor by name: {search_key}')
            doctor_profiles = DoctorProfileRepository.get_doctor_by_name(search_key)
        else:
            logging.info(f'searching doctor by speciality: {search_key}')
            doctor_profiles = DoctorProfileRepository.get_doctor_by_speciality(search_key)

        doctor_details_list = []
        logging.info(f'found {len(doctor_profiles)} doctors')
        for doctor_profile in doctor_profiles:
            # logging.info(f'doctor profiles = {doctor_profile.full_name}')
            if covid_support:
                if (doctor_profile.is_hosp_covid_supported) or doctor_profile.is_hosp_covid_supported == 1:
                    print("am i coming here in if block")
                    doctor_details_list.append(commons.generate_doctor_details(doctor_profile))
            else:
                print("am i coming here in else block")
                doctor_details_list.append(commons.generate_doctor_details(doctor_profile))

        return {'doctor_details': doctor_details_list, 'num_doctors': len(doctor_details_list)}
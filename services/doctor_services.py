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
            doctor_profiles = DoctorProfileRepository.get_doctor_by_name(search_key)
        else:
            doctor_profiles = DoctorProfileRepository.get_doctor_by_speciality(search_key)

        doctor_details_list = []
        logging.info(f'found {len(doctor_details_list)} doctors')
        for doctor_profile in doctor_profiles:
            if covid_support:
                if int(doctor_profile.is_hosp_covid_supported) == 1:
                    doctor_details_list.append(commons.generate_doctor_details(doctor_profile))
            else:
                doctor_details_list.append(commons.generate_doctor_details(doctor_profile))

        return {'doctor_details': doctor_details_list, 'num_doctors': len(doctor_details_list)}
-- delete from doctorprofile;
INSERT INTO doctorprofile VALUES
-- (	user_id, full_name, contact_email, contact_phone, theme, gender, dob, experience, hospital_name, hospital_address, speciality, is_hosp_covid_supported, num_covid_beds_available,
-- 	insurance_accepted)
('doctor_1', 'Keerthana', 'ksugasi@iu.edu', '122435654', 'primary', 'Female', '27-apr-98', '10', 'abc hospitals' , 'Bloomington Indiana', 'Neurology', 1, 10, 4),
('doctor_2', 'Doctor2', 'doctor2@iu.edu', '435654', 'primary', 'Male', '27-apr-95', '5', 'abc hospitals' , 'Bloomington Indiana', 'Cardiology', 0, 0, 0),
('doctor_3', 'NP3', 'np@gmail.com', '43560054', 'primary', 'Female', '27-apr-85', '15', 'San Jose hospitals' , 'San Jose, California', 'Nurse Practioner', 0, 0, 0);
('doctor_4', 'Doctor4', 'doctor4@gmail.com', '4356005413', 'primary', 'Male', '27-jun-85', '15', 'San Jose hospitals' , 'San Jose, California', 'Interventional Cardiology', 0, 0, 0);

insert into healthcareplan values('plan1','insurer_5','HeartCare Plan-1','Heart Care Plan','for heart patients','{"exception1"}', 5000, 1000,1,500,true);
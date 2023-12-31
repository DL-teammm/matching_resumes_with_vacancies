from bs4 import BeautifulSoup
import os
import re
import pandas as pd
import json


class Resume:
    """Class extracts the resume information from HTML page"""
    def __init__(self, soup, resume_id):
        self.soup = soup
        self.resume_id = resume_id
        self.resume_title = self.extract_title()
        self.city = self.extract_information('span', {'data-qa': "resume-personal-address"})
        self.age = self.extract_age()
        self.gender = self.extract_gender
        self.area = self.extract_area()
        self.desired_wage = self.extract_wage()
        self.work_exp = self.extract_work_experience()
        self.education = self.extract_nested_information('div', {'data-qa': "resume-block-education"})
        self.language_prof = self.extract_languages()
        self.skills = self.extract_information('span', {'class': "bloko-tag__section bloko-tag__section_text"})
        self.about = self.extract_information('div',{'data-qa': "resume-block-skills-content"})
        self.dict_resume = self.resume_dict_maker()
        

    def __repr__(self):
        return f'{self.dict_resume}'

    def extract_title(self):
        title = self.extract_information('span', {'data-qa': "resume-block-title-position"})
        main_titles = title.split(',')
        main_title = main_titles[0]
        return main_title

    def extract_age(self):
        raw_age = self.extract_information('span', {'data-qa': "resume-personal-age"})
        digit_pattern = r'\d+'
        if raw_age != "No information":
            age = re.findall(digit_pattern, raw_age)
            age = age[0]
            return age
        else:
            return 0

    def extract_work_experience(self):
        work_exp = self.extract_nested_information('div', {'data-qa': "resume-block-experience"})
        float_pattern = r'\d+'  # Search for any digit in str
        if work_exp != "No information":
            work_exp = re.findall(float_pattern, work_exp) # Extract period of work from the str
            if len(work_exp) == 2:
                work_exp = float(f'{work_exp[0]}.{work_exp[1]}')
            elif len(work_exp) == 1:
                work_exp = work_exp[0]
            return work_exp
        else:
            return 0

    def extract_area(self):
        area = self.extract_information('li', {'data-qa': "resume-block-position-specialization"})
        return area

    def extract_wage(self):
        wage = self.extract_information('span', {'data-qa': "resume-block-salary"})
        int_pattern = r'\d'
        if wage != "No information":
            wage_amount = re.findall(int_pattern, wage)
            wage_str = ''.join(wage_amount)
            wage = int(f'{wage_str}')
            return wage
        else:
            return 0

    def extract_languages(self):
        languages = self.extract_information('p', {'data-qa': "resume-block-language-item"}, to_list=False)
        if type(languages) == str:  # If only one or no language stated in resume
            languages = {"Russian": "Native"}
        return languages

    @property
    def extract_gender(self):
        gender = self.extract_information('span', {'data-qa': "resume-personal-gender"})
        if gender == 'The man':  # If translation inaccurate
            gender = 'Male'
        elif gender == 'Woman':
            gender = 'Female'
        return gender

    def check_for_translation(self, info):
        rus_pattern = r'[а-яА-Я]+'
        if re.search(rus_pattern, info):
            info = self.translator(info)
        return info

    @staticmethod
    def translator(text):  # If the resume is in Russian
        return text

    def extract_information(self, tag: str, attributes: dict, to_list=True):
        finder = self.soup.find_all(tag, attributes)
        if len(finder) == 1:
            finder = self.check_for_translation(finder[0].get_text())
            return finder
        elif len(finder) > 1:
            if to_list:
                listed_info = []
                for part in finder:
                    list_element = part.get_text()
                    list_element = self.check_for_translation(list_element)
                    listed_info.append(list_element)
                return listed_info
            else:
                dict_info = {}
                for dict_part in finder:
                    dict_element = dict_part.get_text()
                    dict_element = self.check_for_translation(dict_element)
                    splitted_dict_element = dict_element.split()
                    dict_info[splitted_dict_element[0]] = splitted_dict_element[2]
                return dict_info
        else:
            return "No information"

    def extract_nested_information(self, tag: str, attributes: dict, to_list=True):
        finder = self.soup.find(tag, attributes)
        if finder is None:
            return "No information"
        else:
            finder = finder.find('span', {'class': "resume-block__title-text resume-block__title-text_sub"})
            finder = self.check_for_translation(finder.get_text())
        return finder

    def resume_dict_maker(self):
        resume_dict = {'id': self.resume_id,
                       'title': self.resume_title,
                       'city': self.city,
                       'age': self.age,
                       'gender': self.gender,
                       'area': self.area,
                       'desired_wage': self.desired_wage,
                       'work_experience': self.work_exp,
                       'education_level': self.education,
                       'languages': self.language_prof,
                       'skills': self.skills,
                       'about': self.about
                       }
        return resume_dict


class ResumeGetter:
    """Запускает процесс скачивания резюме"""
    def __init__(self):
        self.dir_path = "/data/saved_resumes/"
        self.resume_storage = os.listdir(path=self.dir_path)
        self.resume_dict_storage = []

    def get_resume(self):
        counter = 1
        for resume in self.resume_storage:
            print(counter)
            
            with open(f'{self.dir_path}{resume}', "r", encoding="utf8") as resume_page:
                resume_text = BeautifulSoup(resume_page, features="lxml")
                resume_id = str(re.search(r"page_(.+)\.html", resume).group(1))  # забираем id из названия файла
                print(f'Start parce {resume_id}')
                resume_getter = Resume(resume_text, resume_id)
                dict_format = resume_getter.resume_dict_maker()
                dict_format = {key: str(value) if isinstance(value, (list, dict)) else value for key, value in dict_format.items()}
                print(dict_format)
                if counter > 1:
                    df1 = pd.DataFrame.from_dict (dict_format, orient='index').T
                    data = pd.concat([data, df1])
                    print(data)
                else:
                    data = pd.DataFrame.from_dict(dict_format, orient='index').T
                    print(data)
                print(f'Resume {resume_id} saved in json file')
                
                print('*' * 20)
            counter += 1
        data.to_csv("/resumes.csv")
        return


if __name__ == '__main__':
    data = ResumeGetter()
    data.get_resume()



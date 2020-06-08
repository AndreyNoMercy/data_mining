# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД.

# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

# Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from pymongo import MongoClient
import task_2_1



def insert_to_mongo(*args):
    insert_list = []
    for arg in args:
        insert_list.extend(arg.vacancies)
    client = MongoClient('localhost', 27017)
    db = client['data_mining']
    collection = db['vacancies']
    collection.insert_many(insert_list)


def find_salary(min_salary):
    client = MongoClient('localhost', 27017)
    relevant_vacancies = list(client.data_mining.vacancies.find({'$or': [{'max_salary': {'$gt': f'{min_salary}'}},
                                                                          {'min_salary': {'$gt': f'{min_salary}'}}]}))
    for i in relevant_vacancies:
        print(i)
    return relevant_vacancies


def insert_uniq_to_mongo(*args):
    check_list = []
    new_list = []
    for arg in args:
        new_list.extend(arg.vacancies)
    client = MongoClient('localhost', 27017)
    db = client['data_mining']
    collection = db['vacancies']
    for_check = list(client.data_mining.vacancies.find({}, {'_id': 0, 'url': 1}))
    for i in for_check:
        check_list.append(i['url'])
    for i in new_list:
        if i['url'] in check_list:
            print(i)
            new_list.remove(i)
    collection.insert_many(new_list)


if __name__ == '__main__':
    role = 'Data Science'
    n = 1
    insert_uniq_to_mongo(task_2_1.Parser_SJ(role, n), task_2_1.Parser_HH(role, n))





from jinja2.ext import Extension
import os.path


class FoobarExtension(Extension):
    def __init__(self, environment):
        super(FoobarExtension, self).__init__(environment)
        print(environment)
        print(dir(environment))
        self.stem_keys()
        # 'getattr', 'getitem'

        # userLiquibase = environment.filters['use_liquibase']
        # print(environment.filters['use_liquibase'])
        # if userLiquibase == 'yes':

        #    print('ookkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    def stem_keys(self, cookiecutter):
        for key in list(cookiecutter.keys()):
            print(key)

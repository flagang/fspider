import string

import os
from os.path import join, exists
from shutil import copytree, ignore_patterns

from argparse import Namespace

import fspider
from fspider.commands import CMD
from fspider.utils.strings import string_camelcase

ignore=ignore_patterns('*.pyc', '__pycache__', '.svn')
class SpiderCMD(CMD):
    def help(self) -> str:
        return 'create project <project_name> [project_dir]'

    def add_arguments(self):
        self.cmd.add_argument('project_name', help='the project name', type=str)
        self.cmd.add_argument('project_dir', default='.',nargs='*',
                              help='the project dir,current dir will use if not set',
                              )

    def run(self, args: Namespace):
        project_name = args.project_name
        project_dir = args.project_dir
        path = self._create(project_name, project_dir)
        if path:
            self._render(path, project_name)

    def _create(self, project_name: str, project_dir: str):
        path = join(project_dir, project_name)
        if exists(path) :
            print(f'{project_name} has exists  ')
        else:
            copytree(self.templates_dir(), path,ignore=ignore)
            os.rename(os.path.join(path,'module'),os.path.join(path,project_name))
            return path

    def _render(self, path, project_name):
        for root, dirs, files in os.walk(path):
            for f in files:
                file_path = join(root, f)
                if file_path.endswith('tmpl'):
                    self.render_templatefile(file_path, project_name=project_name,ProjectName=string_camelcase(project_name))

    def templates_dir(self):
        _templates_base_dir = join(fspider.__path__[0], 'templates')
        return join(_templates_base_dir, 'project')

    @staticmethod
    def render_templatefile(path, **kwargs):
        with open(path, 'rb') as fp:
            raw = fp.read().decode('utf8')

        content = string.Template(raw).substitute(**kwargs)

        render_path = path[:-len('.tmpl')] if path.endswith('.tmpl') else path
        with open(render_path, 'wb') as fp:
            fp.write(content.encode('utf8'))
        if path.endswith('.tmpl'):
            os.remove(path)

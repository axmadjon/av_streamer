from pip.req import parse_requirements
from setuptools import setup, Extension

install_requirements = parse_requirements('requirements.txt', session='av_streamer')

requirements = [str(ir.req) for ir in install_requirements]

ext_modules = [
    Extension('av_streamer', ['av_streamer/__api.py'])
]

setup(
    name='av_streamer',
    version='1.0',
    author='Axmadjon Xamidov Ikrom og\'li',
    author_email='axmadjon.xamidov@gmail.com',
    url='https://github.com/axmadjon/av_streamer',
    ext_modules=ext_modules,
    install_requires=requirements
)

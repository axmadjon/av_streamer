from setuptools import setup, Extension

requirements = ['av==0.4.0']

ext_modules = [
    Extension('av_streamer', ['av_streamer/__api.py'])
]

setup(
    name='av_streamer',
    version='1.0.1',
    author='Axmadjon Xamidov Ikrom og\'li',
    author_email='axmadjon.xamidov@gmail.com',
    url='https://github.com/axmadjon/av_streamer',
    ext_modules=ext_modules,
    install_requires=requirements
)

from setuptools import setup

requirements = ['av==0.4.0']

setup(
    name='av_streamer',
    version='1.0.3',
    author='Axmadjon Xamidov Ikrom og\'li',
    author_email='axmadjon.xamidov@gmail.com',
    url='https://github.com/axmadjon/av_streamer',
    packages=[
        'av_streamer',
    ],
    package_dir={'av_streamer': 'av_streamer'},
    install_requires=requirements
)

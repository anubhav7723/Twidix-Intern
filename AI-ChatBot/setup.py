from setuptools import setup, find_packages

setup(
    name='ai_chatbot',
    version='0.1.0',
    description='An AI chatbot that can answer general and medical questions.',
    author='Anubhav Gupta',
    author_email='anubhavg0098@gmail.com',  # Replace with your email
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        # Add your runtime dependencies here
        'openai',
        'python-dotenv',
        'fastapi',
        'uvicorn',
        'pydantic',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

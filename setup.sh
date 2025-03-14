#!/bin/bash

# Kiểm tra xem Python đã được cài đặt chưa
if ! command -v python3 &> /dev/null
then
    echo "Python3 chưa được cài đặt. Vui lòng cài đặt Python3 trước."
    exit
fi

# Kiểm tra xem pip đã được cài đặt chưa
if ! command -v pip3 &> /dev/null
then
    echo "pip3 chưa được cài đặt. Vui lòng cài đặt pip3 trước."
    exit
fi

# Tạo và kích hoạt virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt các gói yêu cầu
pip install -r requirements.txt

# Thực hiện các migration
python manage.py migrate

# Tạo superuser
echo "Tạo superuser cho Django:"
python manage.py createsuperuser

# Chạy server
echo "Chạy server Django:"
python manage.py runserver
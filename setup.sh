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

# Tạo môi trường ảo
python3 -m venv venv

# Kiểm tra hệ điều hành để kích hoạt môi trường ảo đúng cách
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate  # Windows
else
    source venv/bin/activate       # Linux/macOS
fi

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

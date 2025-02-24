echo "BUILD START"
python 3.9 -m pip install requirements.txt
python 3.9 manage.py collectstatic --noinput --clear
echo "BUILD END"

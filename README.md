# Keep-It-Fresh
Application Iteration 1

# Deployoment
Do it in Azure portal

# Start up script
```
apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev && gunicorn KeepItFresh.wsgi:application --bind 0.0.0.0:8000 --timeout 600 --access-logfile '-' --error-logfile '-'
```

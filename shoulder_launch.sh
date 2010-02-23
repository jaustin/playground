SERVICE='shoulder_daemon'
SERVICE_EXEC='~/torso-code/playground/shoulder_daemon'
SHOULDER_LAUNCH='/home/desktopuser/torso-scripts/shoulder_launch.sh'
dbus-send --print-reply             --session             --dest=com.cued.Shoulder    /ShoulderLauncher             com.cued.ShoulderLauncher.LaunchApp string:$1
if [ $? -eq 0 ]
then
  echo "DBUS daemon was found and command $1 was launched"
  exit 0
else
  echo "DBUS daemon was not found, the command was not launched, shall we launch it locally?"
  if ps ax | grep -v grep | grep $SERVICE > /dev/null
  then
      echo "$SERVICE service running - strange things are afoot"
  else
      zenity --question --text="It appears the programme to facilitate launching applications is not running. Would you like to start it now and try again?"
      if [ $? -eq 1 ]
      then
        zenity --question --text="Would you like to run the application $1 on the local machine, as the remote one cannot be acceseed?"
        if [ $? -eq 0 ]
        then
          $1
        else
          exit 1
        fi
      else
        echo "launcing the shoulder launcher"
        exec $SERVICE_EXEC &
        sleep 1
        $SHOULDER_LAUNCH $1
      fi
  fi
fi


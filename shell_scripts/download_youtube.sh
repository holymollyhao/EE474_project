mkdir temp && cd temp
youtube-dl "ytsearch:$ARTIST $NAME album version"
ffmpeg -i *.flv -aq 2 "${ARTIST} - ${NAME}.mp3"
rm -rf *.flv
cd .. && mv temp/*.mp3 $PWD && rm -rf temp
mv *.mp3 ~/Music/
echo Your song has been downloaded successfully
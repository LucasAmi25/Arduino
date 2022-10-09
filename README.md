# Arduino


### Comment fonctionne Arduino ?

![arduino](https://user-images.githubusercontent.com/45620484/123973232-e213eb00-d9bb-11eb-8de7-0da83aa728d8.jpeg)

On peut voir en bas 6 Pin analogique de A0 a A5 qu'on vient appeler dans le code avec la fonction analogRead(numPin) numPin étant donc juste le numéro

et au dessus tout les Pins digital qu'on vient appeler dans le code avec la fonction digitalWrite(numPin) ou digitalRead(numPin)

et pour les Pins digital, il faut preciser dans la fonction setup si c'est une sortie ou une entrée de données, on le fait grace a la fonction pinMode(numPin, [OUTPUT ou INPUT])

### L'IDE Arduino

![arduino_IDE](https://user-images.githubusercontent.com/45620484/123975384-93ffe700-d9bd-11eb-9058-b0297698f053.png)

### Faire des captures avec les Pulses sensors Arduino ainsi que la webcam de l'ordinateur :

Tout d'abord, Pour pouvoir effectuer des mesures, il faut effectuer les connections arduino et la connection arduino/ordinateur. Pour les branchements arduino, le fichier qui montre comment brancher est **pulseSensorConnect.jpg** ensuite, pour le brancher a l'ordinateur utilisé un port USB de l'ordinateur avec le port USB B de l'arduino.
Ensuite, dans l'IDE Arduino, veuillez bien vérifier que :

![outilsArduino](https://user-images.githubusercontent.com/45620484/123983074-df1cf880-d9c3-11eb-9deb-a7395b4c4108.png)

Bien selectionner la carte ***Arduino Uno*** en type de carte et que le Port utilisé est le Port ***COM4***

Puis, téléversez le code dans **code_Pulse_Sensor/code_Pulse_Sensor.ino**, ensuite quand celui ci est téléverser, pour récuperer ces données dans des fichiers, veuillez lancer le srcypt **captureDataTread.py** quand l'installation est prete, et que le sujet est pret a etre enregisté. Il y aura en sortie un fichier **basicvideo.mp4** qui va etre la video enregister ainsi qu'un fichier **ground_truth.txt** qui va avoir les différentes mesures des pulses sensors avec le temps des mesures ***(aucun changement de lumiere ne doit etre observé pendant l'enregistrement sinon, celui ci sera biaisé)***.

### Synchronisation

Pour la synchronisation, il y a des valeurs a 0 dans le **ground_thruth.txt** qui est donc au meme moment que l'allumage de la LED et donc pour pouvoir connaitre les Frames ou la Led est allumé, il faut mettre la video **basicvideo.mp4**  dans le meme dossier que le fichier **detectFlash/detectFlash.py** et ensuite, le lancer, normalement les frames qui montre la LED allumé et de nouveau éteinte vont etre enregisté sous la forme d'un fichier **flash[numFrame].jpg**.
# Arduino
# Arduino
# Arduino

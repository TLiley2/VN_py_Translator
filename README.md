# VN_py_Translator
VN_py_Translator is a Visual novel Translator I made in python in about aweek in a half in my spare free time. The function of programs is to overlay translated text onto the screen of any visual novel you are playing. 

The program is not to fast all things considered taking about 15-17 secs to return with a translation overlay. But I've tried to reduce the run time as much as possible if you've got a concrete method of reucing runtime the sound off in the pull request or something IDK ¯\_(ツ)_/¯

<ins>**The app works like this:**</ins>
* Selecting the desired app from drop box
* The program sends the .exe name to the backend which:
  * Checks if the slected app is currently running
  * Takes a screenshot of the app
* The screenshot's file location is sent to the OCR file where:
  * The image is quickly photo edited for readiblity
  * Read by the [EasyOCR](https://github.com/JaidedAI/EasyOCR) engine
  * The text is extracted and sent to Google tranlstae
  * The final list of values is collected
      * The minimum x-value of the bounding box
      * The minimum y-value of the bounding box
      * The Google Translated text
  * Return the final list to the screen overlay function

  # License
  GNU General Public License v3.0
